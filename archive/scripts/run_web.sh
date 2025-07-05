#!/bin/bash
# Mountain Blog Generator - Web UI 起動スクリプト

cd "$(dirname "$0")"

# 仮想環境をアクティベート
source venv/bin/activate

# Pythonパスにプロジェクトルートを追加
export PYTHONPATH="$(pwd):$PYTHONPATH"
export PYTHONIOENCODING=utf-8

echo "🌐 Mountain Blog Generator Web UI を起動中..."
echo "📍 URL: http://localhost:5001"
echo "📋 ヘルスチェック: http://localhost:5001/health"
echo "🔧 デバッグモード: ON"
echo ""
echo "停止するには Ctrl+C を押してください"
echo ""

# Web アプリケーションを起動
python3 src/presentation/web/app.py