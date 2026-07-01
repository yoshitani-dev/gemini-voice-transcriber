@echo off
cd /d "%~dp0"
echo =======================================================
echo   PC録音 ＋ 画面録画 (任意) ツール - Webブラウザ版
echo =======================================================
echo.
echo ブラウザで http://localhost:5000 を開きます...
start http://localhost:5000
Gemini_Web_Server.exe
pause
