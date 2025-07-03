#!/usr/bin/env python3
"""
dotenv不要のシンプルFTPデプロイ
"""
import ftplib
import os
from pathlib import Path

class SimpleFTPDeployer:
    def __init__(self):
        # 直接.envファイルから読み込み
        self.load_env()
        
    def load_env(self):
        """環境変数を.envファイルから読み込み"""
        env_file = Path('.env')
        if env_file.exists():
            with open(env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()
        
        self.ftp_host = os.getenv('LOLIPOP_FTP_HOST', 'ftp.lolipop.jp')
        self.ftp_user = os.getenv('LOLIPOP_FTP_USER')
        self.ftp_pass = os.getenv('LOLIPOP_FTP_PASS')
        self.remote_dir = os.getenv('LOLIPOP_REMOTE_DIR', '/as_teizan')
        self.local_dir = Path('static_site')
        
    def connect(self):
        """FTP接続"""
        self.ftp = ftplib.FTP(self.ftp_host)
        self.ftp.login(self.ftp_user, self.ftp_pass)
        print(f"✅ Connected to {self.ftp_host}")
        
    def disconnect(self):
        """FTP切断"""
        self.ftp.quit()
        print("✅ Disconnected from FTP server")
    
    def create_remote_dir(self, path):
        """リモートディレクトリ作成"""
        try:
            self.ftp.mkd(path)
            print(f"📁 Created directory: {path}")
        except ftplib.error_perm:
            # ディレクトリが既に存在する場合
            pass
    
    def upload_file(self, local_file, remote_path):
        """ファイルアップロード"""
        try:
            with open(local_file, 'rb') as f:
                self.ftp.storbinary(f'STOR {remote_path}', f)
            print(f"✓ {local_file} -> {remote_path}")
            return True
        except Exception as e:
            print(f"❌ Error uploading {local_file}: {e}")
            return False
    
    def upload_directory(self, local_dir, remote_dir=""):
        """ディレクトリ全体を再帰的にアップロード"""
        uploaded_count = 0
        error_count = 0
        
        for item in local_dir.iterdir():
            if item.is_file():
                # ファイルの場合
                remote_path = f"{remote_dir}/{item.name}" if remote_dir else item.name
                if self.upload_file(item, remote_path):
                    uploaded_count += 1
                else:
                    error_count += 1
                    
            elif item.is_dir():
                # ディレクトリの場合
                new_remote_dir = f"{remote_dir}/{item.name}" if remote_dir else item.name
                self.create_remote_dir(new_remote_dir)
                
                # 再帰的にアップロード
                sub_uploaded, sub_errors = self.upload_directory(item, new_remote_dir)
                uploaded_count += sub_uploaded
                error_count += sub_errors
                
        return uploaded_count, error_count
    
    def deploy_all(self):
        """全体デプロイ実行"""
        print("🚀 Starting FTP deployment...")
        print(f"📁 Local: {self.local_dir.absolute()}")
        print(f"🌐 Remote: {self.ftp_host}{self.remote_dir}")
        
        try:
            self.connect()
            
            # リモートディレクトリに移動
            try:
                self.ftp.cwd(self.remote_dir)
                print(f"📂 Changed to directory: {self.remote_dir}")
            except:
                print(f"❌ Could not change to {self.remote_dir}")
                return False
            
            # アップロード実行
            uploaded, errors = self.upload_directory(self.local_dir)
            
            print(f"\n📊 Deploy Results:")
            print(f"   ✅ Uploaded: {uploaded} files")
            print(f"   ❌ Errors: {errors} files")
            
            self.disconnect()
            
            if errors == 0:
                print("🎉 Deployment completed successfully!")
                print(f"🌐 Site URL: https://teizan.omasse.com/")
                return True
            else:
                print(f"⚠️  Deployment completed with {errors} errors")
                return False
                
        except Exception as e:
            print(f"❌ Deployment failed: {e}")
            return False

if __name__ == "__main__":
    deployer = SimpleFTPDeployer()
    deployer.deploy_all()