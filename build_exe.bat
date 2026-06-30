@echo off
echo ========================================
echo Building Executables using PyInstaller
echo ========================================

REM Check if PyInstaller is installed
python -m pip install pyinstaller

REM Build the Web Server (FastAPI) executable
echo.
echo Building web_server.exe...
pyinstaller --name "Gemini_Web_Server" --onefile --add-data "templates;templates" web_server.py

REM Build the CLI executable
echo.
echo Building audio_transcriber.exe...
pyinstaller --name "Gemini_CLI_Transcriber" --onefile audio_transcriber.py

echo.
echo ========================================
echo Build complete! Executables are in the 'dist' folder.
echo ========================================
pause
