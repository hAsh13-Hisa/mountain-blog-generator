#!/usr/bin/env python3
"""
統合デプロイシステム
記事生成 → 静的サイト生成 → FTPアップロード
"""
import json
import os
from datetime import datetime
from pathlib import Path
from ftplib import FTP
import shutil
from static_site_generator import StaticSiteGenerator

class UnifiedDeploySystem:
    def __init__(self):
        self.generator = StaticSiteGenerator()
        self.ftp_host = os.getenv('LOLIPOP_FTP_HOST', 'ftp.lolipop.jp')
        self.ftp_user = os.getenv('LOLIPOP_FTP_USER')
        self.ftp_pass = os.getenv('LOLIPOP_FTP_PASS')
        self.remote_dir = os.getenv('LOLIPOP_REMOTE_DIR', '/mountain-blog')
        
    def deploy_article(self, article_json_path):
        """記事をデプロイ（生成→FTPアップロード）"""
        print(f"=== 記事デプロイ開始: {article_json_path} ===")
        
        # 1. 記事データ読み込み
        with open(article_json_path, 'r', encoding='utf-8') as f:
            article_data = json.load(f)
        
        # 2. 静的サイト生成（分類ページも自動更新）
        print("静的サイト生成中...")
        self.generator.add_article(article_data)
        
        # 3. CSSをコピー
        css_src = Path("static/style.css")
        css_dst = self.generator.base_dir / "css" / "style.css"
        if css_src.exists():
            shutil.copy2(css_src, css_dst)
        
        # 4. FTPアップロード
        print("FTPアップロード開始...")
        self.upload_to_ftp()
        
        print("=== デプロイ完了 ===")
        
    def upload_to_ftp(self):
        """生成されたファイルをFTPでアップロード"""
        try:
            # FTP接続
            ftp = FTP(self.ftp_host)
            ftp.login(self.ftp_user, self.ftp_pass)
            
            # リモートディレクトリに移動（なければ作成）
            self.ensure_remote_dir(ftp, self.remote_dir)
            
            # ローカルの静的サイトディレクトリから全ファイルをアップロード
            self.upload_directory(ftp, self.generator.base_dir, self.remote_dir)
            
            ftp.quit()
            print("FTPアップロード完了")
            
        except Exception as e:
            print(f"FTPエラー: {e}")
            raise
    
    def ensure_remote_dir(self, ftp, path):
        """リモートディレクトリを確認・作成"""
        dirs = path.strip('/').split('/')
        current = '/'
        
        for dir in dirs:
            if dir:
                current = f"{current}/{dir}".replace('//', '/')
                try:
                    ftp.cwd(current)
                except:
                    ftp.mkd(current)
                    ftp.cwd(current)
        
        ftp.cwd('/')
    
    def upload_directory(self, ftp, local_dir, remote_dir):
        """ディレクトリを再帰的にアップロード"""
        local_dir = Path(local_dir)
        
        for item in local_dir.iterdir():
            if item.is_file():
                # ファイルをアップロード
                remote_path = f"{remote_dir}/{item.name}"
                print(f"アップロード: {item} → {remote_path}")
                
                with open(item, 'rb') as f:
                    ftp.storbinary(f'STOR {remote_path}', f)
                    
            elif item.is_dir():
                # サブディレクトリを作成してアップロード
                remote_subdir = f"{remote_dir}/{item.name}"
                try:
                    ftp.mkd(remote_subdir)
                except:
                    pass  # 既に存在する場合
                
                self.upload_directory(ftp, item, remote_subdir)
    
    def deploy_all_articles(self):
        """すべての記事を再デプロイ"""
        articles_dir = Path("data/articles")
        if not articles_dir.exists():
            print("記事ディレクトリが見つかりません")
            return
        
        # すべての記事JSONファイルを処理
        for article_file in articles_dir.glob("*.json"):
            self.deploy_article(article_file)
    
    def check_ftp_connection(self):
        """FTP接続テスト"""
        try:
            ftp = FTP(self.ftp_host)
            ftp.login(self.ftp_user, self.ftp_pass)
            print(f"FTP接続成功: {self.ftp_host}")
            print(f"現在のディレクトリ: {ftp.pwd()}")
            ftp.quit()
            return True
        except Exception as e:
            print(f"FTP接続失敗: {e}")
            return False

# メイン処理
if __name__ == "__main__":
    import sys
    from dotenv import load_dotenv
    
    # 環境変数読み込み
    load_dotenv()
    
    # デプロイシステム初期化
    deployer = UnifiedDeploySystem()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            # FTP接続テスト
            deployer.check_ftp_connection()
        elif sys.argv[1] == "all":
            # 全記事デプロイ
            deployer.deploy_all_articles()
        else:
            # 特定の記事デプロイ
            deployer.deploy_article(sys.argv[1])
    else:
        print("使用方法:")
        print("  python unified_deploy.py test                    # FTP接続テスト")
        print("  python unified_deploy.py <article.json>          # 特定記事のデプロイ")
        print("  python unified_deploy.py all                     # 全記事の再デプロイ")