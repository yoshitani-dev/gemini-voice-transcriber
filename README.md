# 🎙️ Gemini Voice Transcriber (音声文字起こしツール)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![Gemini](https://img.shields.io/badge/AI-Gemini%203.5-blueviolet.svg)](https://aistudio.google.com/)

A powerful, user-friendly desktop application for real-time system audio recording and transcription using the Gemini API. It outputs structured PDF files with auto-generated titles.

Windows環境で動作する、PCシステム音声のリアルタイム録音・文字起こしツールです。Gemini APIを活用し、要約・整形されたPDFマニュアルを自動で生成します。

---

## Language / 言語
- [English (README_EN)](#english)
- [日本語 (README_JA)](#日本語)

---

## English

## 📥 Download
[![Download ZIP](https://img.shields.io/badge/Download-Latest%20ZIP-green?style=for-the-badge&logo=github)](https://github.com/yoshitani-dev/Gemini-Voice-Transcriber/releases/latest/download/Gemini-Voice-Transcriber-Windows.zip)

Simply download the ZIP, extract it, and run the tool on Windows!

### ✨ Features
- **Real-time System Audio Recording**: Captures computer internal audio using WASAPI loopback.
- **High-accuracy AI Transcription**: Powered by Google's Gemini API (`gemini-3.5-flash` with automatic fallback to `gemini-2.0-flash`).
- **🆕 Video Key Slide Extraction**: Automatically extracts important slides, charts, and documents from recorded videos using Gemini's vision capabilities.
- **Filler Word Removal**: Automatically strips out filler words (e.g., "uhm", "uh", "like") and resolves hallucinated repetitions.
- **Auto-generated PDFs**: Converts transcriptions into formatted PDF documents with AI-generated titles. 
- **WAV Splitter Utility**: Built-in tool to split large audio files for smoother uploads.

### 🛠️ Initial Setup: Get Gemini API Key
1. Go to [Google AI Studio](https://aistudio.google.com/apikey).
2. Generate a free API key.

*(No complicated environment variable setup is required! You will be prompted to enter this key the first time you run the app.)*

---

### 🚀 Usage

#### 1. For General Users (Recommended)

1. Download the ZIP file (`Gemini-Voice-Transcriber-Windows.zip`) from the **Releases (Assets)** section.
2. Extract the downloaded ZIP file.
3. Double-click **`run_transcriber.bat`** to start the application. (If you want to record the screen and extract key slides, double-click **`run_screen_recorder.bat`** instead). (You can also drag and drop audio/video files directly onto it for automatic transcription.)

#### 2. For Developers (From Source)

**Prerequisites:**
- Windows 10/11
- Python 3.9 or higher
- ffmpeg (optional, required for video key slide extraction)

**Step 1: Install Dependencies**
Open PowerShell in the project directory and run:
```powershell
pip install -r requirements.txt
```

**Step 2: Run via Command Line**
- **Record and Transcribe**:
  ```powershell
  python audio_transcriber.py
  ```
- **Transcribe existing audio file**:
  ```powershell
  python audio_transcriber.py "path/to/your/audio.mp3"
  ```
- **Transcribe in a specific language**:
  ```powershell
  python audio_transcriber.py "audio.mp3" --language en
  ```
- **WAV Splitter** (For large audio files):
  ```powershell
  python split_wav.py
  ```
- **🆕 Video Key Slide Extraction**:
  ```powershell
  python audio_transcriber.py --video meeting.mp4 --extract-key-slides
  ```
- **🎥 Real-time Screen Recording & Auto Analysis**:
  ```powershell
  python audio_transcriber.py --record-screen
  ```

> [!WARNING]
> **Screen Recording Mode Privacy Notice**
> - The entire desktop will be recorded. Any overlapping windows, notifications, or personal chats will be captured.
> - **IMPORTANT**: Screenshots extracted from the recording will be uploaded to **Google Gemini API cloud servers** for analysis.
> - Please ensure you hide sensitive information before starting.
> - Ensure you have permission to record the meeting.
> - Screen recording requires `ffmpeg`.

If this project is useful, please consider giving it a star ⭐
---



## 日本語

## 📥 簡単ダウンロード
[![ZIPファイルをダウンロード](https://img.shields.io/badge/ダウンロード-最新版ZIP-green?style=for-the-badge&logo=github)](https://github.com/yoshitani-dev/Gemini-Voice-Transcriber/releases/latest/download/Gemini-Voice-Transcriber-Windows.zip)

PC初心者の方は、上記のボタンからZIPファイルをダウンロードして解凍するだけで、簡単にWindows上でツールをご利用いただけます。

### ✨ 主な機能
- **PCシステム音声録音**: WASAPIループバックを使用し、会議や動画の音声をクリアに直接録音。
- **高精度AI文字起こし**: Googleの `gemini-3.5-flash` を使用（高負荷時は `gemini-2.0-flash` へ自動切り替え）。
- **🆕 動画キースライド抽出**: 会議や授業の録画動画から、重要なスライド・チャート・資料をGeminiのAI解析で自動抽出。文字起こしと統合したリッチ議事録を生成。
- **つなぎ言葉（フィラー）の自動除去**: 「えーっと」「あのー」などを自動で取り除き、同じ言葉が連続するループ現象（ハルシネーション）も自動で除去。
- **PDF自動出力**: 文字起こし結果から、AIが最適なタイトルを付けてフォーマットされたPDFを出力。
- **WAV分割機能**: 長時間の巨大な音声ファイルを自動で分割するユーティリティを内蔵。

### 🛠️ 初期設定: Gemini API キーの取得
1. [Google AI Studio](https://aistudio.google.com/apikey) にアクセス。
2. 無料のAPIキーを作成します。

*(※難しい環境変数の設定は不要です！アプリを最初に起動したときに画面から入力できます。)*

---

### 🚀 使い方

#### 1. 一般ユーザー向け（推奨）

1. **Releases** の Assets から ZIPファイル（`Gemini-Voice-Transcriber-Windows.zip`）をダウンロードします。
2. ダウンロードした ZIPファイルを解凍（展開）します。
3. フォルダ内にある **`run_transcriber.bat`** をダブルクリックするだけで起動します。
   （※画面録画とスライド抽出を行いたい場合は、**`run_screen_recorder.bat`** をダブルクリックしてください）
   （音声・動画ファイルをこのアイコンの上にドラッグ＆ドロップすると、直接文字起こしを実行することもできます）

#### 2. 開発者向け（ソースコードから実行）

**動作環境:**
- Windows 10/11
- Python 3.9 以上
- ffmpeg（オプション、動画キースライド抽出に必要）

**手順 1: ライブラリのインストール**
プロジェクトフォルダでPowerShellを開き、以下を実行します：
```powershell
pip install -r requirements.txt
```

**手順 2: コマンドライン（CUI）から実行**
- **PC音声を録音して文字起こし**:
  ```powershell
  python audio_transcriber.py
  ```
- **既存の音声ファイルを文字起こし**:
  ```powershell
  python audio_transcriber.py "音声ファイルのパス.mp3"
  ```
- **🆕 動画からキースライドを抽出する**:
  ```powershell
  python audio_transcriber.py --video 会議録画.mp4 --extract-key-slides
  ```
- **🎥 リアルタイム画面録画 ＆ 全自動解析**:
  ```powershell
  python audio_transcriber.py --record-screen
  ```

> [!WARNING]
> **画面録画モードの注意（プライバシーについて）**
> - 画面録画モードでは「デスクトップ全体」が録画されます。上に重なった別のウィンドウや、ポップアップ通知、個人チャットなどもすべて録画されます。
> - **重要**: 録画された動画から抽出されたスクリーンショット画像は、解析のためにインターネット経由で **Google Gemini API（クラウドサーバー）** へ送信されます。
> - パスワードや機密情報が映り込まないよう十分ご注意ください。
> - 会議などで必要な録画の許可を得た上でご利用ください。
> - 本機能の利用には `ffmpeg` が必須となります。

このプロジェクトが役に立ったら、Starを押してもらえると嬉しいです ⭐
---


## 🗺️ Roadmap / 今後の予定
- [ ] Support export as Markdown / Markdown形式での書き出しサポート
- [ ] Real-time progressive transcription / リアルタイム順次文字起こし表示
- [ ] Support macOS (CoreAudio) / macOSへの対応

---

## 📝 License / ライセンス
This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
本プロジェクトはMITライセンスのもとで公開されています。詳細は [LICENSE](LICENSE) ファイルをご覧ください。
