# 🎙️ Gemini Voice Transcriber — User Manual

> This manual is designed for users of all technical levels.
> Follow these steps in order to get the tool up and running on your Windows PC.

---

## 📋 Features

This tool captures computer internal audio (from meetings, lectures, videos, etc.) and **automatically transcribes it into structured PDF documents**.

- Filler words (like "uhm", "uh", "like") are **automatically filtered out**.
- The AI **automatically generates a title** based on the transcription content.
- Large audio files are automatically compressed before uploading.

```
PC Audio → Auto Recording → Gemini AI Transcription → Formatted PDF Saved!
```

---

## 🗂️ Table of Contents

1. [Initial Setup (First Time Only)](#1-initial-setup-first-time-only)
2. [Record and Transcribe PC Audio (Real-time)](#2-record-and-transcribe-pc-audio-real-time)
3. [Transcribe Existing Audio/Video Files](#3-transcribe-existing-audiovideo-files)
4. [Output Files](#4-output-files)
5. [Troubleshooting Checklist](#5-troubleshooting-checklist)

---

## 1. Initial Setup (First Time Only)

> [!IMPORTANT]
> You only need to perform these steps **once**. It takes about 10 minutes.

### STEP 1: Install Python (If not already installed)

1. Open your browser and go to:  
   👉 **https://www.python.org/downloads/**
2. Click the yellow **"Download Python 3.x.x"** button.
3. Open the downloaded installer file.
4. **⚠️ CRITICAL: Check the box "Add Python to PATH" at the bottom of the first screen!**  
   *(If you miss this, the tool will not run.)*
5. Click **"Install Now"** to begin the installation.
6. Once finished, click "Close".

### STEP 2: Install Required Dependencies

1. Open File Explorer and go to the folder where you extracted this tool (where `run_transcriber.bat` is located).
2. Click on the **address bar** at the top of the File Explorer window (showing the current path).
3. Type **`powershell`** in lowercase and press **Enter**.  
   👉 This opens a blue PowerShell terminal window directly pointing to your project folder!
4. Copy the following command (Ctrl+C):
   ```powershell
   pip install -r requirements.txt
   ```
5. **Right-click** inside the PowerShell window to paste the command automatically.
6. Press **Enter** to run the installation.
   - Text will scroll down the screen. This is normal.
   - Once it shows **`Successfully installed...`**, the process is complete.
   - *(You can ignore any yellow warning messages about "A new release of pip is available".)*

### STEP 3: Get a Gemini API Key

An API key is your personal password to access Google's Gemini AI.  
> [!NOTE]
> It is **completely free** for standard usage!

1. Open your browser and visit:  
   👉 **https://aistudio.google.com/apikey**
2. Sign in with your Google account.
   - ⚠️ **Important**: Work or school accounts (e.g., @company.com) often have administrative restrictions. If you get an error, click your profile icon in the top right and **switch to a personal Gmail account (@gmail.com)**.
3. Click the blue **"Create API key"** button.
4. Select "Create API key in a new project" if prompted.
5. A long code starting with `AIzaSy...` will be displayed. This is your API key.
   - Click the **"Copy"** button and copy it.

That's it for the preparation!
You will enter this API key directly into the application screen the very first time you start it. Please keep it copied.

---

---

## 2. Record and Transcribe PC Audio (Real-time)

Use this method to record meetings, webinars, or videos in real-time.

### How to Start

Double-click the **`run_transcriber.bat`** file!

A local server will start, and a web page will automatically open in your browser (`http://localhost:8000`).

### Using the Web UI

1. Click the **"JP | EN"** language toggle in the top-right corner to switch the interface to English.
2. Click the large **Microphone button** 🎙️ to start recording.
3. Play the audio on your PC (start your video, meeting, etc.).
4. Click the **Stop button** ⏹️ when finished.
5. The tool will automatically:
   - Save the raw audio.
   - Upload it to Gemini API.
   - Transcribe the audio and clean up filler words.
   - Generate an AI title and create a formatted PDF.
6. Click **"Download PDF"** to save your transcription!

---

## 3. Transcribe Existing Audio/Video Files

If you already have audio/video files (mp3, wav, m4a, mp4, etc.):

1. Drag and drop your audio or video file directly into the **dotted upload area** on the browser Web UI.
2. The transcription and PDF generation will start automatically.

*(Alternatively, you can drag & drop the file directly onto the `run_transcriber.bat` icon in File Explorer.)*

---

## 4. Output Files

Once processing completes, files are saved in the **`output`** folder:

| Filename | Description |
|---|---|
| `recording_Datetime.wav` | The raw recorded audio file (Recording mode only). |
| `[AI_Generated_Title]_Datetime.pdf` | 📄 **The formatted PDF transcript (Main output).** |

> [!NOTE]
> The PDF filename and title are automatically generated by the AI based on the conversation content (e.g., `TeamMeeting_20260627_140000.pdf`).

---

## 5. Troubleshooting Checklist

### ❌ Error: "API Key not set"
- Did you enter and save the API key correctly when prompted?
- Are there any extra spaces in the key?

### ❌ Error: "No loopback device found"
- Are your PC speakers or headphones plugged in and working?
- Go to Windows "Sound Settings" and make sure your output device is set to your active speakers.

### ❌ Low Transcription Accuracy / Weird Text Output
- Was the PC volume loud enough during recording?
- Did you record silence? (Recording with no audio playing causes the AI to hallucinate words).

---

## 👥 How to Share This Tool

You can share this tool simply by **sending the folder** (as a ZIP file) to others.

- **No Configuration Needed**: The batch files automatically detect their paths, so they work out-of-the-box anywhere.
- **Important Note**:
  - Delete files in the `output` folder before sharing to protect your privacy.
  - **Do not share your API key**. Receivers must obtain and configure their own API keys (refer to STEP 3 & 4).
