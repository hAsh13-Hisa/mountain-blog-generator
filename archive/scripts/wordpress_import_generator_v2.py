#!/usr/bin/env python3
"""
WordPress インポート用記事生成ツール（改良版）
設定ファイルから情報を読み取る
"""
import sys
import os
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any

# プロジェクトルートをパスに追加
sys.path.insert(0, os.path.abspath('.'))

from config.settings import get_settings
from simple_article_generator import SimpleArticleGenerator

def generate_valid_wxr_with_settings(articles_data: List[Dict[str, Any]], start_time: datetime = None, interval_hours: int = 1) -> str:
    """設定を反映したWordPress WXR形式のXMLを生成"""
    
    settings = get_settings()
    
    if start_time is None:
        start_time = datetime.now() + timedelta(hours=1)
    
    # URLを設定から取得
    wp_url = settings.WP_URL if hasattr(settings, 'WP_URL') else 'https://example.com'
    wp_username = settings.WP_USERNAME if hasattr(settings, 'WP_USERNAME') else 'admin'
    
    # WXR XMLヘッダー
    xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"
	xmlns:excerpt="http://wordpress.org/export/1.2/excerpt/"
	xmlns:content="http://purl.org/rss/1.0/modules/content/"
	xmlns:wfw="http://wellformedweb.org/CommentAPI/"
	xmlns:dc="http://purl.org/dc/elements/1.1/"
	xmlns:wp="http://wordpress.org/export/1.2/"
>

