#!/usr/bin/env python3
"""
Simple FTP deployer without external dependencies
"""
import ftplib
import os
from pathlib import Path

class SimpleFTPDeployer:
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
    
    def upload_file(self, local_file, remote_path):
        """ファイルアップロード"""
        try:
            with open(local_file, 'rb') as f:
                self.ftp.storbinary(f'STOR {remote_path}', f)
            print(f"✅ {local_file} -> {remote_path}")
            return True
        except Exception as e:
            print(f"❌ Error uploading {local_file}: {e}")
            return False
    
    def create_remote_dir(self, path):
        """リモートディレクトリ作成"""
        try:
            self.ftp.mkd(path)
            print(f"📁 Created directory: {path}")
        except ftplib.error_perm:
            # ディレクトリが既に存在する場合
            pass
    
    def upload_css_only(self):
        """CSSファイルのみアップロード（最低限の修正）"""
        self.connect()
        
        try:
            # CSSファイルをアップロード
            css_local = self.local_dir / 'css' / 'style.css'
            css_remote = f'{self.remote_dir}/css/style.css'
            
            # cssディレクトリ作成
            self.create_remote_dir(f'{self.remote_dir}/css')
            
            # CSSファイルアップロード
            if css_local.exists():
                if self.upload_file(css_local, css_remote):
                    print("🎨 CSS修正完了!")
                else:
                    print("❌ CSS更新失敗")
            else:
                print(f"❌ CSSファイルが見つかりません: {css_local}")
                
        finally:
            self.disconnect()

if __name__ == "__main__":
    deployer = SimpleFTPDeployer()
    print("🚀 CSS修正デプロイ開始...")
    deployer.upload_css_only()
    print("✅ 完了!")