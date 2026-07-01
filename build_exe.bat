@echo off
echo ========================================
echo Building Executables using PyInstaller
echo ========================================

REM Check if PyInstaller is installed
python -m pip install pyinstaller


echo.
echo Building audio_transcriber.exe...
pyinstaller --name "Gemini_CLI_Transcriber" --onefile audio_transcriber.py

echo.
echo ========================================
echo Build complete! Executables are in the 'dist' folder.
echo ========================================
pause
