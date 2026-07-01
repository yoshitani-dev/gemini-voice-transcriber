r"""
==========================================================
  Gemini Voice Transcriber Web Server (FastAPI)
==========================================================

Expose audio_transcriber.py functionality as a Web API.
Allows real-time recording and audio/video file uploads
via browser for transcription and PDF generation.

Usage:
  python web_server.py

==========================================================
"""

import io
import os
import sys
import re
import datetime
import time
import threading
import webbrowser
import uvicorn
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse

# audio_transcriber.py から機能をインポート
from audio_transcriber import (
    AudioRecorder,
    transcribe_with_gemini,
    generate_title_from_text,
    generate_minutes_from_text,
    create_pdf,
    GEMINI_MODEL,
    OUTPUT_DIR,
    API_KEY,
)


# ============================================================
# アプリ設定
# ============================================================

PORT = 8000
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

app = FastAPI(title="Gemini Voice Transcriber")

# 出力ディレクトリ作成
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================
# セキュリティ・ミドルウェア
# ============================================================

@app.middleware("http")
async def security_middleware(request: Request, call_next):
    # APIのPOSTリクエストに対してCSRF対策を実施
    if request.url.path.startswith("/api/") and request.method in ["POST", "PUT", "DELETE"]:
        origin = request.headers.get("origin")
        referer = request.headers.get("referer")
        
        # ローカルホストのアドレス一覧
        allowed_origins = [f"http://localhost:{PORT}", f"http://127.0.0.1:{PORT}"]
        
        # Origin ヘッダーのチェック
        if origin and origin not in allowed_origins:
            return JSONResponse({"error": "CSRF verification failed (Invalid Origin)"}, status_code=403)
            
        # Referer ヘッダーのチェック (前方一致の脆弱性を防ぐため厳格化)
        if referer:
            is_valid_referer = False
            for a in allowed_origins:
                # 完全一致、またはその後ろがパス(/)やクエリ(?)で続く場合のみ許可
                if referer == a or referer.startswith(a + "/") or referer.startswith(a + "?"):
                    is_valid_referer = True
                    break
            if not is_valid_referer:
                return JSONResponse({"error": "CSRF verification failed (Invalid Referer)"}, status_code=403)
            
        # OriginもRefererもない場合（ブラウザからのPOSTではないか、no-corsモードの攻撃）
        if not origin and not referer:
            return JSONResponse({"error": "CSRF verification failed (No Origin/Referer)"}, status_code=403)
            
    response = await call_next(request)
    
    # クリックジャッキング等の防止用セキュリティヘッダー
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Content-Security-Policy"] = "frame-ancestors 'none'"
    response.headers["X-Content-Type-Options"] = "nosniff"
    
    return response


# ============================================================
# グローバル状態管理
# ============================================================

class AppState:
    def __init__(self):
        self.status = "idle"          # idle, recording, processing
        self.step = 0                 # 0:待機, 1:アップロード, 2:圧縮, 3:文字起こし, 4:PDF生成
        self.message = ""
        self.recording_seconds = 0
        self.recorder = None
        self.timer_thread = None
        self.result = None            # 最新の結果
        self.error = None

    def reset(self):
        self.status = "idle"
        self.step = 0
        self.message = ""
        self.recording_seconds = 0
        self.result = None
        self.error = None

state = AppState()


