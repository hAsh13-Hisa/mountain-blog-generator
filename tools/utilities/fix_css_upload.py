#!/usr/bin/env python3
"""
CSSファイルを個別にアップロード
"""
import ftplib
import os
from dotenv import load_dotenv

load_dotenv()

try:
    # FTP接続
    ftp = ftplib.FTP(os.getenv('LOLIPOP_FTP_HOST'))
    ftp.login(os.getenv('LOLIPOP_FTP_USER'), os.getenv('LOLIPOP_FTP_PASS'))
    print("✅ FTP接続成功")
    
    # リモートディレクトリに移動
    ftp.cwd(os.getenv('LOLIPOP_REMOTE_DIR'))
    
    # cssディレクトリ作成
    try:
        ftp.mkd('css')
        print("📁 cssディレクトリを作成")
    except:
        print("📁 cssディレクトリは既に存在")
    
    # CSSファイルアップロード
    with open('static_site/css/style.css', 'rb') as f:
        ftp.storbinary('STOR css/style.css', f)
        print("✅ css/style.css をアップロード完了")
    
    # 確認
    ftp.cwd('css')
    css_files = ftp.nlst()
    print(f"📄 css/ 内のファイル: {css_files}")
    
    ftp.quit()
    print("✅ CSS修正完了！")
    
except Exception as e:
    print(f"❌ エラー: {e}")