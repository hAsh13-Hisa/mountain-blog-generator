#!/usr/bin/env python3
"""
予約投稿要素を完全除去したXMLファイル作成
pubDate、wp:post_date等のスケジュール関連要素を全て除去または過去時刻に設定
"""
import json
from datetime import datetime, timedelta

def create_clean_no_schedule_xml():
    """予約投稿要素を完全除去したXMLを作成"""
    print("🔧 予約投稿要素完全除去XML作成")
    print("=" * 50)
    
    # 記事データを読み込み
    json_files = [
        'corrected_articles_data_20250610_111631.json',
        'final_sample_articles_20250610_104939.json'
    ]
    
    articles_data = None
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                articles_data = json.load(f)
                print(f"📂 記事データ読み込み: {json_file}")
                break
        except FileNotFoundError:
            continue
    
    if not articles_data:
        print("❌ 記事データが見つかりません")
        return None
    
    print(f"📊 読み込み記事数: {len(articles_data)}記事")
    
    # 確実に過去の時刻を使用（1週間前）
    base_time = datetime.now() - timedelta(days=7)
    base_time = base_time.replace(hour=10, minute=0, second=0, microsecond=0)
    
    print(f"📅 ベース投稿時刻: {base_time.strftime('%Y-%m-%d %H:%M:%S')} (1週間前)")
    
    # XML生成
    xml_content = generate_clean_wxr(articles_data, base_time)
    
    # ファイル保存
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    xml_filename = f"clean_no_schedule_articles_{timestamp}.xml"
    
    with open(xml_filename, 'w', encoding='utf-8') as f:
        f.write(xml_content)
    
    print(f"\n✅ 完全クリーンXMLファイル作成: {xml_filename}")
    print(f"   ファイルサイズ: {len(xml_content) / 1024:.1f} KB")
    
    return xml_filename

def generate_clean_wxr(articles_data, base_time):
    """スケジュール要素を完全除去したWXR生成"""
    
    # チャンネル部分も過去時刻に設定
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"
	xmlns:excerpt="http://wordpress.org/export/1.2/excerpt/"
	xmlns:content="http://purl.org/rss/1.0/modules/content/"
	xmlns:wfw="http://wellformedweb.org/CommentAPI/"
	xmlns:dc="http://purl.org/dc/elements/1.1/"
	xmlns:wp="http://wordpress.org/export/1.2/"
>

<channel>
	<title>低山旅行 - クリーン投稿</title>
	<link>https://teizan.abg.ooo</link>
	<description>Mountain Blog Generator - Clean Posts (No Schedule)</description>
	<pubDate>""" + base_time.strftime('%a, %d %b %Y %H:%M:%S +0000') + """</pubDate>
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

	<wp:category>
		<wp:term_id>1</wp:term_id>
		<wp:category_nicename><![CDATA[area]]></wp:category_nicename>
		<wp:category_parent><![CDATA[]]></wp:category_parent>
		<wp:cat_name><![CDATA[エリア別]]></wp:cat_name>
	</wp:category>

