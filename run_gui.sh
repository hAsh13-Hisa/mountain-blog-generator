#!/bin/bash
# Low Mountain Blog Generator GUI 起動スクリプト

cd "$(dirname "$0")"

# 仮想環境をアクティベート
source venv/bin/activate

# Pythonパスにプロジェクトルートを追加してGUIを起動
export PYTHONPATH="$(pwd):$PYTHONPATH"
export PYTHONIOENCODING=utf-8

echo "🏔️ Low Mountain Blog Generator を起動中..."
python3 src/presentation/gui.py