@echo off
cd /d "%~dp0"

if "%~1"=="" (
    echo =======================================================
    echo   音声文字起こしツール
    echo =======================================================
    echo.
    echo   PC音声をリアルタイムで録音して文字起こしします。
    echo.
    python audio_transcriber.py
) else (
    echo =======================================================
    echo   ファイル文字起こしツール
    echo =======================================================
    echo.
    echo   処理するファイル: %~nx1
    echo.
    
    rem 動画ファイルかどうかの簡易判定
    echo "%~x1" | findstr /i "\.mp4 \.avi \.mkv \.mov \.wmv \.flv \.webm" >nul
    if not errorlevel 1 (
        echo 【動画ファイルが指定されました】
        
        rem 引数にすでに --extract-key-slides が含まれている場合は質問をスキップ
        echo "%*" | findstr /i "\-\-extract-key-slides" >nul
        if not errorlevel 1 (
            echo ＞ 抽出オプションが指定されているため、確認をスキップしてスライド抽出を行います。
            python audio_transcriber.py --video "%~1" --extract-key-slides
        ) else (
            rem 2分間入力がなければ自動でN（しない）を選択して進行
            choice /C YN /T 120 /D N /M "キースライド（スライド画像）も抽出しますか？ [Y:する / N:しない（音声のみ）]"
            if errorlevel 2 (
                echo.
                echo ＞ スライド抽出はスキップし、音声の文字起こしのみ行います。
                python audio_transcriber.py --video "%~1"
            ) else (
                echo.
                echo ＞ スライド抽出と音声の文字起こしを行います。
                python audio_transcriber.py --video "%~1" --extract-key-slides
            )
        )
    ) else (
        python audio_transcriber.py "%~1"
    )
)

echo.
pause
