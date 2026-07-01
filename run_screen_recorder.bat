@echo off
cd /d "%~dp0"

echo =======================================================
echo   PC録音 ＋ 画面録画 (任意) ツール
echo =======================================================
echo.
echo   PCの音声をリアルタイムで録音し、AIが文字起こしします。
echo   あわせて画面を録画し、スライドを抽出することも可能です。
echo.

choice /C yn /M "画面も録画して自動でスライドを抽出しますか？ [y: 画面録画＋音声 / n: 音声のみ]"
if errorlevel 2 (
    echo.
    echo ＞ 【音声のみ】 画面録画は行わず、PC音声の文字起こしのみ行います。
    python audio_transcriber.py
) else (
    echo.
    echo ＞ 【画面録画＋音声】 画面を録画し、スライド抽出と文字起こしを行います。
    python audio_transcriber.py --record-screen
)

echo.
pause
