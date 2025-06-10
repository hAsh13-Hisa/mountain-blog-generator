#!/usr/bin/env python3
"""
WordPress XML形式での記事エクスポート
最も確実なWordPress投稿方法
"""
import json
import xml.etree.ElementTree as ET
from datetime import datetime
from html import escape
import re

from src.application.services import MountainArticleService
from src.infrastructure.repositories import RepositoryFactory
from config.settings import get_settings


class WordPressXMLExporter:
    """WordPress XML形式でのエクスポート"""
    
    def __init__(self):
        self.settings = get_settings()
        self.service = MountainArticleService()
        self.mountain_repo = RepositoryFactory.get_mountain_repository()
    
    def generate_wordpress_xml(self, articles_data):
        """WordPress形式のXMLを生成"""
        
        # ルート要素
        rss = ET.Element('rss', version='2.0')
        rss.set('xmlns:excerpt', 'http://wordpress.org/export/1.2/excerpt/')
        rss.set('xmlns:content', 'http://purl.org/rss/1.0/modules/content/')
        rss.set('xmlns:wfw', 'http://wellformedweb.org/CommentAPI/')
        rss.set('xmlns:dc', 'http://purl.org/dc/elements/1.1/')
        rss.set('xmlns:wp', 'http://wordpress.org/export/1.2/')
        
        channel = ET.SubElement(rss, 'channel')
        
        # チャンネル情報
        ET.SubElement(channel, 'title').text = '低山旅行 - Mountain Blog Articles'
        ET.SubElement(channel, 'link').text = self.settings.WP_URL
        ET.SubElement(channel, 'description').text = 'Mountain Blog Generator Export'
        ET.SubElement(channel, 'language').text = 'ja'
        ET.SubElement(channel, '{http://wordpress.org/export/1.2/}wxr_version').text = '1.2'
        ET.SubElement(channel, 'generator').text = 'Mountain Blog Generator'
        
        # 記事を追加
        for i, article in enumerate(articles_data):
            item = ET.SubElement(channel, 'item')
            
            # 基本情報
            ET.SubElement(item, 'title').text = article['title']
            ET.SubElement(item, 'link').text = f"{self.settings.WP_URL}/?p={i+1000}"
            ET.SubElement(item, 'pubDate').text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
            
            creator = ET.SubElement(item, '{http://purl.org/dc/elements/1.1/}creator')
            creator.text = 'admin'
            
            ET.SubElement(item, 'description').text = ''
            
            # コンテンツ（CDATAセクションとして）
            content = ET.SubElement(item, '{http://purl.org/rss/1.0/modules/content/}encoded')
            content.text = article['content']
            
            # 抜粋
            excerpt = ET.SubElement(item, '{http://wordpress.org/export/1.2/excerpt/}encoded')
            excerpt.text = article['excerpt']
            
            # WordPress固有の要素
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_date').text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_type').text = 'post'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}status').text = 'draft'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_name').text = self._create_slug(article['title'])
            
            # カテゴリとタグ
            category = ET.SubElement(item, 'category', domain='category', nicename='area')
            category.text = 'エリア別'
            
            # タグを追加
            for tag in article.get('tags', []):
                tag_elem = ET.SubElement(item, 'category', domain='post_tag', nicename=self._create_slug(tag))
                tag_elem.text = tag
        
        # XMLを文字列に変換
        xml_str = ET.tostring(rss, encoding='unicode', method='xml')
        
        # 整形とCDATAセクションの追加
        xml_str = self._format_xml_with_cdata(xml_str)
        
        return xml_str
    
    def _create_slug(self, text):
        """URLスラッグを生成"""
        # 日本語文字を削除し、英数字とハイフンのみにする
        slug = re.sub(r'[^\w\s-]', '', text.lower())
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug[:50]  # 長さ制限
    
    def _format_xml_with_cdata(self, xml_str):
        """XMLを整形し、CDATAセクションを適切に追加"""
        # content:encodedとexcerpt:encodedの内容をCDATAで囲む
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
        
        # XML宣言を追加
        xml_declaration = '<?xml version="1.0" encoding="UTF-8" ?>\n'
        
        return xml_declaration + xml_str
    
    def export_all_articles(self, limit=None):
        """すべての山の記事を生成してXML出力"""
        print("🏔️ WordPress XML形式での記事エクスポート")
        print("="*60)
        
        mountains = self.mountain_repo.get_all()
        if limit:
            mountains = mountains[:limit]
        
        print(f"📊 対象山数: {len(mountains)}山")
        
        # テーマリスト
        themes = [
            "初心者向け登山ガイド",
            "家族でハイキング",
            "秋の紅葉狩り",
            "絶景ハイキング",
            "パワースポット巡り",
            "日帰り登山プラン"
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
                    article_data = {
                        "title": result.article.content.title,
                        "content": result.article.content.content,
                        "excerpt": result.article.content.excerpt,
                        "tags": result.article.content.tags,
                        "mountain_name": mountain.name,
                        "theme": theme
                    }
                    articles_data.append(article_data)
                    print(f" ✅ ({len(result.article.content.content)}文字)")
                else:
                    print(f" ❌ 失敗: {result.error_message}")
                    
            except Exception as e:
                print(f" ❌ エラー: {e}")
        
        # XML生成
        print(f"\n📄 XML生成中...")
        xml_content = self.generate_wordpress_xml(articles_data)
        
        # ファイル保存
        filename = f"wordpress_import_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xml"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(xml_content)
        
        print(f"\n✅ XMLファイル作成完了: {filename}")
        print(f"   記事数: {len(articles_data)}記事")
        print(f"   ファイルサイズ: {len(xml_content) / 1024:.1f} KB")
        
        print("\n📋 WordPressへのインポート手順:")
        print("1. WordPress管理画面にログイン")
        print("2. ツール → インポート → WordPress")
        print("3. 「インポーターの実行」をクリック")
        print("4. XMLファイルを選択してアップロード")
        print("5. 投稿者の割り当てを設定")
        print("6. 「添付ファイルをダウンロードしてインポートする」のチェックを外す")
        print("7. 実行")
        
        return filename, len(articles_data)


def main():
    """メイン処理"""
    exporter = WordPressXMLExporter()
    
    print("🚀 WordPress XML エクスポーター\n")
    
    # 既存のJSONファイルがあれば使用
    import glob
    json_files = glob.glob("bulk_articles_*.json")
    
    if json_files:
        # 最新のJSONファイルを使用
        latest_json = max(json_files)
        print(f"📂 既存のJSONファイルを使用: {latest_json}")
        
        with open(latest_json, 'r', encoding='utf-8') as f:
            articles_data = json.load(f)
        
        xml_content = exporter.generate_wordpress_xml(articles_data)
        
        filename = f"wordpress_import_from_json_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xml"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(xml_content)
        
        print(f"✅ XMLファイル作成: {filename}")
        print(f"   記事数: {len(articles_data)}記事")
    else:
        # 新規生成
        print("新規記事生成モード")
        print("生成する記事数を選択してください:")
        print("1. テスト用（3記事）")
        print("2. 少量（5記事）")
        print("3. 中量（10記事）")
        print("4. 全量（20記事）")
        
        choice = input("\n選択 (1-4): ").strip()
        
        limits = {'1': 3, '2': 5, '3': 10, '4': None}
        limit = limits.get(choice, 3)
        
        filename, count = exporter.export_all_articles(limit=limit)
        
    print("\n✅ 完了！")
    print("WordPressの管理画面からXMLファイルをインポートしてください。")


if __name__ == '__main__':
    main()