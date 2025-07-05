#!/usr/bin/env python3
"""
全ファイルFTPデプロイ
"""
import ftplib
import os
from pathlib import Path

class FullFTPDeployer:
    def __init__(self):
        self.ftp_host = 'ftp.lolipop.jp'
        self.ftp_user = 'pupu.jp-omasse'
        self.ftp_pass = 'paradise55omasse'
        self.remote_dir = '/as_teizan'
        self.local_dir = Path('static_site')
        
    def connect(self):
        """FTP接続"""
        self.ftp = ftplib.FTP(self.ftp_host)
        self.ftp.login(self.ftp_user, self.ftp_pass)
        print(f"🔗 Connected to {self.ftp_host}")
        
    def disconnect(self):
        """FTP切断"""
        self.ftp.quit()
        print("🔚 Disconnected from FTP server")
    
    def create_remote_dir(self, path):
        """リモートディレクトリ作成"""
        try:
            self.ftp.mkd(path)
            print(f"📁 Created: {path}")
        except ftplib.error_perm:
            # ディレクトリが既に存在する場合
            pass
    
    def upload_file(self, local_file, remote_path):
        """ファイルアップロード"""
        try:
            with open(local_file, 'rb') as f:
                self.ftp.storbinary(f'STOR {remote_path}', f)
            print(f"✅ {remote_path}")
            return True
        except Exception as e:
            print(f"❌ Error uploading {local_file}: {e}")
            return False
    
    def upload_directory(self, local_dir, remote_dir):
        """ディレクトリ再帰アップロード"""
        # リモートディレクトリ作成
        self.create_remote_dir(remote_dir)
        
        for item in local_dir.iterdir():
            if item.is_file():
                remote_file = f"{remote_dir}/{item.name}"
                self.upload_file(item, remote_file)
            elif item.is_dir():
                remote_subdir = f"{remote_dir}/{item.name}"
                self.upload_directory(item, remote_subdir)
    
    def deploy_all(self):
        """全ファイルデプロイ"""
        self.connect()
        
        try:
            print("🚀 全ファイルアップロード開始...")
            self.upload_directory(self.local_dir, self.remote_dir)
            print("✅ 全ファイルアップロード完了!")
            
        finally:
            self.disconnect()

if __name__ == "__main__":
    deployer = FullFTPDeployer()
    deployer.deploy_all()