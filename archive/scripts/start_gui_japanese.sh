#!/bin/bash
# 日本語環境でGUIを起動するスクリプト

# 環境変数設定
export PYTHONIOENCODING=utf-8
export LANG=C.UTF-8
export LC_CTYPE=C.UTF-8
export PYTHONHASHSEED=0

# 仮想環境をアクティベート
source venv/bin/activate

# GUI起動
python3 gui_launcher.py
