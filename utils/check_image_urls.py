#!/usr/bin/env python3
"""
画像URLが有効かチェック
"""
import requests

def check_image_urls():
    """画像URLが実際に存在するかチェック"""
    print("🔍 アイキャッチ画像URL有効性チェック")
    print("=" * 50)
    
    # 使用している画像URL
    image_urls = [
        "https://images.unsplash.com/photo-1500000000?w=800&h=400&fit=crop",
        "https://images.unsplash.com/photo-1500000001?w=800&h=400&fit=crop", 
        "https://images.unsplash.com/photo-1500000002?w=800&h=400&fit=crop"
    ]
    
    # より確実な山の画像URL
    better_urls = [
        "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&h=400&fit=crop",  # 山の風景
        "https://images.unsplash.com/photo-1464822759844-d150ad6ba46f?w=800&h=400&fit=crop",  # 山の風景
        "https://images.unsplash.com/photo-1469474968028-56623f02e42e?w=800&h=400&fit=crop"   # 山の風景
    ]
    
    print("📊 現在使用中のURL:")
    for i, url in enumerate(image_urls, 1):
        try:
            response = requests.head(url, timeout=10)
            if response.status_code == 200:
                print(f"   {i}. ✅ {url}")
            else:
                print(f"   {i}. ❌ {url} (Status: {response.status_code})")
        except Exception as e:
            print(f"   {i}. ❌ {url} (Error: {e})")
    
    print(f"\n📊 推奨URL:")
    for i, url in enumerate(better_urls, 1):
        try:
            response = requests.head(url, timeout=10)
            if response.status_code == 200:
                print(f"   {i}. ✅ {url}")
            else:
                print(f"   {i}. ❌ {url} (Status: {response.status_code})")
        except Exception as e:
            print(f"   {i}. ❌ {url} (Error: {e})")
    
    return better_urls

def generate_xml_with_valid_images():
    """有効な画像URLでXMLを再生成"""
    print(f"\n🔧 有効な画像URLでXML再生成")
    print("=" * 50)
    
    import json
    from datetime import datetime, timedelta
    from wordpress_wxr_fixed import generate_valid_wxr
    
    # 既存のJSONデータを読み込み
    json_filename = "sample_articles_improved_20250610_103721.json"
    
    try:
        with open(json_filename, 'r', encoding='utf-8') as f:
            articles_data = json.load(f)
        
        # 有効な画像URLを設定
        valid_image_urls = [
            "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&h=400&fit=crop",  # 円山用
            "https://images.unsplash.com/photo-1464822759844-d150ad6ba46f?w=800&h=400&fit=crop",  # 岩木山用
            "https://images.unsplash.com/photo-1469474968028-56623f02e42e?w=800&h=400&fit=crop"   # 岩手山用
        ]
        
        # 各記事に有効な画像URLを設定
        for i, article in enumerate(articles_data):
            article['featured_image_url'] = valid_image_urls[i % len(valid_image_urls)]
            print(f"📰 {article['mountain_name']}: {article['featured_image_url']}")
        
        # WordPress XML形式で生成
        start_time = datetime.now() + timedelta(hours=1)
        xml_content = generate_valid_wxr(articles_data, start_time, 1)
        
        # ファイル保存
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        xml_filename = f"sample_articles_valid_images_{timestamp}.xml"
        
        with open(xml_filename, 'w', encoding='utf-8') as f:
            f.write(xml_content)
        
        print(f"\n✅ 有効画像URL版XMLファイル作成: {xml_filename}")
        print(f"   記事数: {len(articles_data)}記事")
        print(f"   ファイルサイズ: {len(xml_content) / 1024:.1f} KB")
        
        return xml_filename
        
    except Exception as e:
        print(f"❌ エラー: {e}")
        return None

def main():
    """メイン処理"""
    # 画像URLの有効性をチェック
    check_image_urls()
    
    # 有効な画像URLでXMLを再生成
    xml_filename = generate_xml_with_valid_images()
    
    if xml_filename:
        print(f"\n🎯 WordPressでのテスト手順:")
        print("1. Featured Image from URLプラグインの設定を確認")
        print("   - Settings → Featured Image from URL")
        print("   - 'Auto Set Featured Image' を有効化")
        print("   - 'Enable URL field on post editing' を有効化")
        print(f"2. {xml_filename} をWordPressにインポート")
        print("3. 投稿一覧でアイキャッチ画像を確認")
        print("4. 画像が表示されない場合は各記事を編集して手動設定")
        
        print(f"\n💡 手動設定方法:")
        print("- 記事編集画面の右サイドバー")
        print("- 'Featured Image from URL' セクション")
        print("- 画像URLを入力して 'Set Featured Image' をクリック")

if __name__ == '__main__':
    main()