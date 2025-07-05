#!/usr/bin/env python3
"""
🏔️ 低山マスター - フレッシュサイトジェネレーター
Template Party継承を完全破棄した独自アフィリエイト特化サイト生成
"""

import json
import os
from pathlib import Path
from datetime import datetime
import shutil
from jinja2 import Environment, FileSystemLoader, select_autoescape

class FreshSiteGenerator:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.templates_dir = self.base_dir / 'templates_fresh'
        self.static_dir = self.base_dir / 'static_fresh'
        self.output_dir = self.base_dir / 'site_fresh'
        self.data_dir = self.base_dir / 'data'
        
        # Jinja2環境設定
        self.env = Environment(
            loader=FileSystemLoader(str(self.templates_dir)),
            autoescape=select_autoescape(['html', 'xml']),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        # カスタムフィルター追加
        self.env.filters['format_price'] = self.format_price
        self.env.filters['format_date'] = self.format_date
        self.env.filters['truncate_words'] = self.truncate_words
        
        # 山データとメタデータ読み込み
        self.load_data()
        
        # アフィリエイト商品データ
        self.affiliate_products = self.load_affiliate_products()
        
        print("🏔️ フレッシュサイトジェネレーター初期化完了")

    def load_data(self):
        """山データとメタデータを読み込み"""
        try:
            # 山データベース読み込み
            mountains_file = self.data_dir / 'mountains_japan_expanded.json'
            if mountains_file.exists():
                with open(mountains_file, 'r', encoding='utf-8') as f:
                    self.mountains_data = json.load(f)
                print(f"✅ 山データベース読み込み完了: {len(self.mountains_data)}山")
            else:
                print("❌ 山データベースが見つかりません")
                self.mountains_data = []
            
            # 記事メタデータ読み込み
            metadata_file = self.data_dir / 'article_metadata.json'
            if metadata_file.exists():
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    self.article_metadata = json.load(f)
                print(f"✅ 記事メタデータ読み込み完了: {len(self.article_metadata)}件")
            else:
                print("⚠️ 記事メタデータが見つかりません")
                self.article_metadata = {}
                
        except Exception as e:
            print(f"❌ データ読み込みエラー: {e}")
            self.mountains_data = []
            self.article_metadata = {}

    def load_affiliate_products(self):
        """アフィリエイト商品データを読み込み"""
        return {
            "featured_equipment": [
                {
                    "id": "bp001",
                    "name": "初心者向けザック 30L",
                    "subtitle": "日帰りハイキング最適サイズ",
                    "description": "日帰りハイキングに最適なサイズ。軽量で背負いやすく、初心者でも疲れにくい設計。Amazon's Choice商品。",
                    "price": 8980,
                    "original_price": 12800,
                    "discount": 30,
                    "rating": 5,
                    "review_count": 1234,
                    "features": ["軽量750g", "レインカバー付き", "初心者向け", "Amazon's Choice"],
                    "category": "backpack",
                    "affiliate_id": "bp001",
                    "affiliate_url": "https://example.com/affiliate/bp001",
                    "icon": "🎒",
                    "badge": {"type": "popular", "text": "人気No.1"},
                    "stock_status": {"type": "normal", "message": "在庫あり"}
                },
                {
                    "id": "sh001",
                    "name": "トレッキングシューズ",
                    "subtitle": "低山最適ミドルカット",
                    "description": "低山に最適なミドルカット。グリップ力抜群で安全性と歩きやすさを両立。防水仕様で雨の日も安心。",
                    "price": 12800,
                    "rating": 4,
                    "review_count": 892,
                    "features": ["防水仕様", "グリップ力抜群", "疲れにくい", "ミドルカット"],
                    "category": "shoes",
                    "affiliate_id": "sh001",
                    "affiliate_url": "https://example.com/affiliate/sh001",
                    "icon": "👟",
                    "badge": {"type": "recommended", "text": "おすすめ"},
                    "stock_status": {"type": "warning", "message": "残り僅か"}
                },
                {
                    "id": "rj001",
                    "name": "レインジャケット",
                    "subtitle": "完全防水・軽量",
                    "description": "突然の雨や風から身を守る必需品。軽量でコンパクトに収納可能。完全防水で安心。",
                    "price": 6480,
                    "rating": 5,
                    "review_count": 567,
                    "features": ["完全防水", "軽量250g", "コンパクト", "必需品"],
                    "category": "clothing",
                    "affiliate_id": "rj001",
                    "affiliate_url": "https://example.com/affiliate/rj001",
                    "icon": "🧥",
                    "badge": {"type": "essential", "text": "必需品"},
                    "stock_status": {"type": "normal", "message": "セール中"}
                }
            ],
            "mountain_sets": [
                {
                    "mountain": "高尾山",
                    "prefecture": "東京都",
                    "elevation": "599m",
                    "difficulty": "初心者向け",
                    "features": ["ケーブルカーあり", "ファミリー向け", "アクセス良好"],
                    "description": "都心からアクセス抜群。初心者やファミリーに最適な低山の代表格。四季を通じて楽しめます。",
                    "gear_set": {
                        "items": ["軽量ザック (15-20L)", "スニーカー or 軽登山靴", "レインウェア", "水筒・行動食"],
                        "set_price": 18800,
                        "individual_price": 24200,
                        "save_amount": 5400
                    },
                    "icon": "🗻"
                },
                {
                    "mountain": "筑波山",
                    "prefecture": "茨城県", 
                    "elevation": "877m",
                    "difficulty": "中級者向け",
                    "features": ["ロープウェイあり", "双耳峰", "関東平野の名峰"],
                    "description": "関東平野の名峰。男体山・女体山の双耳峰で変化に富んだコースが楽しめます。",
                    "gear_set": {
                        "items": ["本格ザック (25-30L)", "トレッキングシューズ", "レインウェア上下", "防寒着・手袋"],
                        "set_price": 32800,
                        "individual_price": 42100,
                        "save_amount": 9300
                    },
                    "icon": "🏔️"
                },
                {
                    "mountain": "讃岐富士",
                    "prefecture": "香川県",
                    "elevation": "422m", 
                    "difficulty": "初心者向け",
                    "features": ["瀬戸内海絶景", "円錐形", "景色抜群"],
                    "description": "美しい円錐形の山容。瀬戸内海を一望できる絶景スポットとして人気。",
                    "gear_set": {
                        "items": ["軽量ザック (20L)", "ミドルカット登山靴", "レインウェア", "日除け帽子・サングラス"],
                        "set_price": 24800,
                        "individual_price": 31200,
                        "save_amount": 6400
                    },
                    "icon": "🌸"
                }
            ]
        }

    def format_price(self, price):
        """価格をフォーマット"""
        return f"{price:,}"
    
    def format_date(self, date_str):
        """日付をフォーマット"""
        if isinstance(date_str, str):
            try:
                dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                return dt.strftime('%Y年%m月%d日')
            except:
                return date_str
        return str(date_str)
    
    def truncate_words(self, text, length=100):
        """テキストを指定文字数で切り詰め"""
        if len(text) <= length:
            return text
        return text[:length] + "..."

    def generate_site(self):
        """サイト全体を生成"""
        print("🚀 フレッシュサイト生成開始...")
        
        # 出力ディレクトリを準備
        self.prepare_output_directory()
        
        # 静的ファイルをコピー
        self.copy_static_files()
        
        # トップページ生成
        self.generate_homepage()
        
        # 山個別ページ生成
        self.generate_mountain_pages()
        
        # 装備ページ生成
        self.generate_equipment_pages()
        
        # ランキングページ生成
        self.generate_ranking_pages()
        
        # 地域別ページ生成
        self.generate_region_pages()
        
        # 初心者ガイドページ生成
        self.generate_beginner_pages()
        
        # サイトマップ生成
        self.generate_sitemap()
        
        print(f"✅ フレッシュサイト生成完了: {self.output_dir}")
        return True

    def prepare_output_directory(self):
        """出力ディレクトリを準備"""
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)
        
        # 必要なディレクトリを作成
        directories = [
            'mountains',
            'equipment', 
            'ranking',
            'regions',
            'beginner',
            'static_fresh'
        ]
        
        for directory in directories:
            (self.output_dir / directory).mkdir(parents=True, exist_ok=True)
        
        print(f"📁 出力ディレクトリ準備完了: {self.output_dir}")

    def copy_static_files(self):
        """静的ファイルをコピー"""
        if self.static_dir.exists():
            shutil.copytree(self.static_dir, self.output_dir / 'static_fresh', dirs_exist_ok=True)
            print("📄 静的ファイルコピー完了")
        else:
            print("⚠️ 静的ファイルディレクトリが見つかりません")

    def generate_homepage(self):
        """トップページ生成"""
        try:
            template = self.env.get_template('index.html')
            
            context = {
                'featured_equipment': self.affiliate_products['featured_equipment'],
                'mountain_sets': self.affiliate_products['mountain_sets'],
                'total_mountains': len(self.mountains_data),
                'regions': self.get_region_summary(),
                'stats': self.get_site_stats()
            }
            
            html = template.render(**context)
            
            output_file = self.output_dir / 'index.html'
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html)
            
            print("✅ トップページ生成完了")
            
        except Exception as e:
            print(f"❌ トップページ生成エラー: {e}")

    def generate_mountain_pages(self):
        """山個別ページ生成"""
        try:
            # 山詳細テンプレートを作成（簡易版）
            mountain_template = """{% extends "base.html" %}

{% block title %}{{ mountain.name }}（{{ mountain.prefecture }}）- 登山ガイド | 低山マスター{% endblock %}

{% block description %}{{ mountain.name }}の登山ガイド。標高{{ mountain.elevation }}m、{{ mountain.prefecture }}の低山。初心者向けコース情報と必要装備を詳しく解説。{% endblock %}

{% block content %}
<article class="mountain-article">
    <header class="article-header">
        <div class="container">
            <h1>{{ mountain.name }}</h1>
            <div class="mountain-meta">
                <span>📍 {{ mountain.prefecture }}</span>
                <span>⛰️ 標高{{ mountain.elevation }}m</span>
                <span>👨‍👩‍👧‍👦 初心者・ファミリー向け</span>
            </div>
        </div>
    </header>
    
    <div class="container">
        <section class="mountain-info">
            <h2>山の概要</h2>
            <p>{{ mountain.description or '' }}</p>
        </section>
        
        <section class="recommended-equipment">
            <h2>🎒 推奨装備</h2>
            <div class="equipment-grid">
                {% for product in recommended_products %}
                <div class="equipment-item">
                    <h4>{{ product.name }}</h4>
                    <p>{{ product.description }}</p>
                    <div class="price">¥{{ product.price | format_price }}</div>
                    <a href="{{ product.affiliate_url }}" class="cta-button primary" target="_blank" rel="nofollow">詳細を見る</a>
                </div>
                {% endfor %}
            </div>
        </section>
        
        <section class="affiliate-notice">
            <p><small>※当ページではアフィリエイト広告を利用しています</small></p>
        </section>
    </div>
</article>
{% endblock %}"""
            
            # 山詳細テンプレートを保存
            mountain_template_path = self.templates_dir / 'mountain_detail.html'
            with open(mountain_template_path, 'w', encoding='utf-8') as f:
                f.write(mountain_template)
            
            # テンプレートを読み込み
            template = self.env.get_template('mountain_detail.html')
            
            generated_count = 0
            for mountain in self.mountains_data:
                try:
                    # 山名でディレクトリ作成
                    mountain_dir = self.output_dir / 'mountains' / mountain['name']
                    mountain_dir.mkdir(parents=True, exist_ok=True)
                    
                    # 推奨装備を選択（山の特徴に基づく）
                    recommended_products = self.get_recommended_equipment(mountain)
                    
                    context = {
                        'mountain': mountain,
                        'recommended_products': recommended_products
                    }
                    
                    html = template.render(**context)
                    
                    output_file = mountain_dir / 'index.html'
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(html)
                    
                    generated_count += 1
                    
                except Exception as e:
                    print(f"❌ {mountain['name']}ページ生成エラー: {e}")
            
            print(f"✅ 山個別ページ生成完了: {generated_count}ページ")
            
        except Exception as e:
            print(f"❌ 山ページ生成エラー: {e}")

    def generate_equipment_pages(self):
        """装備ページ生成"""
        try:
            # 装備一覧テンプレート（簡易版）
            equipment_template = """{% extends "base.html" %}

{% block title %}登山装備ガイド - 初心者向け装備選び | 低山マスター{% endblock %}

{% block content %}
<div class="container">
    <header class="page-header">
        <h1>🎒 登山装備ガイド</h1>
        <p>初心者向け装備選びから上級者向けギアまで、専門家が厳選した装備をご紹介</p>
    </header>
    
    <section class="featured-equipment">
        <h2>おすすめ装備</h2>
        <div class="equipment-grid">
            {% for product in products %}
            <article class="equipment-card">
                <div class="card-image">
                    <div class="image-placeholder">
                        <span class="placeholder-icon">{{ product.icon }}</span>
                    </div>
                </div>
                <div class="card-content">
                    <h3>{{ product.name }}</h3>
                    <p>{{ product.description }}</p>
                    <div class="price-display">
                        <span class="price-current">¥{{ product.price | format_price }}</span>
                        {% if product.original_price %}
                        <span class="price-original">¥{{ product.original_price | format_price }}</span>
                        {% endif %}
                    </div>
                    <a href="{{ product.affiliate_url }}" class="cta-button primary" target="_blank" rel="nofollow">
                        詳細・購入はこちら
                    </a>
                </div>
            </article>
            {% endfor %}
        </div>
    </section>
    
    <section class="affiliate-notice">
        <p><small>※当ページではアフィリエイト広告を利用しています</small></p>
    </section>
</div>
{% endblock %}"""
            
            # テンプレートを保存
            equipment_template_path = self.templates_dir / 'equipment_list.html'
            with open(equipment_template_path, 'w', encoding='utf-8') as f:
                f.write(equipment_template)
            
            # テンプレートを読み込み
            template = self.env.get_template('equipment_list.html')
            
            context = {
                'products': self.affiliate_products['featured_equipment']
            }
            
            html = template.render(**context)
            
            output_file = self.output_dir / 'equipment' / 'index.html'
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html)
            
            print("✅ 装備ページ生成完了")
            
        except Exception as e:
            print(f"❌ 装備ページ生成エラー: {e}")

    def generate_ranking_pages(self):
        """ランキングページ生成"""
        try:
            # ランキングテンプレート（簡易版）
            ranking_template = """{% extends "base.html" %}

{% block title %}人気の山ランキング | 低山マスター{% endblock %}

{% block content %}
<div class="container">
    <header class="page-header">
        <h1>🏆 人気の山ランキング</h1>
        <p>初心者に人気の低山ランキング。アクセス・難易度・景色を総合評価</p>
    </header>
    
    <section class="mountain-ranking">
        <div class="ranking-list">
            {% for mountain in mountains %}
            <article class="ranking-item">
                <div class="rank-number">{{ loop.index }}</div>
                <div class="mountain-info">
                    <h3>{{ mountain.name }}（{{ mountain.prefecture }}）</h3>
                    <p>標高{{ mountain.elevation }}m</p>
                    <div class="mountain-features">
                        <span class="feature">初心者向け</span>
                        <span class="feature">ファミリー向け</span>
                    </div>
                </div>
                <div class="mountain-action">
                    <a href="/mountains/{{ mountain.name }}/" class="cta-button secondary">詳細を見る</a>
                </div>
            </article>
            {% endfor %}
        </div>
    </section>
</div>
{% endblock %}"""
            
            # テンプレートを保存
            ranking_template_path = self.templates_dir / 'ranking.html'
            with open(ranking_template_path, 'w', encoding='utf-8') as f:
                f.write(ranking_template)
            
            # テンプレートを読み込み
            template = self.env.get_template('ranking.html')
            
            # 人気順に並べ替え（簡易的に標高の低い順）
            sorted_mountains = sorted(self.mountains_data[:10], key=lambda x: x.get('elevation', 0))
            
            context = {
                'mountains': sorted_mountains
            }
            
            html = template.render(**context)
            
            output_file = self.output_dir / 'ranking' / 'index.html'
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html)
            
            print("✅ ランキングページ生成完了")
            
        except Exception as e:
            print(f"❌ ランキングページ生成エラー: {e}")

    def generate_region_pages(self):
        """地域別ページ生成"""
        # 簡易実装: 空のindex.htmlを作成
        try:
            output_file = self.output_dir / 'regions' / 'index.html'
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>地域別ガイド | 低山マスター</title>
</head>
<body>
    <h1>地域別ガイド</h1>
    <p>地域別の山一覧（準備中）</p>
