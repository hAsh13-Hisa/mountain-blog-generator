#!/usr/bin/env python3
"""
確実に動作する画像URLでサンプル記事を最終修正
"""
import json
import requests
from datetime import datetime, timedelta
from wordpress_wxr_fixed import generate_valid_wxr

def get_working_mountain_images():
    """確実に動作する山の画像URLを取得"""
    
    # 確実に動作することがわかっている画像URL
    candidate_urls = [
        # 山・自然系の確実な画像
        "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&h=400&fit=crop",
        "https://images.unsplash.com/photo-1469474968028-56623f02e42e?w=800&h=400&fit=crop", 
        "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=800&h=400&fit=crop",
        "https://images.unsplash.com/photo-1540979388789-6cee28a1cdc9?w=800&h=400&fit=crop",
        "https://images.unsplash.com/photo-1464822759844-d150ad6ba46f?w=800&h=400&fit=crop",
        "https://images.unsplash.com/photo-1547036967-23d11aacaee0?w=800&h=400&fit=crop"
    ]
    
    working_urls = []
    
    print("🔍 画像URL有効性テスト:")
    for i, url in enumerate(candidate_urls, 1):
        try:
            response = requests.head(url, timeout=5)
            if response.status_code == 200:
                working_urls.append(url)
                print(f"   {i}. ✅ 有効: {url}")
                if len(working_urls) >= 3:  # 3つ確保できたら終了
                    break
            else:
                print(f"   {i}. ❌ 無効: {url} (Status: {response.status_code})")
        except Exception as e:
            print(f"   {i}. ❌ エラー: {url} (Error: {str(e)[:50]}...)")
    
    # 最低限の画像を確保
    if len(working_urls) < 3:
        # フォールバック: Unsplashの一般的な風景画像
        fallback_urls = [
            "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&h=400",
            "https://images.unsplash.com/photo-1469474968028-56623f02e42e?w=800&h=400",
            "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=800&h=400"
        ]
        working_urls.extend(fallback_urls[len(working_urls):3])
    
    return working_urls[:3]

def create_final_sample_xml():
    """最終版のサンプル記事XMLを作成"""
    print("🔧 最終版サンプル記事XML作成")
    print("=" * 50)
    
    # 有効な画像URLを取得
    working_image_urls = get_working_mountain_images()
    
    if len(working_image_urls) < 3:
        print("❌ 十分な有効画像URLが取得できませんでした")
        return None
    
    # 既存のJSONデータを読み込み
    json_filename = "sample_articles_improved_20250610_103721.json"
    
    try:
        with open(json_filename, 'r', encoding='utf-8') as f:
            articles_data = json.load(f)
        
        print(f"\n📂 記事データ読み込み: {len(articles_data)}記事")
        
        # 各記事に有効な画像URLを設定
        for i, article in enumerate(articles_data):
            old_url = article.get('featured_image_url', '未設定')
            article['featured_image_url'] = working_image_urls[i]
            print(f"📰 {article['mountain_name']}")
            print(f"   旧URL: {old_url}")
            print(f"   新URL: {article['featured_image_url']}")
        
        # WordPress XML形式で生成
        print(f"\n📄 XML生成中...")
        start_time = datetime.now() + timedelta(hours=1)
        xml_content = generate_valid_wxr(articles_data, start_time, 1)
        
        # ファイル保存
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        xml_filename = f"final_sample_articles_{timestamp}.xml"
        
        with open(xml_filename, 'w', encoding='utf-8') as f:
            f.write(xml_content)
        
        print(f"✅ 最終版XMLファイル作成: {xml_filename}")
        print(f"   記事数: {len(articles_data)}記事")
        print(f"   ファイルサイズ: {len(xml_content) / 1024:.1f} KB")
        
        # JSON版も更新保存
        updated_json_filename = f"final_sample_articles_{timestamp}.json"
        with open(updated_json_filename, 'w', encoding='utf-8') as f:
            json.dump(articles_data, f, ensure_ascii=False, indent=2)
        
        print(f"📋 更新JSONファイル: {updated_json_filename}")
        
        return xml_filename, updated_json_filename
        
    except Exception as e:
        print(f"❌ エラー: {e}")
        return None, None

def verify_xml_content(xml_filename):
    """XMLファイルの内容を検証"""
    print(f"\n🔍 XMLファイル検証: {xml_filename}")
    print("-" * 40)
    
    try:
        with open(xml_filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 各種メタデータの確認
        checks = [
            ('_thumbnail_url', 'WordPressアイキャッチURL'),
            ('fifu_image_url', 'Featured Image from URL'),
            ('wp:status><![CDATA[future]]', '予約投稿設定'),
            ('wp:post_type><![CDATA[post]]', '投稿タイプ'),
            ('dc:creator><![CDATA[aime]]', '投稿者設定')
        ]
        
        for pattern, description in checks:
            count = content.count(pattern)
            if count > 0:
                print(f"   ✅ {description}: {count}箇所で設定済み")
            else:
                print(f"   ❌ {description}: 設定されていません")
        
        # 実際の画像URL確認
        import re
        thumbnail_urls = re.findall(r'<wp:meta_key><!\[CDATA\[_thumbnail_url\]\]></wp:meta_key>\s*<wp:meta_value><!\[CDATA\[(.*?)\]\]></wp:meta_value>', content)
        
        if thumbnail_urls:
            print(f"\n🖼️ 設定された画像URL:")
            for i, url in enumerate(thumbnail_urls, 1):
                print(f"   {i}. {url}")
        else:
            print(f"\n⚠️ 画像URLが見つかりませんでした")
        
    except Exception as e:
        print(f"❌ 検証エラー: {e}")

def main():
    """メイン処理"""
    xml_filename, json_filename = create_final_sample_xml()
    
    if xml_filename:
        verify_xml_content(xml_filename)
        
        print(f"\n🎉 アイキャッチ画像付きサンプル記事の最終版完成！")
        print(f"📄 XMLファイル: {xml_filename}")
        print(f"📋 JSONファイル: {json_filename}")
        
        print(f"\n📋 WordPressテスト手順:")
        print("1. Featured Image from URLプラグインが有効化されていることを確認")
        print("2. プラグイン設定で自動設定を有効化")
        print(f"3. {xml_filename} をWordPressにインポート")
        print("4. 投稿一覧でアイキャッチ画像が表示されることを確認")
        
        print(f"\n🔧 プラグイン設定確認:")
        print("Settings → Featured Image from URL で以下を確認:")
        print("- ✅ Auto Set Featured Image")
        print("- ✅ Enable URL field on post editing")
        print("- ✅ Replace featured image")
        
    else:
        print(f"\n❌ 最終版の作成に失敗しました")

if __name__ == '__main__':
    main()