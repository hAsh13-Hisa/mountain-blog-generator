#!/usr/bin/env python3
"""
静的サイト全体をFTPデプロイ
"""
import ftplib
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class CompleteFTPDeployer:
    def __init__(self):
        self.ftp_host = os.getenv('LOLIPOP_FTP_HOST', 'ftp.lolipop.jp')
        self.ftp_user = os.getenv('LOLIPOP_FTP_USER')
        self.ftp_pass = os.getenv('LOLIPOP_FTP_PASS')
        self.remote_dir = os.getenv('LOLIPOP_REMOTE_DIR', '/as_teizan')
        self.local_dir = Path('static_site')
        
    def connect(self):
        """FTP接続"""
        self.ftp = ftplib.FTP(self.ftp_host)
        self.ftp.login(self.ftp_user, self.ftp_pass)
        print(f"Connected to {self.ftp_host}")
        
    def disconnect(self):
        """FTP切断"""
        self.ftp.quit()
        print("Disconnected from FTP server")
    
    def create_remote_dir(self, path):
        """リモートディレクトリ作成"""
        try:
            self.ftp.mkd(path)
            print(f"Created directory: {path}")
        except ftplib.error_perm:
            # ディレクトリが既に存在する場合
            pass
    
    def upload_file(self, local_file, remote_path):
        """ファイルアップロード"""
        try:
            with open(local_file, 'rb') as f:
                self.ftp.storbinary(f'STOR {remote_path}', f)
            print(f"✓ {local_file} -> {remote_path}")
        except Exception as e:
            print(f"❌ Error uploading {local_file}: {e}")
    
    def upload_directory(self, local_dir, remote_dir):
        """ディレクトリ全体を再帰的にアップロード"""
        local_path = Path(local_dir)
        
        # ディレクトリ作成
        self.create_remote_dir(remote_dir)
        
        for item in local_path.rglob('*'):
            if item.is_file():
                # リモートパス計算
                relative_path = item.relative_to(local_path)
                remote_path = f"{remote_dir}/{relative_path}".replace('\\', '/')
                
                # ディレクトリ作成
                remote_file_dir = '/'.join(remote_path.split('/')[:-1])
                if remote_file_dir != remote_dir:
                    self.create_remote_dir(remote_file_dir)
                
                # ファイルアップロード
                self.upload_file(item, remote_path)
    
    def deploy_site(self):
        """サイト全体をデプロイ"""
        print("🚀 静的サイト全体のFTPデプロイを開始...")
        
        try:
            self.connect()
            
            # 基本ディレクトリ移動
            try:
                self.ftp.cwd(self.remote_dir)
            except ftplib.error_perm:
                print(f"Creating remote directory: {self.remote_dir}")
                self.ftp.mkd(self.remote_dir)
                self.ftp.cwd(self.remote_dir)
            
            # static_site ディレクトリ全体をアップロード
            print(f"📁 アップロード: {self.local_dir} -> {self.remote_dir}")
            self.upload_directory(self.local_dir, '.')
            
            print("✅ デプロイ完了！")
            print(f"🌐 サイト URL: https://teizan.omasse.com/")
            
        except Exception as e:
            print(f"❌ デプロイエラー: {e}")
        finally:
            self.disconnect()

if __name__ == "__main__":
    deployer = CompleteFTPDeployer()
    deployer.deploy_site()