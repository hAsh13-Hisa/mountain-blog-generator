#!/usr/bin/env python3
"""
1時間前の時刻で投稿するXMLファイル作成
予約投稿エラーを完全回避し、新規記事として自然な設定
"""
import json
from datetime import datetime, timedelta

def create_one_hour_ago_xml():
    """1時間前の時刻で投稿するXMLを作成"""
    print("🔧 1時間前投稿XML作成")
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
    
    # 1時間前の時刻を基準にする
    now = datetime.now()
    one_hour_ago = now - timedelta(hours=1)
    # 分・秒を整数にして見やすくする
    base_time = one_hour_ago.replace(minute=0, second=0, microsecond=0)
    
    print(f"📅 現在時刻: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📅 基準時刻: {base_time.strftime('%Y-%m-%d %H:%M:%S')} (1時間前)")
    
    # XML生成
    xml_content = generate_one_hour_ago_wxr(articles_data, base_time)
    
    # ファイル保存
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    xml_filename = f"one_hour_ago_articles_{timestamp}.xml"
    
    with open(xml_filename, 'w', encoding='utf-8') as f:
        f.write(xml_content)
    
    print(f"\n✅ 1時間前投稿XMLファイル作成: {xml_filename}")
    print(f"   ファイルサイズ: {len(xml_content) / 1024:.1f} KB")
    
    return xml_filename

def generate_one_hour_ago_wxr(articles_data, base_time):
    """1時間前投稿用WXR生成"""
    
    # 1時間前をベースにしたWXRヘッダー
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"
	xmlns:excerpt="http://wordpress.org/export/1.2/excerpt/"
	xmlns:content="http://purl.org/rss/1.0/modules/content/"
	xmlns:wfw="http://wellformedweb.org/CommentAPI/"
	xmlns:dc="http://purl.org/dc/elements/1.1/"
	xmlns:wp="http://wordpress.org/export/1.2/"
>

<channel>
	<title>低山旅行 - 1時間前投稿</title>
	<link>https://teizan.abg.ooo</link>
	<description>Mountain Blog Generator - One Hour Ago Posts</description>
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

    # 各記事を1時間前から数分間隔で投稿
    for i, article in enumerate(articles_data):
        # 各記事を5分ずつずらす（1時間前、1時間5分前、1時間10分前）
        article_time = base_time + timedelta(minutes=i * 5)
        
        # 記事の内容をエスケープ
        title = escape_xml(article['title'])
        content = article['content']
        excerpt = article['excerpt']
        
        xml_content += f"""
	<item>
		<title>{title}</title>
		<link>https://teizan.abg.ooo/?p={i+8000}</link>
		<pubDate>{article_time.strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>
		<dc:creator><![CDATA[aime]]></dc:creator>
		<guid isPermaLink="false">https://teizan.abg.ooo/?p={i+8000}</guid>
		<description></description>
		<content:encoded><![CDATA[{content}]]></content:encoded>
		<excerpt:encoded><![CDATA[{excerpt}]]></excerpt:encoded>
		<wp:post_id>{i+8000}</wp:post_id>
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

def verify_one_hour_ago_xml(xml_filename):
    """1時間前XMLファイルの検証"""
    print(f"\n🔍 1時間前XMLファイル検証: {xml_filename}")
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
                time_diff = (now - post_datetime).total_seconds()
                
                if time_diff > 0:
                    hours_ago = time_diff / 3600
                    time_status = f"過去時刻 ✅ ({hours_ago:.1f}時間前)"
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
        
        if future_count == 0 and publish_count > 0:
            print("   ✅ 全記事が公開済み設定")
        else:
            print("   ❌ 予約投稿設定が残っています")
        
        # 予約投稿関連キーワード確認
        future_keywords = ['future', 'schedule', 'pending']
        print(f"\n🔍 予約投稿関連確認:")
        for keyword in future_keywords:
            count = content.lower().count(keyword)
            if keyword == 'future' and count == 0:
                print(f"   '{keyword}': {count}箇所 ✅")
            elif count == 0:
                print(f"   '{keyword}': {count}箇所 ✅")
            else:
                print(f"   '{keyword}': {count}箇所 ⚠️")
        
        # アイキャッチ画像確認
        thumbnail_count = len(re.findall(r'<wp:meta_key><!\[CDATA\[_thumbnail_url\]\]></wp:meta_key>', content))
        print(f"\n🖼️ アイキャッチ画像: {thumbnail_count}記事に設定済み")
        
        print(f"\n✅ 1時間前XML検証完了")
        return True
        
    except Exception as e:
        print(f"❌ 検証エラー: {e}")
        return False

def create_minimal_one_hour_ago_test():
    """最小限の1時間前テスト用XML"""
    print(f"\n🧪 最小限1時間前テスト用XML作成")
    print("-" * 40)
    
    now = datetime.now()
    one_hour_ago = now - timedelta(hours=1)
    test_time = one_hour_ago.replace(minute=30, second=0, microsecond=0)
    
    test_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:wp="http://wordpress.org/export/1.2/" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:dc="http://purl.org/dc/elements/1.1/">
<channel>
    <title>1時間前テスト投稿</title>
    <pubDate>{test_time.strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>
    <wp:wxr_version>1.2</wp:wxr_version>
    
    <wp:author>
        <wp:author_id>1</wp:author_id>
        <wp:author_login><![CDATA[aime]]></wp:author_login>
        <wp:author_email><![CDATA[aime@example.com]]></wp:author_email>
        <wp:author_display_name><![CDATA[aime]]></wp:author_display_name>
    </wp:author>
    
    <item>
        <title>1時間前投稿テスト記事</title>
        <pubDate>{test_time.strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>
        <dc:creator><![CDATA[aime]]></dc:creator>
        <content:encoded><![CDATA[<h2>1時間前投稿テスト</h2><p>この記事は{test_time.strftime('%Y年%m月%d日 %H時%M分')}に投稿された設定です。予約投稿ではなく、過去の時刻での公開済み記事です。</p>]]></content:encoded>
        <wp:post_id>9001</wp:post_id>
        <wp:post_date><![CDATA[{test_time.strftime('%Y-%m-%d %H:%M:%S')}]]></wp:post_date>
        <wp:post_date_gmt><![CDATA[{test_time.strftime('%Y-%m-%d %H:%M:%S')}]]></wp:post_date_gmt>
        <wp:status><![CDATA[publish]]></wp:status>
        <wp:post_type><![CDATA[post]]></wp:post_type>
    </item>
</channel>
</rss>"""
    
    test_filename = f"minimal_one_hour_ago_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xml"
    with open(test_filename, 'w', encoding='utf-8') as f:
        f.write(test_xml)
    
    print(f"✅ 最小限1時間前テストXML作成: {test_filename}")
    print(f"   投稿時刻: {test_time.strftime('%Y-%m-%d %H:%M:%S')} (1時間前)")
    
    return test_filename