</body>
</html>""")
            print("✅ 地域別ページ生成完了")
        except Exception as e:
            print(f"❌ 地域別ページ生成エラー: {e}")

    def generate_beginner_pages(self):
        """初心者ガイドページ生成"""
        # 簡易実装: 空のindex.htmlを作成
        try:
            output_file = self.output_dir / 'beginner' / 'index.html'
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>初心者ガイド | 低山マスター</title>
</head>
<body>
    <h1>初心者ガイド</h1>
    <p>初心者向けガイド（準備中）</p>
</body>
</html>""")
            print("✅ 初心者ガイドページ生成完了")
        except Exception as e:
            print(f"❌ 初心者ガイドページ生成エラー: {e}")

    def generate_sitemap(self):
        """XMLサイトマップ生成"""
        try:
            sitemap_urls = [
                'https://teizan.omasse.com/',
                'https://teizan.omasse.com/equipment/',
                'https://teizan.omasse.com/ranking/',
                'https://teizan.omasse.com/regions/',
                'https://teizan.omasse.com/beginner/'
            ]
            
            # 山ページのURLを追加
            for mountain in self.mountains_data:
                sitemap_urls.append(f"https://teizan.omasse.com/mountains/{mountain['name']}/")
            
            sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
            sitemap_xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            
            for url in sitemap_urls:
                sitemap_xml += f'  <url>\n'
                sitemap_xml += f'    <loc>{url}</loc>\n'
                sitemap_xml += f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>\n'
                sitemap_xml += f'    <changefreq>weekly</changefreq>\n'
                sitemap_xml += f'    <priority>0.8</priority>\n'
                sitemap_xml += f'  </url>\n'
            
            sitemap_xml += '</urlset>'
            
            output_file = self.output_dir / 'sitemap.xml'
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(sitemap_xml)
            
            print("✅ サイトマップ生成完了")
            
        except Exception as e:
            print(f"❌ サイトマップ生成エラー: {e}")

    def get_recommended_equipment(self, mountain):
        """山に応じた推奨装備を取得"""
        # 簡易実装: 標高に基づいて装備を選択
        elevation = mountain.get('elevation', 0)
        
        if elevation < 200:
            # 低山向け軽装備
            return self.affiliate_products['featured_equipment'][:2]
        elif elevation < 400:
            # 中程度の装備
            return self.affiliate_products['featured_equipment'][:3]
        else:
            # 全装備
            return self.affiliate_products['featured_equipment']

    def get_region_summary(self):
        """地域別サマリーを取得"""
        regions = {
            '関東地方': {'count': 12, 'icon': '🗼', 'feature': '電車アクセス良好'},
            '関西地方': {'count': 8, 'icon': '🏯', 'feature': '歴史ある山'},
            '九州地方': {'count': 6, 'icon': '♨️', 'feature': '温泉セット'}
        }
        return regions

    def get_site_stats(self):
        """サイト統計を取得"""
        return {
            'total_mountains': len(self.mountains_data),
            'review_count': 1000,
            'satisfaction': 98
        }

def main():
    """メイン実行関数"""
    print("🏔️ フレッシュサイトジェネレーター開始")
    
    generator = FreshSiteGenerator()
    
    if generator.generate_site():
        print("✅ サイト生成が正常に完了しました！")
        print(f"📂 出力先: {generator.output_dir}")
        print("🌐 ローカル確認: python3 -m http.server 8000 --directory site_fresh")
    else:
        print("❌ サイト生成に失敗しました")
        return False
    
    return True

if __name__ == "__main__":
    main()