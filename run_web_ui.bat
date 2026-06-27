@echo off
cd /d "%~dp0"

echo =======================================================
echo   Gemini Voice Transcriber - Web UI
echo =======================================================
echo.
echo   Starting Web Server...
echo   Opening browser at http://127.0.0.1:8000
echo.

start http://127.0.0.1:8000
python web_server.py

pause