def main():
    """メイン処理"""
    print("🔧 1時間前投稿XMLツール")
    print("=" * 60)
    
    # メインXML作成
    xml_filename = create_one_hour_ago_xml()
    
    if xml_filename:
        verify_one_hour_ago_xml(xml_filename)
        
        # 最小限テストXML作成
        test_filename = create_minimal_one_hour_ago_test()
        
        print(f"\n🎉 1時間前投稿XML作成完了！")
        print(f"📄 メインXMLファイル: {xml_filename}")
        print(f"🧪 最小限テストファイル: {test_filename}")
        
        now = datetime.now()
        one_hour_ago = now - timedelta(hours=1)
        
        print(f"\n📋 この版の特徴:")
        print("   ✅ 1時間前の時刻で投稿（過去時刻）")
        print("   ✅ 予約投稿エラーを完全回避")
        print("   ✅ 新規記事として適度に自然")
        print("   ✅ WP-Cronに依存しない")
        
        print(f"\n📅 投稿時刻設定:")
        base_time = one_hour_ago.replace(minute=0, second=0, microsecond=0)
        print(f"   記事1: {base_time.strftime('%Y-%m-%d %H:%M:%S')} (1時間前)")
        print(f"   記事2: {(base_time + timedelta(minutes=5)).strftime('%Y-%m-%d %H:%M:%S')} (55分前)")
        print(f"   記事3: {(base_time + timedelta(minutes=10)).strftime('%Y-%m-%d %H:%M:%S')} (50分前)")
        
        print(f"\n📋 WordPress インポート手順:")
        print("1. WordPress管理画面 → ツール → インポート → WordPress")
        print("2. XMLファイルをアップロード")
        print("3. 投稿者を 'aime' に設定")
        print("4. インポート実行")
        print("5. 投稿一覧で全記事が公開済みになっているか確認")
        
        print(f"\n💡 この設定のメリット:")
        print("- 予約投稿エラーが絶対に発生しない")
        print("- 1時間前なので新規記事としてそれなりに自然")
        print("- インポート後即座に確認可能")
        print("- アイキャッチ画像と楽天リンクの動作確認に最適")
        
        print(f"\n⚠️ 重要ポイント:")
        print("- 全ての日時が過去時刻（1時間前）")
        print("- ステータスは全て 'publish'（公開済み）")
        print("- 予約投稿要素は一切含まれていない")
        
    else:
        print("❌ XML作成に失敗しました")

if __name__ == '__main__':
    main()