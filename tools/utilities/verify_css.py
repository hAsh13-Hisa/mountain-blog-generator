#!/usr/bin/env python3
"""
CSSディレクトリの確認
"""
import ftplib
import os
from dotenv import load_dotenv

load_dotenv()

try:
    ftp = ftplib.FTP(os.getenv('LOLIPOP_FTP_HOST'))
    ftp.login(os.getenv('LOLIPOP_FTP_USER'), os.getenv('LOLIPOP_FTP_PASS'))
    
    ftp.cwd(os.getenv('LOLIPOP_REMOTE_DIR'))
    
    # ルートのファイル一覧（詳細）
    print("📁 ルートディレクトリの詳細:")
    items = []
    ftp.retrlines('LIST', items.append)
    for item in items:
        print(f"  {item}")
    
    # cssディレクトリの確認
    print("\n📁 cssディレクトリの確認:")
    try:
        ftp.cwd('css')
        css_items = []
        ftp.retrlines('LIST', css_items.append)
        for item in css_items:
            print(f"  {item}")
        ftp.cwd('..')
    except Exception as e:
        print(f"  ❌ cssディレクトリエラー: {e}")
    
    ftp.quit()
    
except Exception as e:
    print(f"❌ エラー: {e}")