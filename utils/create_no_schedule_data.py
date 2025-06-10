#!/usr/bin/env python3
"""
予約投稿設定を完全に除去したXMLファイル作成
通常の投稿として即座に公開（スケジュール要素なし）
"""
import json
from datetime import datetime

def create_no_schedule_xml():
    """予約投稿設定なしの通常投稿XMLを作成"""
    print("🔧 予約投稿設定なし通常投稿XML作成")
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
    
    # 現在時刻（過去の時刻を使用して確実に公開状態にする）
    now = datetime.now()
    # 1時間前の時刻を基準にして確実に公開済み状態にする
    publish_time = datetime(now.year, now.month, now.day, now.hour - 1, 0, 0)
    
    print(f"📅 投稿時刻: {publish_time.strftime('%Y-%m-%d %H:%M:%S')} (過去時刻)")
    
    # XML生成
    xml_content = generate_simple_publish_wxr(articles_data, publish_time)
    
    # ファイル保存
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    xml_filename = f"no_schedule_articles_{timestamp}.xml"
    
    with open(xml_filename, 'w', encoding='utf-8') as f:
        f.write(xml_content)
    
    print(f"\n✅ 予約設定なしXMLファイル作成: {xml_filename}")
    print(f"   ファイルサイズ: {len(xml_content) / 1024:.1f} KB")
    
    return xml_filename

def generate_simple_publish_wxr(articles_data, base_time):
    """シンプルな通常投稿用WXR生成"""
    
    # 最小限のWXRヘッダー
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"
	xmlns:excerpt="http://wordpress.org/export/1.2/excerpt/"
	xmlns:content="http://purl.org/rss/1.0/modules/content/"
	xmlns:wfw="http://wellformedweb.org/CommentAPI/"
	xmlns:dc="http://purl.org/dc/elements/1.1/"
	xmlns:wp="http://wordpress.org/export/1.2/"
>

