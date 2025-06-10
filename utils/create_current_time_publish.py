#!/usr/bin/env python3
"""
現在時刻で即座公開するXMLファイル作成
新規記事として適切な現在時刻を使用し、予約投稿は行わない
"""
import json
from datetime import datetime, timedelta

def create_current_time_publish_xml():
    """現在時刻で即座公開するXMLを作成"""
    print("🔧 現在時刻即座公開XML作成")
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
    
    # 現在時刻を基準にする（新規記事として適切）
    now = datetime.now()
    print(f"📅 基準時刻: {now.strftime('%Y-%m-%d %H:%M:%S')} (現在時刻)")
    
    # XML生成
    xml_content = generate_current_time_wxr(articles_data, now)
    
    # ファイル保存
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    xml_filename = f"current_time_publish_{timestamp}.xml"
    
    with open(xml_filename, 'w', encoding='utf-8') as f:
        f.write(xml_content)
    
    print(f"\n✅ 現在時刻公開XMLファイル作成: {xml_filename}")
    print(f"   ファイルサイズ: {len(xml_content) / 1024:.1f} KB")
    
    return xml_filename

def generate_current_time_wxr(articles_data, base_time):
    """現在時刻で即座公開用WXR生成"""
    
    # 現在時刻をベースにしたWXRヘッダー
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"
	xmlns:excerpt="http://wordpress.org/export/1.2/excerpt/"
	xmlns:content="http://purl.org/rss/1.0/modules/content/"
	xmlns:wfw="http://wellformedweb.org/CommentAPI/"
	xmlns:dc="http://purl.org/dc/elements/1.1/"
	xmlns:wp="http://wordpress.org/export/1.2/"
>

<channel>
	<title>低山旅行 - 新規記事投稿</title>
	<link>https://teizan.abg.ooo</link>
	<description>Mountain Blog Generator - Current Time Posts</description>
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
		<wp:author_last_name><![CDATA[]]></wp:parameter_last_name>
	</wp:author>

	<wp:category>
		<wp:term_id>1</wp:term_id>
		<wp:category_nicename><![CDATA[area]]></wp:category_nicename>
		<wp:category_parent><![CDATA[]]></wp:category_parent>
		<wp:cat_name><![CDATA[エリア別]]></wp:cat_name>
	</wp:category>

