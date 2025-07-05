#!/usr/bin/env python3
"""
最低限のファイルで問題解決
"""
import ftplib
from pathlib import Path

class QuickFixDeployer:
    def __init__(self):
        self.ftp_host = 'ftp.lolipop.jp'
        self.ftp_user = 'pupu.jp-omasse'
        self.ftp_pass = 'paradise55omasse'
        self.remote_dir = '/as_teizan'
        self.local_dir = Path('static_site')
        
    def connect(self):
        self.ftp = ftplib.FTP(self.ftp_host)
        self.ftp.login(self.ftp_user, self.ftp_pass)
        print(f"🔗 Connected to {self.ftp_host}")
        
    def disconnect(self):
        self.ftp.quit()
        print("🔚 Disconnected")
    
    def upload_file(self, local_file, remote_path):
        try:
            with open(local_file, 'rb') as f:
                self.ftp.storbinary(f'STOR {remote_path}', f)
            print(f"✅ {remote_path}")
            return True
        except Exception as e:
            print(f"❌ {e}")
            return False
    
    def quick_fix(self):
        """必要最小限のファイルアップロード"""
        self.connect()
        
        try:
            # 1. index.html（CSSバージョン更新済み）
            index_local = self.local_dir / 'index.html'
            if index_local.exists():
                self.upload_file(index_local, f'{self.remote_dir}/index.html')
            
            # 2. CSS（念のため再アップロード）
            css_local = self.local_dir / 'css' / 'style.css'
            if css_local.exists():
                self.upload_file(css_local, f'{self.remote_dir}/css/style.css')
                
            print("🎯 最低限修正完了!")
            
        finally:
            self.disconnect()

if __name__ == "__main__":
    deployer = QuickFixDeployer()
    print("🚀 クイック修正デプロイ...")
    deployer.quick_fix()