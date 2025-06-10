#!/usr/bin/env python3
"""
WordPress WXR形式の完全対応版
WordPressの標準WXRフォーマットに完全準拠
"""
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any

def generate_valid_wxr(articles_data: List[Dict[str, Any]], start_time: datetime = None, interval_hours: int = 1) -> str:
    """完全なWordPress WXR形式のXMLを生成"""
    
    if start_time is None:
        start_time = datetime.now() + timedelta(hours=1)
    
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
	<title>低山旅行 - Scheduled Articles</title>
	<link>https://teizan.abg.ooo</link>
	<description>Mountain Blog Generator - Scheduled Export</description>
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
    for i, article in enumerate(articles_data):
        scheduled_time = start_time + timedelta(hours=interval_hours * i)
        
        # 記事の内容をエスケープ
        title = escape_xml(article['title'])
        content = article['content']
        excerpt = article['excerpt']
        
        xml_content += f"""
	<item>
		<title>{title}</title>
		<link>https://teizan.abg.ooo/?p={i+2000}</link>
		<pubDate>{scheduled_time.strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>
		<dc:creator><![CDATA[aime]]></dc:creator>
		<guid isPermaLink="false">https://teizan.abg.ooo/?p={i+2000}</guid>
		<description></description>
		<content:encoded><![CDATA[{content}]]></content:encoded>
		<excerpt:encoded><![CDATA[{excerpt}]]></excerpt:encoded>
		<wp:post_id>{i+2000}</wp:post_id>
		<wp:post_date><![CDATA[{scheduled_time.strftime('%Y-%m-%d %H:%M:%S')}]]></wp:post_date>
		<wp:post_date_gmt><![CDATA[{scheduled_time.strftime('%Y-%m-%d %H:%M:%S')}]]></wp:post_date_gmt>
		<wp:comment_status><![CDATA[open]]></wp:comment_status>
		<wp:ping_status><![CDATA[open]]></wp:ping_status>
		<wp:post_name><![CDATA[{create_slug(article['title'])}]]></wp:post_name>
		<wp:status><![CDATA[future]]></wp:status>
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

        # アイキャッチ画像のメタデータ（複数のプラグイン対応）
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

def main():
    """テスト実行"""
    # 既存のJSONファイルを読み込み
    with open('bulk_articles_20250609_213833.json', 'r', encoding='utf-8') as f:
        articles_data = json.load(f)
    
    # カバー画像URLを追加（実際の山の画像）
    mountain_images = [
        "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&h=400&fit=crop",  # 円山
        "https://images.unsplash.com/photo-1464822759844-d150ad6ba46f?w=800&h=400&fit=crop",  # 岩木山
        "https://images.unsplash.com/photo-1469474968028-56623f02e42e?w=800&h=400&fit=crop"   # 岩手山
    ]
    
    for i, article in enumerate(articles_data):
        article['featured_image_url'] = mountain_images[i % len(mountain_images)]
    
    # スケジュール設定
    start_time = datetime.now() + timedelta(hours=1)
    
    print("🔧 完全なWordPress WXR形式でXML生成中...")
    xml_content = generate_valid_wxr(articles_data, start_time, 1)
    
    # ファイル保存
    filename = f"wordpress_wxr_fixed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xml"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(xml_content)
    
    print(f"✅ 修正されたWXRファイル作成: {filename}")
    print(f"   記事数: {len(articles_data)}記事")
    print(f"   投稿者: aime")
    print(f"   ファイルサイズ: {len(xml_content) / 1024:.1f} KB")
    
    print("\n📋 WordPressインポート手順:")
    print("1. WordPress管理画面 → ツール → インポート → WordPress")
    print("2. XMLファイルをアップロード")
    print("3. 投稿者の割り当て → aime")
    print("4. 実行")

if __name__ == '__main__':
    main()