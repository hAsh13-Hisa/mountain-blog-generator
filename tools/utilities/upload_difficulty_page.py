#!/usr/bin/env python3
"""
difficulty/beginner/ ページを個別にアップロード
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
    
    # difficultyディレクトリ作成
    try:
        ftp.mkd('difficulty')
        print("📁 difficultyディレクトリを作成")
    except:
        print("📁 difficultyディレクトリは既に存在")
    
    # difficulty/beginnerディレクトリ作成
    try:
        ftp.mkd('difficulty/beginner')
        print("📁 difficulty/beginnerディレクトリを作成")
    except:
        print("📁 difficulty/beginnerディレクトリは既に存在")
    
    # HTMLファイルアップロード
    with open('static_site/difficulty/beginner/index.html', 'rb') as f:
        ftp.storbinary('STOR difficulty/beginner/index.html', f)
        print("✅ difficulty/beginner/index.html をアップロード完了")
    
    # 確認
    ftp.cwd('difficulty')
    difficulty_items = ftp.nlst()
    print(f"📄 difficulty/ 内のアイテム: {difficulty_items}")
    
    ftp.cwd('beginner')
    beginner_items = ftp.nlst()
    print(f"📄 difficulty/beginner/ 内のアイテム: {beginner_items}")
    
    ftp.quit()
    print("✅ difficulty/beginner/ ページアップロード完了！")
    print("🌐 https://teizan.omasse.com/difficulty/beginner/ で確認してください")
    
except Exception as e:
    print(f"❌ エラー: {e}")