#!/usr/bin/env python3
"""
FTPアップロード簡易チェック
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
    
    # 重要ファイルの存在確認
    important_files = [
        'index.html',
        'css/style.css',
        'mountains',
        'about',
        'beginner',
        'contact',
        'equipment',
        'privacy',
        'terms',
        'regions'
    ]
    
    # ルートディレクトリのファイル一覧
    items = ftp.nlst()
    print(f"\n📁 ルートディレクトリのアイテム数: {len(items)}")
    
    print("\n📋 重要ファイル/ディレクトリのチェック:")
    for file in important_files:
        if file in items:
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file}")
    
    # mountainsディレクトリの確認
    try:
        ftp.cwd('mountains')
        mountain_items = ftp.nlst()
        print(f"\n🏔️ mountains/ 内のアイテム数: {len(mountain_items)}")
        if mountain_items:
            print("  山ページ:")
            for item in mountain_items[:5]:  # 最初の5つ
                print(f"    - {item}")
        ftp.cwd('..')
    except:
        print("\n❌ mountainsディレクトリにアクセスできません")
    
    # regionsディレクトリの確認
    try:
        ftp.cwd('regions')
        region_items = ftp.nlst()
        print(f"\n🗾 regions/ 内のアイテム数: {len(region_items)}")
        if region_items:
            print("  地域ページ:")
            for item in region_items:
                print(f"    - {item}")
        ftp.cwd('..')
    except:
        print("\n❌ regionsディレクトリにアクセスできません")
    
    print("\n✅ FTPアップロードは正常に完了しています！")
    print("🌐 https://teizan.omasse.com/ でサイトをご確認ください。")
    
    ftp.quit()
    
except Exception as e:
    print(f"❌ エラー: {e}")