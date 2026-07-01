@echo off
cd /d "%~dp0"
echo =======================================================
echo   PC録音 ＋ 画面録画 (任意) ツール - コマンドライン版
echo =======================================================
echo.
echo   PCの音声をリアルタイムで録音し、AIが文字起こしします。
echo   あわせて画面を録画し、スライドを抽出することも可能です。
echo.
choice /C yn /N /M "画面も録画して自動でスライドを抽出しますか？ [y: 画面録画＋音声 / n: 音声のみ] [y,n]? "
if errorlevel 2 (
    echo.
    echo ＞ 【音声のみ】 画面録画は行わず、PC音声の文字起こしのみ行います。
    Gemini_CLI_Transcriber.exe
) else (
    echo.
    echo ＞ 【画面録画＋音声】 画面を録画し、スライド抽出と文字起こしを行います。
    Gemini_CLI_Transcriber.exe --record-screen
)
echo.
pause
