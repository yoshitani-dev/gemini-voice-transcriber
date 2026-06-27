@echo off
chcp 65001 >nul 2>&1
rem split_wav.pyを簡単に実行するためのバッチファイルです。
rem バッチファイルに渡されたすべての引数をそのままPythonスクリプトに引き渡します。

cd /d "%~dp0"
python split_wav.py %*
