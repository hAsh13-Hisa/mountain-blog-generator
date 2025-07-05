#!/bin/bash

# ロリポップFTPデプロイスクリプト

echo "=== ロリポップサーバーへのデプロイ開始 ==="

# 1. 記事生成
echo "1. 新規記事を生成しますか？ (y/n)"
read -r GENERATE_NEW

if [ "$GENERATE_NEW" = "y" ]; then
    echo "生成する山のIDを入力してください (例: mt_maruyama_hokkaido):"
    read -r MOUNTAIN_ID
    python simple_article_generator.py "$MOUNTAIN_ID"
fi

# 2. FTPデプロイ
echo "2. FTPデプロイを実行します..."
python ftp_deploy.py

# 3. 結果確認
echo "3. デプロイ完了！"
echo "サイトURL: https://your-domain.lolipop.jp/mountain-blog/"

# オプション: lftp を使った高速アップロード
# lftp -c "open -u $FTP_USER,$FTP_PASS ftp.lolipop.jp; mirror -R dist/ /mountain-blog/"