#!/usr/bin/env python3
"""
基本動作テスト
"""
import sys
import os

# プロジェクトルートをパスに追加
sys.path.insert(0, os.path.abspath('.'))

try:
    print("🔍 基本動作をテストしています...")
    
    # 設定読み込みテスト
    print("1. 設定読み込み...")
    from config.settings import get_settings
    settings = get_settings()
    print(f"   ✅ WordPress URL: {settings.WP_URL}")
    
    # 山データ読み込みテスト
    print("2. 山データ読み込み...")
    from src.infrastructure.repositories import RepositoryFactory
    mountain_repo = RepositoryFactory.get_mountain_repository()
    mountains = mountain_repo.get_all()
    print(f"   ✅ 山データ: {len(mountains)}山読み込み完了")
    
    # 最初の山を表示
    if mountains:
        first_mountain = mountains[0]
        print(f"   📍 例: {first_mountain.name} ({first_mountain.elevation}m)")
    
    print("\n🎉 基本動作テスト完了！アプリケーションは正常に動作可能です。")
    
except Exception as e:
    print(f"❌ エラー: {e}")
    import traceback
    traceback.print_exc()