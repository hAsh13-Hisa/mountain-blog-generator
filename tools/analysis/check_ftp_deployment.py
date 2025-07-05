#!/usr/bin/env python3
"""
FTPアップロードの正常性チェック
"""
import ftplib
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class FTPDeploymentChecker:
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
        print(f"✅ Connected to {self.ftp_host}")
        
    def disconnect(self):
        """FTP切断"""
        self.ftp.quit()
        print("Disconnected from FTP server")
    
    def get_remote_files(self, path='.'):
        """リモートファイルリストを取得"""
        files = []
        try:
            self.ftp.cwd(path)
            items = []
            self.ftp.retrlines('LIST', items.append)
            
            for item in items:
                parts = item.split()
                if len(parts) >= 9:
                    name = ' '.join(parts[8:])
                    if parts[0].startswith('d'):
                        # ディレクトリ
                        subdir_path = f"{path}/{name}" if path != '.' else name
                        files.append(f"{subdir_path}/")
                        # サブディレクトリを再帰的に探索
                        files.extend(self.get_remote_files(subdir_path))
                    else:
                        # ファイル
                        file_path = f"{path}/{name}" if path != '.' else name
                        files.append(file_path)
        except Exception as e:
            print(f"Error listing {path}: {e}")
        
        return files
    
    def get_local_files(self):
        """ローカルファイルリストを取得"""
        files = []
        for item in self.local_dir.rglob('*'):
            relative_path = item.relative_to(self.local_dir)
            if item.is_dir():
                files.append(f"{relative_path}/")
            else:
                files.append(str(relative_path))
        return sorted(files)
    
    def check_deployment(self):
        """デプロイ状況をチェック"""
        print("🔍 FTPデプロイ状況チェック開始...\n")
        
        try:
            self.connect()
            
            # リモートディレクトリに移動
            self.ftp.cwd(self.remote_dir)
            
            # ローカルファイルリスト
            local_files = self.get_local_files()
            print(f"📁 ローカルファイル数: {len(local_files)}")
            
            # リモートファイルリスト
            remote_files = self.get_remote_files()
            print(f"📁 リモートファイル数: {len(remote_files)}\n")
            
            # 重要なファイルの存在チェック
            important_files = [
                'index.html',
                'css/style.css',
                'mountains/index.html',
                'about/index.html',
                'beginner/index.html',
                'contact/index.html',
                'equipment/index.html',
                'privacy/index.html',
                'terms/index.html',
                'regions/index.html',
                'regions/kanto/index.html',
                'regions/kansai/index.html',
                'regions/kyushu/index.html',
                'regions/北海道/index.html',
                'regions/東京都/index.html',
                'regions/茨城県/index.html',
                'regions/香川県/index.html',
                'mountains/mt_takao/index.html',
                'mountains/mt_maruyama_hokkaido/index.html',
                'mountains/mt_hakodate_hokkaido/index.html',
                'mountains/mt_sanuki_kagawa/index.html',
                'mountains/mt_tsukuba_ibaraki/index.html'
            ]
            
            print("📋 重要ファイルの存在チェック:")
            all_ok = True
            for file in important_files:
                if file in remote_files:
                    print(f"  ✅ {file}")
                else:
                    print(f"  ❌ {file} - 見つかりません！")
                    all_ok = False
            
            # 詳細なファイルリスト
            print("\n📄 リモートファイル一覧:")
            for f in sorted(remote_files):
                if not f.endswith('/'):
                    print(f"  - {f}")
            
            # チェック結果
            print("\n🎯 チェック結果:")
            if all_ok:
                print("✅ 全ての重要ファイルが正常にアップロードされています！")
                print(f"🌐 https://teizan.omasse.com/ で確認してください。")
            else:
                print("❌ 一部のファイルがアップロードされていません。")
                
        except Exception as e:
            print(f"❌ エラー: {e}")
        finally:
            self.disconnect()

if __name__ == "__main__":
    checker = FTPDeploymentChecker()
    checker.check_deployment()