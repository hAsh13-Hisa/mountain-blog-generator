#!/usr/bin/env python3
"""
サイトコンテンツ充実化スクリプト
- 47山すべてのページ作成
- ブログ記事として読み応えのあるコンテンツ追加
- 地域別ページの完成
"""

import json
import os
from pathlib import Path
from datetime import datetime

class ContentImprover:
    def __init__(self):
        self.base_dir = Path(__file__).parent
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
    
    def ensure_directory(self, path):
        """ディレクトリが存在しない場合は作成"""
        path.mkdir(parents=True, exist_ok=True)
    
    def calculate_paths(self, current_path):
        """現在のパスに基づいてルートパスを計算"""
        depth = len([p for p in current_path.parts if p not in ['', '.']])
        root_path = "../" * depth if depth > 0 else ""
        return root_path
    
    def create_all_mountain_pages(self):
        """47山すべてのページを作成"""
        print("⛰️ 全山ページ作成中...")
        
        created_count = 0
        for mountain in self.mountains_data:
            mountain_name = mountain.get('name', '不明な山')
            prefecture = mountain.get('prefecture', '不明')
            elevation = mountain.get('elevation', 0)
            difficulty = mountain.get('difficulty', {})
            location = mountain.get('location', {})
            features = mountain.get('features', [])
            seasons = mountain.get('seasons', {})
            
            # ディレクトリ作成
            mountain_dir = self.base_dir / "mountains" / mountain_name
            self.ensure_directory(mountain_dir)
            
            # 詳細なブログ記事コンテンツを生成
            detailed_content = self.generate_mountain_blog_content(mountain)
            
            # HTMLテンプレート
            html_content = f'''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{mountain_name}登山ガイド | 低山ハイキング完全攻略 - 低山旅行</title>
    <meta name="description" content="{prefecture}の{mountain_name}（標高{elevation}m）の登山ガイド。アクセス、コース詳細、季節情報、装備、安全対策まで初心者向けに詳しく解説。">
    
    <link rel="stylesheet" href="../../css/minimal_design.css">
    
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": "{mountain_name}登山ガイド",
        "description": "{prefecture}の{mountain_name}の詳細登山情報",
        "author": {{
            "@type": "Organization",
            "name": "低山旅行"
        }},
        "publisher": {{
            "@type": "Organization",
            "name": "低山旅行"
        }},
        "datePublished": "2025-01-05",
        "dateModified": "2025-01-05"
    }}
    </script>
</head>
<body>
    <!-- Skip Link -->
    <a href="#main-content" class="sr-only">メインコンテンツへスキップ</a>

    <!-- ヘッダー -->
    <header class="site-header">
        <div class="container">
            <div class="header-content">
                <div class="logo">
                    <a href="../../" aria-label="低山旅行 ホーム">
                        <span class="logo-icon">🏔️</span>
                        <span class="logo-text">低山旅行</span>
                    </a>
                </div>
                
                <nav class="main-nav" aria-label="メインナビゲーション">
                    <ul class="nav-menu">
                        <li><a href="../../mountains/">山を探す</a></li>
                        <li><a href="../../equipment/">装備ガイド</a></li>
                        <li><a href="../../beginner/">初心者向け</a></li>
                        <li><a href="../../regions/">地域別</a></li>
                    </ul>
                </nav>
                
                <button class="mobile-menu-toggle" aria-label="メニューを開く">
                    <span class="menu-line"></span>
                    <span class="menu-line"></span>
                    <span class="menu-line"></span>
                </button>
            </div>
        </div>
        
        <nav class="mobile-nav" aria-label="モバイルナビゲーション">
            <ul class="mobile-menu">
                <li><a href="../../mountains/">山を探す</a></li>
                <li><a href="../../equipment/">装備ガイド</a></li>
                <li><a href="../../beginner/">初心者向け</a></li>
                <li><a href="../../regions/">地域別</a></li>
            </ul>
        </nav>
    </header>

    <!-- メインコンテンツ -->
    <main id="main-content">
        <!-- パンくずナビ -->
        <nav class="breadcrumb section" aria-label="パンくずナビ">
            <div class="container">
                <ol class="breadcrumb-list">
                    <li><a href="../../">ホーム</a></li>
                    <li><a href="../../mountains/">山を探す</a></li>
                    <li aria-current="page">{mountain_name}</li>
                </ol>
            </div>
        </nav>

        <!-- 記事ヘッダー -->
        <article class="mountain-article">
            <header class="article-header section">
                <div class="container">
                    <h1 class="article-title">{mountain_name}登山ガイド</h1>
                    <p class="article-subtitle">
                        {prefecture}の美しい低山（標高{elevation}m）- {difficulty.get('level', '初級')}者向けハイキング
                    </p>
                    <div class="article-meta">
                        <span class="meta-item">📍 {prefecture}</span>
                        <span class="meta-item">📏 標高{elevation}m</span>
                        <span class="meta-item">⛰️ {difficulty.get('level', '初級')}</span>
                        <span class="meta-item">⏱️ {difficulty.get('hiking_time', '約1-2時間')}</span>
                    </div>
                </div>
            </header>

            {detailed_content}
        </article>
    </main>

    <!-- フッター -->
    <footer class="site-footer">
        <div class="container">
            <div class="footer-content">
                <div class="footer-section">
                    <h3>低山旅行</h3>
                    <p>安全で楽しい低山ハイキングを応援する専門サイト。初心者からファミリーまで、誰でも気軽に山歩きを楽しめる情報をお届けします。</p>
                </div>
                
                <div class="footer-section">
                    <h3>人気コンテンツ</h3>
                    <ul class="footer-links">
                        <li><a href="../../mountains/">山を探す</a></li>
                        <li><a href="../../equipment/">装備ガイド</a></li>
                        <li><a href="../../beginner/">初心者向け</a></li>
                        <li><a href="../../regions/">地域別ガイド</a></li>
                    </ul>
                </div>
                
                <div class="footer-section">
                    <h3>サイト情報</h3>
                    <ul class="footer-links">
                        <li><a href="../../about/">このサイトについて</a></li>
                        <li><a href="../../contact/">お問い合わせ</a></li>
                        <li><a href="../../privacy/">プライバシーポリシー</a></li>
                        <li><a href="../../terms/">利用規約</a></li>
                    </ul>
                </div>
            </div>
            
            <div class="footer-bottom">
                <p>&copy; 2025 低山旅行. All rights reserved.</p>
            </div>
        </div>
    </footer>

    <!-- JavaScript -->
    <script src="../../js/minimal.js"></script>
</body>
</html>'''
            
            # ファイル保存
            with open(mountain_dir / "index.html", 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            created_count += 1
        
        print(f"✅ {created_count}山のページを作成完了")
    
    def generate_mountain_blog_content(self, mountain):
        """山のブログ記事コンテンツを生成"""
        mountain_name = mountain.get('name', '不明な山')
        prefecture = mountain.get('prefecture', '不明')
        elevation = mountain.get('elevation', 0)
        difficulty = mountain.get('difficulty', {})
        location = mountain.get('location', {})
        features = mountain.get('features', [])
        seasons = mountain.get('seasons', {})
        
        # 特徴リスト生成
        features_html = ""
        if features:
            for feature in features[:8]:  # 最大8個
                features_html += f"<li class='feature-tag'>{feature}</li>"
        else:
            features_html = "<li class='feature-tag'>自然豊かな低山</li><li class='feature-tag'>初心者向け</li>"
        
        # 季節情報生成
        season_info = ""
        if seasons:
            best_seasons = seasons.get('best', ['春', '秋'])
            season_info = f"ベストシーズンは{'/'.join(best_seasons)}です。"
        else:
            season_info = "年間を通して楽しめる山です。"
        
        # アクセス情報
        access_info = location.get('access_time', '最寄り駅から徒歩・バスでアクセス可能')
        nearest_station = location.get('nearest_station', '要確認')
        
        return f'''
        <!-- 山の概要 -->
        <section class="section mountain-overview">
            <div class="container">
                <div class="mountain-content">
                    <div class="mountain-image">
                        <img src="../../images/hero_mountain_hiking.svg" 
                             alt="{mountain_name}の美しい山容" 
                             class="mountain-main-img">
                    </div>
                    
                    <div class="mountain-intro">
                        <h2>山の魅力</h2>
                        <p>{mountain_name}は{prefecture}に位置する標高{elevation}mの美しい低山です。{difficulty.get('level', '初級')}者向けのハイキングコースとして人気が高く、{difficulty.get('hiking_time', '約1-2時間')}で山頂を目指すことができます。</p>
                        
                        <p>この山の最大の魅力は、手軽にアクセスできる立地でありながら、山頂からは素晴らしい景色を楽しめることです。{season_info}</p>
                        
                        <div class="mountain-features">
                            <h3>この山の特徴</h3>
                            <ul class="feature-tags">
                                {features_html}
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- 登山コース詳細 -->
        <section class="section course-details">
            <div class="container">
                <h2 class="section-title">登山コース詳細</h2>
                
                <div class="course-grid">
                    <div class="course-card">
                        <h3>🚶‍♀️ メインコース</h3>
                        <ul class="course-info">
                            <li><strong>所要時間:</strong> {difficulty.get('hiking_time', '約1-2時間')}</li>
                            <li><strong>歩行距離:</strong> {difficulty.get('distance', '約3-5km')}</li>
                            <li><strong>標高差:</strong> {difficulty.get('elevation_gain', '約200-400m')}</li>
                            <li><strong>難易度:</strong> {difficulty.get('level', '初級')}</li>
                        </ul>
                        <p>最も一般的なルートで、整備された登山道を歩きます。初心者でも安心して登ることができ、要所要所に休憩ポイントがあります。</p>
                    </div>
                    
                    <div class="course-card">
                        <h3>📍 主要ポイント</h3>
                        <ul class="waypoint-list">
                            <li><strong>登山口:</strong> 駐車場・トイレ完備</li>
                            <li><strong>中間地点:</strong> 休憩ベンチあり</li>
                            <li><strong>山頂:</strong> 360度パノラマビュー</li>
                            <li><strong>下山路:</strong> 往路と同じ道を推奨</li>
                        </ul>
                    </div>
                </div>
            </div>
        </section>

        <!-- アクセス情報 -->
        <section class="section access-info">
            <div class="container">
                <h2 class="section-title">アクセス・駐車場情報</h2>
                
                <div class="access-grid">
                    <div class="access-card">
                        <h3>🚃 公共交通機関</h3>
                        <ul class="access-details">
                            <li><strong>最寄り駅:</strong> {nearest_station}</li>
                            <li><strong>駅からのアクセス:</strong> {access_info}</li>
                            <li><strong>所要時間:</strong> 駅から登山口まで徒歩15-30分程度</li>
                        </ul>
                        <p>公共交通機関を利用する場合は、事前に時刻表を確認しておくことをおすすめします。</p>
                    </div>
                    
                    <div class="access-card">
                        <h3>🚗 車でのアクセス</h3>
                        <ul class="access-details">
                            <li><strong>駐車場:</strong> 登山口付近に無料駐車場あり</li>
                            <li><strong>駐車台数:</strong> 約20-30台</li>
                            <li><strong>注意点:</strong> 週末は混雑する可能性があります</li>
                        </ul>
                        <p>早朝の出発がおすすめです。駐車場が満車の場合は、周辺の有料駐車場をご利用ください。</p>
                    </div>
                </div>
            </div>
        </section>

        <!-- 季節情報 -->
        <section class="section seasonal-info">
            <div class="container">
                <h2 class="section-title">季節別楽しみ方</h2>
                
                <div class="season-grid">
                    <div class="season-card">
                        <h3>🌸 春（3-5月）</h3>
                        <p>新緑の季節で、山全体が美しい緑に包まれます。野花も多く咲き、自然の息吹を感じながらハイキングが楽しめます。気温も穏やかで、初心者には最適の季節です。</p>
                    </div>
                    
                    <div class="season-card">
                        <h3>🌞 夏（6-8月）</h3>
                        <p>緑濃い森林浴が楽しめる季節です。朝早い時間帯の登山がおすすめ。水分補給をしっかりと行い、帽子や日焼け止めなどの暑さ対策を忘れずに。</p>
                    </div>
                    
                    <div class="season-card">
                        <h3>🍂 秋（9-11月）</h3>
                        <p>紅葉の美しい季節で、山が色とりどりに染まります。空気が澄んでいるため、山頂からの景色も一段と美しく見えます。最も人気の季節です。</p>
                    </div>
                    
                    <div class="season-card">
                        <h3>❄️ 冬（12-2月）</h3>
                        <p>雪景色が楽しめる場合もありますが、路面状況に注意が必要です。防寒対策をしっかりと行い、アイゼンなどの装備が必要な場合もあります。</p>
                    </div>
                </div>
            </div>
        </section>

        <!-- 推奨装備 -->
        <section class="section equipment-recommendation">
            <div class="container">
                <h2 class="section-title">推奨装備・持ち物</h2>
                
                <div class="equipment-categories">
                    <div class="equipment-category">
                        <h3>必須装備</h3>
                        <ul class="equipment-list">
                            <li>🎒 デイパック（20-30L）</li>
                            <li>👟 トレッキングシューズまたは運動靴</li>
                            <li>🧥 レインウェア（雨具）</li>
                            <li>💧 水分（1L以上推奨）</li>
                            <li>🍫 行動食（エネルギー補給用）</li>
                            <li>🗺️ 地図・コンパス</li>
                        </ul>
                    </div>
                    
                    <div class="equipment-category">
                        <h3>推奨装備</h3>
                        <ul class="equipment-list">
                            <li>🧢 帽子（日除け・防寒）</li>
                            <li>🧤 手袋（必要に応じて）</li>
                            <li>📱 携帯電話（緊急時連絡用）</li>
                            <li>🩹 簡易救急セット</li>
                            <li>🔦 ヘッドライト（日暮れ対策）</li>
                            <li>📷 カメラ（思い出作り）</li>
                        </ul>
                    </div>
                </div>
                
                <div class="equipment-links">
                    <h3>装備選びガイド</h3>
                    <p>登山装備の選び方について詳しく知りたい方は、以下のガイドをご参照ください。</p>
                    <div class="guide-links">
                        <a href="../../equipment/backpack/" class="btn btn-secondary">ザック選びガイド</a>
                        <a href="../../equipment/shoes/" class="btn btn-secondary">登山靴選びガイド</a>
                        <a href="../../equipment/rain/" class="btn btn-secondary">レインウェアガイド</a>
                    </div>
                </div>
            </div>
        </section>

        <!-- 安全対策 -->
        <section class="section safety-tips">
            <div class="container">
                <h2 class="section-title">安全対策・注意事項</h2>
                
                <div class="safety-grid">
                    <div class="safety-card important">
                        <h3>⚠️ 重要な注意事項</h3>
                        <ul class="safety-list">
                            <li>天候が悪化した場合は、無理をせず引き返しましょう</li>
                            <li>単独登山は避け、できるだけ複数人で登山しましょう</li>
                            <li>登山計画を家族や友人に伝えておきましょう</li>
                            <li>体調不良時の登山は避けましょう</li>
                        </ul>
                    </div>
                    
                    <div class="safety-card emergency">
                        <h3>🚨 緊急時の対応</h3>
                        <ul class="safety-list">
                            <li><strong>警察：</strong> 110番</li>
                            <li><strong>消防・救急：</strong> 119番</li>
                            <li><strong>山岳遭難：</strong> 各都道府県警察</li>
                            <li>怪我をした場合は、無理に動かず救助を要請</li>
                        </ul>
                    </div>
                </div>
                
                <div class="weather-info">
                    <h3>🌤️ 天候チェック</h3>
                    <p>登山前には必ず天気予報を確認しましょう。特に以下の場合は登山を中止することをおすすめします：</p>
                    <ul class="weather-warnings">
                        <li>降水確率が50%以上の場合</li>
                        <li>強風注意報・警報が発令されている場合</li>
                        <li>雷注意報が発令されている場合</li>
                        <li>気温が極端に高い・低い場合</li>
                    </ul>
                </div>
            </div>
        </section>

        <!-- 周辺情報 -->
        <section class="section surrounding-info">
            <div class="container">
                <h2 class="section-title">周辺施設・観光情報</h2>
                
                <div class="surrounding-grid">
                    <div class="surrounding-card">
                        <h3>🍽️ グルメ・食事</h3>
                        <p>登山後の楽しみの一つが、地元のグルメです。{prefecture}の郷土料理や、登山口周辺の食堂で美味しい食事を楽しみましょう。</p>
                        <ul class="facility-list">
                            <li>登山口周辺の食堂・レストラン</li>
                            <li>地元特産品を使った料理</li>
                            <li>道の駅での軽食・お土産</li>
                        </ul>
                    </div>
                    
                    <div class="surrounding-card">
                        <h3>♨️ 温泉・入浴施設</h3>
                        <p>登山で疲れた体を癒すには、温泉が一番です。周辺の入浴施設で汗を流し、リフレッシュしましょう。</p>
                        <ul class="facility-list">
                            <li>日帰り温泉施設</li>
                            <li>銭湯・公衆浴場</li>
                            <li>宿泊可能な温泉旅館</li>
                        </ul>
                    </div>
                    
                    <div class="surrounding-card">
                        <h3>🏛️ 観光スポット</h3>
                        <p>{mountain_name}周辺には、歴史的な名所や自然スポットが数多くあります。登山と合わせて観光も楽しみましょう。</p>
                        <ul class="facility-list">
                            <li>歴史的建造物・神社仏閣</li>
                            <li>自然公園・展望台</li>
                            <li>博物館・資料館</li>
                        </ul>
                    </div>
                </div>
            </div>
        </section>

        <!-- まとめ -->
        <section class="section mountain-summary">
            <div class="container">
                <h2 class="section-title">まとめ</h2>
                <div class="summary-content">
                    <p>{mountain_name}は、{prefecture}を代表する美しい低山の一つです。標高{elevation}mという手頃な高さでありながら、山頂からの景色は格別で、登山の喜びを十分に味わうことができます。</p>
                    
                    <p>{difficulty.get('level', '初級')}者向けのコースが整備されており、{difficulty.get('hiking_time', '約1-2時間')}という短時間で登頂できるため、登山初心者や家族連れにも最適です。四季を通じて異なる魅力があり、何度訪れても新しい発見があることでしょう。</p>
                    
                    <p>安全に楽しく登山を行うため、適切な装備と準備を心がけ、天候や体調に十分注意して山行を計画してください。{mountain_name}での素晴らしい登山体験が、皆様の山への愛を深めるきっかけとなることを願っています。</p>
                </div>
                
                <div class="action-buttons">
                    <a href="../../mountains/" class="btn btn-secondary">
                        ← 他の山を探す
                    </a>
                    <a href="../../beginner/" class="btn btn-primary">
                        初心者ガイドを読む
                    </a>
                </div>
            </div>
        </section>
        '''
    
    def update_mountains_index(self):
        """山一覧ページを47山すべて表示するよう更新"""
        print("📝 山一覧ページ更新中...")
        
        mountains_dir = self.base_dir / "mountains"
        
        # 山カードを生成（全47山）
        mountain_cards = ""
        for mountain in self.mountains_data:
            mountain_name = mountain.get('name', '不明な山')
            prefecture = mountain.get('prefecture', '不明')
            elevation = mountain.get('elevation', 0)
            difficulty = mountain.get('difficulty', {}).get('level', '初級')
            
            # 説明文を生成
            description = f"{prefecture}の美しい低山。標高{elevation}mで{difficulty}者向けのハイキングコースです。"
            if len(mountain.get('features', [])) > 0:
                main_feature = mountain['features'][0]
                description += f"{main_feature}が特徴的です。"
            
            mountain_cards += f'''
            <article class="card">
                <div class="card-image">
                    <img src="../images/hero_mountain_hiking.svg" 
                         alt="{mountain_name}のイラスト" 
                         class="card-img"
                         onerror="this.src='../images/hero_mountain_hiking.svg'">
                </div>
                <div class="card-content">
                    <h3 class="card-title">{mountain_name}</h3>
                    <div class="card-meta">
                        <span>📍 {prefecture}</span>
                        <span>📏 標高{elevation}m</span>
                        <span>⛰️ {difficulty}</span>
                    </div>
                    <p class="card-description">
                        {description}
                    </p>
                    <a href="../mountains/{mountain_name}/" class="btn btn-secondary btn-small">
                        詳細を見る
                    </a>
                </div>
            </article>
            '''
        
        content = f'''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>山を探す | 全国47都道府県の低山一覧 - 低山旅行</title>
    <meta name="description" content="全国47都道府県の低山を完全網羅。初心者・ファミリー向けの安全でアクセス良好な低山{len(self.mountains_data)}座をご紹介。標高、難易度、アクセス情報を詳しく解説。">
    
    <link rel="stylesheet" href="../css/minimal_design.css">
    
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "山を探す",
        "description": "全国47都道府県の低山一覧",
        "url": "https://teizan.omasse.com/mountains/"
    }}
    </script>
</head>
<body>
    <!-- Skip Link -->
    <a href="#main-content" class="sr-only">メインコンテンツへスキップ</a>

    <!-- ヘッダー -->
    <header class="site-header">
        <div class="container">
            <div class="header-content">
                <div class="logo">
                    <a href="../" aria-label="低山旅行 ホーム">
                        <span class="logo-icon">🏔️</span>
                        <span class="logo-text">低山旅行</span>
                    </a>
                </div>
                
                <nav class="main-nav" aria-label="メインナビゲーション">
                    <ul class="nav-menu">
                        <li><a href="../mountains/">山を探す</a></li>
                        <li><a href="../equipment/">装備ガイド</a></li>
                        <li><a href="../beginner/">初心者向け</a></li>
                        <li><a href="../regions/">地域別</a></li>
                    </ul>
                </nav>
                
                <button class="mobile-menu-toggle" aria-label="メニューを開く">
                    <span class="menu-line"></span>
                    <span class="menu-line"></span>
                    <span class="menu-line"></span>
                </button>
            </div>
        </div>
        
        <nav class="mobile-nav" aria-label="モバイルナビゲーション">
            <ul class="mobile-menu">
                <li><a href="../mountains/">山を探す</a></li>
                <li><a href="../equipment/">装備ガイド</a></li>
                <li><a href="../beginner/">初心者向け</a></li>
                <li><a href="../regions/">地域別</a></li>
            </ul>
        </nav>
    </header>

    <!-- メインコンテンツ -->
    <main id="main-content">
        <section class="section">
            <div class="container">
                <header class="section-header">
                    <h1 class="section-title">山を探す</h1>
                    <p class="section-subtitle">
                        全国47都道府県の厳選低山{len(self.mountains_data)}座を完全網羅。初心者・ファミリー向けの安全な山をご紹介します。
                    </p>
                    <div class="stats-summary">
                        <div class="stat-item">
                            <span class="stat-number">{len(self.mountains_data)}</span>
                            <span class="stat-label">座の低山</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-number">47</span>
                            <span class="stat-label">都道府県対応</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-number">400m</span>
                            <span class="stat-label">以下の標高</span>
                        </div>
                    </div>
                </header>
                
                <div class="card-grid">
                    {mountain_cards}
                </div>
                
                <div class="text-center">
                    <p class="section-subtitle">すべての山に詳細な登山ガイドをご用意しています</p>
                    <a href="../beginner/" class="btn btn-primary">
                        初心者ガイドを読む
                    </a>
                </div>
            </div>
        </section>
    </main>

    <!-- フッター -->
    <footer class="site-footer">
        <div class="container">
            <div class="footer-content">
                <div class="footer-section">
                    <h3>低山旅行</h3>
                    <p>安全で楽しい低山ハイキングを応援する専門サイト。初心者からファミリーまで、誰でも気軽に山歩きを楽しめる情報をお届けします。</p>
                </div>
                
                <div class="footer-section">
                    <h3>人気コンテンツ</h3>
                    <ul class="footer-links">
                        <li><a href="../mountains/">山を探す</a></li>
                        <li><a href="../equipment/">装備ガイド</a></li>
                        <li><a href="../beginner/">初心者向け</a></li>
                        <li><a href="../regions/">地域別ガイド</a></li>
                    </ul>
                </div>
                
                <div class="footer-section">
                    <h3>サイト情報</h3>
                    <ul class="footer-links">
                        <li><a href="../about/">このサイトについて</a></li>
                        <li><a href="../contact/">お問い合わせ</a></li>
                        <li><a href="../privacy/">プライバシーポリシー</a></li>
                        <li><a href="../terms/">利用規約</a></li>
                    </ul>
                </div>
            </div>
            
            <div class="footer-bottom">
                <p>&copy; 2025 低山旅行. All rights reserved.</p>
            </div>
        </div>
    </footer>

    <!-- JavaScript -->
    <script src="../js/minimal.js"></script>
</body>
</html>'''
        
        with open(mountains_dir / "index.html", 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 山一覧ページ更新完了（{len(self.mountains_data)}山）")
    
    def improve_beginner_content(self):
        """初心者向けページの内容を充実化"""
        print("👶 初心者向けページ充実化中...")
        
        beginner_pages = {
            "basics": {
                "title": "低山ハイキング基礎知識",
                "description": "低山ハイキングを始める前に知っておきたい基本知識",
                "content": self.get_basics_content()
            },
            "safety": {
                "title": "安全対策完全ガイド", 
                "description": "事故を防ぐための基本的な安全対策と緊急時の対処法",
                "content": self.get_safety_content()
            },
            "family": {
                "title": "ファミリーハイキング完全ガイド",
                "description": "子供と一緒に楽しむ低山ハイキングのコツと注意点",
                "content": self.get_family_content()
            }
        }
        
        for page_id, page_info in beginner_pages.items():
            self.create_detailed_beginner_page(page_id, page_info)
        
        print("✅ 初心者向けページ充実化完了")
    
    def get_basics_content(self):
        """基礎知識ページのコンテンツ"""
        return '''
        <!-- 低山ハイキングとは -->
        <section class="section basics-intro">
            <div class="container">
                <h2 class="section-title">低山ハイキングとは</h2>
                
                <div class="intro-content">
                    <div class="intro-text">
                        <p>低山ハイキングとは、標高1000m以下の山を登るアクティビティです。本格的な登山装備や技術を必要とせず、日帰りで気軽に楽しめることが最大の魅力です。</p>
                        
                        <p>都市部からアクセスしやすい場所にある山が多く、週末の日帰り旅行として最適です。体力に自信がない方や登山初心者、小さなお子様連れのファミリーでも安心して楽しめます。</p>
                        
                        <h3>低山ハイキングの魅力</h3>
                        <ul class="benefits-list">
                            <li><strong>気軽さ:</strong> 特別な技術や装備が不要</li>
                            <li><strong>安全性:</strong> 遭難リスクが低く、救助も容易</li>
                            <li><strong>アクセス:</strong> 都市部から日帰りで行ける</li>
                            <li><strong>四季の楽しみ:</strong> 季節ごとに異なる表情を見せる</li>
                            <li><strong>健康効果:</strong> 適度な運動で心身をリフレッシュ</li>
                            <li><strong>コスト:</strong> 高額な装備投資が不要</li>
                        </ul>
                    </div>
                </div>
            </div>
        </section>

        <!-- 準備するもの -->
        <section class="section equipment-basics">
            <div class="container">
                <h2 class="section-title">基本装備・持ち物</h2>
                
                <div class="equipment-levels">
                    <div class="equipment-level">
                        <h3>🔴 必須装備（絶対に必要）</h3>
                        <div class="equipment-grid">
                            <div class="equipment-item">
                                <h4>🎒 デイパック（20-30L）</h4>
                                <p>日帰りハイキングに最適なサイズ。水分や食料、雨具などを収納します。背負いやすさを重視して選びましょう。</p>
                            </div>
                            <div class="equipment-item">
                                <h4>👟 適切な靴</h4>
                                <p>トレッキングシューズが理想ですが、運動靴でも可能。滑りにくく、足首をサポートするものを選びましょう。</p>
                            </div>
                            <div class="equipment-item">
                                <h4>🧥 レインウェア</h4>
                                <p>山の天気は変わりやすいため必携。上下セパレートタイプがおすすめです。</p>
                            </div>
                            <div class="equipment-item">
                                <h4>💧 水分（1L以上）</h4>
                                <p>脱水症状を防ぐため、十分な水分を携帯しましょう。スポーツドリンクもおすすめです。</p>
                            </div>
                        </div>
                    </div>
                    
                    <div class="equipment-level">
                        <h3>🟡 推奨装備（あると便利）</h3>
                        <div class="equipment-simple-list">
                            <ul>
                                <li><strong>🧢 帽子:</strong> 日除けや防寒、怪我防止に</li>
                                <li><strong>🧤 手袋:</strong> 岩場や寒い季節に</li>
                                <li><strong>🍫 行動食:</strong> エネルギー補給用のお菓子やナッツ</li>
                                <li><strong>🗺️ 地図:</strong> スマホアプリでも可</li>
                                <li><strong>🔦 ヘッドライト:</strong> 日暮れ対策</li>
                                <li><strong>🩹 救急セット:</strong> 絆創膏や痛み止めなど</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- 計画の立て方 -->
        <section class="section planning-basics">
            <div class="container">
                <h2 class="section-title">登山計画の立て方</h2>
                
                <div class="planning-steps">
                    <div class="planning-step">
                        <div class="step-number">1</div>
                        <div class="step-content">
                            <h3>山選び</h3>
                            <p>初回は標高300m以下、登山時間2時間以内の山を選びましょう。アクセスが良く、登山道が整備された人気の山がおすすめです。</p>
                            <ul class="tips-list">
                                <li>地元の低山から始める</li>
                                <li>口コミや評判を調べる</li>
                                <li>駐車場の有無を確認</li>
                            </ul>
                        </div>
                    </div>
                    
                    <div class="planning-step">
                        <div class="step-number">2</div>
                        <div class="step-content">
                            <h3>天気確認</h3>
                            <p>登山の3日前から天気予報をチェックし、当日朝にも最終確認をしましょう。雨や強風の予報が出ている場合は延期を検討してください。</p>
                            <ul class="tips-list">
                                <li>降水確率30%以下が理想</li>
                                <li>風速や気温もチェック</li>
                                <li>山の天気は変わりやすいことを考慮</li>
                            </ul>
                        </div>
                    </div>
                    
                    <div class="planning-step">
                        <div class="step-number">3</div>
                        <div class="step-content">
                            <h3>タイムスケジュール</h3>
                            <p>余裕のあるスケジュールを組みましょう。標準コースタイムの1.5倍程度で計画し、16時までには下山完了を目指してください。</p>
                            <ul class="tips-list">
                                <li>早朝出発（6-7時スタート）</li>
                                <li>休憩時間を多めに取る</li>
                                <li>日没時間を考慮する</li>
                            </ul>
                        </div>
                    </div>
                    
                    <div class="planning-step">
                        <div class="step-number">4</div>
                        <div class="step-content">
                            <h3>家族への連絡</h3>
                            <p>登山計画を家族や友人に必ず伝えておきましょう。行き先、メンバー、帰宅予定時刻を明確にし、緊急時の連絡先も共有してください。</p>
                            <ul class="tips-list">
                                <li>登山届（可能な場合）</li>
                                <li>緊急連絡先の確認</li>
                                <li>帰宅予定時刻の設定</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- 歩き方の基本 -->
        <section class="section walking-basics">
            <div class="container">
                <h2 class="section-title">安全な歩き方</h2>
                
                <div class="walking-techniques">
                    <div class="technique-card">
                        <h3>👣 基本的な歩き方</h3>
                        <ul class="technique-list">
                            <li><strong>歩幅を小さく:</strong> 疲労を軽減し、バランスを保ちやすい</li>
                            <li><strong>足裏全体で踏む:</strong> 安定感が増し、滑りにくくなる</li>
                            <li><strong>一定のリズム:</strong> 無理のないペースを維持する</li>
                            <li><strong>前を見る:</strong> 足元だけでなく、進行方向も確認</li>
                        </ul>
                    </div>
                    
                    <div class="technique-card">
                        <h3>⬆️ 登りのコツ</h3>
                        <ul class="technique-list">
                            <li><strong>ゆっくり登る:</strong> 息が上がらない程度のペース</li>
                            <li><strong>ジグザグ歩行:</strong> 急斜面では九の字に歩く</li>
                            <li><strong>休憩を多く:</strong> 15-20分に一度は休憩</li>
                            <li><strong>水分補給:</strong> のどが渇く前に飲む</li>
                        </ul>
                    </div>
                    
                    <div class="technique-card">
                        <h3>⬇️ 下りのコツ</h3>
                        <ul class="technique-list">
                            <li><strong>膝を軽く曲げる:</strong> 衝撃を和らげる</li>
                            <li><strong>かかとから着地:</strong> 重心を後ろに保つ</li>
                            <li><strong>スピードを抑える:</strong> 転倒防止のため慎重に</li>
                            <li><strong>ストックを活用:</strong> バランス補助に</li>
                        </ul>
                    </div>
                </div>
            </div>
        </section>

        <!-- よくある質問 -->
        <section class="section faq-section">
            <div class="container">
                <h2 class="section-title">よくある質問</h2>
                
                <div class="faq-list">
                    <div class="faq-item">
                        <h3>Q: 運動不足でも低山ハイキングはできますか？</h3>
                        <p>A: はい、可能です。低山ハイキングは適度な運動として最適です。最初は短時間・低標高の山から始めて、徐々に体力をつけていきましょう。無理をせず、自分のペースで楽しむことが大切です。</p>
                    </div>
                    
                    <div class="faq-item">
                        <h3>Q: 一人で登山しても大丈夫ですか？</h3>
                        <p>A: 低山であっても、できるだけ複数人での登山をおすすめします。一人で行く場合は、人気のある山を選び、登山計画を家族に伝え、携帯電話の電波状況を事前に確認してください。</p>
                    </div>
                    
                    <div class="faq-item">
                        <h3>Q: 雨が降ってきた場合はどうすればいいですか？</h3>
                        <p>A: すぐにレインウェアを着用し、安全な場所で天候の回復を待ちましょう。雨が強くなったり雷の危険がある場合は、無理をせず下山することを検討してください。</p>
                    </div>
                    
                    <div class="faq-item">
                        <h3>Q: どのくらいの頻度で登山すればいいですか？</h3>
                        <p>A: 個人の体力や時間に合わせて調整してください。月1-2回程度から始めて、慣れてきたら頻度を増やしても良いでしょう。継続することが最も大切です。</p>
                    </div>
                </div>
            </div>
        </section>
        '''
    
    def get_safety_content(self):
        """安全対策ページのコンテンツ"""
        return '''
        <!-- 安全対策の重要性 -->
        <section class="section safety-importance">
            <div class="container">
                <h2 class="section-title">なぜ安全対策が必要なのか</h2>
                
                <div class="importance-content">
                    <p>低山だからといって油断は禁物です。標高が低くても、滑落、迷子、体調不良などのリスクは存在します。適切な準備と知識があれば、これらのリスクを大幅に減らすことができます。</p>
                    
                    <div class="risk-categories">
                        <div class="risk-card">
                            <h3>⚠️ 主要なリスク</h3>
                            <ul class="risk-list">
                                <li>滑落・転倒による怪我</li>
                                <li>道迷い・遭難</li>
                                <li>天候急変への対応不足</li>
                                <li>体調不良・疲労</li>
                                <li>装備不足による事故</li>
                            </ul>
                        </div>
                        
                        <div class="risk-card">
                            <h3>✅ 予防策</h3>
                            <ul class="prevention-list">
                                <li>適切な装備の準備</li>
                                <li>天気予報の確認</li>
                                <li>体調管理と無理のない計画</li>
                                <li>地図・コンパスの携帯</li>
                                <li>登山計画の共有</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- 事前準備 -->
        <section class="section pre-preparation">
            <div class="container">
                <h2 class="section-title">登山前の安全準備</h2>
                
                <div class="preparation-checklist">
                    <div class="prep-category">
                        <h3>📋 情報収集チェックリスト</h3>
                        <ul class="checklist">
                            <li class="check-item">
                                <input type="checkbox" id="weather-check">
                                <label for="weather-check">天気予報の確認（3日前〜当日朝）</label>
                            </li>
                            <li class="check-item">
                                <input type="checkbox" id="route-check">
                                <label for="route-check">登山ルートの事前調査</label>
                            </li>
                            <li class="check-item">
                                <input type="checkbox" id="time-check">
                                <label for="time-check">標準コースタイムの確認</label>
                            </li>
                            <li class="check-item">
                                <input type="checkbox" id="access-check">
                                <label for="access-check">アクセス方法・駐車場の確認</label>
                            </li>
                            <li class="check-item">
                                <input type="checkbox" id="facility-check">
                                <label for="facility-check">トイレ・水場の位置確認</label>
                            </li>
                        </ul>
                    </div>
                    
                    <div class="prep-category">
                        <h3>🎒 装備チェックリスト</h3>
                        <ul class="checklist">
                            <li class="check-item">
                                <input type="checkbox" id="backpack-check">
                                <label for="backpack-check">デイパック（20-30L）</label>
                            </li>
                            <li class="check-item">
                                <input type="checkbox" id="shoes-check">
                                <label for="shoes-check">トレッキングシューズ/運動靴</label>
                            </li>
                            <li class="check-item">
                                <input type="checkbox" id="rain-check">
                                <label for="rain-check">レインウェア（上下）</label>
                            </li>
                            <li class="check-item">
                                <input type="checkbox" id="water-check">
                                <label for="water-check">水分（1L以上）</label>
                            </li>
                            <li class="check-item">
                                <input type="checkbox" id="food-check">
                                <label for="food-check">行動食・昼食</label>
                            </li>
                            <li class="check-item">
                                <input type="checkbox" id="light-check">
                                <label for="light-check">ヘッドライト・予備電池</label>
                            </li>
                            <li class="check-item">
                                <input type="checkbox" id="first-aid-check">
                                <label for="first-aid-check">救急セット</label>
                            </li>
                            <li class="check-item">
                                <input type="checkbox" id="map-check">
                                <label for="map-check">地図・コンパス</label>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </section>

        <!-- 登山中の安全対策 -->
        <section class="section during-hiking">
            <div class="container">
                <h2 class="section-title">登山中の安全対策</h2>
                
                <div class="safety-during">
                    <div class="safety-rule">
                        <h3>🚶‍♀️ 歩行時の注意点</h3>
                        <div class="rule-content">
                            <ul class="safety-tips">
                                <li><strong>一列歩行:</strong> 狭い道では前後に間隔を空けて歩く</li>
                                <li><strong>声かけ:</strong> 「落石注意」「追い越します」など周囲への配慮</li>
                                <li><strong>ペース配分:</strong> 最も体力のない人に合わせる</li>
                                <li><strong>足元確認:</strong> 浮石や滑りやすい場所に注意</li>
                                <li><strong>三点支持:</strong> 岩場では手足のうち三点で体を支える</li>
                            </ul>
                        </div>
                    </div>
                    
                    <div class="safety-rule">
                        <h3>🌧️ 天候変化への対応</h3>
                        <div class="rule-content">
                            <h4>雨が降り始めたら</h4>
                            <ol class="response-steps">
                                <li>速やかにレインウェアを着用</li>
                                <li>滑りやすい場所を避けて安全な場所へ移動</li>
                                <li>雨脚が強くなったら一時避難を検討</li>
                                <li>雷の危険がある場合は即座に下山</li>
                            </ol>
                            
                            <h4>風が強くなったら</h4>
                            <ol class="response-steps">
                                <li>稜線や尾根では特に注意</li>
                                <li>帽子やタオルが飛ばされないよう固定</li>
                                <li>バランスを崩しやすいので慎重に歩行</li>
                                <li>強風警報時は登山中止を検討</li>
                            </ol>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- 緊急時の対応 -->
        <section class="section emergency-response">
            <div class="container">
                <h2 class="section-title">緊急時の対応方法</h2>
                
                <div class="emergency-scenarios">
                    <div class="emergency-card urgent">
                        <h3>🚨 怪我をした場合</h3>
                        <div class="emergency-steps">
                            <h4>軽傷の場合</h4>
                            <ol class="emergency-list">
                                <li>安全な場所に移動し、傷口を清潔にする</li>
                                <li>消毒液で処置し、絆創膏で保護</li>
                                <li>痛みが強い場合は無理をせず下山</li>
                                <li>下山後は医療機関を受診</li>
                            </ol>
                            
                            <h4>重傷の場合</h4>
                            <ol class="emergency-list">
                                <li>無理に動かさず、その場で応急処置</li>
                                <li>110番（警察）または119番（消防・救急）に通報</li>
                                <li>現在地を正確に伝える（山名、登山口からの距離など）</li>
                                <li>救助隊の到着まで体温保持と安静を保つ</li>
                            </ol>
                        </div>
                    </div>
                    
                    <div class="emergency-card warning">
                        <h3>🧭 道に迷った場合</h3>
                        <div class="emergency-steps">
                            <ol class="emergency-list">
                                <li><strong>止まる:</strong> むやみに歩き回らない</li>
                                <li><strong>冷静になる:</strong> パニックにならず現状把握</li>
                                <li><strong>地図確認:</strong> 現在地と正しいルートを確認</li>
                                <li><strong>引き返す:</strong> 確実にわかる場所まで戻る</li>
                                <li><strong>通報:</strong> 自力で解決できない場合は110番</li>
                            </ol>
                            
                            <div class="lost-prevention">
                                <h4>道迷いを防ぐには</h4>
                                <ul class="prevention-tips">
                                    <li>登山前に地図でルートを確認</li>
                                    <li>分岐点では必ず地図で現在地確認</li>
                                    <li>GPSアプリの活用（YAMAP、ヤマレコなど）</li>
                                    <li>目印となる地形や建物を覚えておく</li>
                                </ul>
                            </div>
                        </div>
                    </div>
                    
                    <div class="emergency-card info">
                        <h3>📱 緊急連絡先</h3>
                        <div class="contact-info">
                            <ul class="contact-list">
                                <li><strong>警察（山岳遭難）:</strong> 110番</li>
                                <li><strong>消防・救急:</strong> 119番</li>
                                <li><strong>海上保安庁:</strong> 118番</li>
                            </ul>
                            
                            <div class="contact-tips">
                                <h4>通報時に伝える情報</h4>
                                <ul class="info-list">
                                    <li>山名と登山ルート</li>
                                    <li>現在地（目標となる地形など）</li>
                                    <li>負傷者の人数と容態</li>
                                    <li>通報者の連絡先</li>
                                    <li>天候状況</li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- 予防策 -->
        <section class="section prevention-measures">
            <div class="container">
                <h2 class="section-title">事故を防ぐための心構え</h2>
                
                <div class="prevention-grid">
                    <div class="prevention-card">
                        <h3>💪 体調管理</h3>
                        <ul class="prevention-list">
                            <li>前日は十分な睡眠を取る</li>
                            <li>体調不良時は登山を中止</li>
                            <li>持病がある場合は事前に医師に相談</li>
                            <li>薬を服用中の場合は携帯</li>
                            <li>アルコールは登山前日から控える</li>
                        </ul>
                    </div>
                    
                    <div class="prevention-card">
                        <h3>👥 グループ登山</h3>
                        <ul class="prevention-list">
                            <li>可能な限り複数人で登山する</li>
                            <li>メンバーの体力レベルを把握</li>
                            <li>リーダーを決めて責任体制を明確化</li>
                            <li>全員で装備チェックを行う</li>
                            <li>緊急時の役割分担を決めておく</li>
                        </ul>
                    </div>
                    
                    <div class="prevention-card">
                        <h3>⏰ 時間管理</h3>
                        <ul class="prevention-list">
                            <li>余裕のある計画を立てる</li>
                            <li>16時までに下山完了を目指す</li>
                            <li>定期的に時間をチェック</li>
                            <li>遅れている場合は計画変更も検討</li>
                            <li>日没時間を必ず確認</li>
                        </ul>
                    </div>
                    
                    <div class="prevention-card">
                        <h3>🌡️ 環境把握</h3>
                        <ul class="prevention-list">
                            <li>気温の変化に対応できる服装</li>
                            <li>季節特有のリスクを理解</li>
                            <li>地域特有の注意点を調査</li>
                            <li>野生動物の生息情報確認</li>
                            <li>登山道の最新状況確認</li>
                        </ul>
                    </div>
                </div>
            </div>
        </section>
        '''
    
    def get_family_content(self):
        """ファミリー向けページのコンテンツ"""
        return '''
        <!-- ファミリーハイキングの魅力 -->
        <section class="section family-intro">
            <div class="container">
                <h2 class="section-title">ファミリーハイキングの魅力</h2>
                
                <div class="family-benefits">
                    <div class="benefit-card">
                        <h3>👨‍👩‍👧‍👦 家族の絆深まる</h3>
                        <p>一緒に目標を達成する喜びを共有し、普段とは違う環境で家族の新たな一面を発見できます。自然の中での体験は、家族の大切な思い出となります。</p>
                    </div>
                    
                    <div class="benefit-card">
                        <h3>🌱 子供の成長促進</h3>
                        <p>自然との触れ合いは子供の感性を豊かにし、体力向上や危険回避能力の向上にもつながります。困難を乗り越える経験は自信にもなります。</p>
                    </div>
                    
                    <div class="benefit-card">
                        <h3>💚 健康的な運動</h3>
                        <p>ゲームやスマホから離れ、家族全員で健康的な運動ができます。新鮮な空気を吸いながらの運動は、心身ともにリフレッシュできます。</p>
                    </div>
                    
                    <div class="benefit-card">
                        <h3>🎓 自然教育</h3>
                        <p>植物や動物、地形について学ぶ生きた教材として最適です。季節の変化や環境について、体験を通して学習できます。</p>
                    </div>
                </div>
            </div>
        </section>

        <!-- 年齢別ガイド -->
        <section class="section age-guide">
            <div class="container">
                <h2 class="section-title">年齢別ガイド</h2>
                
                <div class="age-categories">
                    <div class="age-card">
                        <h3>👶 3-5歳（幼児）</h3>
                        <div class="age-content">
                            <h4>特徴・注意点</h4>
                            <ul class="age-tips">
                                <li>体力が限られているため短時間・短距離コース</li>
                                <li>飽きやすいため楽しい要素を盛り込む</li>
                                <li>安全管理が最重要（常に手を繋ぐ）</li>
                                <li>お昼寝タイムを考慮した計画</li>
                            </ul>
                            
                            <h4>おすすめコース</h4>
                            <ul class="course-suggestions">
                                <li>歩行時間30分-1時間以内</li>
                                <li>舗装路または平坦な土の道</li>
                                <li>遊具や展望台がある山</li>
                                <li>車でのアクセスが容易な場所</li>
                            </ul>
                        </div>
                    </div>
                    
                    <div class="age-card">
                        <h3>🧒 6-9歳（小学校低学年）</h3>
                        <div class="age-content">
                            <h4>特徴・注意点</h4>
                            <ul class="age-tips">
                                <li>体力がついてくるが個人差が大きい</li>
                                <li>好奇心旺盛で危険な場所にも興味を示す</li>
                                <li>達成感を感じられる適度な挑戦が重要</li>
                                <li>疲れたときの対処法を準備</li>
                            </ul>
                            
                            <h4>おすすめコース</h4>
                            <ul class="course-suggestions">
                                <li>歩行時間1-2時間程度</li>
                                <li>軽い登り下りがある山道</li>
                                <li>動植物観察ができる自然豊かなコース</li>
                                <li>山頂で景色が楽しめる山</li>
                            </ul>
                        </div>
                    </div>
                    
                    <div class="age-card">
                        <h3>👦 10-12歳（小学校高学年）</h3>
                        <div class="age-content">
                            <h4>特徴・注意点</h4>
                            <ul class="age-tips">
                                <li>体力が大幅に向上し、大人並みのコースも可能</li>
                                <li>自立心が芽生え、責任を持たせることが大切</li>
                                <li>地図読みなどの技術も教えられる</li>
                                <li>友達同士での参加も楽しい</li>
                            </ul>
                            
                            <h4>おすすめコース</h4>
                            <ul class="course-suggestions">
                                <li>歩行時間2-3時間程度</li>
                                <li>軽度の岩場やチェーンコースも体験</li>
                                <li>歴史的な背景がある山</li>
                                <li>地図とコンパスを使った簡単なナビゲーション</li>
                            </ul>
                        </div>
                    </div>
                    
                    <div class="age-card">
                        <h3>👨‍🎓 13歳以上（中学生以上）</h3>
                        <div class="age-content">
                            <h4>特徴・注意点</h4>
                            <ul class="age-tips">
                                <li>大人とほぼ同等の体力と判断力</li>
                                <li>登山の楽しさを理解し、自主的な参加</li>
                                <li>安全管理の知識も身につけられる</li>
                                <li>将来の登山パートナーとして育成</li>
                            </ul>
                            
                            <h4>おすすめコース</h4>
                            <ul class="course-suggestions">
                                <li>歩行時間3-4時間程度</li>
                                <li>本格的な登山技術を要するコース</li>
                                <li>テント泊や山小屋泊も検討</li>
                                <li>登山計画の立案から参加</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- 子供向け装備 -->
        <section class="section kids-equipment">
            <div class="container">
                <h2 class="section-title">子供向け装備ガイド</h2>
                
                <div class="equipment-categories">
                    <div class="equipment-category">
                        <h3>👶 必須装備（子供用）</h3>
                        <div class="equipment-grid">
                            <div class="equipment-item">
                                <h4>🎒 子供用ザック</h4>
                                <ul class="equipment-details">
                                    <li>5-15L程度の小さめサイズ</li>
                                    <li>子供自身の飲み物とおやつを入れる</li>
                                    <li>背負うことで責任感を育てる</li>
                                    <li>好きなキャラクターや色を選ぶ</li>
                                </ul>
                            </div>
                            
                            <div class="equipment-item">
                                <h4>👟 子供用靴</h4>
                                <ul class="equipment-details">
                                    <li>底が厚く、グリップ力のある運動靴</li>
                                    <li>足首をサポートするハイカットタイプ</li>
                                    <li>サイズは少し余裕があるもの</li>
                                    <li>紐がしっかり結べることを確認</li>
                                </ul>
                            </div>
                            
                            <div class="equipment-item">
                                <h4>🧢 帽子・手袋</h4>
                                <ul class="equipment-details">
                                    <li>日除けと頭部保護のため必須</li>
                                    <li>風で飛ばされないよう紐付き</li>
                                    <li>寒い季節は手袋も準備</li>
                                    <li>紛失防止のため予備も携帯</li>
                                </ul>
                            </div>
                            
                            <div class="equipment-item">
                                <h4>🧥 レインウェア（子供用）</h4>
                                <ul class="equipment-details">
                                    <li>子供のサイズに合ったもの</li>
                                    <li>着脱が簡単なタイプ</li>
                                    <li>明るい色で視認性を高める</li>
                                    <li>ポンチョタイプは風で危険な場合も</li>
                                </ul>
                            </div>
                        </div>
                    </div>
                    
                    <div class="equipment-category">
                        <h3>🍭 子供向け特別装備</h3>
                        <div class="special-equipment">
                            <ul class="special-list">
                                <li><strong>🍪 お気に入りのおやつ:</strong> モチベーション維持に効果的</li>
                                <li><strong>🧸 小さなおもちゃ:</strong> 休憩時の退屈しのぎ</li>
                                <li><strong>📷 使い捨てカメラ:</strong> 子供の目線で記録</li>
                                <li><strong>🎵 口笛・ホイッスル:</strong> 緊急時の連絡手段</li>
                                <li><strong>🩹 子供用救急セット:</strong> 絆創膏やウェットティッシュ</li>
                                <li><strong>🧻 多めの着替え:</strong> 汚れや濡れに対応</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- 楽しませるコツ -->
        <section class="section entertainment-tips">
            <div class="container">
                <h2 class="section-title">子供を楽しませるコツ</h2>
                
                <div class="entertainment-grid">
                    <div class="entertainment-card">
                        <h3>🎯 目標設定・ゲーム化</h3>
                        <ul class="entertainment-list">
                            <li><strong>小さな目標:</strong> 「次の休憩ポイントまで」など短期目標</li>
                            <li><strong>数え遊び:</strong> 石や花の数を数える</li>
                            <li><strong>しりとり:</strong> 歩きながらできる言葉遊び</li>
                            <li><strong>クイズ大会:</strong> 自然や動物に関するクイズ</li>
                            <li><strong>宝探し:</strong> 特定の葉っぱや石を探すゲーム</li>
                        </ul>
                    </div>
                    
                    <div class="entertainment-card">
                        <h3>🔍 自然観察・学習</h3>
                        <ul class="entertainment-list">
                            <li><strong>動植物観察:</strong> 図鑑を持参して名前を調べる</li>
                            <li><strong>写真撮影:</strong> 気になったものを撮影</li>
                            <li><strong>音を聞く:</strong> 鳥の声や風の音に耳を傾ける</li>
                            <li><strong>匂いを嗅ぐ:</strong> 森の香りや花の匂いを楽しむ</li>
                            <li><strong>感触遊び:</strong> 葉っぱや石の感触を楽しむ</li>
                        </ul>
                    </div>
                    
                    <div class="entertainment-card">
                        <h3>📖 ストーリー作り</h3>
                        <ul class="entertainment-list">
                            <li><strong>冒険物語:</strong> 自分たちを主人公にした冒険談</li>
                            <li><strong>妖精探し:</strong> 木陰に住む妖精を探す設定</li>
                            <li><strong>タイムトラベル:</strong> 昔の人の生活を想像する</li>
                            <li><strong>動物の気持ち:</strong> 出会った動物の気持ちを考える</li>
                            <li><strong>山の伝説:</strong> その山にまつわる話を作る</li>
                        </ul>
                    </div>
                    
                    <div class="entertainment-card">
                        <h3>🏆 達成感の演出</h3>
                        <ul class="entertainment-list">
                            <li><strong>記念撮影:</strong> 各ポイントで家族写真</li>
                            <li><strong>登頂証明書:</strong> 手作りの証明書を作成</li>
                            <li><strong>お疲れ様会:</strong> 下山後の楽しみを用意</li>
                            <li><strong>日記作成:</strong> 帰宅後に絵日記を書く</li>
                            <li><strong>思い出グッズ:</strong> 落ち葉や石をお土産に</li>
                        </ul>
                    </div>
                </div>
            </div>
        </section>

        <!-- 安全対策（子供向け） -->
        <section class="section kids-safety">
            <div class="container">
                <h2 class="section-title">子供の安全対策</h2>
                
                <div class="safety-categories">
                    <div class="safety-category">
                        <h3>⚠️ 基本的な安全ルール</h3>
                        <div class="safety-rules">
                            <ul class="safety-checklist">
                                <li><strong>手を繋ぐ:</strong> 危険な場所では必ず大人と手を繋ぐ</li>
                                <li><strong>先頭に出ない:</strong> 大人の後ろを歩く</li>
                                <li><strong>勝手に離れない:</strong> 常に大人の視界内にいる</li>
                                <li><strong>大きな声を出さない:</strong> 野生動物を刺激しない</li>
                                <li><strong>植物を取らない:</strong> 自然保護のマナー</li>
                                <li><strong>ゴミは持ち帰る:</strong> 環境保護の意識</li>
                            </ul>
                        </div>
                    </div>
                    
                    <div class="safety-category">
                        <h3>🚨 緊急時対応（子供向け）</h3>
                        <div class="emergency-kids">
                            <h4>迷子になった場合</h4>
                            <ol class="emergency-steps-kids">
                                <li>その場で止まって大きな声で家族を呼ぶ</li>
                                <li>怖がらずにその場で待つ</li>
                                <li>知らない人についていかない</li>
                                <li>ホイッスルがあれば吹く</li>
                            </ol>
                            
                            <h4>怪我をした場合</h4>
                            <ol class="emergency-steps-kids">
                                <li>すぐに大人に伝える</li>
                                <li>痛い場所を無理に動かさない</li>
                                <li>大人の指示に従う</li>
                                <li>泣いても大丈夫、我慢しない</li>
                            </ol>
                        </div>
                    </div>
                </div>
                
                <div class="preparation-family">
                    <h3>👨‍👩‍👧‍👦 家族での準備</h3>
                    <div class="preparation-grid">
                        <div class="prep-item">
                            <h4>事前説明</h4>
                            <ul class="prep-details">
                                <li>どこに行くのか、何をするのかを説明</li>
                                <li>危険な場所について教える</li>
                                <li>ルールを一緒に決める</li>
                                <li>楽しい要素も伝えてワクワク感を演出</li>
                            </ul>
                        </div>
                        
                        <div class="prep-item">
                            <h4>役割分担</h4>
                            <ul class="prep-details">
                                <li>子供にも小さな責任を持たせる</li>
                                <li>お兄ちゃん・お姉ちゃんには弟妹の見守り</li>
                                <li>写真係、時間係など楽しい役割</li>
                                <li>緊急時の連絡先を覚えさせる</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- おすすめファミリー山 -->
        <section class="section family-mountains">
            <div class="container">
                <h2 class="section-title">ファミリーにおすすめの山</h2>
                
                <div class="family-mountain-grid">
                    <div class="mountain-card family-friendly">
                        <h3>🌸 初心者ファミリー向け</h3>
                        <ul class="mountain-list">
                            <li><strong>高尾山（東京）:</strong> ケーブルカーあり、整備された道</li>
                            <li><strong>円山（北海道）:</strong> 短時間、市内からアクセス良好</li>
                            <li><strong>若草山（奈良）:</strong> なだらかな芝生の山</li>
                            <li><strong>眉山（徳島）:</strong> ロープウェイで楽々登山</li>
                        </ul>
                        <p class="mountain-note">標高300m以下、歩行時間1-2時間、トイレ・休憩施設完備</p>
                    </div>
                    
                    <div class="mountain-card intermediate">
                        <h3>⛰️ 中級ファミリー向け</h3>
                        <ul class="mountain-list">
                            <li><strong>筑波山（茨城）:</strong> ケーブルカー・ロープウェイ両方あり</li>
                            <li><strong>讃岐富士（香川）:</strong> 美しい円錐形、景色抜群</li>
                            <li><strong>金華山（岐阜）:</strong> 歴史的背景、岐阜城</li>
                            <li><strong>立花山（福岡）:</strong> 自然豊か、動植物観察</li>
                        </ul>
                        <p class="mountain-note">標高400-600m、歩行時間2-3時間、ある程度の体力必要</p>
                    </div>
                </div>
                
                <div class="season-recommendations">
                    <h3>🗓️ 季節別おすすめ</h3>
                    <div class="season-grid">
                        <div class="season-item">
                            <h4>🌸 春（3-5月）</h4>
                            <p>新緑が美しく、気候も穏やか。花見も楽しめる山がおすすめ。</p>
                        </div>
                        <div class="season-item">
                            <h4>🌞 夏（6-8月）</h4>
                            <p>早朝出発で暑さを避ける。水遊びができる沢がある山も人気。</p>
                        </div>
                        <div class="season-item">
                            <h4>🍂 秋（9-11月）</h4>
                            <p>紅葉が美しく、気候も最適。最もファミリーハイキングに適した季節。</p>
                        </div>
                        <div class="season-item">
                            <h4>❄️ 冬（12-2月）</h4>
                            <p>雪景色も楽しいが、防寒対策と安全管理をより慎重に。</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        '''
    
    def create_detailed_beginner_page(self, page_id, page_info):
        """詳細な初心者向けページを作成"""
        page_dir = self.base_dir / "beginner" / page_id
        self.ensure_directory(page_dir)
        
        html_content = f'''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_info["title"]} | 初心者向け完全ガイド - 低山旅行</title>
    <meta name="description" content="{page_info['description']}について詳しく解説。初心者でも安心して低山ハイキングを始められる実践的なガイドです。">
    
    <link rel="stylesheet" href="../../css/minimal_design.css">
    
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": "{page_info['title']}",
        "description": "{page_info['description']}",
        "author": {{
            "@type": "Organization",
            "name": "低山旅行"
        }},
        "publisher": {{
            "@type": "Organization", 
            "name": "低山旅行"
        }},
        "datePublished": "2025-01-05",
        "dateModified": "2025-01-05"
    }}
    </script>
</head>
<body>
    <!-- Skip Link -->
    <a href="#main-content" class="sr-only">メインコンテンツへスキップ</a>

    <!-- ヘッダー -->
    <header class="site-header">
        <div class="container">
            <div class="header-content">
                <div class="logo">
                    <a href="../../" aria-label="低山旅行 ホーム">
                        <span class="logo-icon">🏔️</span>
                        <span class="logo-text">低山旅行</span>
                    </a>
                </div>
                
                <nav class="main-nav" aria-label="メインナビゲーション">
                    <ul class="nav-menu">
                        <li><a href="../../mountains/">山を探す</a></li>
                        <li><a href="../../equipment/">装備ガイド</a></li>
                        <li><a href="../../beginner/">初心者向け</a></li>
                        <li><a href="../../regions/">地域別</a></li>
                    </ul>
                </nav>
                
                <button class="mobile-menu-toggle" aria-label="メニューを開く">
                    <span class="menu-line"></span>
                    <span class="menu-line"></span>
                    <span class="menu-line"></span>
                </button>
            </div>
        </div>
        
        <nav class="mobile-nav" aria-label="モバイルナビゲーション">
            <ul class="mobile-menu">
                <li><a href="../../mountains/">山を探す</a></li>
                <li><a href="../../equipment/">装備ガイド</a></li>
                <li><a href="../../beginner/">初心者向け</a></li>
                <li><a href="../../regions/">地域別</a></li>
            </ul>
        </nav>
    </header>

    <!-- メインコンテンツ -->
    <main id="main-content">
        <!-- パンくずナビ -->
        <nav class="breadcrumb section" aria-label="パンくずナビ">
            <div class="container">
                <ol class="breadcrumb-list">
                    <li><a href="../../">ホーム</a></li>
                    <li><a href="../../beginner/">初心者向け</a></li>
                    <li aria-current="page">{page_info["title"]}</li>
                </ol>
            </div>
        </nav>

        <!-- 記事ヘッダー -->
        <article class="beginner-article">
            <header class="article-header section">
                <div class="container">
                    <h1 class="article-title">{page_info["title"]}</h1>
                    <p class="article-subtitle">{page_info["description"]}</p>
                    <div class="article-meta">
                        <span class="meta-item">📚 初心者向け</span>
                        <span class="meta-item">🔰 完全ガイド</span>
                        <span class="meta-item">⏱️ 読了時間：10-15分</span>
                    </div>
                </div>
            </header>

            {page_info["content"]}
        </article>
    </main>

    <!-- フッター -->
    <footer class="site-footer">
        <div class="container">
            <div class="footer-content">
                <div class="footer-section">
                    <h3>低山旅行</h3>
                    <p>安全で楽しい低山ハイキングを応援する専門サイト。初心者からファミリーまで、誰でも気軽に山歩きを楽しめる情報をお届けします。</p>
                </div>
                
                <div class="footer-section">
                    <h3>人気コンテンツ</h3>
                    <ul class="footer-links">
                        <li><a href="../../mountains/">山を探す</a></li>
                        <li><a href="../../equipment/">装備ガイド</a></li>
                        <li><a href="../../beginner/">初心者向け</a></li>
                        <li><a href="../../regions/">地域別ガイド</a></li>
                    </ul>
                </div>
                
                <div class="footer-section">
                    <h3>サイト情報</h3>
                    <ul class="footer-links">
                        <li><a href="../../about/">このサイトについて</a></li>
                        <li><a href="../../contact/">お問い合わせ</a></li>
                        <li><a href="../../privacy/">プライバシーポリシー</a></li>
                        <li><a href="../../terms/">利用規約</a></li>
                    </ul>
                </div>
            </div>
            
            <div class="footer-bottom">
                <p>&copy; 2025 低山旅行. All rights reserved.</p>
            </div>
        </div>
    </footer>

    <!-- JavaScript -->
    <script src="../../js/minimal.js"></script>
</body>
</html>'''
        
        with open(page_dir / "index.html", 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    def improve_regions_page(self):
        """地域別ページを完成させる"""
        print("🗾 地域別ページ完成中...")
        
        # 都道府県別の山をグループ化
        regions_data = self.group_mountains_by_region()
        
        regions_content = self.generate_regions_content(regions_data)
        
        regions_dir = self.base_dir / "regions"
        
        html_content = f'''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>地域別ガイド | 全国47都道府県の低山を地域別に紹介 - 低山旅行</title>
    <meta name="description" content="全国47都道府県の低山を地域別にご紹介。関東、関西、九州など各地域の特色ある低山とアクセス情報を詳しく解説します。">
    
    <link rel="stylesheet" href="../css/minimal_design.css">
    
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "地域別ガイド",
        "description": "全国47都道府県の低山を地域別に紹介",
        "url": "https://teizan.omasse.com/regions/"
    }}
    </script>
</head>
<body>
    <!-- Skip Link -->
    <a href="#main-content" class="sr-only">メインコンテンツへスキップ</a>

    <!-- ヘッダー -->
    <header class="site-header">
        <div class="container">
            <div class="header-content">
                <div class="logo">
                    <a href="../" aria-label="低山旅行 ホーム">
                        <span class="logo-icon">🏔️</span>
                        <span class="logo-text">低山旅行</span>
                    </a>
                </div>
                
                <nav class="main-nav" aria-label="メインナビゲーション">
                    <ul class="nav-menu">
                        <li><a href="../mountains/">山を探す</a></li>
                        <li><a href="../equipment/">装備ガイド</a></li>
                        <li><a href="../beginner/">初心者向け</a></li>
                        <li><a href="../regions/">地域別</a></li>
                    </ul>
                </nav>
                
                <button class="mobile-menu-toggle" aria-label="メニューを開く">
                    <span class="menu-line"></span>
                    <span class="menu-line"></span>
                    <span class="menu-line"></span>
                </button>
            </div>
        </div>
        
        <nav class="mobile-nav" aria-label="モバイルナビゲーション">
            <ul class="mobile-menu">
                <li><a href="../mountains/">山を探す</a></li>
                <li><a href="../equipment/">装備ガイド</a></li>
                <li><a href="../beginner/">初心者向け</a></li>
                <li><a href="../regions/">地域別</a></li>
            </ul>
        </nav>
    </header>

    <!-- メインコンテンツ -->
    <main id="main-content">
        <section class="section">
            <div class="container">
                <header class="section-header">
                    <h1 class="section-title">地域別ガイド</h1>
                    <p class="section-subtitle">
                        全国47都道府県の低山を地域別にご紹介。お住まいの地域から気軽にアクセスできる山を見つけましょう。
                    </p>
                </header>
                
                {regions_content}
                
                <div class="regional-tips">
                    <h2 class="section-title">地域別登山のコツ</h2>
                    <div class="tips-grid">
                        <div class="tip-card">
                            <h3>🚃 交通アクセス</h3>
                            <p>都市部では公共交通機関が充実していますが、地方では車でのアクセスが便利です。事前に交通手段を確認しましょう。</p>
                        </div>
                        
                        <div class="tip-card">
                            <h3>🌤️ 気候特性</h3>
                            <p>北海道と沖縄では気候が大きく異なります。各地域の気候特性を理解して、適切な装備を準備しましょう。</p>
                        </div>
                        
                        <div class="tip-card">
                            <h3>🏛️ 文化・歴史</h3>
                            <p>各地域には独自の文化や歴史があります。登山と合わせて地域の文化や歴史スポットも楽しみましょう。</p>
                        </div>
                        
                        <div class="tip-card">
                            <h3>🍽️ 地域グルメ</h3>
                            <p>登山後の楽しみとして、その地域の郷土料理やご当地グルメを味わうのもおすすめです。</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </main>

    <!-- フッター -->
    <footer class="site-footer">
        <div class="container">
            <div class="footer-content">
                <div class="footer-section">
                    <h3>低山旅行</h3>
                    <p>安全で楽しい低山ハイキングを応援する専門サイト。初心者からファミリーまで、誰でも気軽に山歩きを楽しめる情報をお届けします。</p>
                </div>
                
                <div class="footer-section">
                    <h3>人気コンテンツ</h3>
                    <ul class="footer-links">
                        <li><a href="../mountains/">山を探す</a></li>
                        <li><a href="../equipment/">装備ガイド</a></li>
                        <li><a href="../beginner/">初心者向け</a></li>
                        <li><a href="../regions/">地域別ガイド</a></li>
                    </ul>
                </div>
                
                <div class="footer-section">
                    <h3>サイト情報</h3>
                    <ul class="footer-links">
                        <li><a href="../about/">このサイトについて</a></li>
                        <li><a href="../contact/">お問い合わせ</a></li>
                        <li><a href="../privacy/">プライバシーポリシー</a></li>
                        <li><a href="../terms/">利用規約</a></li>
                    </ul>
                </div>
            </div>
            
            <div class="footer-bottom">
                <p>&copy; 2025 低山旅行. All rights reserved.</p>
            </div>
        </div>
    </footer>

    <!-- JavaScript -->
    <script src="../js/minimal.js"></script>
</body>
</html>'''
        
        with open(regions_dir / "index.html", 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print("✅ 地域別ページ完成")
    
    def group_mountains_by_region(self):
        """山を地域別にグループ化"""
        regions = {
            "北海道": {"icon": "🐻", "mountains": []},
            "東北": {"icon": "🌾", "mountains": []},
            "関東": {"icon": "🗼", "mountains": []},
            "中部": {"icon": "🗻", "mountains": []},
            "関西": {"icon": "🏯", "mountains": []},
            "中国": {"icon": "🦌", "mountains": []},
            "四国": {"icon": "🍊", "mountains": []},
            "九州": {"icon": "♨️", "mountains": []}
        }
        
        # 都道府県から地域への対応
        prefecture_to_region = {
            "北海道": "北海道",
            "青森県": "東北", "岩手県": "東北", "宮城県": "東北", "秋田県": "東北", "山形県": "東北", "福島県": "東北",
            "茨城県": "関東", "栃木県": "関東", "群馬県": "関東", "埼玉県": "関東", "千葉県": "関東", "東京都": "関東", "神奈川県": "関東",
            "新潟県": "中部", "富山県": "中部", "石川県": "中部", "福井県": "中部", "山梨県": "中部", "長野県": "中部", "岐阜県": "中部", "静岡県": "中部", "愛知県": "中部",
            "三重県": "関西", "滋賀県": "関西", "京都府": "関西", "大阪府": "関西", "兵庫県": "関西", "奈良県": "関西", "和歌山県": "関西",
            "鳥取県": "中国", "島根県": "中国", "岡山県": "中国", "広島県": "中国", "山口県": "中国",
            "徳島県": "四国", "香川県": "四国", "愛媛県": "四国", "高知県": "四国",
            "福岡県": "九州", "佐賀県": "九州", "長崎県": "九州", "熊本県": "九州", "大分県": "九州", "宮崎県": "九州", "鹿児島県": "九州", "沖縄県": "九州"
        }
        
        for mountain in self.mountains_data:
            prefecture = mountain.get('prefecture', '不明')
            region = prefecture_to_region.get(prefecture, "その他")
            if region in regions:
                regions[region]["mountains"].append(mountain)
        
        return regions
    
    def generate_regions_content(self, regions_data):
        """地域別コンテンツを生成"""
        content = '<div class="regions-overview">'
        
        for region_name, region_info in regions_data.items():
            mountains = region_info["mountains"]
            if not mountains:  # 山がない地域はスキップ
                continue
                
            icon = region_info["icon"]
            mountain_count = len(mountains)
            
            # 代表的な山を3つ選出
            representative_mountains = mountains[:3]
            mountain_names = [m.get('name', '不明') for m in representative_mountains]
            
            content += f'''
            <div class="region-section">
                <h3 class="region-title">
                    <span class="region-icon">{icon}</span>
                    {region_name}地方
                    <span class="mountain-count">（{mountain_count}座）</span>
                </h3>
                
                <div class="region-content">
                    <div class="region-description">
                        <p>{self.get_region_description(region_name)}</p>
                        
                        <div class="representative-mountains">
                            <h4>代表的な山</h4>
                            <ul class="mountain-list">
            '''
            
            for mountain in representative_mountains:
                mountain_name = mountain.get('name', '不明')
                prefecture = mountain.get('prefecture', '不明')
                elevation = mountain.get('elevation', 0)
                content += f'<li><a href="../mountains/{mountain_name}/">{mountain_name}</a>（{prefecture}・{elevation}m）</li>'
            
            content += '''
                            </ul>
                        </div>
                    </div>
                    
                    <div class="region-features">
                        <h4>地域の特徴</h4>
                        <ul class="feature-list">
            '''
            
            region_features = self.get_region_features(region_name)
            for feature in region_features:
                content += f'<li>{feature}</li>'
            
            content += '''
                        </ul>
                    </div>
                </div>
            </div>
            '''
        
        content += '</div>'
        return content
    
    def get_region_description(self, region_name):
        """地域の説明を取得"""
        descriptions = {
            "北海道": "雄大な自然と美しい景色が魅力の北海道。都市部からアクセスしやすい低山も多く、四季を通じて異なる表情を楽しめます。",
            "東北": "豊かな自然と歴史ある山々が特徴の東北地方。温泉とセットで楽しめる山も多く、季節の変化が美しい地域です。",
            "関東": "首都圏からアクセス抜群の関東地方。電車で気軽に行ける低山が多く、初心者や日帰りハイキングに最適です。",
            "中部": "日本アルプスの麓に位置する美しい低山の宝庫。富士山を望める山も多く、絶景を楽しめます。",
            "関西": "歴史と文化が息づく関西地方。古都の山々は歴史的な背景も豊富で、文化と自然を同時に楽しめます。",
            "中国": "瀬戸内海や日本海を望める山が多い中国地方。穏やかな気候で年間を通してハイキングを楽しめます。",
            "四国": "四国八十八ヶ所の霊場も点在する四国地方。信仰の山としての歴史も深く、心安らぐハイキングが楽しめます。",
            "九州": "火山活動によって形成された独特の地形と、豊富な温泉が魅力。登山後の温泉が楽しみの一つです。"
        }
        return descriptions.get(region_name, "魅力的な低山が点在する地域です。")
    
    def get_region_features(self, region_name):
        """地域の特徴を取得"""
        features = {
            "北海道": ["雄大な自然景観", "野生動物との出会い", "短い夏登山シーズン", "新千歳空港からのアクセス"],
            "東北": ["豊富な温泉", "美しい紅葉", "雪景色も楽しめる", "郷土料理が豊富"],
            "関東": ["電車アクセス抜群", "日帰り可能", "初心者向けコース多数", "都市部から近い"],
            "中部": ["富士山の眺望", "高原の爽やかさ", "山岳文化が根付く", "アルプスの入門として"],
            "関西": ["歴史的背景豊富", "古寺巡りと組み合わせ", "交通アクセス良好", "文化的価値"],
            "中国": ["瀬戸内海の眺望", "穏やかな気候", "島嶼部の山も魅力", "海の幸も楽しめる"],
            "四国": ["お遍路文化", "信仰の山", "温暖な気候", "独特の文化"],
            "九州": ["火山地形", "豊富な温泉", "南国の雰囲気", "活火山の迫力"]
        }
        return features.get(region_name, ["自然豊かな環境", "地域の文化", "美しい景色", "アクセス良好"])
    
    def run_all_improvements(self):
        """すべての改善を実行"""
        print("🔧 サイトコンテンツ充実化開始")
        print("=" * 50)
        
        # 47山すべてのページ作成
        self.create_all_mountain_pages()
        
        # 山一覧ページ更新
        self.update_mountains_index()
        
        # 初心者向けページ充実化
        self.improve_beginner_content()
        
        # 地域別ページ完成
        self.improve_regions_page()
        
        print("=" * 50)
        print("🎉 サイトコンテンツ充実化完了！")
        print(f"📊 作成されたページ: {len(self.mountains_data)}山 + 改善されたページ")

def main():
    improver = ContentImprover()
    improver.run_all_improvements()
    
    print("\n🚀 次のステップ:")
    print("1. サーバーを再起動して変更を確認")
    print("2. check_site.py でサイト品質を再チェック")

if __name__ == "__main__":
    main()