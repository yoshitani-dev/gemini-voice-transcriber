@echo off
cd /d "%~dp0"

echo =======================================================
echo   画面録画 ＆ スライド抽出ツール
echo =======================================================
echo.
echo   画面を録画し、自動でキースライド抽出と文字起こしを行います。
echo.
Gemini_CLI_Transcriber.exe --record-screen
echo.
pause
