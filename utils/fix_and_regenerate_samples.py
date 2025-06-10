#!/usr/bin/env python3
"""
アイキャッチ画像付きサンプル記事を再生成
"""
import json
from datetime import datetime, timedelta
from wordpress_wxr_fixed import generate_valid_wxr

def fix_and_regenerate_samples():
    """既存のJSONデータを使ってアイキャッチ画像付きXMLを再生成"""
    print("🔧 アイキャッチ画像付きサンプル記事の修正・再生成")
    print("=" * 60)
    
    # 既存のJSONファイルを読み込み
    json_filename = "sample_articles_improved_20250610_103721.json"
    
    try:
        with open(json_filename, 'r', encoding='utf-8') as f:
            articles_data = json.load(f)
        
        print(f"📂 既存データ読み込み: {len(articles_data)}記事")
        
        # 各記事にアイキャッチ画像URLが設定されているか確認
        for i, article in enumerate(articles_data):
            print(f"\n📰 {article['mountain_name']}:")
            
            if 'featured_image_url' in article and article['featured_image_url']:
                print(f"   🖼️ 既存画像URL: {article['featured_image_url']}")
            else:
                # 画像URLが設定されていない場合は追加
                mountain_images = [
                    "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&h=400&fit=crop",  # 円山
                    "https://images.unsplash.com/photo-1464822759844-d150ad6ba46f?w=800&h=400&fit=crop",  # 岩木山
                    "https://images.unsplash.com/photo-1469474968028-56623f02e42e?w=800&h=400&fit=crop"   # 岩手山
                ]
                article['featured_image_url'] = mountain_images[i % len(mountain_images)]
                print(f"   🆕 新規画像URL: {article['featured_image_url']}")
        
        # WordPress XML形式で再生成
        print(f"\n📄 アイキャッチ画像付きXML生成中...")
        
        # スケジュール設定（1時間間隔）
        start_time = datetime.now() + timedelta(hours=1)
        
        xml_content = generate_valid_wxr(articles_data, start_time, 1)
        
        # ファイル名にタイムスタンプを追加
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        xml_filename = f"sample_articles_with_images_{timestamp}.xml"
        
        with open(xml_filename, 'w', encoding='utf-8') as f:
            f.write(xml_content)
        
        print(f"✅ 修正版XMLファイル作成: {xml_filename}")
        print(f"   記事数: {len(articles_data)}記事")
        print(f"   ファイルサイズ: {len(xml_content) / 1024:.1f} KB")
        
        # XMLファイル内にアイキャッチ画像メタデータが含まれているか確認
        print(f"\n🔍 アイキャッチ画像メタデータ確認:")
        
        if '_thumbnail_url' in xml_content:
            print("   ✅ _thumbnail_url メタデータ: 含まれています")
        else:
            print("   ❌ _thumbnail_url メタデータ: 見つかりません")
        
        if 'fifu_image_url' in xml_content:
            print("   ✅ fifu_image_url メタデータ: 含まれています")
        else:
            print("   ❌ fifu_image_url メタデータ: 見つかりません")
        
        # 各記事のアイキャッチ画像URLを表示
        print(f"\n🖼️ 各記事のアイキャッチ画像:")
        for article in articles_data:
            print(f"   📰 {article['mountain_name']}: {article['featured_image_url']}")
        
        print(f"\n📋 WordPressインポート手順:")
        print("1. WordPress管理画面 → ツール → インポート → WordPress")
        print(f"2. {xml_filename} をアップロード")
        print("3. 投稿者の割り当て → aime")
        print("4. 実行")
        print("\n💡 Featured Image from URLプラグインが有効化されていることを確認してください")
        
        return xml_filename
        
    except FileNotFoundError:
        print(f"❌ JSONファイルが見つかりません: {json_filename}")
        return None
    except Exception as e:
        print(f"❌ エラー: {e}")
        return None

def test_xml_content(xml_filename):
    """XMLファイルの内容をテスト"""
    print(f"\n🧪 XMLファイル内容テスト: {xml_filename}")
    print("-" * 40)
    
    try:
        with open(xml_filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # アイキャッチ画像関連のメタデータをチェック
        metadata_checks = [
            ('_thumbnail_url', '標準WordPressアイキャッチURL'),
            ('fifu_image_url', 'Featured Image from URL プラグイン用URL'),
            ('_thumbnail_alt', 'アイキャッチ画像代替テキスト'),
            ('fifu_image_alt', 'プラグイン用代替テキスト')
        ]
        
        for meta_key, description in metadata_checks:
            count = content.count(meta_key)
            if count > 0:
                print(f"   ✅ {meta_key}: {count}個の記事で設定済み ({description})")
            else:
                print(f"   ❌ {meta_key}: 設定されていません ({description})")
        
        # 具体的な画像URLを確認
        print(f"\n🔍 設定された画像URL:")
        import re
        thumbnail_urls = re.findall(r'<wp:meta_key><!\[CDATA\[_thumbnail_url\]\]></wp:meta_key>\s*<wp:meta_value><!\[CDATA\[(.*?)\]\]></wp:meta_value>', content)
        
        for i, url in enumerate(thumbnail_urls, 1):
            print(f"   {i}. {url}")
        
        if not thumbnail_urls:
            print("   ⚠️ 画像URLが見つかりませんでした")
        
    except Exception as e:
        print(f"❌ XMLファイル読み込みエラー: {e}")

def main():
    """メイン処理"""
    xml_filename = fix_and_regenerate_samples()
    
    if xml_filename:
        test_xml_content(xml_filename)
        
        print(f"\n🎉 アイキャッチ画像付きサンプル記事の準備完了！")
        print(f"📄 使用するXMLファイル: {xml_filename}")
        print(f"\n🔧 今度はアイキャッチ画像が正しく表示されるはずです")
    else:
        print(f"\n❌ 修正に失敗しました")

if __name__ == '__main__':
    main()