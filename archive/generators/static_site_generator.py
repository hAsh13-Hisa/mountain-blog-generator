#!/usr/bin/env python3
"""
静的サイトジェネレーター
記事生成時に分類ページも自動更新
"""
import json
import os
from datetime import datetime
from pathlib import Path
from collections import defaultdict
import shutil

class StaticSiteGenerator:
    def __init__(self):
        self.base_dir = Path("static_site")
        self.articles_data = Path("data/articles_metadata.json")
        self.template_dir = Path("templates")
        
        # ディレクトリ構造作成
        self.create_directory_structure()
        
        # 記事メタデータ読み込み（なければ初期化）
        self.load_metadata()
    
    def create_directory_structure(self):
        """必要なディレクトリ構造を作成"""
        directories = [
            self.base_dir / "articles",
            self.base_dir / "regions",
            self.base_dir / "tags",
            self.base_dir / "difficulty",
            self.base_dir / "css",
            self.base_dir / "js",
            self.base_dir / "images"
        ]
        for dir in directories:
            dir.mkdir(parents=True, exist_ok=True)
    
    def load_metadata(self):
        """記事メタデータを読み込み"""
        if self.articles_data.exists():
            with open(self.articles_data, 'r', encoding='utf-8') as f:
                self.metadata = json.load(f)
        else:
            self.metadata = {"articles": [], "last_updated": None}
    
    def save_metadata(self):
        """記事メタデータを保存"""
        self.metadata["last_updated"] = datetime.now().isoformat()
        with open(self.articles_data, 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, ensure_ascii=False, indent=2)
    
    def add_article(self, article_data):
        """新規記事を追加して全ページを再生成"""
        # メタデータに追加
        article_meta = {
            "id": article_data["id"],
            "title": article_data["title"],
            "mountain_name": article_data["mountain_name"],
            "elevation": article_data["elevation"],
            "region": article_data["region"],
            "prefecture": article_data["prefecture"],
            "difficulty": article_data["difficulty"],
            "tags": article_data["keywords"],
            "date": datetime.now().isoformat(),
            "featured_image": article_data["featured_image_url"],
            "summary": article_data["meta_description"]
        }
        
        # 既存記事をチェック（重複防止）
        existing_ids = [a["id"] for a in self.metadata["articles"]]
        if article_meta["id"] not in existing_ids:
            self.metadata["articles"].insert(0, article_meta)  # 新着順
        
        # 個別記事ページ生成
        self.generate_article_page(article_data)
        
        # 全体ページ再生成
        self.regenerate_all_pages()
        
        # メタデータ保存
        self.save_metadata()
    
    def generate_article_page(self, article_data):
        """個別記事ページ生成"""
        template = self.get_article_template()
        
        # 商品HTML生成
        products_html = ""
        for product in article_data["affiliate_products"]:
            products_html += f"""
            <div class="product-card">
                <a href="{product['affiliateUrl']}" target="_blank" rel="noopener">
                    <img src="{product['mediumImageUrl']}" alt="{product['itemName']}">
                    <h4>{product['itemName']}</h4>
                </a>
            </div>
            """
        
        # テンプレート置換
        html = template.format(
            title=article_data["title"],
            mountain_name=article_data["mountain_name"],
            elevation=article_data["elevation"],
            region=article_data["region"],
            difficulty=article_data["difficulty"],
            date=datetime.now().strftime("%Y年%m月%d日"),
            featured_image=article_data["featured_image_url"],
            content=article_data["content"],
            products=products_html,
            tags=" ".join([f'<a href="/tags/{tag}.html" class="tag">#{tag}</a>' for tag in article_data["keywords"]])
        )
        
        # 保存
        filename = f"{article_data['id']}.html"
        with open(self.base_dir / "articles" / filename, 'w', encoding='utf-8') as f:
            f.write(html)
    
    def regenerate_all_pages(self):
        """すべての分類ページを再生成"""
        # 静的ファイルのコピー
        self.copy_static_files()
        
        # トップページ（新着順）
        self.generate_index_page()
        
        # 地域別ページ
        self.generate_region_pages()
        
        # タグ別ページ
        self.generate_tag_pages()
        
        # 難易度別ページ
        self.generate_difficulty_pages()
        
        # サイトマップ
        self.generate_sitemap()
    
    def copy_static_files(self):
        """静的ファイル（CSS、JS等）をコピー"""
        static_dir = Path("static")
        if not static_dir.exists():
            return
        
        # CSSファイル
        css_src = static_dir / "style.css"
        if css_src.exists():
            shutil.copy2(css_src, self.base_dir / "css" / "style.css")
        
        # その他の静的ファイルがあれば追加
    
    def generate_index_page(self):
        """トップページ（新着情報）生成"""
        template = self.get_index_template()
        
        # 新着記事（最新10件）
        recent_articles = self.metadata["articles"][:10]
        articles_html = self.generate_article_cards(recent_articles)
        
        # 統計情報
        stats = self.calculate_stats()
        
        html = template.format(
            total_articles=stats["total"],
            total_regions=len(stats["regions"]),
            last_updated=datetime.now().strftime("%Y年%m月%d日"),
            articles=articles_html
        )
        
        with open(self.base_dir / "index.html", 'w', encoding='utf-8') as f:
            f.write(html)
    
    def generate_region_pages(self):
        """地域別ページ生成"""
        # 地域別に記事を分類
        regions = defaultdict(list)
        for article in self.metadata["articles"]:
            regions[article["region"]].append(article)
        
        # 地域別インデックス
        region_index_html = self.get_region_index_template()
        regions_list = ""
        for region, articles in regions.items():
            regions_list += f"""
            <div class="region-card">
                <h3><a href="/regions/{region}.html">{region}</a></h3>
                <p>{len(articles)}件の山</p>
            </div>
            """
        
        with open(self.base_dir / "regions" / "index.html", 'w', encoding='utf-8') as f:
            f.write(region_index_html.format(regions=regions_list))
        
        # 各地域ページ
        region_template = self.get_region_template()
        for region, articles in regions.items():
            articles_html = self.generate_article_cards(articles)
            html = region_template.format(
                region=region,
                count=len(articles),
                articles=articles_html
            )
            with open(self.base_dir / "regions" / f"{region}.html", 'w', encoding='utf-8') as f:
                f.write(html)
    
    def generate_tag_pages(self):
        """タグ別ページ生成"""
        # タグ別に記事を分類
        tags = defaultdict(list)
        for article in self.metadata["articles"]:
            for tag in article["tags"]:
                tags[tag].append(article)
        
        # タグ一覧ページ
        tag_index_html = self.get_tag_index_template()
        tags_list = ""
        for tag, articles in sorted(tags.items(), key=lambda x: len(x[1]), reverse=True):
            tags_list += f"""
            <div class="tag-item">
                <a href="/tags/{tag}.html">{tag} ({len(articles)})</a>
            </div>
            """
        
        with open(self.base_dir / "tags" / "index.html", 'w', encoding='utf-8') as f:
            f.write(tag_index_html.format(tags=tags_list))
        
        # 各タグページ
        tag_template = self.get_tag_template()
        for tag, articles in tags.items():
            articles_html = self.generate_article_cards(articles)
            html = tag_template.format(
                tag=tag,
                count=len(articles),
                articles=articles_html
            )
            with open(self.base_dir / "tags" / f"{tag}.html", 'w', encoding='utf-8') as f:
                f.write(html)
    
    def generate_difficulty_pages(self):
        """難易度別ページ生成"""
        # 難易度別に分類
        difficulties = defaultdict(list)
        for article in self.metadata["articles"]:
            difficulties[article["difficulty"]].append(article)
        
        # 難易度別ページ
        for difficulty, articles in difficulties.items():
            template = self.get_difficulty_template()
            articles_html = self.generate_article_cards(articles)
            html = template.format(
                difficulty=difficulty,
                count=len(articles),
                articles=articles_html
            )
            filename = difficulty.replace("-", "_") + ".html"
            with open(self.base_dir / "difficulty" / filename, 'w', encoding='utf-8') as f:
                f.write(html)
    
    def generate_article_cards(self, articles):
        """記事カードHTMLを生成"""
        cards = ""
        for article in articles:
            cards += f"""
            <article class="article-card">
                <img src="{article['featured_image']}" alt="{article['title']}" loading="lazy">
                <div class="card-content">
                    <h3><a href="/articles/{article['id']}.html">{article['title']}</a></h3>
                    <div class="meta">
                        <span class="region">{article['region']}</span>
                        <span class="elevation">{article['elevation']}m</span>
                        <span class="difficulty">{article['difficulty']}</span>
                    </div>
                    <p class="summary">{article['summary']}</p>
                    <div class="tags">
                        {' '.join([f'<a href="/tags/{tag}.html" class="tag">#{tag}</a>' for tag in article['tags'][:3]])}
                    </div>
                </div>
            </article>
            """
        return cards
    
    def generate_sitemap(self):
        """サイトマップ生成"""
        sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
        sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        
        # トップページ
        sitemap += f"""
        <url>
            <loc>https://your-domain.com/</loc>
            <lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod>
            <priority>1.0</priority>
        </url>
        """
        
        # 記事ページ
        for article in self.metadata["articles"]:
            sitemap += f"""
        <url>
            <loc>https://your-domain.com/articles/{article['id']}.html</loc>
            <lastmod>{article['date'][:10]}</lastmod>
            <priority>0.8</priority>
        </url>
            """
        
        sitemap += '</urlset>'
        
        with open(self.base_dir / "sitemap.xml", 'w', encoding='utf-8') as f:
            f.write(sitemap)
    
    def calculate_stats(self):
        """統計情報を計算"""
        regions = set()
        tags = set()
        for article in self.metadata["articles"]:
            regions.add(article["region"])
            tags.update(article["tags"])
        
        return {
            "total": len(self.metadata["articles"]),
            "regions": regions,
            "tags": tags
        }
    
    # テンプレート取得メソッド
    def get_article_template(self):
        return """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="/css/style.css">
</head>
<body>
    <header>
        <h1><a href="/">日本の低山ガイド</a></h1>
        <nav>
            <a href="/">新着</a>
            <a href="/regions/">地域別</a>
            <a href="/tags/">タグ別</a>
            <a href="/difficulty/初級.html">初級</a>
            <a href="/difficulty/初級_中級.html">初級-中級</a>
        </nav>
    </header>
    
    <main>
        <article>
            <h1>{title}</h1>
            <div class="article-meta">
                <span>{mountain_name}</span>
                <span>{elevation}m</span>
                <span>{region}</span>
                <span>{difficulty}</span>
                <span>{date}</span>
            </div>
            <img src="{featured_image}" alt="{title}" class="featured-image">
            <div class="content">{content}</div>
            <div class="affiliate-section">
                <h2>おすすめ商品</h2>
                <div class="products">{products}</div>
            </div>
            <div class="tags">{tags}</div>
        </article>
    </main>
    
    <footer>
        <p>&copy; 2025 日本の低山ガイド</p>
    </footer>
</body>
</html>"""
    
    def get_index_template(self):
        return """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>日本の低山ガイド - 新着情報</title>
    <link rel="stylesheet" href="/css/style.css">
</head>
<body>
    <header>
        <h1>日本の低山ガイド</h1>
        <nav>
            <a href="/" class="active">新着</a>
            <a href="/regions/">地域別</a>
            <a href="/tags/">タグ別</a>
            <a href="/difficulty/初級.html">初級</a>
            <a href="/difficulty/初級_中級.html">初級-中級</a>
        </nav>
    </header>
    
    <main>
        <section class="hero">
            <h2>新着の山情報</h2>
            <p>全{total_articles}件 / {total_regions}地域 / 最終更新: {last_updated}</p>
        </section>
        
        <section class="articles">
            {articles}
        </section>
    </main>
    
    <footer>
        <p>&copy; 2025 日本の低山ガイド</p>
    </footer>
</body>
</html>"""
    
    def get_region_index_template(self):
        return """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>地域から探す - 日本の低山ガイド</title>
    <link rel="stylesheet" href="/css/style.css">
</head>
<body>
    <header>
        <h1><a href="/">日本の低山ガイド</a></h1>
        <nav>
            <a href="/">新着</a>
            <a href="/regions/" class="active">地域別</a>
            <a href="/tags/">タグ別</a>
        </nav>
    </header>
    
    <main>
        <h2>地域から探す</h2>
        <div class="region-grid">{regions}</div>
    </main>
    
    <footer>
        <p>&copy; 2025 日本の低山ガイド</p>
    </footer>
</body>
</html>"""
    
    def get_region_template(self):
        return """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>{region}の山 - 日本の低山ガイド</title>
    <link rel="stylesheet" href="/css/style.css">
</head>
<body>
    <header>
        <h1><a href="/">日本の低山ガイド</a></h1>
        <nav>
            <a href="/">新着</a>
            <a href="/regions/" class="active">地域別</a>
            <a href="/tags/">タグ別</a>
        </nav>
    </header>
    
    <main>
        <h2>{region}の山 ({count}件)</h2>
        <div class="articles">{articles}</div>
    </main>
    
    <footer>
        <p>&copy; 2025 日本の低山ガイド</p>
    </footer>
</body>
</html>"""
    
    def get_tag_index_template(self):
        return """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>タグ一覧 - 日本の低山ガイド</title>
    <link rel="stylesheet" href="/css/style.css">
</head>
<body>
    <header>
        <h1><a href="/">日本の低山ガイド</a></h1>
        <nav>
            <a href="/">新着</a>
            <a href="/regions/">地域別</a>
            <a href="/tags/" class="active">タグ別</a>
        </nav>
    </header>
    
    <main>
        <h2>タグから探す</h2>
        <div class="tag-cloud">{tags}</div>
    </main>
    
    <footer>
        <p>&copy; 2025 日本の低山ガイド</p>
    </footer>
</body>
</html>"""
    
    def get_tag_template(self):
        return """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>#{tag} - 日本の低山ガイド</title>
    <link rel="stylesheet" href="/css/style.css">
</head>
<body>
    <header>
        <h1><a href="/">日本の低山ガイド</a></h1>
        <nav>
            <a href="/">新着</a>
            <a href="/regions/">地域別</a>
            <a href="/tags/" class="active">タグ別</a>
        </nav>
    </header>
    
    <main>
        <h2>#{tag} ({count}件)</h2>
        <div class="articles">{articles}</div>
    </main>
    
    <footer>
        <p>&copy; 2025 日本の低山ガイド</p>
    </footer>
</body>
</html>"""
    
    def get_difficulty_template(self):
        return """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>{difficulty} - 日本の低山ガイド</title>
    <link rel="stylesheet" href="/css/style.css">
</head>
<body>
    <header>
        <h1><a href="/">日本の低山ガイド</a></h1>
        <nav>
            <a href="/">新着</a>
            <a href="/regions/">地域別</a>
            <a href="/tags/">タグ別</a>
            <a href="/difficulty/{difficulty}.html" class="active">{difficulty}</a>
        </nav>
    </header>
    
    <main>
        <h2>{difficulty}の山 ({count}件)</h2>
        <div class="articles">{articles}</div>
    </main>
    
    <footer>
        <p>&copy; 2025 日本の低山ガイド</p>
    </footer>
</body>
</html>"""


# 実行例
if __name__ == "__main__":
    generator = StaticSiteGenerator()
    
    # サンプル記事データ（実際は生成された記事データを使用）
    sample_article = {
        "id": "mt_maruyama_hokkaido",
        "title": "札幌市民に愛される円山（225m）- 都市近郊の原始林ハイキング",
        "mountain_name": "円山",
        "elevation": 225,
        "region": "北海道",
        "prefecture": "北海道",
        "difficulty": "初級",
        "keywords": ["札幌", "都市近郊", "原始林", "神宮", "野生動物"],
        "featured_image_url": "https://example.com/maruyama.jpg",
        "meta_description": "札幌市内から15分でアクセスできる円山。原始林と野生動物に出会える都市近郊の低山です。",
        "content": "<p>記事本文...</p>",
        "affiliate_products": []
    }
    
    # 記事追加（自動的に全ページ更新）
    generator.add_article(sample_article)