#!/usr/bin/env python3
"""
静的サイト生成スクリプト
WordPress不要で記事を生成・公開
"""
import json
import os
from datetime import datetime
from pathlib import Path
import frontmatter
import markdown
from src.application.services import MountainArticleService
from src.infrastructure.repositories import MountainRepository

class StaticSiteGenerator:
    def __init__(self):
        self.content_dir = Path("content/posts")
        self.data_dir = Path("src/_data")
        self.output_dir = Path("dist")
        
        # ディレクトリ作成
        self.content_dir.mkdir(parents=True, exist_ok=True)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # サービス初期化
        self.article_service = MountainArticleService()
        self.mountain_repo = MountainRepository()
    
    def generate_article_markdown(self, mountain_id):
        """記事をMarkdown形式で生成"""
        # 記事生成
        article = self.article_service.generate_article(mountain_id)
        
        # Frontmatter付きMarkdown作成
        post = frontmatter.Post(article['content'])
        post['title'] = article['title']
        post['date'] = datetime.now().isoformat()
        post['mountain'] = article['mountain_name']
        post['elevation'] = article['elevation']
        post['keywords'] = article['keywords']
        post['description'] = article['meta_description']
        post['featured_image'] = article['featured_image_url']
        post['affiliate_products'] = article['affiliate_products']
        
        # ファイル名生成
        filename = f"{datetime.now().strftime('%Y-%m-%d')}-{mountain_id}.md"
        filepath = self.content_dir / filename
        
        # 保存
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(frontmatter.dumps(post))
        
        return filepath
    
    def generate_all_articles(self):
        """全山の記事を生成"""
        mountains = self.mountain_repo.get_all_mountains()
        generated_files = []
        
        for mountain in mountains[:5]:  # まず5記事でテスト
            print(f"Generating article for {mountain['name']}...")
            filepath = self.generate_article_markdown(mountain['id'])
            generated_files.append(filepath)
        
        return generated_files
    
    def generate_site_data(self):
        """サイトデータJSON生成"""
        mountains = self.mountain_repo.get_all_mountains()
        
        # 山データ
        with open(self.data_dir / "mountains.json", 'w', encoding='utf-8') as f:
            json.dump(mountains, f, ensure_ascii=False, indent=2)
        
        # サイト設定
        site_config = {
            "title": "日本の低山ガイド",
            "description": "標高400m以下の登山道整備済み低山ガイド",
            "url": "https://lowmountains.jp",
            "author": "低山ガイド編集部"
        }
        
        with open(self.data_dir / "site.json", 'w', encoding='utf-8') as f:
            json.dump(site_config, f, ensure_ascii=False, indent=2)
    
    def build_static_site(self):
        """静的サイトビルド"""
        print("Building static site...")
        
        # 1. 記事生成
        self.generate_all_articles()
        
        # 2. サイトデータ生成
        self.generate_site_data()
        
        # 3. 11tyビルド実行
        os.system("npx @11ty/eleventy")
        
        print("Static site built successfully!")

if __name__ == "__main__":
    generator = StaticSiteGenerator()
    generator.build_static_site()