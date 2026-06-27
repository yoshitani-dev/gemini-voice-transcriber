"""セットアップガイドをPDF化するスクリプト（reportlab版）"""
import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor

# フォント登録
font_path = None
for name in ["msgothic.ttc", "meiryo.ttc", "YuGothM.ttc"]:
    p = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts", name)
    if os.path.exists(p):
        font_path = p
        break

if not font_path:
    print("日本語フォントが見つかりません。")
    exit(1)

print(f"フォント: {font_path}")
pdfmetrics.registerFont(TTFont("JP", font_path, subfontIndex=0))

# PDF作成
output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "セットアップガイド.pdf")
c = canvas.Canvas(output_path, pagesize=A4)
W, H = A4
MARGIN_L = 25 * mm
MARGIN_R = 20 * mm
TEXT_W = W - MARGIN_L - MARGIN_R
y = H - 30 * mm

def new_page():
    global y
    c.showPage()
    y = H - 25 * mm

def check_space(needed=20):
    global y
    if y < needed * mm:
        new_page()

def title(text):
    global y
    c.setFont("JP", 20)
    c.drawCentredString(W / 2, y, text)
    y -= 12 * mm

def heading(text):
    global y
    check_space(25)
    y -= 6 * mm
    c.setFillColor(HexColor("#2563EB"))
    c.setFont("JP", 15)
    c.drawString(MARGIN_L, y, text)
    c.setFillColor(HexColor("#000000"))
    y -= 4 * mm
    c.setStrokeColor(HexColor("#2563EB"))
    c.line(MARGIN_L, y, W - MARGIN_R, y)
    c.setStrokeColor(HexColor("#000000"))
    y -= 6 * mm

def subheading(text):
    global y
    check_space(18)
    y -= 4 * mm
    c.setFont("JP", 12)
    c.setFillColor(HexColor("#1E40AF"))
    c.drawString(MARGIN_L, y, text)
    c.setFillColor(HexColor("#000000"))
    y -= 7 * mm

def body(text):
    global y
    check_space(12)
    c.setFont("JP", 10)
    # 長い行は折り返す
    max_chars = 55
    while len(text) > max_chars:
        c.drawString(MARGIN_L, y, text[:max_chars])
        text = text[max_chars:]
        y -= 5 * mm
        check_space(10)
    c.drawString(MARGIN_L, y, text)
    y -= 6 * mm

def bullet(text):
    global y
    check_space(12)
    c.setFont("JP", 10)
    c.drawString(MARGIN_L + 3 * mm, y, "・ " + text)
    y -= 6 * mm

def code_block(text):
    global y
    check_space(14)
    c.setFillColor(HexColor("#F3F4F6"))
    c.rect(MARGIN_L, y - 2 * mm, TEXT_W, 7 * mm, fill=1, stroke=0)
    c.setFillColor(HexColor("#000000"))
    c.setFont("JP", 9)
    c.drawString(MARGIN_L + 3 * mm, y, text)
    y -= 9 * mm

def warn(text):
    global y
    check_space(14)
    c.setFillColor(HexColor("#DC2626"))
    c.setFont("JP", 10)
    c.drawString(MARGIN_L, y, "⚠ " + text)
    c.setFillColor(HexColor("#000000"))
    y -= 6 * mm

def separator():
    global y
    y -= 3 * mm
    c.setStrokeColor(HexColor("#E5E7EB"))
    c.line(MARGIN_L, y, W - MARGIN_R, y)
    c.setStrokeColor(HexColor("#000000"))
    y -= 5 * mm

def table_row(col1, col2, is_header=False):
    global y
    check_space(12)
    c.setFont("JP", 9)
    if is_header:
        c.setFillColor(HexColor("#E5E7EB"))
        c.rect(MARGIN_L, y - 2 * mm, TEXT_W, 7 * mm, fill=1, stroke=1)
        c.setFillColor(HexColor("#000000"))
    else:
        c.rect(MARGIN_L, y - 2 * mm, TEXT_W, 7 * mm, fill=0, stroke=1)
    c.line(MARGIN_L + TEXT_W * 0.4, y - 2 * mm, MARGIN_L + TEXT_W * 0.4, y + 5 * mm)
    c.drawString(MARGIN_L + 2 * mm, y, col1)
    c.drawString(MARGIN_L + TEXT_W * 0.4 + 2 * mm, y, col2)
    y -= 7 * mm

# ============================================================
# 本文
# ============================================================
print("PDF生成中...")

title("音声文字起こしツール")
c.setFont("JP", 14)
c.drawCentredString(W / 2, y, "セットアップガイド (Web対応版)")
y -= 10 * mm

