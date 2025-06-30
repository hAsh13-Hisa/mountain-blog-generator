#!/bin/bash

# lftpを使った高速FTPデプロイ
# lftpインストール: sudo apt-get install lftp

source .env

echo "=== lftp高速デプロイ開始 ==="

# lftp設定
cat > ~/.lftprc << EOF
set ssl:verify-certificate no
set ftp:ssl-allow no
set ftp:passive-mode on
EOF

# デプロイ実行
lftp -c "
open ftp://$LOLIPOP_FTP_USER:$LOLIPOP_FTP_PASS@$LOLIPOP_FTP_HOST
mirror -R --verbose --parallel=5 dist/ $LOLIPOP_REMOTE_DIR/
bye
"

echo "=== デプロイ完了 ==="