# ============================================================
# APIエンドポイント
# ============================================================

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    """メインページを返す"""
    index_path = os.path.join(TEMPLATES_DIR, "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())


@app.post("/api/recording/start")
async def start_recording():
    """PC音声のリアルタイム録音を開始"""
    if state.status != "idle":
        return JSONResponse({"error": "既に処理中です"}, status_code=400)

    try:
        state.reset()
        state.status = "recording"
        state.message = "PC音声を録音中..."
        state.recorder = AudioRecorder()
        state.recorder.start_recording()

        # 録音時間カウント用スレッド
        def timer():
            while state.status == "recording":
                time.sleep(1)
                state.recording_seconds += 1
        state.timer_thread = threading.Thread(target=timer, daemon=True)
        state.timer_thread.start()

        return {"success": True, "message": "録音を開始しました"}
    except Exception as e:
        state.reset()
        state.error = str(e)
        return JSONResponse({"error": str(e)}, status_code=500)


@app.post("/api/recording/stop")
async def stop_recording():
    """録音を停止し、文字起こし→PDF生成を実行"""
    if state.status != "recording" or not state.recorder:
        return JSONResponse({"error": "録音中ではありません"}, status_code=400)

    # 録音停止
    state.recorder.stop_recording()
    state.status = "processing"
    state.step = 1
    state.message = "録音データを保存中..."

    # バックグラウンドで処理
    def process():
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            audio_filename = f"recording_{timestamp}.wav"
            audio_filepath = os.path.join(OUTPUT_DIR, audio_filename)

            if not state.recorder.save_wav(audio_filepath):
                state.error = "録音データの保存に失敗しました"
                state.status = "idle"
                return
            state.recorder.cleanup()

            # 文字起こし実行
            _process_audio(audio_filepath, audio_filename, timestamp)

        except Exception as e:
            state.error = str(e)
            state.status = "idle"

    threading.Thread(target=process, daemon=True).start()
    return {"success": True, "message": "録音を停止しました。文字起こしを開始します..."}


@app.post("/api/transcribe")
async def transcribe_file(file: UploadFile = File(...)):
    """アップロードされた音声ファイルを文字起こし"""
    if state.status != "idle":
        return JSONResponse({"error": "既に処理中です"}, status_code=400)

    state.reset()
    state.status = "processing"
    state.step = 1
    state.message = "ファイルを受信中..."

    # ファイルを一時保存
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    _, ext = os.path.splitext(file.filename or "audio.wav")
    # 安全なASCIIファイル名に変換
    safe_name = f"upload_{timestamp}{ext}"
    tmp_filepath = os.path.join(OUTPUT_DIR, safe_name)

    try:
        import shutil
        with open(tmp_filepath, "wb") as f:
            shutil.copyfileobj(file.file, f)
    except Exception as e:
        state.reset()
        return JSONResponse({"error": f"ファイル保存エラー: {e}"}, status_code=500)

    audio_filename = file.filename or safe_name

    # バックグラウンドで処理
    def process():
        try:
            _process_audio(tmp_filepath, audio_filename, timestamp)
        except Exception as e:
            state.error = str(e)
            state.status = "idle"

    threading.Thread(target=process, daemon=True).start()
    return {"success": True, "message": "文字起こしを開始します..."}


@app.get("/api/status")
async def get_status():
    """現在の処理状態を返す"""
    return {
        "status": state.status,
        "step": state.step,
        "message": state.message,
        "recording_seconds": state.recording_seconds,
        "error": state.error,
    }


@app.get("/api/result")
async def get_result():
    """最新の文字起こし結果を返す"""
    if state.result:
        return state.result
    return {"success": False, "message": "結果がありません"}


@app.get("/api/download/{filename}")
async def download_pdf(filename: str):
    """PDFファイルをダウンロード"""
    # パストラバーサル防止: ファイル名にディレクトリ区切りや".."が含まれていないことを確認
    if ".." in filename or "/" in filename or "\\" in filename:
        return JSONResponse({"error": "不正なファイル名です"}, status_code=400)
    filepath = os.path.join(OUTPUT_DIR, filename)
    # 解決後のパスがOUTPUT_DIR内であることを二重チェック
    if not os.path.abspath(filepath).startswith(os.path.abspath(OUTPUT_DIR)):
        return JSONResponse({"error": "不正なファイル名です"}, status_code=400)
    if not os.path.exists(filepath):
        return JSONResponse({"error": "ファイルが見つかりません"}, status_code=404)
    return FileResponse(
        filepath,
        media_type="application/pdf",
        filename=filename,
    )


# ============================================================
# 共通処理: 音声→文字起こし→PDF
# ============================================================

def _process_audio(audio_filepath, audio_filename, timestamp):
    """音声ファイルの文字起こしとPDF生成を実行（進捗を細かくstateに反映）"""
    from google import genai
    import mimetypes

    api_key = os.environ.get("GEMINI_API_KEY", API_KEY).strip()
    if not api_key:
        state.error = "APIキーが設定されていません。環境変数 GEMINI_API_KEY を設定してください。"
        state.status = "idle"
        return

    try:
        # ========== Step 2/3: 音声ファイルの圧縮・アップロード・文字起こし ==========
        def progress_cb(step: int, msg: str):
            state.step = step
            state.message = msg

        full_text, _ = transcribe_with_gemini(
            audio_filepath, api_key, progress_callback=progress_cb
        )

        if not full_text:
            state.error = "文字起こしに失敗しました。ファイル形式を確認してください。"
            state.status = "idle"
            return

        # ========== 議事録生成 ==========
        state.step = 4
        state.message = "AIが議事録を生成中..."
        minutes_text = generate_minutes_from_text(full_text, api_key)

        # ========== タイトル生成 ==========
        state.message = "AIがタイトルを自動生成中..."
        title_name = generate_title_from_text(full_text, api_key)
        title_name = re.sub(r'[\\/:*?"<>|]', '', title_name).strip()
        if not title_name:
            title_name = "文字起こし結果"

        # ========== Step 5: PDF生成 ==========
        state.step = 5
        state.message = "PDFを生成中..."

        pdf_filename = f"{title_name}_{timestamp}.pdf"
        pdf_filepath = os.path.join(OUTPUT_DIR, pdf_filename)
        create_pdf(full_text, "", pdf_filepath, audio_filename=audio_filename, minutes_text=minutes_text)

        # 結果を保存
        state.result = {
            "success": True,
            "title": title_name,
            "minutes_text": minutes_text,
            "full_text": full_text,
            "pdf_filename": pdf_filename,
        }

        state.status = "idle"
        state.step = 0
        state.message = "完了しました！"

    except Exception as e:
        state.error = f"処理エラー: {e}"
        state.status = "idle"


# ============================================================
# サーバー起動
# ============================================================

if __name__ == "__main__":
    # Windows PowerShellの文字コード問題を回避
    if sys.platform == "win32":
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

    port = PORT

    # APIキーチェック
    api_key = os.environ.get("GEMINI_API_KEY", API_KEY).strip()
    if not api_key:
        print("=" * 50)
        print("  [!] APIキーが設定されていません")
        print("=" * 50)
        print()
        print("  PowerShellで以下を実行してください:")
        print('  setx GEMINI_API_KEY "あなたのAPIキー"')
        print()
        print("  APIキー取得: https://aistudio.google.com/apikey")
        print()
        input("Enterキーで終了...")
        sys.exit(1)

    print("=" * 50)
    print("  Gemini Voice Transcriber")
    print("=" * 50)
    print(f"  モデル: {GEMINI_MODEL}")
    print(f"  URL: http://localhost:{port}")
    print(f"  終了: Ctrl+C")
    print()

    # 少し遅延してからブラウザを開く
    def open_browser():
        time.sleep(1.5)
        webbrowser.open(f"http://localhost:{port}")
    threading.Thread(target=open_browser, daemon=True).start()

    uvicorn.run(app, host="127.0.0.1", port=port, log_level="warning")
