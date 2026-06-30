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
[![Download ZIP](https://img.shields.io/badge/Download-Latest%20ZIP-green?style=for-the-badge&logo=github)](https://github.com/yoshitani-dev/Gemini-Voice-Transcriber/releases/latest/download/Gemini-Voice-Transcriber.zip)

Simply download the ZIP, extract it, and run the tool on Windows!

### ✨ Features
- **Real-time System Audio Recording**: Captures computer internal audio using WASAPI loopback.
- **High-accuracy AI Transcription**: Powered by Google's Gemini API (`gemini-3.5-flash` with automatic fallback to `gemini-2.0-flash`).
- **🆕 Video Key Slide Extraction**: Automatically extracts important slides, charts, and documents from recorded videos using Gemini's vision capabilities.
- **Filler Word Removal**: Automatically strips out filler words (e.g., "uhm", "uh", "like") and resolves hallucinated repetitions.
- **Bilingual Web UI**: Easy-to-use browser interface with light/dark theme aesthetics and English/Japanese language toggle.
- **Auto-generated PDFs**: Converts transcriptions into formatted PDF documents with AI-generated titles. 
- **WAV Splitter Utility**: Built-in tool to split large audio files for smoother uploads.

### 🛠️ Installation

#### Prerequisites
- Windows 10/11
- Python 3.9 or higher
- ffmpeg (optional, required for video key slide extraction)

#### Step 1: Install Dependencies
Open PowerShell in the project directory and run:
```powershell
pip install -r requirements.txt
```

#### Step 2: Get Gemini API Key
1. Go to [Google AI Studio](https://aistudio.google.com/apikey).
2. Generate a free API key.

#### Step 3: Set Environment Variable
Register your API key to Windows:
```powershell
setx GEMINI_API_KEY "YOUR_API_KEY_HERE"
```
*Note: Restart your terminal/command prompt after running this command to apply the changes.*

---

### 🚀 Usage

#### 1. Via Web Browser UI (Recommended)
Launch the local web server:
```powershell
python web_server.py
```
Open `http://127.0.0.1:8000` in your browser. Click the microphone button to record, or upload an audio file to transcribe.

#### 2. Via Command Line
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

#### 3. WAV Splitter
For large audio files:
```powershell
python split_wav.py
```

#### 4. 🆕 Video Key Slide Extraction
Extract important slides and generate rich minutes from recorded meeting videos:
```powershell
# Basic usage
python audio_transcriber.py --video meeting.mp4 --extract-key-slides

# Custom settings
python audio_transcriber.py --video meeting.mp4 --extract-key-slides --frame-interval 30 --max-key-slides 15

# Dry-run (check frame extraction without API calls)
python audio_transcriber.py --video meeting.mp4 --extract-key-slides --dry-run
```

**Output files:**
- `key_slides/` — Extracted key slide images
- `key_slides.json` — Structured analysis data for each slide
- `rich_minutes.md` — Integrated minutes with slides and transcript

If this project is useful, please consider giving it a star ⭐
---



## 日本語

## 📥 簡単ダウンロード
[![ZIPファイルをダウンロード](https://img.shields.io/badge/ダウンロード-最新版ZIP-green?style=for-the-badge&logo=github)](https://github.com/yoshitani-dev/Gemini-Voice-Transcriber/releases/latest/download/Gemini-Voice-Transcriber.zip)

PC初心者の方は、上記のボタンからZIPファイルをダウンロードして解凍するだけで、簡単にWindows上でツールをご利用いただけます。

### ✨ 主な機能
- **PCシステム音声録音**: WASAPIループバックを使用し、会議や動画の音声をクリアに直接録音。
- **高精度AI文字起こし**: Googleの `gemini-3.5-flash` を使用（高負荷時は `gemini-2.0-flash` へ自動切り替え）。
- **�᥆ 動画キースライド抽出**: 会議や授業の録画動画から、重要なスライド・チャート・資料をGeminiのAI解析で自動抽出。文字起こしと統合したリッチ議事録を生成。
- **つなぎ言葉（フィラー）の自動除去**: 「えーっと」「あのー」などを自動で取り除き、同じ言葉が連続するループ現象（ハルシネーション）も自動で除去。
- **日英バイリンガル Web UI**: ブラウザからボタン一つで録音・アップロード・文字起こしができる美しい操作画面。言語切り替えに対応。
- **PDF自動出力**: 文字起こし結果から、AIが最適なタイトルを付けてフォーマットされたPDFを出力。
- **WAV分割機能**: 長時間の巨大な音声ファイルを自動で分割するユーティリティを内蔵。

### 🛠️ 初期設定

#### 動作環境
- Windows 10/11
- Python 3.9 以上
- ffmpeg（オプション、動画キースライド抽出に必要）

#### 手順 1: ライブラリのインストール
プロジェクトフォルダでPowerShellを開き、以下を実行します：
```powershell
pip install -r requirements.txt
```

#### 手順 2: Gemini API キーの取得
1. [Google AI Studio](https://aistudio.google.com/apikey) にアクセス。
2. 無料のAPIキーを作成します。

#### 手順 3: APIキーの登録
WindowsにAPIキーを環境変数として登録します：
```powershell
setx GEMINI_API_KEY "取得したAPIキー"
```
*※設定後、設定を反映させるために一度PowerShellやコマンドプロンプトを閉じてください。*

---

### 🚀 使い方

#### 1. ブラウザ画面（Web UI）から使う（推奨）
Webサーバーを起動します：
```powershell
python web_server.py
```
起動後、ブラウザで `http://127.0.0.1:8000` を開きます。画面の「JP/EN」ボタンで言語が切り替わります。

#### 2. コマンドライン（CUI）から使う
- **PC音声を録音して文字起こし**:
  ```powershell
  python audio_transcriber.py
  ```
- **既存の音声ファイルを文字起こし**:
  ```powershell
  python audio_transcriber.py "音声ファイルのパス.mp3"
  ```

#### 3. バッチファイルから使う
ダブルクリックするだけで簡単に起動できるバッチファイルも同梱しています：
- `run_transcriber.bat` (ダブルクリックでPC音声の録音を開始。音声・動画ファイルをこのアイコンの上にドラッグ＆ドロップすると直接文字起こしを実行します)

#### 4. 🆕 動画からキースライドを抽出する
会議や授業の録画動画から、重要なスライドを抽出してリッチ議事録を生成します：
```powershell
# 基本的な使い方
python audio_transcriber.py --video 会議録画.mp4 --extract-key-slides

# 詳細設定
python audio_transcriber.py --video 会議録画.mp4 --extract-key-slides --frame-interval 30 --max-key-slides 15

# 動作確認（APIを呼ばずにフレーム抽出だけ確認）
python audio_transcriber.py --video 会議録画.mp4 --extract-key-slides --dry-run
```

**出力ファイル:**
- `key_slides/` — 抽出されたキースライド画像
- `key_slides.json` — 各スライドの構造化された解析データ
- `rich_minutes.md` — スライドと文字起こしが統合されたリッチ議事録

> ※ ffmpegが必要です。インストール: `winget install ffmpeg`

このプロジェクトが役に立ったら、Starを押してもらえると嬉しいです ⭐
---


## 🗺️ Roadmap / 今後の予定
- [ ] Add dark mode support to the Web UI / Web UIのダークモード対応
- [ ] Support export as Markdown / Markdown形式での書き出しサポート
- [ ] Real-time progressive transcription / リアルタイム順次文字起こし表示
- [ ] Support macOS (CoreAudio) / macOSへの対応

---

## 📝 License / ライセンス
This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
本プロジェクトはMITライセンスのもとで公開されています。詳細は [LICENSE](LICENSE) ファイルをご覧ください。
