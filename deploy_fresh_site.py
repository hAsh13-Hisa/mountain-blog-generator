#!/usr/bin/env python3
"""
フレッシュサイトをFTPデプロイ（static_site_newを上書き）
"""
import ftplib
import os
from pathlib import Path
import mimetypes

# FTP設定
FTP_HOST = 'ftp.lolipop.jp'
FTP_USER = 'pupu.jp-omasse'
FTP_PASS = 'paradise55omasse'
REMOTE_DIR = '/as_teizan'
LOCAL_DIR = Path('site_fresh')

class FreshSiteFTPDeployer:
    def __init__(self):
        self.ftp_host = FTP_HOST
        self.ftp_user = FTP_USER
        self.ftp_pass = FTP_PASS
        self.remote_dir = REMOTE_DIR
        self.local_dir = LOCAL_DIR
        self.ftp = None
        
    def connect(self):
        """FTP接続"""
        try:
            self.ftp = ftplib.FTP(self.ftp_host)
            self.ftp.login(self.ftp_user, self.ftp_pass)
            print(f"✅ FTP接続成功: {self.ftp_host}")
            return True
        except Exception as e:
            print(f"❌ FTP接続失敗: {e}")
            return False
        
    def disconnect(self):
        """FTP切断"""
        if self.ftp:
            self.ftp.quit()
            print("🔌 FTP接続を切断しました")
    
    def create_remote_directory(self, remote_path):
        """リモートディレクトリを作成"""
        try:
            self.ftp.mkd(remote_path)
            print(f"📁 ディレクトリ作成: {remote_path}")
        except ftplib.error_perm:
            # ディレクトリが既に存在する場合は無視
            pass
    
    def upload_file(self, local_file, remote_file):
        """ファイルをアップロード"""
        try:
            # 全てバイナリモードでアップロード（UTF-8のテキストファイルも含む）
            with open(local_file, 'rb') as f:
                self.ftp.storbinary(f'STOR {remote_file}', f)
            
            print(f"⬆️  {local_file} → {remote_file}")
            return True
        except Exception as e:
            print(f"❌ アップロード失敗 {local_file}: {e}")
            return False
    
    def upload_directory(self, local_path, remote_path=""):
        """ディレクトリを再帰的にアップロード"""
        if not local_path.exists():
            print(f"❌ ローカルディレクトリが存在しません: {local_path}")
            return False
        
        # リモートディレクトリに移動
        if remote_path:
            try:
                self.ftp.cwd(f"{self.remote_dir}/{remote_path}")
            except ftplib.error_perm:
                # ディレクトリが存在しない場合は作成
                self.create_remote_directory(f"{self.remote_dir}/{remote_path}")
                self.ftp.cwd(f"{self.remote_dir}/{remote_path}")
        else:
            self.ftp.cwd(self.remote_dir)
        
        uploaded_count = 0
        failed_count = 0
        
        for item in local_path.iterdir():
            if item.is_file():
                # ファイルをアップロード
                remote_file_path = item.name
                if self.upload_file(item, remote_file_path):
                    uploaded_count += 1
                else:
                    failed_count += 1
                    
            elif item.is_dir():
                # ディレクトリを再帰的にアップロード
                remote_subdir = f"{remote_path}/{item.name}" if remote_path else item.name
                self.create_remote_directory(f"{self.remote_dir}/{remote_subdir}")
                
                # サブディレクトリを処理
                sub_uploaded, sub_failed = self.upload_directory(item, remote_subdir)
                uploaded_count += sub_uploaded
                failed_count += sub_failed
        
        return uploaded_count, failed_count
    
    def deploy(self):
        """デプロイメイン処理"""
        print("🚀 フレッシュサイトのデプロイを開始...")
        print(f"📂 ローカル: {self.local_dir}")
        print(f"🌐 リモート: {self.ftp_host}{self.remote_dir}")
        
        if not self.local_dir.exists():
            print(f"❌ ローカルサイトディレクトリが存在しません: {self.local_dir}")
            return False
        
        if not self.connect():
            return False
        
        try:
            # リモートディレクトリに移動
            self.ftp.cwd(self.remote_dir)
            
            # 重要：メインのindex.htmlを直接上書き
            main_index = self.local_dir / 'index.html'
            if main_index.exists():
                if self.upload_file(main_index, 'index.html'):
                    print("🎯 メインページ (index.html) を上書きしました")
                else:
                    print("❌ メインページの上書きに失敗")
                    return False
            
            uploaded_count, failed_count = self.upload_directory(self.local_dir)
            
            print(f"\n📊 デプロイ結果:")
            print(f"✅ 成功: {uploaded_count}ファイル")
            print(f"❌ 失敗: {failed_count}ファイル")
            
            if failed_count == 0:
                print(f"\n🎉 フレッシュサイトデプロイ完了！")
                print(f"🌐 サイトURL: https://teizan.omasse.com/")
                return True
            else:
                print(f"\n⚠️  一部ファイルのアップロードに失敗しました")
                return False
                
        except Exception as e:
            print(f"❌ デプロイ中にエラーが発生: {e}")
            return False
        finally:
            self.disconnect()

def main():
    deployer = FreshSiteFTPDeployer()
    success = deployer.deploy()
    
    if success:
        print("\n✅ フレッシュサイトデプロイが正常に完了しました！")
        print("🔗 https://teizan.omasse.com/ でサイトを確認してください")
        print("🎨 完全新デザインが反映されています")
    else:
        print("\n❌ デプロイに失敗しました")
    
    return success

if __name__ == "__main__":
    main()