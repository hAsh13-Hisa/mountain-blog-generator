#!/usr/bin/env python3
"""
JSONベースの記事管理システム
article_metadata.jsonを使用して完全な記事生成と管理を行う
"""
import json
from pathlib import Path
import os
from datetime import datetime

class JSONArticleManager:
    def __init__(self):
        self.metadata_file = Path('data/article_metadata.json')
        self.static_dir = Path('static_site')
        self.templates_dir = Path('templates')
        
        # 出力ディレクトリの確保
        self.static_dir.mkdir(exist_ok=True)
        (self.static_dir / 'mountains').mkdir(exist_ok=True)
        (self.static_dir / 'css').mkdir(exist_ok=True)
        
    def load_metadata(self):
        """記事メタデータを読み込み"""
        with open(self.metadata_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save_metadata(self, metadata):
        """記事メタデータを保存"""
        with open(self.metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    def generate_article_html(self, article_data, metadata):
        """単一記事のHTMLを生成"""
        
        # アフィリエイト商品の構築
        affiliate_html = self.build_affiliate_section(article_data, metadata)
        
        # 基本HTML構造
        html_content = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{article_data['subtitle']} - 低山旅行</title>
    <meta name="description" content="{article_data['meta_description']}">
    <meta name="keywords" content="{article_data['seo']['keywords']}">
    <meta name="author" content="低山旅行">
    
    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://teizan.omasse.com{article_data['url']}">
    <meta property="og:title" content="{article_data['subtitle']}">
    <meta property="og:description" content="{article_data['meta_description']}">
    <meta property="og:image" content="{article_data['seo']['og_image']}">
    
    <!-- Twitter -->
    <meta property="twitter:card" content="summary_large_image">
    <meta property="twitter:url" content="https://teizan.omasse.com{article_data['url']}">
    <meta property="twitter:title" content="{article_data['subtitle']}">
    <meta property="twitter:description" content="{article_data['meta_description']}">
    <meta property="twitter:image" content="{article_data['seo']['og_image']}">
    
    <!-- Favicon -->
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <link rel="apple-touch-icon" href="/apple-touch-icon.png">
    
    <!-- CSS -->
    <link rel="stylesheet" href="/css/style.css?v={datetime.now().strftime('%Y%m%d%H%M')}">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    
    <!-- Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', 'GA_MEASUREMENT_ID');
    </script>
</head>
<body>
    <!-- Skip to main content (accessibility) -->
    <a href="#main-content" class="skip-link">メインコンテンツへスキップ</a>
    
    {self.generate_header()}
    
    <main id="main-content" role="main">
        <div class="container">
            <!-- パンくずナビ -->
            <nav class="breadcrumb" aria-label="パンくずナビ">
                <ol>
                    <li><a href="/">ホーム</a></li>
                    <li><a href="/mountains/">山一覧</a></li>
                    <li aria-current="page">{article_data['title']}</li>
                </ol>
            </nav>
            
            <!-- 記事ヘッダー -->
            <header class="article-header">
                <h1>{article_data['subtitle']}</h1>
                <img src="{article_data['featured_image']}" alt="{article_data['title']}" class="featured-image" loading="lazy">
                
                <div class="article-meta">
                    <div class="meta-item">
                        <span class="meta-label">🏔️ 山名:</span>
                        <span class="meta-value">{article_data['title']}</span>
                    </div>
                    <div class="meta-item">
                        <span class="meta-label">📍 都道府県:</span>
                        <span class="meta-value">{article_data['prefecture']}</span>
                    </div>
                    <div class="meta-item">
                        <span class="meta-label">📏 標高:</span>
                        <span class="meta-value">{article_data['elevation']}m</span>
                    </div>
                    <div class="meta-item">
                        <span class="meta-label">⏱️ 登山時間:</span>
                        <span class="meta-value">{article_data['hiking_time']}</span>
                    </div>
                    <div class="meta-item">
                        <span class="meta-label">🎯 難易度:</span>
                        <span class="meta-value">{article_data['difficulty']}</span>
                    </div>
                </div>
            </header>
            
            <!-- 記事本文 -->
            <article class="article-content">
                {self.generate_article_content(article_data)}
            </article>
            
            {affiliate_html}
            
        </div>
    </main>
    
    {self.generate_footer()}
    
    <!-- JavaScript -->
    <script>
        {self.generate_javascript()}
    </script>
</body>
</html>"""
        
        return html_content
    
    def generate_header(self):
        """共通ヘッダーを生成"""
        return '''    <header role="banner">
        <nav class="navbar" role="navigation" aria-label="メインナビゲーション">
            <div class="container">
                <h1><a href="/" aria-label="低山旅行ホームページへ">🏔️ 低山旅行</a></h1>
                <ul class="nav-links" role="menubar">
                    <li role="none"><a href="/" role="menuitem">ホーム</a></li>
                    <li role="none"><a href="/mountains/" role="menuitem">山一覧</a></li>
                    <li role="none"><a href="/regions/" role="menuitem">地域別</a></li>
                    <li role="none"><a href="/beginner/" role="menuitem">初心者ガイド</a></li>
                    <li role="none"><a href="/about/" role="menuitem">このサイトについて</a></li>
                </ul>
                <!-- モバイルメニューボタン -->
                <button class="mobile-menu-toggle" aria-label="メニューを開く" aria-expanded="false">
                    <span></span>
                    <span></span>
                    <span></span>
                </button>
            </div>
        </nav>
    </header>'''
    
    def generate_footer(self):
        """共通フッターを生成"""
        return '''    <footer role="contentinfo">
        <div class="container">
            <div class="footer-content">
                <div class="footer-section">
                    <h3>低山旅行について</h3>
                    <p>初心者・家族向けの低山登山情報を提供しています。</p>
                </div>
                <div class="footer-section">
                    <h3>カテゴリ</h3>
                    <ul>
                        <li><a href="/regions/kanto/">関東地方</a></li>
                        <li><a href="/regions/kansai/">関西地方</a></li>
                        <li><a href="/regions/kyushu/">九州地方</a></li>
                        <li><a href="/difficulty/beginner/">初心者向け</a></li>
                    </ul>
                </div>
                <div class="footer-section">
                    <h3>サイト情報</h3>
                    <ul>
                        <li><a href="/privacy/">プライバシーポリシー</a></li>
                        <li><a href="/terms/">利用規約</a></li>
                        <li><a href="/contact/">お問い合わせ</a></li>
                        <li><a href="/sitemap.xml">サイトマップ</a></li>
                    </ul>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2025 低山旅行. All rights reserved.</p>
                <p>当サイトは楽天アフィリエイトプログラムに参加しています。</p>
                <p>記載の価格・商品情報は掲載時点のものです。最新情報は各サイトでご確認ください。</p>
            </div>
        </div>
    </footer>'''
    
    def generate_javascript(self):
        """共通JavaScriptを生成"""
        return '''        // モバイルメニュー制御
        document.querySelector('.mobile-menu-toggle')?.addEventListener('click', function() {
            this.classList.toggle('active');
            document.querySelector('.nav-links').classList.toggle('active');
            this.setAttribute('aria-expanded', 
                this.getAttribute('aria-expanded') === 'false' ? 'true' : 'false');
        });
        
        // スムーススクロール
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth' });
                }
            });
        });
        
        // 読み込み完了時のアニメーション
        document.addEventListener('DOMContentLoaded', function() {
            document.body.classList.add('loaded');
        });'''
    
    def generate_article_content(self, article_data):
        """記事本文を生成（詳細コンテンツ）"""
        features_list = "\n".join([f"                    <li>{feature}</li>" for feature in article_data['features']])
        
        # 山ごとの詳細コンテンツ
        detailed_content = self.get_detailed_content(article_data['id'])
        
        return f'''                <div class="content-section">
                    <h2>🎯 {article_data['title']}の魅力</h2>
                    <p>{article_data['description']}</p>
                    
                    <h3>⭐ 主な特徴</h3>
                    <ul class="features-list">
{features_list}
                    </ul>
                </div>
                
                {detailed_content}
                
                <div class="content-section">
                    <h2>🚗 アクセス情報</h2>
                    <div class="access-info">
                        <div class="access-item">
                            <h3>🚉 最寄り駅</h3>
                            <p>{article_data['access']['station']}</p>
                        </div>
                        <div class="access-item">
                            <h3>🚌 交通手段</h3>
                            <p>{article_data['access']['transport']}</p>
                        </div>
                        <div class="access-item">
                            <h3>🅿️ 駐車場</h3>
                            <p>{article_data['access']['parking']}</p>
                        </div>
                    </div>
                </div>
                
                <div class="content-section">
                    <h2>📊 基本情報</h2>
                    <table class="info-table">
                        <tr>
                            <th>標高</th>
                            <td>{article_data['elevation']}m</td>
                        </tr>
                        <tr>
                            <th>所在地</th>
                            <td>{article_data['prefecture']}</td>
                        </tr>
                        <tr>
                            <th>登山時間</th>
                            <td>{article_data['hiking_time']}</td>
                        </tr>
                        <tr>
                            <th>難易度</th>
                            <td>{article_data['difficulty']}</td>
                        </tr>
                        <tr>
                            <th>カテゴリ</th>
                            <td>{article_data['category']}</td>
                        </tr>
                    </table>
                </div>'''
    
    def get_detailed_content(self, article_id):
        """山ごとの詳細コンテンツを取得"""
        content_map = {
            "mt_hakodate_hokkaido": '''                <div class="content-section">
                    <h2>🌃 函館山の夜景体験</h2>
                    <p>函館山は標高334mながら、日本三大夜景の一つとして知られる絶景スポットです。津軽海峡に面した函館の街並みが扇状に広がる美しい光景は、多くの観光客を魅了し続けています。</p>
                    
                    <h3>🚠 ロープウェイでのアクセス</h3>
                    <p>函館山ロープウェイは最も人気のアクセス方法です。約3分間の空中散歩で山頂まで運んでくれます。運行時間は季節により異なりますが、夜景を楽しむなら夕方から夜間の運行時間を確認しましょう。</p>
                    
                    <h3>🥾 登山道での楽しみ</h3>
                    <p>ハイキングコースも整備されており、約1時間で山頂に到達できます。旧函館要塞の遺跡や豊かな自然を楽しみながら登山できるのが魅力です。春から秋にかけてが登山のベストシーズンです。</p>
                    
                    <h3>🏛️ 歴史と文化</h3>
                    <p>函館山は明治時代に要塞として使用された歴史があります。現在も砲台跡や観測所跡が残っており、函館の歴史を感じながら散策することができます。</p>
                </div>
                
                <div class="content-section">
                    <h2>📅 ベストタイミング</h2>
                    <h3>🌅 夕日と夜景のダブル楽しみ</h3>
                    <p>日没1時間前に到着すれば、美しい夕日から始まり、街に明かりが灯る過程、そして完成された夜景まで一連の変化を楽しめます。特に冬の澄んだ空気の中で見る夜景は格別です。</p>
                    
                    <h3>🌸 四季の魅力</h3>
                    <ul class="season-list">
                        <li><strong>春（4-5月）</strong>：桜の季節で、山頂からの眺めに華やかさが加わります</li>
                        <li><strong>夏（6-8月）</strong>：緑豊かな函館の街並みと海の青さのコントラスト</li>
                        <li><strong>秋（9-11月）</strong>：紅葉と澄んだ空気で、最も美しい夜景が楽しめる季節</li>
                        <li><strong>冬（12-3月）</strong>：雪化粧した街並みと、空気が澄んで遠くまで見渡せる絶景</li>
                    </ul>
                </div>''',
            
            "mt_maruyama_hokkaido": '''                <div class="content-section">
                    <h2>🌲 札幌の都市オアシス</h2>
                    <p>円山は札幌市民に愛され続ける標高225mの低山です。市街地から地下鉄で15分という抜群のアクセスでありながら、山頂では原始林の豊かな自然を体験できる貴重なスポットです。</p>
                    
                    <h3>🦌 野生動物との出会い</h3>
                    <p>円山では、エゾリスやキタキツネ、野鳥など様々な野生動物に出会うことができます。特に早朝の登山では、静寂な森の中で動物たちの営みを観察できる機会が多くあります。</p>
                    
                    <h3>🌸 円山公園と桜</h3>
                    <p>円山公園は札幌の桜の名所として有名で、春には花見客で賑わいます。公園から登山道に入ることで、都市の喧騒から一転して静かな森の世界へと導かれます。</p>
                </div>
                
                <div class="content-section">
                    <h2>🥾 登山コースガイド</h2>
                    <h3>🚶‍♂️ 初心者向けルート</h3>
                    <p>円山公園駐車場から山頂まで約1時間の初心者向けコースです。よく整備された登山道で、道標も充実しているため迷う心配がありません。</p>
                    
                    <h3>🏔️ 山頂からの眺望</h3>
                    <p>山頂からは札幌市街地が一望でき、天気が良い日には石狩湾や手稲山まで見渡すことができます。都市部からこれほど近い場所で、これだけの自然と眺望が楽しめるのは円山ならではの魅力です。</p>
                </div>''',
            
            "mt_takao": '''                <div class="content-section">
                    <h2>🚠 多彩なアクセス方法</h2>
                    <p>高尾山の大きな魅力は、ケーブルカーやリフトを利用した気軽なアクセスです。体力に自信がない方や小さなお子様連れでも、山頂近くまで楽に到達できます。</p>
                    
                    <h3>🥾 6つの登山コース</h3>
                    <p>高尾山には6つの異なる登山コースが用意されており、初心者から上級者まで楽しめます：</p>
                    <ul class="course-list">
                        <li><strong>1号路</strong>：最も人気の舗装された道。薬王院を通る王道コース</li>
                        <li><strong>2号路</strong>：途中まで1号路と同じ、霞台ループコース</li>
                        <li><strong>3号路</strong>：カツラ林の美しい自然コース</li>
                        <li><strong>4号路</strong>：吊り橋が楽しめる山の中腹コース</li>
                        <li><strong>5号路</strong>：山頂まで最短距離、上級者向け</li>
                        <li><strong>6号路</strong>：琵琶滝を通る滝と自然のコース</li>
                    </ul>
                </div>
                
                <div class="content-section">
                    <h2>⛩️ 薬王院と文化体験</h2>
                    <p>高尾山薬王院は1200年以上の歴史を持つ古刹で、パワースポットとしても有名です。山登りと合わせて参拝することで、心身ともにリフレッシュできます。</p>
                    
                    <h3>🍜 山頂グルメ</h3>
                    <p>山頂や山腹には茶屋や食堂があり、高尾山名物のとろろそばや天狗焼きなどのグルメを楽しめます。登山の疲れを癒やしながら、美味しい食事も楽しみの一つです。</p>
                </div>''',
            
            "mt_tsukuba_ibaraki": '''                <div class="content-section">
                    <h2>⛩️ 双峰の神秘</h2>
                    <p>筑波山は男体山（871m）と女体山（877m）の双峰からなる日本百名山です。「西の富士、東の筑波」と称され、古くから信仰の山として親しまれてきました。</p>
                    
                    <h3>🚠 2つのアクセス方法</h3>
                    <p>筑波山には2つの便利なアクセス方法があります：</p>
                    <ul class="access-list">
                        <li><strong>筑波山ケーブルカー</strong>：宮脇駅から筑波山頂駅（男体山側）へ約8分</li>
                        <li><strong>筑波山ロープウェイ</strong>：つつじヶ丘駅から女体山駅へ約6分</li>
                    </ul>
                    
                    <h3>🌅 関東平野の絶景</h3>
                    <p>山頂からは関東平野が360度見渡せ、天気の良い日には富士山やスカイツリーまで望むことができます。特に夕日や夜景は絶景で、多くの観光客が訪れます。</p>
                </div>
                
                <div class="content-section">
                    <h2>🥾 登山コースの選択</h2>
                    <h3>👨‍👩‍👧‍👦 家族向けコース</h3>
                    <p>御幸ヶ原コース（男体山）は比較的緩やかで、家族連れにおすすめです。約90分で山頂に到達でき、途中には休憩ポイントも充実しています。</p>
                    
                    <h3>🏃‍♂️ チャレンジコース</h3>
                    <p>白雲橋コース（女体山）はやや急峻ですが、巨石群や自然の造形美を楽しめる本格的な登山コースです。</p>
                </div>''',
            
            "mt_sanuki_kagawa": '''                <div class="content-section">
                    <h2>🗾 瀬戸内海の絶景</h2>
                    <p>讃岐富士（飯野山）は香川県のシンボルとも言える美しい山容を持つ標高422mの山です。瀬戸内海に浮かぶ島々や四国の山並みを一望できる絶景スポットです。</p>
                    
                    <h3>🎨 富士山のような美しい山容</h3>
                    <p>どの角度から見ても美しい円錐形を保つその姿から「讃岐富士」と呼ばれています。特に坂出市側から見る姿は、まさに小さな富士山そのものです。</p>
                </div>
                
                <div class="content-section">
                    <h2>🥾 登山とうどんの旅</h2>
                    <h3>🍜 うどん県ならではの楽しみ</h3>
                    <p>登山の前後には、香川県名物のうどんを楽しむのが定番です。山麓には地元の人気うどん店が点在しており、登山とグルメを組み合わせた一日を過ごせます。</p>
                    
                    <h3>🌊 瀬戸内の四季</h3>
                    <p>春は桜、夏は青い海と空、秋は紅葉、冬は澄んだ空気の中での絶景と、四季それぞれに異なる魅力を持つ山です。瀬戸内海の穏やかな気候のため、年間を通して登山を楽しめます。</p>
                </div>'''
        }
        
        return content_map.get(article_id, '''                <div class="content-section">
                    <h2>✨ 登山の楽しみ</h2>
                    <p>この山ならではの魅力と楽しみ方をご紹介します。四季折々の自然の美しさと、登山の達成感をぜひ体験してください。</p>
                </div>''')
    
    def build_affiliate_section(self, article_data, metadata):
        """アフィリエイトセクションを構築"""
        affiliate_products = metadata.get('affiliate_products', {})
        product_htmls = []
        
        for product_id in article_data.get('affiliate_products', []):
            if product_id in affiliate_products:
                product = affiliate_products[product_id]
                product_html = f'''                <div class="affiliate-product">
                    <h4>{product['name']}</h4>
                    <p>{product['description']}</p>
                    <div class="price-range">{product['price_range']}</div>
                    <a href="{product['rakuten_url']}" target="_blank" rel="noopener noreferrer" class="affiliate-link">
                        楽天で詳細を見る
                    </a>
                </div>'''
                product_htmls.append(product_html)
        
        if product_htmls:
            return f'''            
            <div class="affiliate-section">
                <h2>🛒 おすすめ登山用品</h2>
                <p class="affiliate-intro">{article_data['title']}登山におすすめの用品をご紹介します。</p>
                
                <div class="affiliate-products">
{chr(10).join(product_htmls)}
                </div>
                
                <div class="affiliate-notice">
                    <p>※ 当サイトは楽天アフィリエイトプログラムに参加しています。商品購入により収益を得る場合があります。</p>
                    <p>※ 価格・商品情報は掲載時点のものです。最新情報は各サイトでご確認ください。</p>
                </div>
            </div>'''
        else:
            return ""
    
    def generate_mountains_list(self, metadata):
        """山一覧ページを生成"""
        articles = metadata['articles']
        mountain_cards = []
        
        for article_id, article_data in articles.items():
            if article_data['status'] == 'published':
                card_html = f'''                <a href="{article_data['url']}" class="mountain-card">
                    <img src="{article_data['featured_image']}" alt="{article_data['title']}" loading="lazy">
                    <div class="mountain-card-content">
                        <h3>{article_data['title']}</h3>
                        <div class="mountain-meta">{article_data['prefecture']} - 標高{article_data['elevation']}m</div>
                        <p>{article_data['description']}</p>
                    </div>
                </a>'''
                mountain_cards.append(card_html)
        
        list_html = f'''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>山一覧 - 低山旅行</title>
    <meta name="description" content="初心者・家族向けの低山一覧。標高400m以下の登りやすい山をご紹介します。">
    <meta name="keywords" content="低山, 登山, ハイキング, 初心者, 家族旅行, 日帰り, アウトドア">
    <meta name="author" content="低山旅行">
    
    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://teizan.omasse.com/">
    <meta property="og:title" content="山一覧 - 低山旅行">
    <meta property="og:description" content="初心者・家族向けの低山一覧。標高400m以下の登りやすい山をご紹介します。">
    <meta property="og:image" content="https://teizan.omasse.com/images/og-image.jpg">
    
    <!-- Twitter -->
    <meta property="twitter:card" content="summary_large_image">
    <meta property="twitter:url" content="https://teizan.omasse.com/">
    <meta property="twitter:title" content="山一覧 - 低山旅行">
    <meta property="twitter:description" content="初心者・家族向けの低山一覧。標高400m以下の登りやすい山をご紹介します。">
    <meta property="twitter:image" content="https://teizan.omasse.com/images/og-image.jpg">
    
    <!-- Favicon -->
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <link rel="apple-touch-icon" href="/apple-touch-icon.png">
    
    <!-- CSS -->
    <link rel="stylesheet" href="/css/style.css?v={datetime.now().strftime('%Y%m%d%H%M')}">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    
    <!-- Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', 'GA_MEASUREMENT_ID');
    </script>
</head>
<body>
    <!-- Skip to main content (accessibility) -->
    <a href="#main-content" class="skip-link">メインコンテンツへスキップ</a>
    
    {self.generate_header()}
    
    <main id="main-content" role="main">
        <div class="container">
            
            <div class="page-header">
                <h1>🏔️ 山一覧</h1>
                <p class="page-description">初心者・家族向けの低山を厳選してご紹介。標高400m以下で登山道が整備された、安全で楽しめる山々です。</p>
            </div>
            
            <div class="mountain-grid">
{chr(10).join(mountain_cards)}
            </div>
            
            <div class="section">
                <h2>🎯 山選びのポイント</h2>
                <div class="tips-grid">
                    <div class="tip-card">
                        <h3>🥾 難易度で選ぶ</h3>
                        <p>登山経験に応じて、初級・中級コースから選択。標高400m以下の山は初心者にもおすすめです。</p>
                    </div>
                    <div class="tip-card">
                        <h3>🚗 アクセスで選ぶ</h3>
                        <p>公共交通機関でアクセスできる山なら、車がなくても楽しめます。駐車場の有無も事前にチェック。</p>
                    </div>
                    <div class="tip-card">
                        <h3>🌸 季節で選ぶ</h3>
                        <p>春の花、夏の新緑、秋の紅葉など、季節ごとの魅力を楽しめる山を選びましょう。</p>
                    </div>
                </div>
            </div>
            
        </div>
    </main>
    
    {self.generate_footer()}
    
    <!-- JavaScript -->
    <script>
        {self.generate_javascript()}
    </script>
</body>
</html>'''
        
        return list_html
    
    def generate_all_articles(self):
        """全ての記事を生成"""
        print("📰 JSON based article generation starting...")
        
        metadata = self.load_metadata()
        
        # 各記事ページの生成
        generated_count = 0
        for article_id, article_data in metadata['articles'].items():
            if article_data['status'] == 'published':
                # 記事ディレクトリの作成
                article_dir = self.static_dir / article_data['url'].strip('/')
                article_dir.mkdir(parents=True, exist_ok=True)
                
                # HTML生成
                html_content = self.generate_article_html(article_data, metadata)
                
                # ファイル保存
                output_file = article_dir / 'index.html'
                output_file.write_text(html_content, encoding='utf-8')
                
                print(f"  ✅ Generated: {article_data['title']} -> {output_file}")
                generated_count += 1
        
        # 山一覧ページの生成
        mountains_dir = self.static_dir / 'mountains'
        mountains_dir.mkdir(exist_ok=True)
        
        list_html = self.generate_mountains_list(metadata)
        list_file = mountains_dir / 'index.html'
        list_file.write_text(list_html, encoding='utf-8')
        
        print(f"  ✅ Generated: Mountains list -> {list_file}")
        
        print(f"\n✅ JSON-based article generation completed!")
        print(f"   📊 Generated {generated_count} articles + 1 list page")
        print(f"   📁 Output directory: {self.static_dir}")
        
        return True

def main():
    """メイン処理"""
    generator = JSONArticleManager()
    generator.generate_all_articles()

if __name__ == "__main__":
    main()