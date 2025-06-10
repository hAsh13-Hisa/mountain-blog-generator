#!/usr/bin/env python3
"""
予約時間調整版XMLファイル作成
- 最初の記事: 予約なし（即座に公開）
- 2記事目以降: 10分間隔で予約投稿
"""
import json
from datetime import datetime, timedelta
from wordpress_wxr_fixed import generate_valid_wxr

def create_adjusted_schedule_xml():
    """調整されたスケジュールでXML作成"""
    print("🔧 予約時間調整版XML作成")
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
    
    # スケジュール設定
    now = datetime.now()
    print(f"📅 現在時刻: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    
    schedule_info = []
    for i, article in enumerate(articles_data):
        if i == 0:
            # 最初の記事は即座に公開
            article_time = now
            status = "publish"
            schedule_type = "即座に公開"
        else:
            # 2記事目以降は10分間隔で予約投稿
            article_time = now + timedelta(minutes=10 * i)
            status = "future"
            schedule_type = f"{10 * i}分後に予約投稿"
        
        schedule_info.append({
            'article_name': article.get('mountain_name', f'記事{i+1}'),
            'schedule_time': article_time,
            'status': status,
            'schedule_type': schedule_type
        })
    
    print(f"\n⏰ 投稿スケジュール:")
    for info in schedule_info:
        print(f"   {info['article_name']}: {info['schedule_time'].strftime('%Y-%m-%d %H:%M:%S')} ({info['schedule_type']})")
    
    # カスタムXML生成（最初の記事のステータスを変更）
    xml_content = generate_custom_wxr_with_mixed_status(articles_data, schedule_info)
    
    # ファイル保存
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    xml_filename = f"adjusted_schedule_articles_{timestamp}.xml"
    
    with open(xml_filename, 'w', encoding='utf-8') as f:
        f.write(xml_content)
    
    print(f"\n✅ 調整済みXMLファイル作成: {xml_filename}")
    print(f"   ファイルサイズ: {len(xml_content) / 1024:.1f} KB")
    
    return xml_filename

def generate_custom_wxr_with_mixed_status(articles_data, schedule_info):
    """即座公開と予約投稿が混在するカスタムWXR生成"""
    
    # WXR XMLヘッダー
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"
	xmlns:excerpt="http://wordpress.org/export/1.2/excerpt/"
	xmlns:content="http://purl.org/rss/1.0/modules/content/"
	xmlns:wfw="http://wellformedweb.org/CommentAPI/"
	xmlns:dc="http://purl.org/dc/elements/1.1/"
	xmlns:wp="http://wordpress.org/export/1.2/"
>

<channel>
	<title>低山旅行 - Mixed Schedule Articles</title>
	<link>https://teizan.abg.ooo</link>
	<description>Mountain Blog Generator - Adjusted Schedule Export</description>
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

    # 各記事を追加
    for i, (article, schedule) in enumerate(zip(articles_data, schedule_info)):
        scheduled_time = schedule['schedule_time']
        post_status = schedule['status']
        
        # 記事の内容をエスケープ
        title = escape_xml(article['title'])
        content = article['content']
        excerpt = article['excerpt']
        
        xml_content += f"""
	<item>
		<title>{title}</title>
		<link>https://teizan.abg.ooo/?p={i+3000}</link>
		<pubDate>{scheduled_time.strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>
		<dc:creator><![CDATA[aime]]></dc:creator>
		<guid isPermaLink="false">https://teizan.abg.ooo/?p={i+3000}</guid>
		<description></description>
		<content:encoded><![CDATA[{content}]]></content:encoded>
		<excerpt:encoded><![CDATA[{excerpt}]]></excerpt:encoded>
		<wp:post_id>{i+3000}</wp:post_id>
		<wp:post_date><![CDATA[{scheduled_time.strftime('%Y-%m-%d %H:%M:%S')}]]></wp:post_date>
		<wp:post_date_gmt><![CDATA[{scheduled_time.strftime('%Y-%m-%d %H:%M:%S')}]]></wp:post_date_gmt>
		<wp:comment_status><![CDATA[open]]></wp:comment_status>
		<wp:ping_status><![CDATA[open]]></wp:ping_status>
		<wp:post_name><![CDATA[{create_slug(article['title'])}]]></wp:post_name>
		<wp:status><![CDATA[{post_status}]]></wp:status>
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
			<wp:meta_key><![CDATA[_thumbnail_id]]></wp:meta_key>
			<wp:meta_value><![CDATA[0]]></wp:meta_value>
		</wp:postmeta>
		<wp:postmeta>
			<wp:meta_key><![CDATA[fifu_image_url]]></wp:meta_key>
			<wp:meta_value><![CDATA[{article['featured_image_url']}]]></wp:meta_value>
		</wp:postmeta>
		<wp:postmeta>
			<wp:meta_key><![CDATA[fifu_image_alt]]></wp:meta_key>
			<wp:meta_value><![CDATA[{title}のアイキャッチ画像]]></wp:meta_value>
		</wp:postmeta>
		<wp:postmeta>
			<wp:meta_key><![CDATA[_yoast_wpseo_opengraph-image]]></wp:meta_key>
			<wp:meta_value><![CDATA[{article['featured_image_url']}]]></wp:meta_value>
		</wp:postmeta>
		<wp:postmeta>
			<wp:meta_key><![CDATA[_yoast_wpseo_twitter-image]]></wp:meta_key>
			<wp:meta_value><![CDATA[{article['featured_image_url']}]]></wp:meta_value>
		</wp:postmeta>
		<wp:postmeta>
			<wp:meta_key><![CDATA[_wp_attachment_image_alt]]></wp:meta_key>
			<wp:meta_value><![CDATA[{title}のアイキャッチ画像]]></wp:meta_value>
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

def verify_schedule_xml(xml_filename):
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
        
        print(f"📊 投稿ステータス:")
        print(f"   即座公開 (publish): {publish_count}記事")
        print(f"   予約投稿 (future): {future_count}記事")
        
        # 投稿日時を抽出
        post_dates = re.findall(r'<wp:post_date><!\[CDATA\[(.*?)\]\]></wp:post_date>', content)
        
        print(f"\n📅 投稿日時:")
        for i, post_date in enumerate(post_dates, 1):
            status = "即座公開" if i == 1 else "予約投稿"
            print(f"   記事{i}: {post_date} ({status})")
        
        print(f"\n✅ XMLファイル検証完了")
        return True
        
    except Exception as e:
        print(f"❌ 検証エラー: {e}")
        return False

def main():
    """メイン処理"""
    print("🔧 予約時間調整版XML作成ツール")
    print("=" * 60)
    
    xml_filename = create_adjusted_schedule_xml()
    
    if xml_filename:
        verify_schedule_xml(xml_filename)
        
        print(f"\n🎉 調整完了！")
        print(f"📄 XMLファイル: {xml_filename}")
        
        print(f"\n📋 投稿設定:")
        print("   1記事目: 即座に公開")
        print("   2記事目: 10分後に予約投稿")
        print("   3記事目: 20分後に予約投稿")
        
        print(f"\n📋 WordPress インポート手順:")
        print("1. WordPress管理画面 → ツール → インポート → WordPress")
        print(f"2. {xml_filename} をアップロード")
        print("3. 投稿者を 'aime' に設定")
        print("4. インポート実行")
        print("5. 投稿一覧で確認:")
        print("   - 1記事目が公開されているか")
        print("   - 2,3記事目が予約投稿になっているか")
        
    else:
        print("❌ XML作成に失敗しました")

if __name__ == '__main__':
    main()