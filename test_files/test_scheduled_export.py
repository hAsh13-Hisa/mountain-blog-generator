#!/usr/bin/env python3
"""
スケジュール投稿機能のテスト
"""
import json
from datetime import datetime, timedelta
from wordpress_scheduled_exporter import WordPressScheduledExporter

def test_scheduled_export():
    """既存のJSONからスケジュール投稿XMLを生成"""
    print("⏰ スケジュール投稿機能テスト")
    print("="*50)
    
    # 既存のJSONファイルを使用
    with open('bulk_articles_20250609_213833.json', 'r', encoding='utf-8') as f:
        articles_data = json.load(f)
    
    print(f"📊 記事数: {len(articles_data)}記事")
    
    # カバー画像URLを追加（テスト用）
    for i, article in enumerate(articles_data):
        article['featured_image_url'] = f"https://images.unsplash.com/photo-{1500000000 + i}?w=800&h=400&fit=crop"
    
    exporter = WordPressScheduledExporter()
    
    # スケジュール設定
    start_time = datetime.now() + timedelta(hours=1)  # 1時間後から開始
    interval_hours = 1  # 1時間ごと
    
    print(f"\n📅 スケジュール設定:")
    print(f"   開始時刻: {start_time.strftime('%Y-%m-%d %H:%M')}")
    print(f"   公開間隔: {interval_hours}時間ごと")
    
    # 公開スケジュール表示
    print(f"\n📅 公開スケジュール:")
    for i, article in enumerate(articles_data):
        scheduled_time = start_time + timedelta(hours=interval_hours * i)
        print(f"   {i+1}. {scheduled_time.strftime('%Y-%m-%d %H:%M')} - {article['title'][:40]}...")
    
    # XML生成
    print(f"\n📄 XML生成中...")
    xml_content = exporter.generate_scheduled_xml(articles_data, start_time, interval_hours)
    
    # ファイル保存
    filename = f"wordpress_scheduled_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xml"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(xml_content)
    
    print(f"\n✅ XMLファイル作成完了: {filename}")
    print(f"   記事数: {len(articles_data)}記事")
    print(f"   ファイルサイズ: {len(xml_content) / 1024:.1f} KB")
    
    # XMLの内容を確認
    print(f"\n🔍 XML内容確認:")
    if 'status>future' in xml_content:
        print("   ✅ 予約投稿（future）ステータス設定済み")
    if 'meta_key>_thumbnail_url' in xml_content:
        print("   ✅ アイキャッチ画像URL設定済み")
    if 'post_date' in xml_content:
        print("   ✅ 投稿日時設定済み")
    
    print(f"\n📋 WordPress設定手順:")
    print("1. WordPress管理画面 → ツール → インポート → WordPress")
    print("2. XMLファイルをアップロード")
    print("3. 投稿者の割り当てを設定")
    print("4. 実行")
    print("\n💡 アイキャッチ画像の自動設定:")
    print("プラグイン「Featured Image from URL」をインストールすると")
    print("XMLのmeta_valueから自動でアイキャッチ画像が設定されます")
    
    return filename

def main():
    test_scheduled_export()

if __name__ == '__main__':
    main()