"""

    # 各記事を現在時刻で即座公開として追加
    for i, article in enumerate(articles_data):
        # 各記事を数秒ずつずらして投稿順序を明確にする
        article_time = base_time + timedelta(seconds=i * 10)
        
        # 記事の内容をエスケープ
        title = escape_xml(article['title'])
        content = article['content']
        excerpt = article['excerpt']
        
        xml_content += f"""
	<item>
		<title>{title}</title>
		<link>https://teizan.abg.ooo/?p={i+7000}</link>
		<pubDate>{article_time.strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>
		<dc:creator><![CDATA[aime]]></dc:creator>
		<guid isPermaLink="false">https://teizan.abg.ooo/?p={i+7000}</guid>
		<description></description>
		<content:encoded><![CDATA[{content}]]></content:encoded>
		<excerpt:encoded><![CDATA[{excerpt}]]></excerpt:encoded>
		<wp:post_id>{i+7000}</wp:post_id>
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

        # アイキャッチ画像のメタデータ
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

def verify_current_time_xml(xml_filename):
    """現在時刻XMLファイルの検証"""
    print(f"\n🔍 現在時刻XMLファイル検証: {xml_filename}")
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
            print(f"   {i+1}. {pub_date}")
        
        # wp:post_date確認
        post_dates = re.findall(r'<wp:post_date><!\[CDATA\[(.*?)\]\]></wp:post_date>', content)
        print(f"\n📅 wp:post_date確認:")
        for i, post_date in enumerate(post_dates, 1):
            try:
                post_datetime = datetime.strptime(post_date, '%Y-%m-%d %H:%M:%S')
                time_diff = abs((post_datetime - now).total_seconds())
                
                if time_diff < 3600:  # 1時間以内
                    time_status = "現在時刻付近 ✅"
                elif post_datetime > now:
                    time_status = "未来時刻 ⚠️"
                else:
                    time_status = "過去時刻"
                
                print(f"   記事{i}: {post_date} ({time_status})")
            except:
                print(f"   記事{i}: {post_date} (解析失敗)")
        
        # ステータス確認
        publish_count = len(re.findall(r'<wp:status><!\[CDATA\[publish\]\]></wp:status>', content))
        future_count = len(re.findall(r'<wp:status><!\[CDATA\[future\]\]></wp:status>', content))
        
        print(f"\n📊 ステータス確認:")
        print(f"   即座公開 (publish): {publish_count}記事")
        print(f"   予約投稿 (future): {future_count}記事")
        
        if future_count == 0 and publish_count > 0:
            print("   ✅ 全記事が即座公開設定")
        else:
            print("   ⚠️ 予約投稿設定が含まれています")
        
        # アイキャッチ画像確認
        thumbnail_count = len(re.findall(r'<wp:meta_key><!\[CDATA\[_thumbnail_url\]\]></wp:meta_key>', content))
        print(f"\n🖼️ アイキャッチ画像: {thumbnail_count}記事に設定済み")
        
        # 投稿者確認
        authors = re.findall(r'<dc:creator><!\[CDATA\[(.*?)\]\]></dc:creator>', content)
        unique_authors = set(authors)
        print(f"\n👤 投稿者: {', '.join(unique_authors)}")
        
        print(f"\n✅ 現在時刻XML検証完了")
        return True
        
    except Exception as e:
        print(f"❌ 検証エラー: {e}")
        return False

def create_simple_current_test():
    """シンプルな現在時刻テスト用XML"""
    print(f"\n🧪 シンプル現在時刻テスト用XML作成")
    print("-" * 40)
    
    now = datetime.now()
    
    simple_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:wp="http://wordpress.org/export/1.2/" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:dc="http://purl.org/dc/elements/1.1/">
<channel>
    <title>現在時刻テスト投稿</title>
    <pubDate>{now.strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>
    <wp:wxr_version>1.2</wp:wxr_version>
    
    <wp:author>
        <wp:author_id>1</wp:author_id>
        <wp:author_login><![CDATA[aime]]></wp:author_login>
        <wp:author_email><![CDATA[aime@example.com]]></wp:author_email>
        <wp:author_display_name><![CDATA[aime]]></wp:author_display_name>
    </wp:author>
    
    <item>
        <title>現在時刻即座公開テスト</title>
        <pubDate>{now.strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>
        <dc:creator><![CDATA[aime]]></dc:creator>
        <content:encoded><![CDATA[<h2>現在時刻即座公開テスト</h2><p>この記事は{now.strftime('%Y年%m月%d日 %H時%M分')}に作成され、即座に公開される設定です。予約投稿ではありません。</p>]]></content:encoded>
        <wp:post_id>9999</wp:post_id>
        <wp:post_date><![CDATA[{now.strftime('%Y-%m-%d %H:%M:%S')}]]></wp:post_date>
        <wp:post_date_gmt><![CDATA[{now.strftime('%Y-%m-%d %H:%M:%S')}]]></wp:post_date_gmt>
        <wp:status><![CDATA[publish]]></wp:status>
        <wp:post_type><![CDATA[post]]></wp:post_type>
    </item>
</channel>
</rss>"""
    
    test_filename = f"simple_current_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xml"
    with open(test_filename, 'w', encoding='utf-8') as f:
        f.write(simple_xml)
    
    print(f"✅ シンプル現在時刻テストXML作成: {test_filename}")
    print(f"   投稿時刻: {now.strftime('%Y-%m-%d %H:%M:%S')} (現在時刻)")
    
    return test_filename

def main():
    """メイン処理"""
    print("🔧 現在時刻即座公開XMLツール")
    print("=" * 60)
    
    # メインXML作成
    xml_filename = create_current_time_publish_xml()
    
    if xml_filename:
        verify_current_time_xml(xml_filename)
        
        # シンプルテストXML作成
        test_filename = create_simple_current_test()
        
        print(f"\n🎉 現在時刻即座公開XML作成完了！")
        print(f"📄 メインXMLファイル: {xml_filename}")
        print(f"🧪 シンプルテストファイル: {test_filename}")
        
        print(f"\n📋 この版の特徴:")
        print("   ✅ 現在時刻で新規記事として投稿")
        print("   ✅ ブログとして自然な投稿日時")
        print("   ✅ 予約投稿は行わない（即座公開）")
        print("   ✅ WP-Cronに依存しない")
        
        print(f"\n📅 投稿日時設定:")
        now = datetime.now()
        print(f"   記事1: {now.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   記事2: {(now + timedelta(seconds=10)).strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   記事3: {(now + timedelta(seconds=20)).strftime('%Y-%m-%d %H:%M:%S')}")
        print("   → 数秒差で投稿順序を明確化")
        
        print(f"\n📋 WordPress インポート手順:")
        print("1. WordPress管理画面 → ツール → インポート → WordPress")
        print("2. XMLファイルをアップロード")
        print("3. 投稿者を 'aime' に設定")
        print("4. インポート実行")
        print("5. 投稿一覧で全記事が新規公開されているか確認")
        
        print(f"\n💡 この版のメリット:")
        print("- 新規記事として適切な投稿日時")
        print("- 読者にとって自然なブログ投稿")
        print("- RSS・SEOに適した時系列")
        print("- 予約投稿の問題を完全回避")
        
    else:
        print("❌ XML作成に失敗しました")

if __name__ == '__main__':
    main()