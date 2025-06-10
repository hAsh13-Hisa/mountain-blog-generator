#!/usr/bin/env python3
"""
WordPress投稿テスト
"""
import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from config.settings import get_settings
from src.infrastructure.api_clients import WordPressAPIClient

def test_wordpress_connection():
    """WordPress接続テスト"""
    try:
        print("🧪 WordPress投稿テストを開始...")
        
        client = WordPressAPIClient()
        
        # 簡単なテスト投稿データ
        test_post = {
            "title": "テスト投稿 - Mountain Blog Generator",
            "content": "<p>これはMountain Blog Generatorからのテスト投稿です。</p><p>正常に動作していることを確認するためのテストです。</p>",
            "status": "draft",  # 下書きとして投稿
            "excerpt": "Mountain Blog Generatorのテスト投稿",
            "categories": [1],  # デフォルトカテゴリ
        }
        
        print("📝 テスト投稿を作成中...")
        post_id = client.create_post(test_post)
        
        print(f"✅ 投稿成功! WordPress投稿ID: {post_id}")
        print(f"🌐 URL: {get_settings().WP_URL}/wp-admin/post.php?post={post_id}&action=edit")
        
    except Exception as e:
        print(f"❌ テスト失敗: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_wordpress_connection()