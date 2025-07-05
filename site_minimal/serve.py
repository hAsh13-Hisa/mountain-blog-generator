#!/usr/bin/env python3
"""
ローカル開発サーバー - ミニマルデザインプレビュー用
"""

import http.server
import socketserver
import os
import sys
import webbrowser
from pathlib import Path

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(Path(__file__).parent), **kwargs)
    
    def end_headers(self):
        # セキュリティヘッダー追加
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('X-Frame-Options', 'DENY')
        self.send_header('X-XSS-Protection', '1; mode=block')
        super().end_headers()
    
    def log_message(self, format, *args):
        # ログのカスタマイズ
        message = format % args
        print(f"[Server] {self.address_string()} - {message}")

def main():
    # ポート設定
    PORT = 8080
    
    # 現在のディレクトリを site_minimal に変更
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("🏔️ 低山旅行 - ミニマルデザイン開発サーバー")
    print("=" * 50)
    print(f"📁 サーバールート: {script_dir}")
    print(f"🌐 ローカルURL: http://localhost:{PORT}")
    print(f"📱 モバイルテスト: http://0.0.0.0:{PORT}")
    print("=" * 50)
    print("📋 利用可能なページ:")
    print("  / - トップページ（ミニマルデザイン）")
    print("  /css/minimal_design.css - CSSファイル")
    print("  /js/minimal.js - JavaScriptファイル")
    print("=" * 50)
    print("⚡ サーバー起動中... (Ctrl+C で停止)")
    print()
    
    try:
        with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
            # ブラウザで自動的に開く
            try:
                webbrowser.open(f'http://localhost:{PORT}')
                print("🚀 ブラウザでページを開きました")
            except Exception as e:
                print(f"⚠️  ブラウザの自動起動に失敗: {e}")
                print(f"手動でブラウザから http://localhost:{PORT} にアクセスしてください")
            
            print(f"✅ サーバーがポート {PORT} で起動しました")
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 サーバーを停止しています...")
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"❌ エラー: ポート {PORT} は既に使用されています")
            print("他のサーバーを停止するか、別のポートを使用してください")
        else:
            print(f"❌ サーバーエラー: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 予期しないエラー: {e}")
        sys.exit(1)
    
    print("👋 サーバーを停止しました")

if __name__ == "__main__":
    main()