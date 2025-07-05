#!/bin/bash
# 複数キーワード対応版記事生成スクリプト

# 仮想環境をアクティベート
source venv/bin/activate

# コマンドを実行
python simple_article_generator_v2.py "$@"

# 仮想環境を終了
deactivate