#!/usr/bin/env python3
"""
プラグイン版エンドポイントのテスト
"""
import requests
import json
import base64
from config.settings import get_settings

def test_plugin_endpoint():
    """プラグインエンドポイントをテスト"""
    settings = get_settings()
    
    print("🔍 プラグイン版エンドポイントテスト")
    print("="*50)
    
    # 認証ヘッダー
    app_password = settings.WP_APP_PASSWORD.replace(' ', '')
    credentials = f"{settings.WP_USERNAME}:{app_password}"
    encoded = base64.b64encode(credentials.encode()).decode()
    
    headers = {
        "Authorization": f"Basic {encoded}",
        "Content-Type": "application/json"
    }
    
    # テストエンドポイント
    test_url = f"{settings.WP_URL}/wp-json/mountain-blog/v1/test"
    print(f"📍 テストURL: {test_url}")
    
    print("\n1️⃣ テストエンドポイント確認...")
    try:
        response = requests.get(test_url, headers=headers, timeout=10)
        print(f"   ステータス: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ プラグイン正常動作！")
            print(f"   メッセージ: {result.get('message', 'Unknown')}")
            print(f"   ユーザー: {result.get('user', 'Unknown')}")
            return True
        elif response.status_code == 404:
            print("   ❌ エンドポイントが見つかりません")
            print("   → プラグインがインストール・有効化されているか確認してください")
        else:
            print(f"   ❌ エラー: {response.text}")
        
        return False
        
    except Exception as e:
        print(f"   ❌ 接続エラー: {e}")
        return False

def test_bulk_posting():
    """大量投稿をテスト"""
    settings = get_settings()
    
    print("\n2️⃣ 大量投稿テスト")
    print("="*50)
    
    # 認証ヘッダー
    app_password = settings.WP_APP_PASSWORD.replace(' ', '')
    credentials = f"{settings.WP_USERNAME}:{app_password}"
    encoded = base64.b64encode(credentials.encode()).decode()
    
    headers = {
        "Authorization": f"Basic {encoded}",
        "Content-Type": "application/json"
    }
    
    # 既存のJSONファイルを読み込み
    try:
        with open('bulk_articles_20250609_213833.json', 'r', encoding='utf-8') as f:
            articles_data = json.load(f)
        print(f"📊 投稿予定記事数: {len(articles_data)}記事")
    except FileNotFoundError:
        print("❌ JSONファイルが見つかりません")
        return False
    
    # プラグイン用にデータを整形
    bulk_data = []
    for article in articles_data:
        bulk_data.append({
            'title': article['title'],
            'content': article['content'],
            'excerpt': article['excerpt'],
            'tags': article['tags']
        })
    
    # 大量投稿エンドポイント
    bulk_url = f"{settings.WP_URL}/wp-json/mountain-blog/v1/bulk-create"
    print(f"📍 投稿URL: {bulk_url}")
    
    print("\n📝 WordPress一括投稿実行中...")
    try:
        response = requests.post(
            bulk_url,
            json=bulk_data,
            headers=headers,
            timeout=120  # 大量投稿なので長めのタイムアウト
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n🎉 大量投稿成功！")
            print(f"   作成数: {result.get('created_count', 0)}記事")
            print(f"   エラー数: {result.get('error_count', 0)}記事")
            
            # 作成された投稿の詳細
            created_posts = result.get('created_posts', [])
            print(f"\n📝 作成された記事:")
            for i, post in enumerate(created_posts[:5]):  # 最初の5件を表示
                print(f"   {i+1}. ID:{post['post_id']} - {post['title'][:40]}...")
                
            if len(created_posts) > 5:
                print(f"   ... 他{len(created_posts)-5}記事")
            
            # エラーがあれば表示
            if result.get('errors'):
                print(f"\n⚠️  エラー詳細:")
                for error in result['errors'][:3]:
                    print(f"   記事{error['index']}: {error['error']}")
            
            print(f"\n🔗 WordPress管理画面:")
            print(f"   下書き一覧: {settings.WP_URL}/wp-admin/edit.php?post_status=draft")
            print(f"   投稿一覧: {settings.WP_URL}/wp-admin/edit.php")
            
            return True
            
        else:
            print(f"❌ 投稿失敗: {response.status_code}")
            print(f"   レスポンス: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 投稿エラー: {e}")
        return False

def main():
    print("🚀 プラグイン版 WordPress大量投稿テスト\n")
    
    print("📋 必要な作業:")
    print("1. mountain-blog-bulk-poster.php をWordPressプラグインとしてアップロード")
    print("2. WordPress管理画面でプラグインを有効化")
    print("3. 以下のテストを実行\n")
    
    # 1. エンドポイント確認
    endpoint_works = test_plugin_endpoint()
    
    if endpoint_works:
        print("\n" + "="*60)
        
        # 2. 大量投稿テスト
        bulk_success = test_bulk_posting()
        
        if bulk_success:
            print("\n" + "="*60)
            print("\n🎊 完全成功！")
            print("✅ Mountain Blog Generatorの大量投稿システムが正常に動作しています。")
            print("\n🔄 今後のワークフロー:")
            print("1. 記事生成 → JSON出力")
            print("2. プラグインエンドポイント → WordPress一括投稿")
            print("3. 管理画面で確認・公開")
        else:
            print("\n⚠️  エンドポイントは動作していますが、投稿でエラーが発生しました。")
    else:
        print("\n❌ プラグインエンドポイントにアクセスできません。")
        print("\n📋 確認事項:")
        print("1. プラグインファイルが正しくアップロードされているか")
        print("2. プラグインが有効化されているか")
        print("3. ユーザーに適切な権限があるか")

if __name__ == '__main__':
    main()