body("PCの知識がゼロでも、このガイドの通りに進めれば使えるようになります。")
body("所要時間：約15分")

separator()
heading("このツールでできること")
bullet("ブラウザで動く綺麗な画面（Web UI）で直感的に操作できます。")
bullet("PCで流れている音声を録音して自動で文字起こし＆PDF保存。")
bullet("音声・動画ファイルを画面にドラッグ＆ドロップするだけで文字起こし＆PDF保存。")
bullet("大容量ファイル（100MB以上）も自動的に圧縮してアップロード。")

separator()
heading("STEP 1：Pythonをインストールする")
body("1. ブラウザで以下のURLを開く")
code_block("https://www.python.org/downloads/")
body("2. 黄色い「Download Python 3.x.x」ボタンをクリック")
body("3. ダウンロードしたファイルを開く")
warn("最重要：最初の画面の最下部にある「Add Python to PATH」に必ずチェック！")
body("5. 「Install Now」をクリックしてインストール開始")
body("6. インストールが終わったら「Close」をクリック")

subheading("確認方法")
body("PowerShellを開いて以下を入力し、バージョンが表示されればOK：")
code_block("python --version")

separator()
heading("STEP 2：ツールのフォルダを配置・共有する")
body("フォルダ全体（web_server.py等を含むフォルダ）をPCの好きな場所に配置します。")
body("例：C:\\文字起こしツール\\")

subheading("👥 他の人に配る・共有する方法")
body("このフォルダ全体をそのままZIPなどで他の人に渡すだけで共有可能です。")
bullet("設定変更不要：バッチファイルが自分のフォルダを自動判別するため、書き換え不要で動作。")
bullet("注意点：他の人に渡す前に output フォルダ内の個人ファイルは消しておくと安全です。")

separator()
heading("STEP 3：必要なライブラリをインストールする")
body("1. PowerShellを開く（Windowsキー + R → powershell → Enter）")
body("2. ファイルを置いたフォルダに移動する（例）：")
code_block('cd "C:\\文字起こしツール"')
body("3. 以下を入力して必要な部品をインストール：")
code_block("pip install -r requirements.txt")
body("4. 「Successfully installed」と出れば成功！")

separator()
heading("STEP 4：Gemini APIキーを取得する")
body("APIキー＝AIを使うための無料のパスワード。")
body("1. ブラウザで以下を開く")
code_block("https://aistudio.google.com/apikey")
body("2. 個人のGmailアカウント（@gmail.com）でログインする")
warn("会社や学校のアカウントだと権限エラーになることがあります")
body("3.「APIキーを作成」をクリックしてキーをコピーする")

separator()
heading("STEP 5：APIキーをPCに登録する")
body("1. PowerShellで以下を入力（キーを差し替えてください）：")
code_block('setx GEMINI_API_KEY "AIzaSyここに貼り付け"')
body("2.「SUCCESS: 指定した値は保存されました。」と出たら完了")
warn("PowerShellを完全に閉じて開き直してください（設定反映のため）")

separator()
heading("🎉 使い方（セットアップ完了後）")
body("1.「run_transcriber.bat」をダブルクリック")
body("2. 黒い画面が開いた後、自動的にブラウザが立ち上がりWeb画面が開きます。")
body("3. 画面内のボタンやエリアを使って、直感的に操作できます：")
bullet("PC音声をリアルタイム録音：大きなマイクボタンをクリック（開始・停止）")
bullet("ファイルを文字起こし：音声や動画ファイルを点線エリアにドラッグ＆ドロップ")
body("4. 完了後、画面上の「PDFをダウンロード」ボタンからPDFを保存します。")
body("5. 終了時は起動した黒い画面を「×」ボタンで閉じます。")

separator()
heading("出力ファイルの場所")
body("ツールフォルダ内の output フォルダに保存されます。")
table_row("ファイル", "内容", True)
table_row("[AIタイトル]_[日時].pdf", "文字起こし結果のPDF（タイムスタンプ＆全文）")
table_row("recording_[日時].wav", "録音された生の音声データ（録音時のみ）")

separator()
heading("よくあるトラブルと対処法")
table_row("症状", "対処法", True)
table_row("サーバーに接続できません", "PythonのPATHチェック忘れ、またはAPIキー未登録")
table_row("APIキーがないと言われる", "setxの後、PowerShellを一度閉じて開き直す")
table_row("キーを作成する権限がない", "個人のGmailに切り替える")
table_row("録音エラーが出る", "PCの音量やスピーカー接続を確認してください")

separator()
heading("費用について")
bullet("Python・ツール本体：完全無料")
bullet("Gemini API：無料枠あり（通常利用ではお金はかかりません）")

# 保存
c.save()
print(f"完了！ → {output_path}")