<channel>
	<title>山ブログ記事インポート</title>
	<link>{wp_url}</link>
	<description>Mountain Blog Generator - Import</description>
	<pubDate>{datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>
	<language>ja</language>
	<wp:wxr_version>1.2</wp:wxr_version>
	<wp:base_site_url>{wp_url}</wp:base_site_url>
	<wp:base_blog_url>{wp_url}</wp:base_blog_url>

	<wp:author>
		<wp:author_id>1</wp:author_id>
		<wp:author_login><![CDATA[{wp_username}]]></wp:author_login>
		<wp:author_email><![CDATA[{wp_username}@example.com]]></wp:author_email>
		<wp:author_display_name><![CDATA[{wp_username}]]></wp:author_display_name>
		<wp:author_first_name><![CDATA[]]></wp:author_first_name>
		<wp:author_last_name><![CDATA[]]></wp:author_last_name>
	</wp:author>

	<wp:category>
		<wp:term_id>1</wp:term_id>
		<wp:category_nicename><![CDATA[mountain]]></wp:category_nicename>
		<wp:category_parent><![CDATA[]]></wp:category_parent>
		<wp:cat_name><![CDATA[山の記事]]></wp:cat_name>
	</wp:category>

"""
    
    # 各記事を追加
    for i, article in enumerate(articles_data):
        # 投稿時刻を計算
        post_date = start_time + timedelta(hours=interval_hours * i)
        post_date_gmt = post_date.strftime('%Y-%m-%d %H:%M:%S')
        pub_date = post_date.strftime('%a, %d %b %Y %H:%M:%S +0000')
        
        # 投稿ステータス（即時公開）
        post_status = 'publish'
        
        # 記事IDを生成
        post_id = 1000 + i
        
        # タグの処理
        tags_xml = ""
        if 'tags' in article and article['tags']:
            for tag in article['tags']:
                tags_xml += f"""
		<category domain="post_tag" nicename="{tag.lower().replace(' ', '-')}"><![CDATA[{tag}]]></category>"""
        
        # アイキャッチ画像の情報（Featured Image from URLプラグイン対応）
        featured_image_xml = ""
        if article.get('featured_image_url'):
            featured_image_xml = f"""
		<wp:postmeta>
			<wp:meta_key>fifu_image_url</wp:meta_key>
			<wp:meta_value><![CDATA[{article['featured_image_url']}]]></wp:meta_value>
		</wp:postmeta>
		<wp:postmeta>
			<wp:meta_key>fifu_image_alt</wp:meta_key>
			<wp:meta_value><![CDATA[{article.get('featured_image_alt', '')}]]></wp:meta_value>
		</wp:postmeta>
		<wp:postmeta>
			<wp:meta_key>_thumbnail_id</wp:meta_key>
			<wp:meta_value><![CDATA[fifu]]></wp:meta_value>
		</wp:postmeta>"""
        
        xml_content += f"""
	<item>
		<title>{article['title']}</title>
		<link>{wp_url}/?p={post_id}</link>
		<pubDate>{pub_date}</pubDate>
		<dc:creator><![CDATA[{wp_username}]]></dc:creator>
		<guid isPermaLink="false">{wp_url}/?p={post_id}</guid>
		<description></description>
		<content:encoded><![CDATA[{article['content']}]]></content:encoded>
		<excerpt:encoded><![CDATA[{article.get('excerpt', '')}]]></excerpt:encoded>
		<wp:post_id>{post_id}</wp:post_id>
		<wp:post_date>{post_date_gmt}</wp:post_date>
		<wp:post_date_gmt>{post_date_gmt}</wp:post_date_gmt>
		<wp:comment_status>open</wp:comment_status>
		<wp:ping_status>open</wp:ping_status>
		<wp:post_name>{article['mountain_name'].lower().replace(' ', '-')}-{post_date.strftime('%Y%m%d')}</wp:post_name>
		<wp:status>{post_status}</wp:status>
		<wp:post_parent>0</wp:post_parent>
		<wp:menu_order>0</wp:menu_order>
		<wp:post_type>post</wp:post_type>
		<wp:post_password></wp:post_password>
		<wp:is_sticky>0</wp:is_sticky>
		<category domain="category" nicename="mountain"><![CDATA[山の記事]]></category>{tags_xml}{featured_image_xml}
	</item>
"""
    
    xml_content += """
</channel>
</rss>"""
    
    return xml_content

class WordPressImportGenerator:
    """WordPressインポート用ジェネレーター（改良版）"""
    
    def __init__(self):
        self.generator = SimpleArticleGenerator()
        self.settings = get_settings()
    
    def check_settings(self):
        """設定の確認"""
        print("\n📋 現在の設定:")
        print(f"   WordPress URL: {self.settings.WP_URL if hasattr(self.settings, 'WP_URL') else '未設定'}")
        print(f"   WordPress ユーザー: {self.settings.WP_USERNAME if hasattr(self.settings, 'WP_USERNAME') else '未設定'}")
        print(f"   楽天APP ID: {'設定済み' if hasattr(self.settings, 'RAKUTEN_APP_ID') and self.settings.RAKUTEN_APP_ID else '未設定'}")
        print()
    
    def generate_import_file(self, mountain_ids: list, output_filename: str = None):
        """複数の山の記事を生成してWXR形式で出力"""
        
        if not output_filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_filename = f"wordpress_import_{timestamp}.xml"
        
        print(f"🔧 WordPress インポートファイル生成開始")
        self.check_settings()
        print(f"📋 対象の山: {len(mountain_ids)}件")
        print("=" * 60)
        
        articles_data = []
        
        for i, mountain_id in enumerate(mountain_ids, 1):
            print(f"\n[{i}/{len(mountain_ids)}] {mountain_id}")
            try:
                # 記事を生成
                article = self.generator.generate_single_article(mountain_id)
                if article:
                    articles_data.append(article)
                    print(f"✅ 生成成功")
                else:
                    print(f"❌ 生成失敗")
            except Exception as e:
                print(f"❌ エラー: {e}")
        
        if not articles_data:
            print("\n❌ 記事が生成されませんでした")
            return None
        
        # WXR形式のXMLを生成（設定を反映）
        print(f"\n📝 WXR形式XMLファイル作成中...")
        xml_content = generate_valid_wxr_with_settings(articles_data)
        
        # ファイルに保存
        try:
            with open(output_filename, 'w', encoding='utf-8') as f:
                f.write(xml_content)
            
            print(f"✅ インポートファイル作成完了: {output_filename}")
            print(f"\n📌 WordPressへのインポート方法:")
            print("1. WordPress管理画面にログイン")
            print("2. ツール → インポート → WordPress を選択")
            print("3. 生成されたXMLファイルをアップロード")
            print("4. 記事の投稿者を選択してインポート実行")
            
            return output_filename
            
        except Exception as e:
            print(f"❌ ファイル保存エラー: {e}")
            return None

def main():
    """メイン処理"""
    print("🔧 WordPress インポートファイル生成ツール（改良版）")
    print("=" * 60)
    
    generator = WordPressImportGenerator()
    
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python wordpress_import_generator_v2.py <mountain_id1> <mountain_id2> ...")
        print("\n例:")
        print("  python wordpress_import_generator_v2.py mt_takao mt_fuji_shizuoka")
        return
    
    mountain_ids = sys.argv[1:]
    generator.generate_import_file(mountain_ids)

if __name__ == '__main__':
    main()