<channel>
	<title>低山旅行 - 通常投稿</title>
	<link>https://teizan.abg.ooo</link>
	<description>Mountain Blog Generator - Regular Posts</description>
	<pubDate>""" + datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000') + """</pubDate>
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

    # 各記事を追加（過去時刻で公開済み状態）
    for i, article in enumerate(articles_data):
        # 各記事に少しずつ時間差をつける（数分差）
        article_time = base_time.replace(minute=base_time.minute + (i * 5))
        
        # 記事の内容をエスケープ
        title = escape_xml(article['title'])
        content = article['content']
        excerpt = article['excerpt']
        
        xml_content += f"""
	<item>
		<title>{title}</title>
		<link>https://teizan.abg.ooo/?p={i+5000}</link>
		<pubDate>{article_time.strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>
		<dc:creator><![CDATA[aime]]></dc:creator>
		<guid isPermaLink="false">https://teizan.abg.ooo/?p={i+5000}</guid>
		<description></description>
		<content:encoded><![CDATA[{content}]]></content:encoded>
		<excerpt:encoded><![CDATA[{excerpt}]]></excerpt:encoded>
		<wp:post_id>{i+5000}</wp:post_id>
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

        # アイキャッチ画像のメタデータ（シンプル版）
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

def verify_no_schedule_xml(xml_filename):
    """生成されたXMLファイルの内容を検証"""
    print(f"\n🔍 XMLファイル検証: {xml_filename}")
    print("-" * 40)
    
    try:
        with open(xml_filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # ステータス確認
        import re
        publish_count = len(re.findall(r'<wp:status><!\[CDATA\[publish\]\]></wp:status>', content))
        future_count = len(re.findall(r'<wp:status><!\[CDATA\[future\]\]></wp:status>', content))
        draft_count = len(re.findall(r'<wp:status><!\[CDATA\[draft\]\]></wp:status>', content))
        
        print(f"📊 投稿ステータス:")
        print(f"   公開済み (publish): {publish_count}記事")
        print(f"   予約投稿 (future): {future_count}記事 ← これが0であることを確認")
        print(f"   下書き (draft): {draft_count}記事")
        
        if future_count == 0:
            print("   ✅ 予約投稿設定は完全に除去されました")
        else:
            print("   ❌ まだ予約投稿設定が残っています")
        
        # 投稿日時を抽出
        post_dates = re.findall(r'<wp:post_date><!\[CDATA\[(.*?)\]\]></wp:post_date>', content)
        
        print(f"\n📅 投稿日時:")
        for i, post_date in enumerate(post_dates, 1):
            # 現在時刻と比較
            from datetime import datetime
            post_datetime = datetime.strptime(post_date, '%Y-%m-%d %H:%M:%S')
            now = datetime.now()
            
            if post_datetime < now:
                time_status = "過去時刻 ✅"
            else:
                time_status = "未来時刻 ⚠️"
            
            print(f"   記事{i}: {post_date} ({time_status})")
        
        # アイキャッチ画像確認
        thumbnail_urls = len(re.findall(r'<wp:meta_key><!\[CDATA\[_thumbnail_url\]\]></wp:meta_key>', content))
        fifu_urls = len(re.findall(r'<wp:meta_key><!\[CDATA\[fifu_image_url\]\]></wp:meta_key>', content))
        
        print(f"\n🖼️ アイキャッチ画像:")
        print(f"   _thumbnail_url: {thumbnail_urls}記事")
        print(f"   fifu_image_url: {fifu_urls}記事")
        
        # 投稿者確認
        authors = re.findall(r'<dc:creator><!\[CDATA\[(.*?)\]\]></dc:creator>', content)
        unique_authors = set(authors)
        print(f"\n👤 投稿者:")
        for author in unique_authors:
            count = authors.count(author)
            print(f"   {author}: {count}記事")
        
        # スケジュール関連のキーワード検索
        schedule_keywords = ['future', 'schedule', 'cron']
        print(f"\n🔍 スケジュール関連チェック:")
        for keyword in schedule_keywords:
            count = content.lower().count(keyword)
            if keyword == 'future' and count > 0:
                print(f"   '{keyword}': {count}箇所 (wp:status以外での使用を確認)")
            else:
                print(f"   '{keyword}': {count}箇所")
        
        print(f"\n✅ XMLファイル検証完了")
        return True
        
    except Exception as e:
        print(f"❌ 検証エラー: {e}")
        return False

def create_simple_test_xml():
    """最小限のテスト用XML作成"""
    print(f"\n🧪 最小限テスト用XML作成")
    print("-" * 30)
    
    # 過去の時刻を使用
    past_time = datetime.now().replace(hour=datetime.now().hour - 2, minute=0, second=0)
    
    simple_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:wp="http://wordpress.org/export/1.2/" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:dc="http://purl.org/dc/elements/1.1/">
<channel>
    <title>テスト投稿</title>
    <wp:wxr_version>1.2</wp:wxr_version>
    
    <wp:author>
        <wp:author_id>1</wp:author_id>
        <wp:author_login><![CDATA[aime]]></wp:author_login>
        <wp:author_email><![CDATA[aime@example.com]]></wp:author_email>
        <wp:author_display_name><![CDATA[aime]]></wp:author_display_name>
    </wp:author>
    
    <item>
        <title>シンプル通常投稿テスト</title>
        <dc:creator><![CDATA[aime]]></dc:creator>
        <content:encoded><![CDATA[<h2>通常投稿テスト</h2><p>これは予約投稿設定なしの通常投稿テストです。</p>]]></content:encoded>
        <wp:post_id>9000</wp:post_id>
        <wp:post_date><![CDATA[{past_time.strftime('%Y-%m-%d %H:%M:%S')}]]></wp:post_date>
        <wp:post_date_gmt><![CDATA[{past_time.strftime('%Y-%m-%d %H:%M:%S')}]]></wp:post_date_gmt>
        <wp:status><![CDATA[publish]]></wp:status>
        <wp:post_type><![CDATA[post]]></wp:post_type>
    </item>
</channel>
</rss>"""
    
    test_filename = f"simple_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xml"
    with open(test_filename, 'w', encoding='utf-8') as f:
        f.write(simple_xml)
    
    print(f"✅ 最小限テストXML作成: {test_filename}")
    print(f"   投稿時刻: {past_time.strftime('%Y-%m-%d %H:%M:%S')} (2時間前)")
    
    return test_filename

def main():
    """メイン処理"""
    print("🔧 予約投稿設定完全除去XMLツール")
    print("=" * 60)
    
    # メインXML作成
    xml_filename = create_no_schedule_xml()
    
    if xml_filename:
        verify_no_schedule_xml(xml_filename)
        
        # 最小限テストXML作成
        test_filename = create_simple_test_xml()
        
        print(f"\n🎉 予約設定なしXML作成完了！")
        print(f"📄 メインXMLファイル: {xml_filename}")
        print(f"🧪 テストXMLファイル: {test_filename}")
        
        print(f"\n📋 この版の特徴:")
        print("   ✅ 予約投稿設定が完全に除去されている")
        print("   ✅ 全記事が過去時刻で公開済み状態")
        print("   ✅ WP-Cronに依存しない")
        print("   ✅ 即座にすべて公開される")
        
        print(f"\n📋 推奨テスト順序:")
        print(f"1. まず {test_filename} で動作確認")
        print(f"2. 問題なければ {xml_filename} をインポート")
        
        print(f"\n📋 WordPress インポート手順:")
        print("1. WordPress管理画面 → ツール → インポート → WordPress")
        print("2. XMLファイルをアップロード")
        print("3. 投稿者を 'aime' に設定")
        print("4. インポート実行")
        print("5. 投稿一覧で全記事が 'パブリッシュ済み' になっているか確認")
        
        print(f"\n⚠️ 重要:")
        print("- この版では予約投稿は一切行われません")
        print("- インポートと同時に全記事が公開されます")
        print("- スケジュール機能は使用されません")
        
    else:
        print("❌ XML作成に失敗しました")

if __name__ == '__main__':
    main()