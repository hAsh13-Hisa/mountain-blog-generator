#!/usr/bin/env python3
"""
アフィリエイト収益最大化対応の静的サイトジェネレーター
Template Party桜ピンクテンプレート + 低山アフィリエイト特化版
"""
import json
import os
import re
from datetime import datetime
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

class AffiliateStaticGeneratorNew:
    def __init__(self):
        self.output_dir = Path("static_site_new")
        self.templates_dir = Path("templates_new")
        self.static_dir = Path("static_new")
        
        # Jinja2環境を設定
        self.env = Environment(
            loader=FileSystemLoader(str(self.templates_dir)),
            autoescape=select_autoescape(['html', 'xml'])
        )
        
        # カスタムフィルタを追加
        self.env.filters['format_price'] = self.format_price
        
        self.load_data()
        self.load_affiliate_data()
    
    def load_data(self):
        """データファイルを読み込み"""
        try:
            with open('data/mountains_japan_expanded.json', 'r', encoding='utf-8') as f:
                self.mountains_data = json.load(f)
            
            with open('data/article_metadata.json', 'r', encoding='utf-8') as f:
                self.article_metadata = json.load(f)
        except FileNotFoundError as e:
            print(f"データファイルが見つかりません: {e}")
            self.mountains_data = {"mountains": []}
            self.article_metadata = {}
    
    def load_affiliate_data(self):
        """アフィリエイト商品データを読み込み（仮データ）"""
        self.equipment_data = {
            "backpacks": [
                {
                    "id": "bp001",
                    "name": "初心者向けザック 30L",
                    "brand": "アウトドアブランドA",
                    "price": 12800,
                    "sale_price": 8980,
                    "discount_percent": 30,
                    "description": "日帰りハイキングに最適なサイズ。軽量で背負いやすく、初心者でも疲れにくい設計。",
                    "features": ["軽量", "通気性", "初心者向け", "日帰り用"],
                    "rating": 4.5,
                    "affiliate_url": "https://example.com/affiliate/bp001",
                    "image": "/static_new/images/equipment/backpack.jpg",
                    "badge": "人気No.1",
                    "pros": ["軽量で疲れにくい", "通気性が良い", "価格が手頃"],
                    "cons": ["大容量ではない", "長期縦走には不向き"],
                    "shipping_free": True,
                    "cta_text": "詳細を見る"
                }
            ],
            "shoes": [
                {
                    "id": "sh001",
                    "name": "トレッキングシューズ",
                    "brand": "登山靴メーカーB",
                    "price": 12800,
                    "description": "低山に最適なミドルカット。グリップ力抜群で安全性と歩きやすさを両立。",
                    "features": ["ミドルカット", "グリップ力", "初心者向け"],
                    "rating": 4.3,
                    "affiliate_url": "https://example.com/affiliate/sh001",
                    "image": "/static_new/images/equipment/shoes.jpg",
                    "badge": "おすすめ"
                }
            ],
            "jackets": [
                {
                    "id": "jk001",
                    "name": "レインジャケット",
                    "brand": "アウトドアウェアC",
                    "price": 6480,
                    "description": "突然の雨や風から身を守る必需品。軽量でコンパクトに収納可能。",
                    "features": ["防水", "軽量", "コンパクト", "必需品"],
                    "rating": 4.7,
                    "affiliate_url": "https://example.com/affiliate/jk001",
                    "image": "/static_new/images/equipment/jacket.jpg",
                    "badge": "必需品"
                }
            ]
        }
        
        # 装備セットデータ
        self.equipment_sets = {
            "takao": {
                "id": "set_takao",
                "title": "高尾山完全装備セット",
                "description": "都心からアクセス抜群の高尾山に最適な軽装備セット",
                "mountain_id": "takao",
                "difficulty": "beginner",
                "difficulty_text": "初心者向け",
                "season": "通年",
                "target_user": "初心者・ファミリー",
                "total_price": 25000,
                "sale_total": 18800,
                "categories": [
                    {
                        "name": "ザック・バッグ",
                        "icon": "🎒",
                        "items": [self.equipment_data["backpacks"][0]]
                    }
                ],
                "expert_comment": "高尾山は登山初心者に最適な山です。このセットがあれば安全に楽しめます。",
                "related_mountains": [
                    {"name": "高尾山", "slug": "takao", "prefecture": "東京都"}
                ]
            }
        }
    
    def create_directories(self):
        """出力ディレクトリを作成"""
        directories = [
            self.output_dir,
            self.output_dir / "mountains",
            self.output_dir / "equipment",
            self.output_dir / "regions",
            self.output_dir / "beginner",
            self.output_dir / "ranking",
            self.output_dir / "static_new",
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
        
        print(f"出力ディレクトリを作成しました: {self.output_dir}")
    
    def copy_static_files(self):
        """静的ファイルをコピー"""
        import shutil
        
        if self.static_dir.exists():
            # static_newディレクトリ全体をコピー
            if (self.output_dir / "static_new").exists():
                shutil.rmtree(self.output_dir / "static_new")
            shutil.copytree(self.static_dir, self.output_dir / "static_new")
            print("静的ファイルをコピーしました")
        else:
            print(f"警告: 静的ファイルディレクトリが見つかりません: {self.static_dir}")
    
    def generate_index_page(self):
        """トップページを生成"""
        template = self.env.get_template('index.html')
        
        # おすすめ装備を選出
        featured_equipment = [
            self.equipment_data["backpacks"][0],
            self.equipment_data["shoes"][0],
            self.equipment_data["jackets"][0]
        ]
        
        # 人気の山を選出（仮データ）
        popular_mountains = self.mountains_data.get("mountains", [])[:3]
        
        content = template.render(
            featured_equipment=featured_equipment,
            popular_mountains=popular_mountains,
            equipment_sets=self.equipment_sets
        )
        
        output_file = self.output_dir / "index.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"トップページを生成しました: {output_file}")
    
    def generate_mountain_pages(self):
        """山の詳細ページを生成"""
        if not self.mountains_data or "mountains" not in self.mountains_data:
            print("山データが見つかりません")
            return
        
        for mountain in self.mountains_data["mountains"]:
            self.generate_mountain_detail_page(mountain)
    
    def generate_mountain_detail_page(self, mountain):
        """個別山詳細ページを生成"""
        mountain_name = mountain.get("name", "名称不明")
        prefecture = mountain.get("prefecture", "")
        slug = self.create_slug(mountain_name)
        
        # 山に適した装備を推奨（簡易ロジック）
        elevation = mountain.get("elevation", 0)
        if elevation < 200:
            recommended_set = "軽装備セット"
            equipment_items = [self.equipment_data["backpacks"][0]]
        else:
            recommended_set = "本格装備セット"
            equipment_items = list(self.equipment_data["backpacks"]) + list(self.equipment_data["shoes"])
        
        # 山詳細ページテンプレート（簡易版）
        content = self.create_mountain_detail_html(
            mountain, recommended_set, equipment_items
        )
        
        # ディレクトリ作成
        mountain_dir = self.output_dir / "mountains" / slug
        mountain_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = mountain_dir / "index.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"山詳細ページを生成: {mountain_name} -> {output_file}")
    
    def create_mountain_detail_html(self, mountain, recommended_set, equipment_items):
        """山詳細ページのHTML生成（簡易版）"""
        mountain_name = mountain.get("name", "名称不明")
        prefecture = mountain.get("prefecture", "")
        elevation = mountain.get("elevation", 0)
        description = mountain.get("description", "")
        
        # 装備セクション
        equipment_html = ""
        for item in equipment_items:
            equipment_html += f"""
            <div class="equipment-item">
                <h4>{item['name']}</h4>
                <p>{item['description']}</p>
                <div class="price">¥{item.get('sale_price', item['price']):,}</div>
                <a href="{item['affiliate_url']}" class="cta-button primary" target="_blank" rel="nofollow">詳細を見る</a>
            </div>
            """
        
        return f"""
        <!DOCTYPE html>
        <html lang="ja">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{mountain_name}（{prefecture}）- 登山ガイド | 低山マスター</title>
            <meta name="description" content="{mountain_name}の登山ガイド。標高{elevation}m、{prefecture}の低山。初心者向けコース情報と必要装備を詳しく解説。">
            <link rel="stylesheet" href="/static_new/css/mountain_affiliate_theme.css">
            <link rel="stylesheet" href="/static_new/css/components.css">
            <link rel="stylesheet" href="/static_new/css/affiliate.css">
        </head>
        <body>
            <header role="banner" class="site-header">
                <div class="container">
                    <div class="header-content">
                        <div class="logo">
                            <a href="/">
                                <span class="logo-icon">🏔️</span>
                                <span class="logo-text">低山マスター</span>
                            </a>
                        </div>
                        <nav class="main-nav">
                            <ul class="nav-menu">
                                <li><a href="/">ホーム</a></li>
                                <li><a href="/mountains/">山一覧</a></li>
                                <li><a href="/equipment/" class="cta-nav">装備レビュー</a></li>
                                <li><a href="/ranking/" class="cta-nav">ランキング</a></li>
                                <li><a href="/beginner/">初心者ガイド</a></li>
                                <li><a href="/regions/">地域別</a></li>
                            </ul>
                        </nav>
                    </div>
                </div>
            </header>
            
            <main class="main-content">
                <article class="mountain-article">
                    <header class="article-header">
                        <div class="container">
                            <h1>{mountain_name}</h1>
                            <div class="mountain-meta">
                                <span>📍 {prefecture}</span>
                                <span>⛰️ 標高{elevation}m</span>
                                <span>👨‍👩‍👧‍👦 初心者・ファミリー向け</span>
                            </div>
                        </div>
                    </header>
                    
                    <div class="container">
                        <section class="mountain-info">
                            <h2>山の概要</h2>
                            <p>{description}</p>
                        </section>
                        
                        <section class="recommended-equipment">
                            <h2>🎒 推奨装備: {recommended_set}</h2>
                            <div class="equipment-grid">
                                {equipment_html}
                            </div>
                        </section>
                        
                        <section class="affiliate-notice">
                            <p><small>※当ページではアフィリエイト広告を利用しています</small></p>
                        </section>
                    </div>
                </article>
            </main>
            
            <footer class="site-footer">
                <div class="container">
                    <p>&copy; 2025 低山マスター. All rights reserved.</p>
                </div>
            </footer>
        </body>
        </html>
        """
    
    def format_price(self, price):
        """価格をフォーマット（カンマ区切り）"""
        if price is None:
            return "0"
        return f"{price:,}"
    
    def create_slug(self, text):
        """URLスラッグを作成"""
        # 日本語を含む文字列から安全なURLスラッグを作成
        slug = re.sub(r'[^\w\s-]', '', text.lower())
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug.strip('-')
    
    def generate_equipment_pages(self):
        """装備関連ページを生成"""
        # 装備カテゴリページ
        equipment_dir = self.output_dir / "equipment"
        equipment_dir.mkdir(parents=True, exist_ok=True)
        
        # 装備一覧ページ（簡易版）
        equipment_list_html = self.create_equipment_list_html()
        with open(equipment_dir / "index.html", 'w', encoding='utf-8') as f:
            f.write(equipment_list_html)
        
        print("装備ページを生成しました")
    
    def create_equipment_list_html(self):
        """装備一覧ページHTML"""
        all_equipment = []
        for category in self.equipment_data.values():
            all_equipment.extend(category)
        
        equipment_cards = ""
        for item in all_equipment:
            equipment_cards += f"""
            <div class="equipment-card">
                <div class="card-image">
                    <img src="{item.get('image', '/static_new/images/equipment/default.jpg')}" alt="{item['name']}" loading="lazy">
                    {f'<div class="card-badge">{item["badge"]}</div>' if item.get('badge') else ''}
                </div>
                <div class="card-content">
                    <h3>{item['name']}</h3>
                    <p class="card-description">{item['description']}</p>
                    <div class="card-price">
                        {f'<span class="price-current">¥{item["sale_price"]:,}</span>' if item.get('sale_price') else ''}
                        <span class="price-current">¥{item['price']:,}</span>
                    </div>
                    <a href="{item['affiliate_url']}" class="cta-button primary" target="_blank" rel="nofollow">詳細を見る</a>
                </div>
            </div>
            """
        
        return f"""
        <!DOCTYPE html>
        <html lang="ja">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>登山装備一覧 | 低山マスター</title>
            <meta name="description" content="初心者向け登山装備の完全ガイド。専門家が厳選したおすすめ商品をご紹介。">
            <link rel="stylesheet" href="/static_new/css/mountain_affiliate_theme.css">
            <link rel="stylesheet" href="/static_new/css/components.css">
            <link rel="stylesheet" href="/static_new/css/affiliate.css">
        </head>
        <body>
            <header role="banner" class="site-header">
                <div class="container">
                    <div class="header-content">
                        <div class="logo">
                            <a href="/">
                                <span class="logo-icon">🏔️</span>
                                <span class="logo-text">低山マスター</span>
                            </a>
                        </div>
                        <nav class="main-nav">
                            <ul class="nav-menu">
                                <li><a href="/">ホーム</a></li>
                                <li><a href="/mountains/">山一覧</a></li>
                                <li><a href="/equipment/" class="cta-nav">装備レビュー</a></li>
                                <li><a href="/ranking/" class="cta-nav">ランキング</a></li>
                                <li><a href="/beginner/">初心者ガイド</a></li>
                                <li><a href="/regions/">地域別</a></li>
                            </ul>
                        </nav>
                    </div>
                </div>
            </header>
            
            <main class="main-content">
                <section class="equipment-showcase">
                    <div class="container">
                        <h1 class="section-title">
                            <span class="section-icon">🎒</span>
                            登山装備一覧
                        </h1>
                        <p class="section-subtitle">専門家が厳選した初心者向け登山装備</p>
                        
                        <div class="equipment-grid">
                            {equipment_cards}
                        </div>
                    </div>
                </section>
            </main>
            
            <footer class="site-footer">
                <div class="container">
                    <p>&copy; 2025 低山マスター. All rights reserved.</p>
                    <p><small>※当サイトではアフィリエイト広告を利用しています</small></p>
                </div>
            </footer>
        </body>
        </html>
        """
    
    def generate_all(self):
        """全ページを生成"""
        print("🚀 アフィリエイト特化サイト生成開始...")
        
        self.create_directories()
        self.copy_static_files()
        self.generate_index_page()
        self.generate_mountain_pages()
        self.generate_equipment_pages()
        
        print(f"✅ サイト生成完了! 出力先: {self.output_dir}")
        print(f"📁 生成されたファイル:")
        print(f"   - トップページ: {self.output_dir}/index.html")
        print(f"   - 山詳細ページ: {self.output_dir}/mountains/*/index.html")
        print(f"   - 装備ページ: {self.output_dir}/equipment/index.html")

def main():
    generator = AffiliateStaticGeneratorNew()
    generator.generate_all()

if __name__ == "__main__":
    main()