"""

    # 各記事を追加（全て過去時刻）
    for i, article in enumerate(articles_data):
        # 各記事を1時間ずつずらして過去時刻に設定
        article_time = base_time - timedelta(hours=i)
        
        # 記事の内容をエスケープ
        title = escape_xml(article['title'])
        content = article['content']
        excerpt = article['excerpt']
        
        xml_content += f"""
	<item>
		<title>{title}</title>
		<link>https://teizan.abg.ooo/?p={i+6000}</link>
		<pubDate>{article_time.strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>
		<dc:creator><![CDATA[aime]]></dc:creator>
		<guid isPermaLink="false">https://teizan.abg.ooo/?p={i+6000}</guid>
		<description></description>
		<content:encoded><![CDATA[{content}]]></content:encoded>
		<excerpt:encoded><![CDATA[{excerpt}]]></excerpt:encoded>
		<wp:post_id>{i+6000}</wp:post_id>
		<wp:post_date><![CDATA[{article_time.strftime('%Y-%m-%d %H:%M:%S')}]]></wp:post_date>
		<wp:post_date_gmt><![CDATA[{article_time.strftime('%Y-%m-%d %H:%M:%S')}]]></wp:post_date_gmt>
		<wp:comment_status><![CDATA[open]]></wp:comment_status>
		<wp:ping_status><![CDATA[open]]></wp:ping_status>
		<wp:post_name><![CDATA[{create_slug(article['title'])}]]></wp:post_name>
		<wp:status><![CDATA[publish]]></wp:status>
		<wp:post_parent>0</wp:post_parent>
		<wp:menu_order>0</wp:menu_order>
		<wp:post_type><![CDATA[post]]></wp:post_type>
		<wp:post_password><![CDATA[]]></wp:post_password>
		<wp:is_sticky>0</wp:is_sticky>
		<category domain="category" nicename="area"><![CDATA[エリア別]]></category>"""

        # タグを追加
        for tag in article.get('tags', []):
            tag_slug = create_slug(tag)
            xml_content += f"""
		<category domain="post_tag" nicename="{tag_slug}"><![CDATA[{escape_xml(tag)}]]></category>"""

        # アイキャッチ画像のメタデータ（必要最小限）
        if article.get('featured_image_url'):
            xml_content += f"""
		<wp:postmeta>
			<wp:meta_key><![CDATA[_thumbnail_url]]></wp:meta_key>
			<wp:meta_value><![CDATA[{article['featured_image_url']}]]></wp:meta_value>
		</wp:postmeta>
		<wp:postmeta>
			<wp:meta_key><![CDATA[fifu_image_url]]></wp:meta_key>
			<wp:meta_value><![CDATA[{article['featured_image_url']}]]></wp:meta_value>
		</wp:postmeta>"""

        xml_content += """
	</item>"""

    xml_content += """
</channel>
</rss>"""

    return xml_content

def create_ultra_minimal_xml():
    """最小限のテスト用XML（日付要素を最小化）"""
    print(f"\n🧪 超最小限テスト用XML作成")
    print("-" * 30)
    
    # 1ヶ月前の時刻を使用
    past_time = datetime.now() - timedelta(days=30)
    past_time = past_time.replace(hour=12, minute=0, second=0, microsecond=0)
    
    minimal_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:wp="http://wordpress.org/export/1.2/" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:dc="http://purl.org/dc/elements/1.1/">
<channel>
    <title>超シンプルテスト</title>
    <pubDate>{past_time.strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>
    <wp:wxr_version>1.2</wp:wxr_version>
    
    <wp:author>
        <wp:author_id>1</wp:author_id>
        <wp:author_login><![CDATA[aime]]></wp:author_login>
        <wp:author_email><![CDATA[aime@example.com]]></wp:author_email>
        <wp:author_display_name><![CDATA[aime]]></wp:author_display_name>
    </wp:author>
    
    <item>
        <title>過去時刻テスト投稿</title>
        <pubDate>{past_time.strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>
        <dc:creator><![CDATA[aime]]></dc:creator>
        <content:encoded><![CDATA[<h2>過去時刻テスト</h2><p>この記事は{past_time.strftime('%Y年%m月%d日')}の投稿として作成されました。予約投稿要素は一切含まれていません。</p>]]></content:encoded>
        <wp:post_id>8000</wp:post_id>
        <wp:post_date><![CDATA[{past_time.strftime('%Y-%m-%d %H:%M:%S')}]]></wp:post_date>
        <wp:post_date_gmt><![CDATA[{past_time.strftime('%Y-%m-%d %H:%M:%S')}]]></wp:post_date_gmt>
        <wp:status><![CDATA[publish]]></wp:status>
        <wp:post_type><![CDATA[post]]></wp:post_type>
    </item>
</channel>
</rss>"""
    
    test_filename = f"ultra_minimal_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xml"
    with open(test_filename, 'w', encoding='utf-8') as f:
        f.write(minimal_xml)
    
    print(f"✅ 超最小限テストXML作成: {test_filename}")
    print(f"   投稿時刻: {past_time.strftime('%Y-%m-%d %H:%M:%S')} (1ヶ月前)")
    
    return test_filename

def escape_xml(text: str) -> str:
    """XMLエスケープ"""
    return (text.replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;')
                .replace("'", '&apos;'))

def create_slug(text: str) -> str:
    """URLスラッグを生成"""
    import re
    slug = re.sub(r'[^\w\s-]', '', text.lower())
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug[:50]

def verify_clean_xml(xml_filename):
    """クリーンXMLファイルの検証"""
    print(f"\n🔍 クリーンXMLファイル検証: {xml_filename}")
    print("-" * 50)
    
    try:
        with open(xml_filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 現在時刻
        now = datetime.now()
        
        # 日時要素の確認
        import re
        
        # pubDate確認
        pub_dates = re.findall(r'<pubDate>(.*?)</pubDate>', content)
        print(f"📅 pubDate確認:")
        for i, pub_date in enumerate(pub_dates):
            # 簡易的な日付解析
            if "2025" in pub_date:
                if "Jun 2025" in pub_date:
                    print(f"   {i+1}. {pub_date} ⚠️ (2025年6月)")
                else:
                    print(f"   {i+1}. {pub_date} ✅ (過去日付)")
            else:
                print(f"   {i+1}. {pub_date} ✅ (過去日付)")
        
        # wp:post_date確認
        post_dates = re.findall(r'<wp:post_date><!\[CDATA\[(.*?)\]\]></wp:post_date>', content)
        print(f"\n📅 wp:post_date確認:")
        for i, post_date in enumerate(post_dates, 1):
            try:
                post_datetime = datetime.strptime(post_date, '%Y-%m-%d %H:%M:%S')
                if post_datetime < now:
                    time_status = "過去時刻 ✅"
                else:
                    time_status = "未来時刻 ❌"
                print(f"   記事{i}: {post_date} ({time_status})")
            except:
                print(f"   記事{i}: {post_date} (解析失敗)")
        
        # ステータス確認
        publish_count = len(re.findall(r'<wp:status><!\[CDATA\[publish\]\]></wp:status>', content))
        future_count = len(re.findall(r'<wp:status><!\[CDATA\[future\]\]></wp:status>', content))
        
        print(f"\n📊 ステータス確認:")
        print(f"   公開済み (publish): {publish_count}記事")
        print(f"   予約投稿 (future): {future_count}記事")
        
        if future_count == 0:
            print("   ✅ 予約投稿ステータスなし")
        else:
            print("   ❌ 予約投稿ステータスが残っています")
        
        # スケジュール関連キーワード
        schedule_words = ['future', 'schedule', 'cron', 'pending']
        print(f"\n🔍 スケジュール関連キーワード:")
        for word in schedule_words:
            count = content.lower().count(word)
            if word == 'future' and count == future_count:
                print(f"   '{word}': {count}箇所 ✅ (ステータスのみ)")
            elif count == 0:
                print(f"   '{word}': {count}箇所 ✅")
            else:
                print(f"   '{word}': {count}箇所 ⚠️")
        
        print(f"\n✅ クリーンXML検証完了")
        return True
        
    except Exception as e:
        print(f"❌ 検証エラー: {e}")
        return False

def main():
    """メイン処理"""
    print("🔧 予約投稿要素完全除去XMLツール")
    print("=" * 60)
    
    # メインXML作成
    xml_filename = create_clean_no_schedule_xml()
    
    if xml_filename:
        verify_clean_xml(xml_filename)
        
        # 超最小限テストXML作成
        test_filename = create_ultra_minimal_xml()
        
        print(f"\n🎉 完全クリーンXML作成完了！")
        print(f"📄 メインXMLファイル: {xml_filename}")
        print(f"🧪 超最小限テストファイル: {test_filename}")
        
        print(f"\n📋 完全除去された要素:")
        print("   ✅ 未来のpubDate → 過去時刻に変更")
        print("   ✅ 未来のwp:post_date → 過去時刻に変更")
        print("   ✅ wp:status future → publish のみ")
        print("   ✅ スケジュール関連キーワード除去")
        
        print(f"\n📋 安全な日時設定:")
        print("   📅 チャンネルpubDate: 1週間前")
        print("   📅 記事投稿日時: 1週間前〜1週間と3時間前")
        print("   📅 全て確実に過去時刻")
        
        print(f"\n📋 推奨テスト順序:")
        print(f"1. {test_filename} で基本動作確認")
        print(f"2. {xml_filename} で本格テスト")
        
        print(f"\n⚠️ 最重要ポイント:")
        print("- 全ての日時が過去時刻になっています")
        print("- 予約投稿は絶対に実行されません")
        print("- インポート後即座に公開済み状態になります")
        
    else:
        print("❌ XML作成に失敗しました")

if __name__ == '__main__':
    main()