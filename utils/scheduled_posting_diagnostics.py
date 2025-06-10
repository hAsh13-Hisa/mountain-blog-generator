#!/usr/bin/env python3
"""
予約投稿の問題診断スクリプト
WordPress WXR形式とスケジュール設定の詳細検証
"""
import json
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import requests

def diagnose_xml_file(xml_filename):
    """XMLファイルの詳細診断"""
    print(f"🔍 XMLファイル診断: {xml_filename}")
    print("=" * 60)
    
    try:
        # XMLファイルを読み込み
        with open(xml_filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 基本統計
        print(f"📊 ファイル基本情報:")
        print(f"   ファイルサイズ: {len(content)} bytes ({len(content)/1024:.1f} KB)")
        print(f"   行数: {content.count(chr(10)) + 1}")
        
        # WXR形式確認
        print(f"\n📋 WXR形式チェック:")
        required_elements = [
            ('wp:wxr_version', 'WXRバージョン'),
            ('wp:base_site_url', 'ベースサイトURL'),
            ('wp:author', '投稿者情報'),
            ('<item>', '記事アイテム'),
            ('wp:status><![CDATA[future]]', '予約投稿設定'),
            ('wp:post_date', '投稿日時設定')
        ]
        
        for element, description in required_elements:
            count = content.count(element)
            status = "✅" if count > 0 else "❌"
            print(f"   {status} {description}: {count}箇所")
        
        # 予約投稿詳細チェック
        print(f"\n⏰ 予約投稿設定詳細:")
        
        # 投稿日時を抽出
        import re
        post_dates = re.findall(r'<wp:post_date><!\[CDATA\[(.*?)\]\]></wp:post_date>', content)
        pub_dates = re.findall(r'<pubDate>(.*?)</pubDate>', content)
        
        print(f"   検出された投稿日時:")
        for i, (post_date, pub_date) in enumerate(zip(post_dates, pub_dates), 1):
            print(f"     記事{i}: {post_date} (GMT: {pub_date})")
            
            # 日時の妥当性チェック
            try:
                parsed_date = datetime.strptime(post_date, '%Y-%m-%d %H:%M:%S')
                now = datetime.now()
                if parsed_date > now:
                    time_diff = parsed_date - now
                    print(f"              → 未来日時 ✅ ({time_diff.total_seconds()/3600:.1f}時間後)")
                else:
                    print(f"              → 過去日時 ⚠️ (予約投稿されない可能性)")
            except Exception as e:
                print(f"              → 日時パース失敗 ❌ ({e})")
        
        # ステータス確認
        future_status_count = content.count('<wp:status><![CDATA[future]]></wp:status>')
        draft_status_count = content.count('<wp:status><![CDATA[draft]]></wp:status>')
        publish_status_count = content.count('<wp:status><![CDATA[publish]]></wp:status>')
        
        print(f"\n📝 投稿ステータス:")
        print(f"   future (予約投稿): {future_status_count}記事")
        print(f"   draft (下書き): {draft_status_count}記事")
        print(f"   publish (公開済み): {publish_status_count}記事")
        
        # 投稿者設定確認
        author_info = re.findall(r'<dc:creator><!\[CDATA\[(.*?)\]\]></dc:creator>', content)
        if author_info:
            unique_authors = set(author_info)
            print(f"\n👤 投稿者設定:")
            for author in unique_authors:
                count = author_info.count(author)
                print(f"   {author}: {count}記事")
        
        # 画像URL確認
        thumbnail_urls = re.findall(r'<wp:meta_key><!\[CDATA\[_thumbnail_url\]\]></wp:meta_key>\s*<wp:meta_value><!\[CDATA\[(.*?)\]\]></wp:meta_value>', content)
        fifu_urls = re.findall(r'<wp:meta_key><!\[CDATA\[fifu_image_url\]\]></wp:meta_key>\s*<wp:meta_value><!\[CDATA\[(.*?)\]\]></wp:meta_value>', content)
        
        print(f"\n🖼️ アイキャッチ画像設定:")
        print(f"   _thumbnail_url設定: {len(thumbnail_urls)}記事")
        print(f"   fifu_image_url設定: {len(fifu_urls)}記事")
        
        if thumbnail_urls:
            print(f"   画像URL例: {thumbnail_urls[0][:80]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ 診断エラー: {e}")
        return False

def test_image_urls(xml_filename):
    """画像URLの有効性テスト"""
    print(f"\n🔍 アイキャッチ画像URL有効性テスト")
    print("-" * 40)
    
    try:
        with open(xml_filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        import re
        thumbnail_urls = re.findall(r'<wp:meta_value><!\[CDATA\[(https://images\.unsplash\.com/.*?)\]\]></wp:meta_value>', content)
        unique_urls = list(set(thumbnail_urls))
        
        print(f"📊 発見された画像URL: {len(unique_urls)}個")
        
        for i, url in enumerate(unique_urls, 1):
            try:
                response = requests.head(url, timeout=10)
                if response.status_code == 200:
                    print(f"   {i}. ✅ {url}")
                else:
                    print(f"   {i}. ❌ {url} (HTTP {response.status_code})")
            except Exception as e:
                print(f"   {i}. ❌ {url} (Error: {str(e)[:50]})")
                
    except Exception as e:
        print(f"❌ 画像URLテストエラー: {e}")

def generate_test_xml():
    """テスト用の最小限XML生成"""
    print(f"\n🔧 テスト用最小限XML生成")
    print("-" * 40)
    
    # 現在時刻から1時間後
    test_time = datetime.now() + timedelta(hours=1)
    
    xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:excerpt="http://wordpress.org/export/1.2/excerpt/" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:wfw="http://wellformedweb.org/CommentAPI/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:wp="http://wordpress.org/export/1.2/">
<channel>
    <title>テスト予約投稿</title>
    <link>https://teizan.abg.ooo</link>
    <description>Scheduled Post Test</description>
    <pubDate>{datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>
    <language>ja</language>
    <wp:wxr_version>1.2</wp:wxr_version>
    <wp:base_site_url>https://teizan.abg.ooo</wp:base_site_url>
    <wp:base_blog_url>https://teizan.abg.ooo</wp:base_blog_url>
    
    <wp:author>
        <wp:author_id>1</wp:author_id>
        <wp:author_login><![CDATA[aime]]></wp:author_login>
        <wp:author_email><![CDATA[aime@example.com]]></wp:author_email>
        <wp:author_display_name><![CDATA[aime]]></wp:author_display_name>
        <wp:author_first_name><![CDATA[]]></wp:author_first_name>
        <wp:author_last_name><![CDATA[]]></wp:author_last_name>
    </wp:author>
    
    <item>
        <title>テスト予約投稿記事</title>
        <link>https://teizan.abg.ooo/?p=9999</link>
        <pubDate>{test_time.strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>
        <dc:creator><![CDATA[aime]]></dc:creator>
        <guid isPermaLink="false">https://teizan.abg.ooo/?p=9999</guid>
        <description></description>
        <content:encoded><![CDATA[<h2>予約投稿テスト</h2><p>この記事は{test_time.strftime('%Y年%m月%d日 %H時%M分')}に自動投稿される予定です。</p>]]></content:encoded>
        <excerpt:encoded><![CDATA[予約投稿のテスト記事です。]]></excerpt:encoded>
        <wp:post_id>9999</wp:post_id>
        <wp:post_date><![CDATA[{test_time.strftime('%Y-%m-%d %H:%M:%S')}]]></wp:post_date>
        <wp:post_date_gmt><![CDATA[{test_time.strftime('%Y-%m-%d %H:%M:%S')}]]></wp:post_date_gmt>
        <wp:comment_status><![CDATA[open]]></wp:comment_status>
        <wp:ping_status><![CDATA[open]]></wp:ping_status>
        <wp:post_name><![CDATA[test-scheduled-post]]></wp:post_name>
        <wp:status><![CDATA[future]]></wp:status>
        <wp:post_parent>0</wp:post_parent>
        <wp:menu_order>0</wp:menu_order>
        <wp:post_type><![CDATA[post]]></wp:post_type>
        <wp:post_password><![CDATA[]]></wp:post_password>
        <wp:is_sticky>0</wp:is_sticky>
        <wp:postmeta>
            <wp:meta_key><![CDATA[_thumbnail_url]]></wp:meta_key>
            <wp:meta_value><![CDATA[https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&h=400&fit=crop]]></wp:meta_value>
        </wp:postmeta>
        <wp:postmeta>
            <wp:meta_key><![CDATA[fifu_image_url]]></wp:meta_key>
            <wp:meta_value><![CDATA[https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&h=400&fit=crop]]></wp:meta_value>
        </wp:postmeta>
    </item>
</channel>
</rss>"""
    
    filename = f"test_scheduled_post_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xml"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(xml_content)
    
    print(f"✅ テストXML作成: {filename}")
    print(f"   予約投稿時刻: {test_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   現在から: {(test_time - datetime.now()).total_seconds()/60:.1f}分後")
    
    return filename

def analyze_wordpress_settings():
    """WordPress設定分析"""
    print(f"\n⚙️ WordPress設定確認事項")
    print("-" * 40)
    
    checklist = [
        "✅ WordPress管理画面 → 設定 → 一般",
        "   → タイムゾーンが正しく設定されているか確認",
        "",
        "✅ WordPress管理画面 → ツール → インポート",
        "   → WordPressインポーターがインストール済みか確認",
        "",
        "✅ プラグイン確認:",
        "   → Featured Image from URL プラグインが有効化済み",
        "   → WP Cron（予約投稿機能）が有効",
        "",
        "✅ サーバー設定確認:",
        "   → wp-cron.php の実行権限",
        "   → DISABLE_WP_CRON が false に設定",
        "",
        "✅ 投稿者権限確認:",
        "   → 'aime' ユーザーの投稿権限",
        "   → 未来の投稿を作成する権限"
    ]
    
    for item in checklist:
        print(item)

def main():
    """メイン診断実行"""
    print("🔍 予約投稿問題診断ツール")
    print("=" * 60)
    
    # 最新のXMLファイルを診断
    xml_files = [
        'final_sample_articles_20250610_104939.xml',
        'wordpress_wxr_fixed_20250610_111252.xml'
    ]
    
    for xml_file in xml_files:
        try:
            print(f"\n{'='*60}")
            success = diagnose_xml_file(xml_file)
            if success:
                test_image_urls(xml_file)
        except FileNotFoundError:
            print(f"⚠️ ファイルが見つかりません: {xml_file}")
        except Exception as e:
            print(f"❌ 診断エラー: {e}")
    
    # テスト用XML生成
    test_xml = generate_test_xml()
    
    # WordPress設定確認項目
    analyze_wordpress_settings()
    
    print(f"\n🎯 推奨対処法:")
    print("1. 生成されたテストXMLで予約投稿をテスト")
    print("2. WordPress管理画面でタイムゾーン設定を確認")
    print("3. WP-Cronの動作状況を確認")
    print("4. 'aime'ユーザーの権限設定を確認")
    print("5. Featured Image from URLプラグインの設定を再確認")
    
    print(f"\n📋 テスト手順:")
    print(f"1. {test_xml} をWordPressにインポート")
    print("2. 投稿一覧で予約投稿が表示されることを確認")
    print("3. 指定時刻に自動投稿されるかを確認")

if __name__ == '__main__':
    main()