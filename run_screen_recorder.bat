@echo off
cd /d "%~dp0"

set "EXE_PATH="
if exist "Gemini_CLI_Transcriber.exe" (
    set "EXE_PATH=Gemini_CLI_Transcriber.exe"
) else if exist "audio_transcriber.py" (
    set "EXE_PATH=python audio_transcriber.py"
) else (
    echo 実行に必要なファイル（Gemini_CLI_Transcriber.exe または audio_transcriber.py）が見つかりません。
    pause
    exit /b
)

echo =======================================================
echo   画面録画 ＆ スライド抽出ツール
echo =======================================================
echo.
echo   画面を録画し、自動でキースライド抽出と文字起こしを行います。
echo.
%EXE_PATH% --record-screen
echo.
pause
