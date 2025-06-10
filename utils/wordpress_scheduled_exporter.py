#!/usr/bin/env python3
"""
WordPress スケジュール投稿対応XMLエクスポーター
1時間ごとの自動公開とカバー画像対応
"""
import json
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from html import escape
import re
import requests
from typing import List, Dict, Any

from src.application.services import MountainArticleService
from src.infrastructure.repositories import RepositoryFactory
from config.settings import get_settings
from config.logging_config import get_logger


class WordPressScheduledExporter:
    """スケジュール投稿対応のWordPress XMLエクスポーター"""
    
    def __init__(self):
        self.settings = get_settings()
        self.service = MountainArticleService()
        self.mountain_repo = RepositoryFactory.get_mountain_repository()
        self.logger = get_logger("scheduled_exporter")
    
    def generate_scheduled_xml(self, articles_data: List[Dict[str, Any]], start_time: datetime = None, interval_hours: int = 1):
        """
        スケジュール投稿対応のXMLを生成
        
        Args:
            articles_data: 記事データのリスト
            start_time: 最初の公開時刻（デフォルト: 現在時刻の1時間後）
            interval_hours: 公開間隔（時間）
        """
        if start_time is None:
            # デフォルトは現在時刻の1時間後から開始
            start_time = datetime.now() + timedelta(hours=1)
        
        # ルート要素 - 正しいWordPress名前空間を使用
        rss = ET.Element('rss')
        rss.set('version', '2.0')
        rss.set('xmlns:excerpt', 'http://wordpress.org/export/1.2/excerpt/')
        rss.set('xmlns:content', 'http://purl.org/rss/1.0/modules/content/')
        rss.set('xmlns:wfw', 'http://wellformedweb.org/CommentAPI/')
        rss.set('xmlns:dc', 'http://purl.org/dc/elements/1.1/')
        rss.set('xmlns:wp', 'http://wordpress.org/export/1.2/')
        
        channel = ET.SubElement(rss, 'channel')
        
        # チャンネル情報
        ET.SubElement(channel, 'title').text = '低山旅行 - Scheduled Articles'
        ET.SubElement(channel, 'link').text = self.settings.WP_URL
        ET.SubElement(channel, 'description').text = 'Mountain Blog Generator - Scheduled Export'
        ET.SubElement(channel, 'pubDate').text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
        ET.SubElement(channel, 'language').text = 'ja'
        ET.SubElement(channel, '{http://wordpress.org/export/1.2/}wxr_version').text = '1.2'
        ET.SubElement(channel, 'generator').text = 'https://wordpress.org/?v=6.3'
        
        # 必要なサイト情報を追加
        ET.SubElement(channel, '{http://wordpress.org/export/1.2/}base_site_url').text = self.settings.WP_URL
        ET.SubElement(channel, '{http://wordpress.org/export/1.2/}base_blog_url').text = self.settings.WP_URL
        
        # 記事を追加
        for i, article in enumerate(articles_data):
            item = ET.SubElement(channel, 'item')
            
            # スケジュール時刻を計算
            scheduled_time = start_time + timedelta(hours=interval_hours * i)
            
            # 基本情報
            ET.SubElement(item, 'title').text = article['title']
            ET.SubElement(item, 'link').text = f"{self.settings.WP_URL}/?p={i+2000}"
            ET.SubElement(item, 'pubDate').text = scheduled_time.strftime('%a, %d %b %Y %H:%M:%S +0000')
            
            creator = ET.SubElement(item, '{http://purl.org/dc/elements/1.1/}creator')
            creator.text = 'aime'
            
            ET.SubElement(item, 'guid', isPermaLink='false').text = f"{self.settings.WP_URL}/?p={i+2000}"
            ET.SubElement(item, 'description').text = ''
            
            # コンテンツ（CDATAセクションとして）
            content = ET.SubElement(item, '{http://purl.org/rss/1.0/modules/content/}encoded')
            content.text = article['content']
            
            # 抜粋
            excerpt = ET.SubElement(item, '{http://wordpress.org/export/1.2/excerpt/}encoded')
            excerpt.text = article['excerpt']
            
            # WordPress固有の要素
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_id').text = str(i+2000)
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_date').text = scheduled_time.strftime('%Y-%m-%d %H:%M:%S')
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_date_gmt').text = scheduled_time.strftime('%Y-%m-%d %H:%M:%S')
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}comment_status').text = 'open'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}ping_status').text = 'open'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_name').text = self._create_slug(article['title'])
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}status').text = 'future'  # 予約投稿
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_parent').text = '0'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}menu_order').text = '0'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_type').text = 'post'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_password').text = ''
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}is_sticky').text = '0'
            
            # カテゴリとタグ
            category = ET.SubElement(item, 'category', domain='category', nicename='area')
            category.text = 'エリア別'
            
            # タグを追加
            for tag in article.get('tags', []):
                tag_elem = ET.SubElement(item, 'category', domain='post_tag', nicename=self._create_slug(tag))
                tag_elem.text = tag
            
            # カバー画像（アイキャッチ画像）の添付
            if article.get('featured_image_url'):
                self._add_featured_image(item, article['featured_image_url'], article['title'])
        
        # XMLを文字列に変換
        xml_str = ET.tostring(rss, encoding='unicode', method='xml')
        
        # 整形とCDATAセクションの追加
        xml_str = self._format_xml_with_cdata(xml_str)
        
        return xml_str
    
    def _add_featured_image(self, item, image_url, title):
        """アイキャッチ画像の情報を追加"""
        # WordPressのポストメタデータとして画像URLを追加
        postmeta = ET.SubElement(item, '{http://wordpress.org/export/1.2/}postmeta')
        ET.SubElement(postmeta, '{http://wordpress.org/export/1.2/}meta_key').text = '_thumbnail_url'
        ET.SubElement(postmeta, '{http://wordpress.org/export/1.2/}meta_value').text = image_url
        
        # 画像の代替テキスト
        postmeta_alt = ET.SubElement(item, '{http://wordpress.org/export/1.2/}postmeta')
        ET.SubElement(postmeta_alt, '{http://wordpress.org/export/1.2/}meta_key').text = '_thumbnail_alt'
        ET.SubElement(postmeta_alt, '{http://wordpress.org/export/1.2/}meta_value').text = f"{title}のアイキャッチ画像"
    
    def _create_slug(self, text):
        """URLスラッグを生成"""
        slug = re.sub(r'[^\w\s-]', '', text.lower())
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug[:50]
    
    def _format_xml_with_cdata(self, xml_str):
        """XMLを整形し、CDATAセクションを適切に追加"""
        xml_str = re.sub(
            r'<content:encoded>(.*?)</content:encoded>',
            lambda m: f'<content:encoded><![CDATA[{m.group(1)}]]></content:encoded>',
            xml_str,
            flags=re.DOTALL
        )
        
        xml_str = re.sub(
            r'<excerpt:encoded>(.*?)</excerpt:encoded>',
            lambda m: f'<excerpt:encoded><![CDATA[{m.group(1)}]]></excerpt:encoded>',
            xml_str,
            flags=re.DOTALL
        )
        
        xml_declaration = '<?xml version="1.0" encoding="UTF-8" ?>\n'
        
        return xml_declaration + xml_str
    
    def export_scheduled_articles(self, count=10, start_time=None, interval_hours=1):
        """
        スケジュール投稿用の記事を生成してXML出力
        
        Args:
            count: 生成する記事数
            start_time: 最初の公開時刻
            interval_hours: 公開間隔（時間）
        """
        print("⏰ WordPress スケジュール投稿XMLエクスポート")
        print("="*60)
        
        mountains = self.mountain_repo.get_all()[:count]
        
        print(f"📊 設定:")
        print(f"   記事数: {count}記事")
        print(f"   開始時刻: {start_time or '現在時刻の1時間後'}")
        print(f"   公開間隔: {interval_hours}時間ごと")
        
        # テーマリスト
        themes = [
            "初心者向け登山ガイド",
            "家族でハイキング",
            "秋の紅葉狩り",
            "絶景ハイキング",
            "パワースポット巡り",
            "日帰り登山プラン",
            "週末日帰りハイキング",
            "低山縦走コース",
            "季節の花を楽しむ登山",
            "温泉付き登山プラン"
        ]
        
        articles_data = []
        
        print("\n📝 記事生成中...")
        for i, mountain in enumerate(mountains):
            theme = themes[i % len(themes)]
            print(f"{i+1}. {mountain.name} - {theme}", end="")
            
            try:
                result = self.service.create_and_publish_article(
                    mountain_id=mountain.id,
                    theme=theme,
                    publish=False
                )
                
                if result.success:
                    # カバー画像URL（Unsplashのサンプル画像）
                    featured_image_url = None
                    if hasattr(result.article.content, 'featured_image') and result.article.content.featured_image:
                        featured_image_url = result.article.content.featured_image.url
                    
                    article_data = {
                        "title": result.article.content.title,
                        "content": result.article.content.content,
                        "excerpt": result.article.content.excerpt,
                        "tags": result.article.content.tags,
                        "featured_image_url": featured_image_url,
                        "mountain_name": mountain.name,
                        "theme": theme
                    }
                    articles_data.append(article_data)
                    print(f" ✅ ({len(result.article.content.content)}文字)")
                else:
                    print(f" ❌ 失敗: {result.error_message}")
                    
            except Exception as e:
                print(f" ❌ エラー: {e}")
        
        # スケジュール情報を表示
        if start_time is None:
            start_time = datetime.now() + timedelta(hours=1)
        
        print(f"\n📅 公開スケジュール:")
        for i in range(len(articles_data)):
            scheduled_time = start_time + timedelta(hours=interval_hours * i)
            print(f"   {i+1}. {scheduled_time.strftime('%Y-%m-%d %H:%M')} - {articles_data[i]['title'][:30]}...")
        
        # XML生成
        print(f"\n📄 XML生成中...")
        xml_content = self.generate_scheduled_xml(articles_data, start_time, interval_hours)
        
        # ファイル保存
        filename = f"wordpress_scheduled_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xml"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(xml_content)
        
        print(f"\n✅ XMLファイル作成完了: {filename}")
        print(f"   記事数: {len(articles_data)}記事")
        print(f"   ファイルサイズ: {len(xml_content) / 1024:.1f} KB")
        
        self._print_import_instructions()
        
        return filename, len(articles_data)
    
    def _print_import_instructions(self):
        """インポート手順を表示"""
        print("\n📋 WordPressへのインポート手順:")
        print("1. WordPress管理画面 → ツール → インポート → WordPress")
        print("2. XMLファイルをアップロード")
        print("3. 投稿者の割り当てを設定")
        print("4. 実行")
        print("\n⚠️  重要な注意事項:")
        print("- 記事は「予約投稿」として登録されます")
        print("- 指定時刻になると自動的に公開されます")
        print("- カバー画像は手動で設定が必要な場合があります")
        print("\n💡 カバー画像の設定:")
        print("- プラグイン「Featured Image from URL」を使用すると")
        print("  画像URLから自動でアイキャッチ画像を設定できます")


