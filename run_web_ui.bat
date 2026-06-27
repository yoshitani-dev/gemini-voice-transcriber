@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo =======================================================
echo   Gemini Voice Transcriber - Web UI
echo =======================================================
echo.
echo   Webサーバーを起動しています...
echo   自動的にブラウザで操作画面が開きます。
echo   (画面が開かない場合はブラウザで http://127.0.0.1:8000 を開いてください)
echo.

:: ブラウザで自動的にWeb UIを開く
start http://127.0.0.1:8000

:: Webサーバーを起動する
python web_server.py

pause
