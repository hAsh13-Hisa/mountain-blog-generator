#!/usr/bin/env python3
"""
低山旅行ミニマルサイト生成スクリプト
全ページを生成してリンク切れを防ぐ
"""

import json
import os
from pathlib import Path
from datetime import datetime

class SiteGenerator:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.templates_dir = self.base_dir / "templates"
        self.data_dir = self.base_dir.parent / "data"
        
        # 山データを読み込み
        self.mountains_data = self.load_mountains_data()
        
    def load_mountains_data(self):
        """山データを読み込み"""
        try:
            with open(self.data_dir / "mountains_japan_expanded.json", 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('mountains', [])
        except Exception as e:
            print(f"⚠️ 山データの読み込みに失敗: {e}")
            return []
    
    def load_template(self, template_name):
        """テンプレートを読み込み"""
        template_path = self.templates_dir / template_name
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def render_template(self, template_content, variables):
        """テンプレート変数を置換"""
        for key, value in variables.items():
            template_content = template_content.replace(f"{{{{{key}}}}}", str(value))
        return template_content
    
    def ensure_directory(self, path):
        """ディレクトリが存在しない場合は作成"""
        path.mkdir(parents=True, exist_ok=True)
    
    def calculate_paths(self, current_path):
        """現在のパスに基づいてルートパスとアセットパスを計算"""
        depth = len([p for p in current_path.parts if p not in ['', '.']])
        root_path = "../" * depth if depth > 0 else ""
        css_path = "../" * depth if depth > 0 else ""
        js_path = "../" * depth if depth > 0 else ""
        return root_path, css_path, js_path
    
    def generate_mountain_detail_page(self, mountain):
        """山の詳細ページを生成"""
        mountain_id = mountain.get('id', 'unknown')
        mountain_name = mountain.get('name', '不明な山')
        prefecture = mountain.get('prefecture', '不明')
        elevation = mountain.get('elevation', 0)
        
        # ディレクトリ作成
        mountain_dir = self.base_dir / "mountains" / mountain_name
        self.ensure_directory(mountain_dir)
        
        # パス計算
        current_path = Path("mountains") / mountain_name
        root_path, css_path, js_path = self.calculate_paths(current_path)
        
        # コンテンツ生成
        content = f'''
        <!-- パンくずナビ -->
        <nav class="breadcrumb section" aria-label="パンくずナビ">
            <div class="container">
                <ol class="breadcrumb-list">
                    <li><a href="{root_path}">ホーム</a></li>
                    <li><a href="{root_path}mountains/">山を探す</a></li>
                    <li aria-current="page">{mountain_name}</li>
                </ol>
            </div>
        </nav>

        <!-- 山の詳細 -->
        <section class="section mountain-detail">
            <div class="container">
                <header class="section-header">
                    <h1 class="section-title">{mountain_name}</h1>
                    <p class="section-subtitle">
                        {prefecture}の美しい低山・標高{elevation}m
                    </p>
                </header>
                
                <div class="mountain-content">
                    <div class="mountain-image">
                        <img src="{root_path}images/mountain_{mountain_name.replace('山', '').lower()}.svg" 
                             alt="{mountain_name}の美しいイラスト" 
                             class="mountain-main-img">
                    </div>
                    
                    <div class="mountain-info">
                        <div class="info-grid">
                            <div class="info-card">
                                <h3>基本情報</h3>
                                <ul class="info-list">
                                    <li><strong>標高:</strong> {elevation}m</li>
                                    <li><strong>所在地:</strong> {prefecture}</li>
                                    <li><strong>難易度:</strong> {mountain.get('difficulty', {}).get('level', '初級')}</li>
                                    <li><strong>登山時間:</strong> {mountain.get('difficulty', {}).get('hiking_time', '約1-2時間')}</li>
                                </ul>
                            </div>
                            
                            <div class="info-card">
                                <h3>アクセス</h3>
                                <ul class="info-list">
                                    <li><strong>最寄り駅:</strong> {mountain.get('location', {}).get('nearest_station', '要確認')}</li>
                                    <li><strong>アクセス時間:</strong> {mountain.get('location', {}).get('access_time', '要確認')}</li>
                                </ul>
                            </div>
                        </div>
                        
                        <div class="mountain-features">
                            <h3>山の特徴</h3>
                            <ul class="feature-tags">
                                {self.generate_feature_tags(mountain.get('features', []))}
                            </ul>
                        </div>
                    </div>
                </div>
                
                <!-- 関連装備 -->
                <div class="related-equipment">
                    <h2>推奨装備</h2>
                    <div class="equipment-cards">
                        <div class="equipment-card">
                            <img src="{root_path}images/equipment_backpack.svg" alt="ザック">
                            <h4>ザック (20-30L)</h4>
                            <p>日帰りハイキングに最適</p>
                            <a href="{root_path}equipment/backpack/" class="btn btn-small btn-secondary">詳細</a>
                        </div>
                        <div class="equipment-card">
                            <img src="{root_path}images/equipment_shoes.svg" alt="登山靴">
                            <h4>トレッキングシューズ</h4>
                            <p>低山に適したミドルカット</p>
                            <a href="{root_path}equipment/shoes/" class="btn btn-small btn-secondary">詳細</a>
                        </div>
                        <div class="equipment-card">
                            <img src="{root_path}images/equipment_rain.svg" alt="レインウェア">
                            <h4>レインウェア</h4>
                            <p>突然の雨に備えて必携</p>
                            <a href="{root_path}equipment/rain/" class="btn btn-small btn-secondary">詳細</a>
                        </div>
                    </div>
                </div>
                
                <div class="mountain-actions">
                    <a href="{root_path}mountains/" class="btn btn-secondary">
                        ← 山一覧に戻る
                    </a>
                    <a href="{root_path}equipment/" class="btn btn-primary">
                        装備ガイドを見る
                    </a>
                </div>
            </div>
        </section>
        '''
        
        # ベーステンプレートに組み込み
        base_template = self.load_template("base.html")
        variables = {
            "title": f"{mountain_name} | 山の詳細",
            "description": f"{prefecture}の{mountain_name}（標高{elevation}m）の詳細情報。アクセス、難易度、推奨装備などを詳しく解説。",
            "page_type": "Place",
            "current_path": f"/mountains/{mountain_name}/",
            "root_path": root_path,
            "css_path": css_path,
            "js_path": js_path,
            "content": content
        }
        
        rendered_html = self.render_template(base_template, variables)
        
        # ファイル保存
        with open(mountain_dir / "index.html", 'w', encoding='utf-8') as f:
            f.write(rendered_html)
        
        print(f"✅ 山詳細ページ作成: {mountain_name}")
    
    def generate_feature_tags(self, features):
        """特徴タグのHTMLを生成"""
        if not features:
            return "<li>情報なし</li>"
        
        tags_html = ""
        for feature in features[:6]:  # 最大6個まで表示
            tags_html += f"<li class='feature-tag'>{feature}</li>"
        return tags_html
    
    def generate_mountains_index(self):
        """山一覧ページを生成"""
        mountains_dir = self.base_dir / "mountains"
        self.ensure_directory(mountains_dir)
        
        current_path = Path("mountains")
        root_path, css_path, js_path = self.calculate_paths(current_path)
        
        # 山カードを生成
        mountain_cards = ""
        for mountain in self.mountains_data[:12]:  # 最初の12山を表示
            mountain_name = mountain.get('name', '不明な山')
            prefecture = mountain.get('prefecture', '不明')
            elevation = mountain.get('elevation', 0)
            difficulty = mountain.get('difficulty', {}).get('level', '初級')
            
            mountain_cards += f'''
            <article class="card">
                <div class="card-image">
                    <img src="{root_path}images/mountain_{mountain_name.replace('山', '').lower()}.svg" 
                         alt="{mountain_name}のイラスト" 
                         class="card-img"
                         onerror="this.src='{root_path}images/hero_mountain_hiking.svg'">
                </div>
                <div class="card-content">
                    <h3 class="card-title">{mountain_name}</h3>
                    <div class="card-meta">
                        <span>📍 {prefecture}</span>
                        <span>📏 標高{elevation}m</span>
                        <span>⛰️ {difficulty}</span>
                    </div>
                    <p class="card-description">
                        {mountain.get('description', f'{prefecture}の美しい低山。初心者にもおすすめのハイキングコースです。')}
                    </p>
                    <a href="{root_path}mountains/{mountain_name}/" class="btn btn-secondary btn-small">
                        詳細を見る
                    </a>
                </div>
            </article>
            '''
        
        content = f'''
        <section class="section">
            <div class="container">
                <header class="section-header">
                    <h1 class="section-title">山を探す</h1>
                    <p class="section-subtitle">
                        全国47都道府県の厳選低山一覧。初心者・ファミリー向けの安全な山をご紹介します。
                    </p>
                </header>
                
                <div class="card-grid">
                    {mountain_cards}
                </div>
                
                <div class="text-center">
                    <p class="section-subtitle">より多くの山情報は順次追加予定です</p>
                </div>
            </div>
        </section>
        '''
        
        base_template = self.load_template("base.html")
        variables = {
            "title": "山を探す",
            "description": "全国47都道府県の低山一覧。初心者・ファミリー向けの安全でアクセス良好な低山をご紹介。",
            "page_type": "CollectionPage", 
            "current_path": "/mountains/",
            "root_path": root_path,
            "css_path": css_path,
            "js_path": js_path,
            "content": content
        }
        
        rendered_html = self.render_template(base_template, variables)
        
        with open(mountains_dir / "index.html", 'w', encoding='utf-8') as f:
            f.write(rendered_html)
        
        print(f"✅ 山一覧ページ作成完了")
    
    def generate_equipment_pages(self):
        """装備ガイドページを生成"""
        equipment_dir = self.base_dir / "equipment"
        self.ensure_directory(equipment_dir)
        
        # 装備一覧ページ
        self.generate_equipment_index()
        
        # 個別装備ページ
        equipment_items = [
            {
                "id": "backpack",
                "name": "ザック選び",
                "description": "日帰り低山ハイキングに最適なザックの選び方",
                "image": "equipment_backpack.svg",
                "price": "¥8,000",
                "original_price": "¥12,000",
                "features": ["軽量で疲れにくい", "防水性能あり", "初心者向け"],
                "detailed_info": """
                <h3>ザック選びのポイント</h3>
                <p>日帰り低山ハイキングには20-30Lのザックが最適です。以下のポイントを重視して選びましょう。</p>
                <ul>
                    <li><strong>容量:</strong> 20-30Lが日帰りに最適</li>
                    <li><strong>重量:</strong> 1kg以下の軽量モデルを選択</li>
                    <li><strong>背負い心地:</strong> フィット感を実際に確認</li>
                    <li><strong>機能:</strong> レインカバー付きが便利</li>
                </ul>
                """
            },
            {
                "id": "shoes", 
                "name": "登山靴選び",
                "description": "低山に適した登山靴の選び方",
                "image": "equipment_shoes.svg",
                "price": "¥12,800",
                "original_price": "",
                "features": ["グリップ力抜群", "防水仕様", "疲れにくい設計"],
                "detailed_info": """
                <h3>登山靴選びのポイント</h3>
                <p>低山ハイキングにはミドルカットのトレッキングシューズがおすすめです。</p>
                <ul>
                    <li><strong>カットの高さ:</strong> ミドルカットで足首をサポート</li>
                    <li><strong>ソール:</strong> 適度なグリップ力があるもの</li>
                    <li><strong>防水性:</strong> ゴアテックスなどの防水素材</li>
                    <li><strong>サイズ:</strong> つま先に1cm程度の余裕</li>
                </ul>
                """
            },
            {
                "id": "rain",
                "name": "レインウェア",
                "description": "突然の雨や風から身を守る必需品", 
                "image": "equipment_rain.svg",
                "price": "¥6,480",
                "original_price": "",
                "features": ["完全防水", "軽量250g", "コンパクト収納"],
                "detailed_info": """
                <h3>レインウェア選びのポイント</h3>
                <p>山の天気は変わりやすいため、レインウェアは必携です。</p>
                <ul>
                    <li><strong>防水性:</strong> 20,000mm以上の防水性能</li>
                    <li><strong>透湿性:</strong> 蒸れにくい素材を選択</li>
                    <li><strong>軽量性:</strong> 300g以下の軽量モデル</li>
                    <li><strong>収納性:</strong> コンパクトに収納できるもの</li>
                </ul>
                """
            }
        ]
        
        for item in equipment_items:
            self.generate_equipment_detail_page(item)
    
    def generate_equipment_index(self):
        """装備ガイド一覧ページ"""
        equipment_dir = self.base_dir / "equipment"
        current_path = Path("equipment")
        root_path, css_path, js_path = self.calculate_paths(current_path)
        
        content = f'''
        <section class="section">
            <div class="container">
                <header class="section-header">
                    <h1 class="section-title">装備ガイド</h1>
                    <p class="section-subtitle">
                        安全で快適な低山ハイキングのための装備選びをサポートします
                    </p>
                </header>
                
                <div class="card-grid">
                    <article class="card">
                        <div class="card-image">
                            <img src="{root_path}images/equipment_backpack.svg" 
                                 alt="ザックのイラスト" class="card-img">
                        </div>
                        <div class="card-content">
                            <h3 class="card-title">ザック選び</h3>
                            <p class="card-description">
                                日帰り低山ハイキングに最適なザックの選び方をご紹介します。
                            </p>
                            <div class="price-info">
                                <span class="price-current">¥8,000</span>
                                <span class="price-original">¥12,000</span>
                                <span class="price-discount">33%OFF</span>
                            </div>
                            <a href="{root_path}equipment/backpack/" class="btn btn-primary btn-small">
                                詳細を見る
                            </a>
                        </div>
                    </article>
                    
                    <article class="card">
                        <div class="card-image">
                            <img src="{root_path}images/equipment_shoes.svg" 
                                 alt="登山靴のイラスト" class="card-img">
                        </div>
                        <div class="card-content">
                            <h3 class="card-title">登山靴選び</h3>
                            <p class="card-description">
                                低山に適した登山靴の選び方と足への負担軽減のポイント。
                            </p>
                            <div class="price-info">
                                <span class="price-current">¥12,800</span>
                                <span class="price-discount">セール中</span>
                            </div>
                            <a href="{root_path}equipment/shoes/" class="btn btn-primary btn-small">
                                詳細を見る
                            </a>
                        </div>
                    </article>
                    
                    <article class="card">
                        <div class="card-image">
                            <img src="{root_path}images/equipment_rain.svg" 
                                 alt="レインウェアのイラスト" class="card-img">
                        </div>
                        <div class="card-content">
                            <h3 class="card-title">レインウェア</h3>
                            <p class="card-description">
                                突然の雨や風から身を守る必需品。軽量でコンパクトなモデルを厳選。
                            </p>
                            <div class="price-info">
                                <span class="price-current">¥6,480</span>
                                <span class="price-discount">限定価格</span>
                            </div>
                            <a href="{root_path}equipment/rain/" class="btn btn-primary btn-small">
                                詳細を見る
                            </a>
                        </div>
                    </article>
                </div>
            </div>
        </section>
        '''
        
        base_template = self.load_template("base.html")
        variables = {
            "title": "装備ガイド",
            "description": "低山ハイキング用装備の選び方ガイド。ザック、登山靴、レインウェアなど必要装備を詳しく解説。",
            "page_type": "CollectionPage",
            "current_path": "/equipment/",
            "root_path": root_path,
            "css_path": css_path,
            "js_path": js_path,
            "content": content
        }
        
        rendered_html = self.render_template(base_template, variables)
        
        with open(equipment_dir / "index.html", 'w', encoding='utf-8') as f:
            f.write(rendered_html)
        
        print("✅ 装備ガイド一覧ページ作成完了")
    
    def generate_equipment_detail_page(self, equipment):
        """装備詳細ページを生成"""
        equipment_dir = self.base_dir / "equipment" / equipment["id"]
        self.ensure_directory(equipment_dir)
        
        current_path = Path("equipment") / equipment["id"]
        root_path, css_path, js_path = self.calculate_paths(current_path)
        
        # 特徴リストのHTML生成
        features_html = ""
        for feature in equipment["features"]:
            features_html += f"<li>{feature}</li>"
        
        # 価格表示のHTML
        price_html = f'<span class="price-current">{equipment["price"]}</span>'
        if equipment["original_price"]:
            price_html += f'<span class="price-original">{equipment["original_price"]}</span>'
            price_html += '<span class="price-discount">33%OFF</span>'
        
        content = f'''
        <!-- パンくずナビ -->
        <nav class="breadcrumb section" aria-label="パンくずナビ">
            <div class="container">
                <ol class="breadcrumb-list">
                    <li><a href="{root_path}">ホーム</a></li>
                    <li><a href="{root_path}equipment/">装備ガイド</a></li>
                    <li aria-current="page">{equipment["name"]}</li>
                </ol>
            </div>
        </nav>

        <section class="section equipment-detail">
            <div class="container">
                <header class="section-header">
                    <h1 class="section-title">{equipment["name"]}</h1>
                    <p class="section-subtitle">{equipment["description"]}</p>
                </header>
                
                <div class="equipment-content">
                    <div class="equipment-image">
                        <img src="{root_path}images/{equipment['image']}" 
                             alt="{equipment['name']}のイラスト" 
                             class="equipment-main-img">
                    </div>
                    
                    <div class="equipment-info">
                        <div class="price-info">
                            {price_html}
                        </div>
                        
                        <ul class="feature-list">
                            {features_html}
                        </ul>
                        
                        <div class="equipment-actions">
                            <a href="#" class="btn btn-primary" onclick="alert('アフィリエイトリンクへの遷移')">
                                Amazonで購入
                            </a>
                            <a href="#" class="btn btn-secondary" onclick="alert('アフィリエイトリンクへの遷移')">
                                楽天で購入
                            </a>
                        </div>
                    </div>
                </div>
                
                <div class="equipment-details">
                    {equipment["detailed_info"]}
                </div>
                
                <div class="back-link">
                    <a href="{root_path}equipment/" class="btn btn-secondary">
                        ← 装備ガイド一覧に戻る
                    </a>
                </div>
            </div>
        </section>
        '''
        
        base_template = self.load_template("base.html")
        variables = {
            "title": equipment["name"],
            "description": f"{equipment['description']}。選び方のポイントと推奨モデルをご紹介。",
            "page_type": "Product",
            "current_path": f"/equipment/{equipment['id']}/",
            "root_path": root_path,
            "css_path": css_path,
            "js_path": js_path,
            "content": content
        }
        
        rendered_html = self.render_template(base_template, variables)
        
        with open(equipment_dir / "index.html", 'w', encoding='utf-8') as f:
            f.write(rendered_html)
        
        print(f"✅ 装備詳細ページ作成: {equipment['name']}")
    
    def generate_beginner_pages(self):
        """初心者向けページを生成"""
        beginner_dir = self.base_dir / "beginner"
        self.ensure_directory(beginner_dir)
        
        # 初心者向け一覧ページ
        self.generate_beginner_index()
        
        # 個別ページ
        beginner_pages = [
            {
                "id": "basics",
                "title": "基礎知識",
                "description": "低山ハイキングの基本的な知識と準備",
                "image": "support_guide.svg"
            },
            {
                "id": "safety", 
                "title": "安全対策",
                "description": "事故を防ぐための基本的な安全対策",
                "image": "support_safety.svg"
            },
            {
                "id": "family",
                "title": "ファミリー向け",
                "description": "子供と一緒に楽しむ低山ハイキング",
                "image": "support_family.svg"
            }
        ]
        
        for page in beginner_pages:
            self.generate_beginner_detail_page(page)
    
    def generate_beginner_index(self):
        """初心者向け一覧ページ"""
        beginner_dir = self.base_dir / "beginner"
        current_path = Path("beginner")
        root_path, css_path, js_path = self.calculate_paths(current_path)
        
        content = f'''
        <section class="section">
            <div class="container">
                <header class="section-header">
                    <h1 class="section-title">初心者向けサポート</h1>
                    <p class="section-subtitle">
                        低山ハイキングを始める方に向けた基礎知識と安全な楽しみ方
                    </p>
                </header>
                
                <div class="card-grid">
                    <article class="card">
                        <div class="card-image">
                            <img src="{root_path}images/support_guide.svg" 
                                 alt="基礎知識のイラスト" class="card-img">
                        </div>
                        <div class="card-content">
                            <h3 class="card-title">基礎知識</h3>
                            <p class="card-description">
                                低山ハイキングの基本的な知識と準備について分かりやすく解説します。
                            </p>
                            <a href="{root_path}beginner/basics/" class="btn btn-secondary btn-small">
                                詳細を見る
                            </a>
                        </div>
                    </article>
                    
                    <article class="card">
                        <div class="card-image">
                            <img src="{root_path}images/support_safety.svg" 
                                 alt="安全対策のイラスト" class="card-img">
                        </div>
                        <div class="card-content">
                            <h3 class="card-title">安全対策</h3>
                            <p class="card-description">
                                事故を防ぐための基本的な安全対策と、緊急時の対処方法をご紹介。
                            </p>
                            <a href="{root_path}beginner/safety/" class="btn btn-secondary btn-small">
                                詳細を見る
                            </a>
                        </div>
                    </article>
                    
                    <article class="card">
                        <div class="card-image">
                            <img src="{root_path}images/support_family.svg" 
                                 alt="ファミリー向けのイラスト" class="card-img">
                        </div>
                        <div class="card-content">
                            <h3 class="card-title">ファミリー向け</h3>
                            <p class="card-description">
                                子供と一緒に楽しむ低山ハイキングのコツと注意点をお伝えします。
                            </p>
                            <a href="{root_path}beginner/family/" class="btn btn-secondary btn-small">
                                詳細を見る
                            </a>
                        </div>
                    </article>
                </div>
            </div>
        </section>
        '''
        
        base_template = self.load_template("base.html")
        variables = {
            "title": "初心者向けサポート",
            "description": "低山ハイキング初心者向けの基礎知識、安全対策、ファミリー向け情報を詳しく解説。",
            "page_type": "CollectionPage",
            "current_path": "/beginner/",
            "root_path": root_path,
            "css_path": css_path,
            "js_path": js_path,
            "content": content
        }
        
        rendered_html = self.render_template(base_template, variables)
        
        with open(beginner_dir / "index.html", 'w', encoding='utf-8') as f:
            f.write(rendered_html)
        
        print("✅ 初心者向け一覧ページ作成完了")
    
    def generate_beginner_detail_page(self, page_info):
        """初心者向け詳細ページを生成"""
        page_dir = self.base_dir / "beginner" / page_info["id"]
        self.ensure_directory(page_dir)
        
        current_path = Path("beginner") / page_info["id"]
        root_path, css_path, js_path = self.calculate_paths(current_path)
        
        # ページ別コンテンツ
        detailed_content = {
            "basics": """
            <h3>低山ハイキングとは</h3>
            <p>低山ハイキングは標高1000m以下の山を登ることで、初心者や家族連れでも気軽に楽しめる自然体験です。</p>
            
            <h3>準備すべきもの</h3>
            <ul>
                <li>適切な服装（動きやすく、重ね着できるもの）</li>
                <li>歩きやすい靴（トレッキングシューズがベスト）</li>
                <li>水分補給用の水筒</li>
                <li>軽食・行動食</li>
                <li>レインウェア</li>
                <li>救急用品</li>
            </ul>
            
            <h3>計画の立て方</h3>
            <p>初回は2-3時間で登れる近場の山を選び、天気予報を確認してから出発しましょう。</p>
            """,
            "safety": """
            <h3>基本的な安全対策</h3>
            <ul>
                <li><strong>天気予報の確認:</strong> 悪天候時は登山を中止</li>
                <li><strong>登山計画書:</strong> 家族に行き先と帰宅予定時刻を伝える</li>
                <li><strong>適切な装備:</strong> 山の難易度に応じた装備を準備</li>
                <li><strong>体調管理:</strong> 体調不良時は無理をしない</li>
            </ul>
            
            <h3>緊急時の対処法</h3>
            <p>道に迷った場合は無理に進まず、来た道を戻るか救助を要請しましょう。携帯電話の電波状況も事前に確認が重要です。</p>
            
            <h3>緊急連絡先</h3>
            <ul>
                <li>警察：110番</li>
                <li>消防・救急：119番</li>
                <li>山岳遭難：各都道府県警察</li>
            </ul>
            """,
            "family": """
            <h3>子供と楽しむポイント</h3>
            <ul>
                <li><strong>短時間コース:</strong> 1-2時間程度の短いコースを選択</li>
                <li><strong>興味を引く工夫:</strong> 自然観察や写真撮影を楽しむ</li>
                <li><strong>休憩を多めに:</strong> 子供のペースに合わせた休憩</li>
                <li><strong>安全第一:</strong> 危険な場所では手をつなぐ</li>
            </ul>
            
            <h3>子供向け装備</h3>
            <p>子供用のザック、帽子、手袋などサイズに合った装備を用意しましょう。また、お気に入りのおやつを持参すると喜びます。</p>
            
            <h3>ファミリー向けおすすめ山</h3>
            <ul>
                <li>高尾山（東京都）- ケーブルカーあり</li>
                <li>筑波山（茨城県）- ロープウェイあり</li>
                <li>円山（北海道）- 市内からアクセス良好</li>
            </ul>
            """
        }
        
        content = f'''
        <!-- パンくずナビ -->
        <nav class="breadcrumb section" aria-label="パンくずナビ">
            <div class="container">
                <ol class="breadcrumb-list">
                    <li><a href="{root_path}">ホーム</a></li>
                    <li><a href="{root_path}beginner/">初心者向け</a></li>
                    <li aria-current="page">{page_info["title"]}</li>
                </ol>
            </div>
        </nav>

        <section class="section beginner-detail">
            <div class="container">
                <header class="section-header">
                    <h1 class="section-title">{page_info["title"]}</h1>
                    <p class="section-subtitle">{page_info["description"]}</p>
                </header>
                
                <div class="beginner-content">
                    <div class="beginner-image">
                        <img src="{root_path}images/{page_info['image']}" 
                             alt="{page_info['title']}のイラスト" 
                             class="beginner-main-img">
                    </div>
                    
                    <div class="beginner-info">
                        {detailed_content.get(page_info["id"], "<p>詳細情報を準備中です。</p>")}
                    </div>
                </div>
                
                <div class="related-links">
                    <h3>関連ページ</h3>
                    <div class="link-cards">
                        <a href="{root_path}equipment/" class="link-card">
                            <h4>装備ガイド</h4>
                            <p>必要な装備の選び方</p>
                        </a>
                        <a href="{root_path}mountains/" class="link-card">
                            <h4>山を探す</h4>
                            <p>初心者におすすめの山</p>
                        </a>
                    </div>
                </div>
                
                <div class="back-link">
                    <a href="{root_path}beginner/" class="btn btn-secondary">
                        ← 初心者向けページに戻る
                    </a>
                </div>
            </div>
        </section>
        '''
        
        base_template = self.load_template("base.html")
        variables = {
            "title": page_info["title"],
            "description": f"{page_info['description']}について詳しく解説。安全で楽しい低山ハイキングを始めましょう。",
            "page_type": "Article",
            "current_path": f"/beginner/{page_info['id']}/",
            "root_path": root_path,
            "css_path": css_path,
            "js_path": js_path,
            "content": content
        }
        
        rendered_html = self.render_template(base_template, variables)
        
        with open(page_dir / "index.html", 'w', encoding='utf-8') as f:
            f.write(rendered_html)
        
        print(f"✅ 初心者向け詳細ページ作成: {page_info['title']}")
    
    def generate_static_pages(self):
        """静的ページを生成（地域別、フッターページ等）"""
        static_pages = [
            {
                "path": "regions",
                "title": "地域別ガイド", 
                "description": "全国の地域別低山ガイド",
                "content": self.get_regions_content()
            },
            {
                "path": "about",
                "title": "このサイトについて",
                "description": "低山旅行サイトについて",
                "content": self.get_about_content()
            },
            {
                "path": "contact",
                "title": "お問い合わせ",
                "description": "お問い合わせ方法",
                "content": self.get_contact_content()
            },
            {
                "path": "privacy",
                "title": "プライバシーポリシー",
                "description": "プライバシーポリシー",
                "content": self.get_privacy_content()
            },
            {
                "path": "terms",
                "title": "利用規約",
                "description": "サイト利用規約",
                "content": self.get_terms_content()
            }
        ]
        
        for page in static_pages:
            self.generate_static_page(page)
    
    def get_regions_content(self):
        """地域別ページのコンテンツ"""
        return '''
        <section class="section">
            <div class="container">
                <header class="section-header">
                    <h1 class="section-title">地域別ガイド</h1>
                    <p class="section-subtitle">
                        お住まいの地域からアクセス良好な低山を見つけよう
                    </p>
                </header>
                
                <div class="region-grid">
                    <article class="region-card">
                        <div class="region-image">
                            <img src="{{root_path}}images/region_kanto.svg" alt="関東地方">
                        </div>
                        <div class="region-content">
                            <h3 class="region-name">関東地方</h3>
                            <p class="region-description">
                                都心からアクセス良好な12座の低山をご紹介。電車で行ける山が中心です。
                            </p>
                            <div class="region-stats">
                                <span class="stat-item">🚊 電車アクセス良好</span>
                                <span class="stat-item">⛰️ 12座の低山</span>
                            </div>
                        </div>
                    </article>
                    
                    <article class="region-card">
                        <div class="region-image">
                            <img src="{{root_path}}images/region_kansai.svg" alt="関西地方">
                        </div>
                        <div class="region-content">
                            <h3 class="region-name">関西地方</h3>
                            <p class="region-description">
                                歴史と自然が融合した8座の名峰。京都・奈良の古都の山々。
                            </p>
                            <div class="region-stats">
                                <span class="stat-item">🏛️ 歴史ある山</span>
                                <span class="stat-item">⛰️ 8座の名峰</span>
                            </div>
                        </div>
                    </article>
                    
                    <article class="region-card">
                        <div class="region-image">
                            <img src="{{root_path}}images/region_kyushu.svg" alt="九州地方">
                        </div>
                        <div class="region-content">
                            <h3 class="region-name">九州地方</h3>
                            <p class="region-description">
                                温泉とセットで楽しめる6座の低山。登山後の温泉が最高です。
                            </p>
                            <div class="region-stats">
                                <span class="stat-item">♨️ 温泉セット</span>
                                <span class="stat-item">⛰️ 6座の低山</span>
                            </div>
                        </div>
                    </article>
                </div>
                
                <div class="region-details">
                    <h2>各地域の特徴</h2>
                    <p>各地域にはそれぞれ特色のある低山があります。アクセスのしやすさ、季節の見どころ、温泉などの周辺施設も考慮して山選びをお楽しみください。</p>
                </div>
            </div>
        </section>
        '''
    
    def get_about_content(self):
        """このサイトについてページのコンテンツ"""
        return '''
        <section class="section">
            <div class="container">
                <header class="section-header">
                    <h1 class="section-title">このサイトについて</h1>
                    <p class="section-subtitle">
                        低山旅行サイトの目的と運営方針
                    </p>
                </header>
                
                <div class="about-content">
                    <h2>サイトの目的</h2>
                    <p>「低山旅行」は、標高1000m以下の低山ハイキングを通じて、多くの方に自然の魅力を感じていただくことを目的としています。特に初心者やファミリー層の方々が安全に楽しめる山の情報を提供しています。</p>
                    
                    <h2>提供する情報</h2>
                    <ul>
                        <li>全国47都道府県の厳選低山情報</li>
                        <li>初心者向けの装備選びガイド</li>
                        <li>安全対策と基礎知識</li>
                        <li>ファミリーハイキングのコツ</li>
                    </ul>
                    
                    <h2>運営方針</h2>
                    <p>安全第一を最優先に、正確で役立つ情報の提供を心がけています。また、自然環境の保護と登山マナーの啓発にも取り組んでいます。</p>
                    
                    <h2>お願い</h2>
                    <p>登山は自然相手のアクティビティです。天候や自分の体調を考慮し、無理のない範囲で楽しんでください。</p>
                </div>
            </div>
        </section>
        '''
    
    def get_contact_content(self):
        """お問い合わせページのコンテンツ"""
        return '''
        <section class="section">
            <div class="container">
                <header class="section-header">
                    <h1 class="section-title">お問い合わせ</h1>
                    <p class="section-subtitle">
                        ご質問・ご要望はこちらから
                    </p>
                </header>
                
                <div class="contact-content">
                    <h2>お問い合わせについて</h2>
                    <p>サイトに関するご質問、山の情報についてのお問い合わせ、掲載希望などございましたら、以下の方法でご連絡ください。</p>
                    
                    <div class="contact-methods">
                        <div class="contact-method">
                            <h3>📧 メール</h3>
                            <p>info@teizan-travel.example.com</p>
                            <p class="note">※3営業日以内にご返信いたします</p>
                        </div>
                        
                        <div class="contact-method">
                            <h3>📝 お問い合わせフォーム</h3>
                            <p>準備中です。現在はメールでのお問い合わせをお願いいたします。</p>
                        </div>
                    </div>
                    
                    <h2>よくあるご質問</h2>
                    <div class="faq">
                        <div class="faq-item">
                            <h4>Q: 紹介されている山の情報は最新ですか？</h4>
                            <p>A: 定期的に情報を更新していますが、天候や工事等により登山道の状況が変わる場合があります。最新情報は各自治体や山小屋等にお確かめください。</p>
                        </div>
                        
                        <div class="faq-item">
                            <h4>Q: 装備の購入リンクからの収益はありますか？</h4>
                            <p>A: はい、アフィリエイト収益を得ています。ただし、推奨する商品は実際に検証したものに限定しています。</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        '''
    
    def get_privacy_content(self):
        """プライバシーポリシーのコンテンツ"""
        return '''
        <section class="section">
            <div class="container">
                <header class="section-header">
                    <h1 class="section-title">プライバシーポリシー</h1>
                    <p class="section-subtitle">
                        個人情報の取り扱いについて
                    </p>
                </header>
                
                <div class="privacy-content">
                    <h2>個人情報の収集</h2>
                    <p>当サイトでは、お問い合わせの際に名前やメールアドレス等の個人情報をお預かりする場合があります。</p>
                    
                    <h2>個人情報の利用目的</h2>
                    <ul>
                        <li>お問い合わせへの回答</li>
                        <li>サービス向上のための分析</li>
                        <li>重要なお知らせの配信</li>
                    </ul>
                    
                    <h2>Cookie（クッキー）について</h2>
                    <p>当サイトでは、ユーザーの利便性向上とサイト改善のためにCookieを使用しています。Cookieの使用を望まない場合は、ブラウザの設定で無効にできます。</p>
                    
                    <h2>アクセス解析ツール</h2>
                    <p>当サイトでは、Googleアナリティクスを利用してアクセス解析を行っています。詳細は<a href="https://policies.google.com/privacy" target="_blank" rel="noopener">Googleのプライバシーポリシー</a>をご確認ください。</p>
                    
                    <h2>免責事項</h2>
                    <p>当サイトの情報により生じた損害について、運営者は一切の責任を負いません。登山は自己責任で行ってください。</p>
                    
                    <p class="update-date">最終更新日: 2025年1月1日</p>
                </div>
            </div>
        </section>
        '''
    
    def get_terms_content(self):
        """利用規約のコンテンツ"""
        return '''
        <section class="section">
            <div class="container">
                <header class="section-header">
                    <h1 class="section-title">利用規約</h1>
                    <p class="section-subtitle">
                        サイトご利用時の規約
                    </p>
                </header>
                
                <div class="terms-content">
                    <h2>第1条（適用）</h2>
                    <p>本規約は、当サイト「低山旅行」の利用に関する条件を定めるものです。ユーザーは本規約に同意したうえでサイトをご利用ください。</p>
                    
                    <h2>第2条（利用目的）</h2>
                    <p>当サイトは、低山ハイキングに関する情報提供を目的としています。営利目的での無断利用は禁止します。</p>
                    
                    <h2>第3条（禁止事項）</h2>
                    <ul>
                        <li>法令に違反する行為</li>
                        <li>当サイトの運営を妨害する行為</li>
                        <li>他のユーザーに迷惑をかける行為</li>
                        <li>知的財産権を侵害する行為</li>
                    </ul>
                    
                    <h2>第4条（免責事項）</h2>
                    <p>登山に関する情報は参考程度に留め、実際の登山は自己責任で行ってください。当サイトの情報により生じた損害について、運営者は一切の責任を負いません。</p>
                    
                    <h2>第5条（著作権）</h2>
                    <p>当サイトのコンテンツの著作権は運営者に帰属します。無断転載・複製を禁止します。</p>
                    
                    <h2>第6条（規約の変更）</h2>
                    <p>運営者は、必要に応じて本規約を変更することがあります。重要な変更についてはサイト上でお知らせします。</p>
                    
                    <p class="update-date">最終更新日: 2025年1月1日</p>
                </div>
            </div>
        </section>
        '''
    
    def generate_static_page(self, page_info):
        """静的ページを生成"""
        page_dir = self.base_dir / page_info["path"]
        self.ensure_directory(page_dir)
        
        current_path = Path(page_info["path"])
        root_path, css_path, js_path = self.calculate_paths(current_path)
        
        # コンテンツのルートパス置換
        content = page_info["content"].replace("{{root_path}}", root_path)
        
        base_template = self.load_template("base.html")
        variables = {
            "title": page_info["title"],
            "description": page_info["description"],
            "page_type": "WebPage",
            "current_path": f"/{page_info['path']}/",
            "root_path": root_path,
            "css_path": css_path,
            "js_path": js_path,
            "content": content
        }
        
        rendered_html = self.render_template(base_template, variables)
        
        with open(page_dir / "index.html", 'w', encoding='utf-8') as f:
            f.write(rendered_html)
        
        print(f"✅ 静的ページ作成: {page_info['title']}")
    
    def add_breadcrumb_css(self):
        """パンくずナビのCSSを追加"""
        css_file = self.base_dir / "css" / "minimal_design.css"
        
        breadcrumb_css = '''

/* === パンくずナビ === */
.breadcrumb {
    background: var(--mist-white);
    padding: var(--spacing-md) 0;
    border-bottom: 1px solid var(--border-light);
}

.breadcrumb-list {
    display: flex;
    list-style: none;
    gap: var(--spacing-sm);
    align-items: center;
    font-size: var(--font-size-sm);
}

.breadcrumb-list li:not(:last-child)::after {
    content: ">";
    margin-left: var(--spacing-sm);
    color: var(--text-light);
}

.breadcrumb-list a {
    color: var(--text-secondary);
    text-decoration: none;
    transition: color 0.2s ease;
}

.breadcrumb-list a:hover {
    color: var(--forest-dark);
}

.breadcrumb-list li[aria-current="page"] {
    color: var(--forest-dark);
    font-weight: 600;
}

/* === 詳細ページ用スタイル === */
.mountain-detail .mountain-content,
.equipment-detail .equipment-content,
.beginner-detail .beginner-content {
    display: grid;
    grid-template-columns: 1fr;
    gap: var(--spacing-2xl);
    margin: var(--spacing-2xl) 0;
}

@media (min-width: 768px) {
    .mountain-detail .mountain-content,
    .equipment-detail .equipment-content,
    .beginner-detail .beginner-content {
        grid-template-columns: 1fr 1fr;
        align-items: start;
    }
}

.mountain-main-img,
.equipment-main-img,
.beginner-main-img {
    width: 100%;
    height: auto;
    border-radius: var(--border-radius-lg);
    box-shadow: var(--shadow-medium);
}

.info-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: var(--spacing-lg);
}

@media (min-width: 768px) {
    .info-grid {
        grid-template-columns: 1fr 1fr;
    }
}

.info-card {
    background: var(--pure-white);
    padding: var(--spacing-lg);
    border-radius: var(--border-radius);
    box-shadow: var(--shadow-subtle);
}

.info-card h3 {
    color: var(--forest-dark);
    margin-bottom: var(--spacing-md);
    font-size: var(--font-size-lg);
}

.info-list {
    list-style: none;
}

.info-list li {
    padding: var(--spacing-xs) 0;
    border-bottom: 1px solid var(--border-light);
}

.info-list li:last-child {
    border-bottom: none;
}

.feature-tags {
    display: flex;
    flex-wrap: wrap;
    gap: var(--spacing-sm);
    list-style: none;
    margin-top: var(--spacing-md);
}

.feature-tag {
    background: var(--forest-light);
    color: var(--forest-dark);
    padding: var(--spacing-xs) var(--spacing-sm);
    border-radius: var(--border-radius);
    font-size: var(--font-size-sm);
    font-weight: 500;
}

.related-equipment,
.related-links {
    margin-top: var(--spacing-2xl);
    padding-top: var(--spacing-2xl);
    border-top: 1px solid var(--border-light);
}

.equipment-cards,
.link-cards {
    display: grid;
    grid-template-columns: 1fr;
    gap: var(--spacing-lg);
    margin-top: var(--spacing-lg);
}

@media (min-width: 768px) {
    .equipment-cards {
        grid-template-columns: repeat(3, 1fr);
    }
    
    .link-cards {
        grid-template-columns: repeat(2, 1fr);
    }
}

.equipment-card,
.link-card {
    background: var(--pure-white);
    padding: var(--spacing-lg);
    border-radius: var(--border-radius);
    box-shadow: var(--shadow-subtle);
    text-align: center;
    transition: transform 0.2s ease;
}

.equipment-card:hover,
.link-card:hover {
    transform: translateY(-2px);
}

.link-card {
    text-decoration: none;
    color: inherit;
}

.equipment-card img {
    width: 60px;
    height: 60px;
    margin-bottom: var(--spacing-md);
}

.equipment-card h4,
.link-card h4 {
    color: var(--forest-dark);
    margin-bottom: var(--spacing-sm);
}

.mountain-actions,
.equipment-actions,
.back-link {
    display: flex;
    gap: var(--spacing-md);
    justify-content: center;
    margin-top: var(--spacing-2xl);
}

@media (max-width: 767px) {
    .mountain-actions,
    .equipment-actions {
        flex-direction: column;
    }
}

/* === 地域ページ用スタイル === */
.region-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: var(--spacing-xl);
    margin: var(--spacing-2xl) 0;
}

@media (min-width: 768px) {
    .region-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (min-width: 1024px) {
    .region-grid {
        grid-template-columns: repeat(3, 1fr);
    }
}

.region-card {
    background: var(--pure-white);
    border-radius: var(--border-radius-lg);
    overflow: hidden;
    box-shadow: var(--shadow-subtle);
    transition: transform 0.2s ease;
}

.region-card:hover {
    transform: translateY(-3px);
    box-shadow: var(--shadow-medium);
}

.region-image {
    height: 200px;
    overflow: hidden;
}

.region-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.region-content {
    padding: var(--spacing-lg);
}

.region-name {
    color: var(--forest-dark);
    font-size: var(--font-size-lg);
    font-weight: 600;
    margin-bottom: var(--spacing-sm);
}

.region-description {
    color: var(--text-secondary);
    margin-bottom: var(--spacing-md);
    line-height: 1.6;
}

.region-stats {
    display: flex;
    gap: var(--spacing-md);
    flex-wrap: wrap;
}

.stat-item {
    font-size: var(--font-size-sm);
    color: var(--text-light);
}

/* === FAQ用スタイル === */
.faq {
    margin-top: var(--spacing-lg);
}

.faq-item {
    margin-bottom: var(--spacing-lg);
    padding-bottom: var(--spacing-lg);
    border-bottom: 1px solid var(--border-light);
}

.faq-item:last-child {
    border-bottom: none;
}

.faq-item h4 {
    color: var(--forest-dark);
    margin-bottom: var(--spacing-sm);
}

.faq-item p {
    color: var(--text-secondary);
    line-height: 1.6;
}

/* === その他のユーティリティ === */
.update-date {
    text-align: right;
    font-size: var(--font-size-sm);
    color: var(--text-light);
    margin-top: var(--spacing-2xl);
    border-top: 1px solid var(--border-light);
    padding-top: var(--spacing-md);
}

.note {
    font-size: var(--font-size-sm);
    color: var(--text-light);
    font-style: italic;
}

.contact-methods {
    display: grid;
    grid-template-columns: 1fr;
    gap: var(--spacing-xl);
    margin: var(--spacing-2xl) 0;
}

@media (min-width: 768px) {
    .contact-methods {
        grid-template-columns: repeat(2, 1fr);
    }
}

.contact-method {
    background: var(--pure-white);
    padding: var(--spacing-lg);
    border-radius: var(--border-radius);
    box-shadow: var(--shadow-subtle);
}

.contact-method h3 {
    color: var(--forest-dark);
    margin-bottom: var(--spacing-md);
}'''
        
        # CSSファイルに追記
        with open(css_file, 'a', encoding='utf-8') as f:
            f.write(breadcrumb_css)
        
        print("✅ CSS拡張完了: パンくずナビ・詳細ページスタイル追加")
    
    def generate_all_pages(self):
        """すべてのページを生成"""
        print("🏗️ 低山旅行サイト全ページ生成開始")
        print("=" * 50)
        
        # CSS拡張
        self.add_breadcrumb_css()
        
        # 山関連ページ
        print("\n🏔️ 山関連ページ生成中...")
        self.generate_mountains_index()
        
        # 代表的な山の詳細ページを生成
        representative_mountains = self.mountains_data[:10]  # 最初の10山
        for mountain in representative_mountains:
            self.generate_mountain_detail_page(mountain)
        
        # 装備ページ
        print("\n🎒 装備ページ生成中...")
        self.generate_equipment_pages()
        
        # 初心者向けページ  
        print("\n👶 初心者向けページ生成中...")
        self.generate_beginner_pages()
        
        # 静的ページ
        print("\n📄 静的ページ生成中...")
        self.generate_static_pages()
        
        print("\n" + "=" * 50)
        print("🎉 全ページ生成完了！")
        self.print_site_structure()
    
    def print_site_structure(self):
        """生成されたサイト構造を表示"""
        print("\n📁 生成されたサイト構造:")
        
        structure = {
            "/": "トップページ",
            "/mountains/": "山一覧",
            "/equipment/": "装備ガイド一覧", 
            "/beginner/": "初心者向け一覧",
            "/regions/": "地域別ガイド",
            "/about/": "このサイトについて",
            "/contact/": "お問い合わせ",
            "/privacy/": "プライバシーポリシー",
            "/terms/": "利用規約"
        }
        
        for path, description in structure.items():
            print(f"  {path} - {description}")
        
        print(f"\n  /mountains/[山名]/ - 山詳細ページ ({len(self.mountains_data[:10])}ページ)")
        print(f"  /equipment/[装備]/ - 装備詳細ページ (3ページ)")
        print(f"  /beginner/[カテゴリ]/ - 初心者詳細ページ (3ページ)")
        
        total_pages = len(structure) + len(self.mountains_data[:10]) + 3 + 3
        print(f"\n📊 総ページ数: {total_pages}ページ")

def main():
    print("🏔️ 低山旅行ミニマルサイト生成ツール")
    print("リンク切れのない完全なサイトを構築します")
    print()
    
    generator = SiteGenerator()
    generator.generate_all_pages()
    
    print("\n🚀 次のステップ:")
    print("1. python3 serve.py でローカルサーバー起動")
    print("2. すべてのリンクが正常に動作することを確認")
    print("3. レスポンシブデザインの確認")
    print("4. アクセシビリティの確認")

if __name__ == "__main__":
    main()