def main():
    """メイン処理"""
    exporter = WordPressScheduledExporter()
    
    print("⏰ WordPress スケジュール投稿エクスポーター\n")
    
    print("設定を入力してください:")
    
    # 記事数
    count_input = input("記事数 (デフォルト: 10): ").strip()
    count = int(count_input) if count_input else 10
    
    # 開始時刻
    print("\n開始時刻の設定:")
    print("1. 現在時刻の1時間後から（デフォルト）")
    print("2. 明日の朝9時から")
    print("3. カスタム設定")
    
    time_choice = input("選択 (1-3): ").strip() or '1'
    
    start_time = None
    if time_choice == '2':
        tomorrow = datetime.now() + timedelta(days=1)
        start_time = tomorrow.replace(hour=9, minute=0, second=0, microsecond=0)
    elif time_choice == '3':
        date_str = input("開始日時 (YYYY-MM-DD HH:MM): ")
        try:
            start_time = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
        except:
            print("無効な日時形式です。デフォルトを使用します。")
    
    # 公開間隔
    interval_input = input("\n公開間隔（時間） (デフォルト: 1): ").strip()
    interval_hours = int(interval_input) if interval_input else 1
    
    print("\n" + "="*60)
    
    # 実行
    filename, article_count = exporter.export_scheduled_articles(
        count=count,
        start_time=start_time,
        interval_hours=interval_hours
    )
    
    print("\n✅ 完了！")
    print(f"生成されたXMLファイルをWordPressにインポートしてください。")
    print(f"記事は設定したスケジュールに従って自動的に公開されます。")


if __name__ == '__main__':
    main()