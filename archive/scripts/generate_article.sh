#!/bin/bash
# 簡単記事生成スクリプト

# 仮想環境をアクティベート
source venv/bin/activate

# コマンドを実行
python simple_article_generator.py "$@"

# 仮想環境を終了
deactivate