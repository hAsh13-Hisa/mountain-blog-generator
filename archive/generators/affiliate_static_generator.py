#!/usr/bin/env python3
"""
アフィリエイト対応の静的サイトジェネレーター
"""
import json
import os
import re
from datetime import datetime
from pathlib import Path

class AffiliateStaticGenerator:
    def __init__(self):
        self.output_dir = Path("static_site")
        self.load_data()
    
    def load_data(self):
        """データファイルを読み込み"""
        with open('data/mountains_japan_expanded.json', 'r', encoding='utf-8') as f:
            self.mountains_data = json.load(f)
    
    def create_html_template(self, title, content, meta_description="", structured_data=None):
        """強化版HTMLテンプレート（SEO・アクセシビリティ対応）"""
        # 構造化データのデフォルト
        if not structured_data:
            structured_data = {
                "@context": "https://schema.org",
                "@type": "WebSite",
                "name": "低山旅行",
                "description": "初心者・家族向けの低山旅行情報サイト",
                "url": "https://your-domain.com"
            }
        
        structured_data_json = json.dumps(structured_data, ensure_ascii=False, indent=2)
        
        return f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{meta_description}">
    <meta name="keywords" content="低山, 登山, ハイキング, 初心者, 家族旅行, 日帰り, アウトドア">
    <meta name="author" content="低山旅行">
    
    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://your-domain.com/">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{meta_description}">
    <meta property="og:image" content="https://your-domain.com/images/og-image.jpg">
    
    <!-- Twitter -->
    <meta property="twitter:card" content="summary_large_image">
    <meta property="twitter:url" content="https://your-domain.com/">
    <meta property="twitter:title" content="{title}">
    <meta property="twitter:description" content="{meta_description}">
    <meta property="twitter:image" content="https://your-domain.com/images/og-image.jpg">
    
    <!-- Favicon -->
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <link rel="apple-touch-icon" href="/apple-touch-icon.png">
    
    <!-- CSS -->
    <link rel="stylesheet" href="/css/style.css?v=202507032251">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    
    <!-- 構造化データ -->
    <script type="application/ld+json">
    {structured_data_json}
    </script>
    
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
    
    <header role="banner">
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
    </header>
    
    <main id="main-content" role="main">
        {content}
    </main>
    
    <!-- サイドバー（記事ページ用） -->
    <aside class="sidebar" role="complementary" aria-label="関連情報">
        <!-- 動的に挿入される -->
    </aside>
    
    <footer role="contentinfo">
        <div class="container">
            <div class="footer-content">
                <div class="footer-section">
                    <h3>低山旅行について</h3>
                    <p>初心者・家族向けの低山登山情報を提供しています。</p>
                </div>
                <div class="footer-section">
                    <h3>地域別低山ガイド</h3>
                    <ul>
                        <li><a href="/regions/関東/">関東の低山 (17山)</a></li>
                        <li><a href="/regions/関西/">関西の低山 (12山)</a></li>
                        <li><a href="/regions/九州/">九州の低山 (6山)</a></li>
                        <li><a href="/regions/東北/">東北の低山 (3山)</a></li>
                        <li><a href="/regions/中部/">中部の低山 (3山)</a></li>
                        <li><a href="/regions/四国/">四国の低山 (3山)</a></li>
                        <li><a href="/regions/北海道/">北海道の低山 (2山)</a></li>
                        <li><a href="/regions/中国/">中国の低山 (1山)</a></li>
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
    </footer>
    
    <!-- JavaScript -->
    <script>
        // モバイルメニュー制御
        document.querySelector('.mobile-menu-toggle')?.addEventListener('click', function() {{
            this.classList.toggle('active');
            document.querySelector('.nav-links').classList.toggle('active');
            this.setAttribute('aria-expanded', 
                this.getAttribute('aria-expanded') === 'false' ? 'true' : 'false');
        }});
        
        // スムーススクロール
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
            anchor.addEventListener('click', function (e) {{
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {{
                    target.scrollIntoView({{ behavior: 'smooth' }});
                }}
            }});
        }});
        
        // 読み込み完了時のアニメーション
        document.addEventListener('DOMContentLoaded', function() {{
            document.body.classList.add('loaded');
        }});
    </script>
</body>
</html>"""
    
    def create_css(self):
        """CSSファイルを作成"""
        css_dir = self.output_dir / "css"
        css_dir.mkdir(parents=True, exist_ok=True)
        
        css_content = """
/* ===== 低山旅行サイト CSS（デザイン仕様書準拠） ===== */

/* リセット & 基本設定 */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

:root {
    /* カラーパレット（仕様書準拠） */
    --primary-color: #2c5234;
    --accent-color: #f0a500;
    --sub-color: #e8f5e8;
    --text-color: #333333;
    --text-sub: #666666;
    --bg-color: #fafafa;
    --affiliate-bg: #fff3e0;
    --price-color: #e53935;
    --cta-color: #d84315;
}

/* タイポグラフィ */
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Noto Sans JP', sans-serif;
    line-height: 1.7;
    color: var(--text-color);
    background-color: var(--bg-color);
    font-size: 16px;
}

h1 { font-size: 2.2rem; font-weight: 700; line-height: 1.3; }
h2 { font-size: 1.6rem; font-weight: 600; line-height: 1.4; }
h3 { font-size: 1.3rem; font-weight: 600; line-height: 1.4; }
p { font-size: 1rem; line-height: 1.7; margin-bottom: 1.2rem; }

/* レイアウト */
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

/* ===== アクセシビリティ ===== */
.skip-link {
    position: absolute;
    top: -40px;
    left: 6px;
    z-index: 10000;
    background: #000;
    color: #fff;
    padding: 8px;
    text-decoration: none;
    font-size: 0.9rem;
    border-radius: 4px;
    opacity: 0;
    transition: all 0.3s ease;
}

.skip-link:focus {
    top: 6px;
    opacity: 1;
}

/* ===== ヘッダー ===== */
header[role="banner"] {
    background: linear-gradient(135deg, var(--primary-color), #3d6b47);
    color: white;
    padding: 1rem 0;
    box-shadow: 0 4px 20px rgba(44, 82, 52, 0.3);
    position: sticky;
    top: 0;
    z-index: 9999;
}

.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.navbar h1 a {
    color: white;
    text-decoration: none;
    font-size: 1.8rem;
    font-weight: 800;
    transition: transform 0.2s ease;
}

.navbar h1 a:hover {
    transform: scale(1.05);
}

.nav-links {
    display: flex;
    list-style: none;
    gap: 1.5rem;
}

.nav-links a {
    color: white;
    text-decoration: none;
    font-weight: 500;
    padding: 0.7rem 1.2rem;
    border-radius: 25px;
    transition: all 0.3s ease;
    border: 1px solid transparent;
}

.nav-links a:hover {
    background-color: rgba(255, 255, 255, 0.2);
    border-color: rgba(255, 255, 255, 0.3);
    transform: translateY(-2px);
}

/* ===== メインコンテンツ ===== */
main {
    min-height: calc(100vh - 200px);
    padding: 2rem 0;
}

/* ===== ヒーローセクション ===== */
.hero {
    text-align: center;
    margin-bottom: 4rem;
    padding: 4rem 2rem;
    background: linear-gradient(135deg, 
        rgba(44, 82, 52, 0.05), 
        rgba(240, 165, 0, 0.05));
    border-radius: 20px;
    position: relative;
    overflow: hidden;
}

.hero::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 200"><path d="M0,100 C300,150 700,50 1000,100 L1000,200 L0,200 Z" fill="%23e8f5e8" opacity="0.3"/></svg>') no-repeat center bottom;
    background-size: cover;
}

.hero h1 {
    font-size: 3.5rem;
    color: var(--primary-color);
    margin-bottom: 1.5rem;
    font-weight: 800;
    position: relative;
    z-index: 2;
}

.hero p {
    font-size: 1.3rem;
    color: var(--text-sub);
    max-width: 700px;
    margin: 0 auto;
    position: relative;
    z-index: 2;
}

/* ===== セクションタイトル ===== */
.section-title {
    font-size: 2rem;
    color: var(--primary-color);
    margin-bottom: 3rem;
    text-align: center;
    position: relative;
    font-weight: 700;
}

.section-title::after {
    content: '';
    display: block;
    width: 80px;
    height: 4px;
    background: linear-gradient(90deg, var(--primary-color), var(--accent-color));
    margin: 1rem auto;
    border-radius: 2px;
}

/* ===== 記事カードグリッド ===== */
.mountain-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 2.5rem;
    margin-top: 2rem;
}

.mountain-card {
    background: white;
    border-radius: 20px;
    overflow: hidden;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    box-shadow: 0 8px 25px rgba(44, 82, 52, 0.1);
    border: 1px solid rgba(44, 82, 52, 0.1);
}

.mountain-card:hover {
    transform: translateY(-12px) scale(1.02);
    box-shadow: 0 20px 40px rgba(44, 82, 52, 0.2);
}

.mountain-card img {
    width: 100%;
    height: 240px;
    object-fit: cover;
    transition: transform 0.4s ease;
}

.mountain-card:hover img {
    transform: scale(1.1);
}

.mountain-card-content {
    padding: 2rem;
}

.mountain-card h3 {
    color: var(--primary-color);
    margin-bottom: 1rem;
    font-size: 1.4rem;
    font-weight: 700;
}

.mountain-card .mountain-meta {
    color: var(--text-sub);
    font-size: 0.9rem;
    margin-bottom: 1rem;
    padding: 0.4rem 0.8rem;
    background: var(--sub-color);
    border-radius: 15px;
    display: inline-block;
    font-weight: 500;
}

.mountain-card p {
    color: var(--text-sub);
    line-height: 1.6;
    margin-bottom: 0;
}

.mountain-card a {
    text-decoration: none;
    color: inherit;
}

/* ===== 記事ページ ===== */
.article-container {
    max-width: 900px;
    margin: 0 auto;
    background: white;
    border-radius: 20px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    overflow: hidden;
}

.article-header {
    padding: 3rem 2rem 2rem;
    background: linear-gradient(135deg, #f8f9fa, var(--sub-color));
}

.article-header h1 {
    color: var(--primary-color);
    margin-bottom: 1.5rem;
    line-height: 1.3;
}

.article-meta {
    color: var(--text-sub);
    margin-bottom: 1.5rem;
    font-size: 0.95rem;
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
}

.mountain-info {
    background: white;
    color: var(--primary-color);
    padding: 0.5rem 1rem;
    border-radius: 20px;
    font-weight: 600;
    border: 2px solid var(--sub-color);
}

.featured-image {
    width: 100%;
    height: 400px;
    object-fit: cover;
}

.article-content {
    padding: 3rem 2rem;
    line-height: 1.8;
}

.article-content h2 {
    color: var(--primary-color);
    margin: 3rem 0 1.5rem 0;
    border-left: 5px solid var(--accent-color);
    padding-left: 1.5rem;
    position: relative;
}

.article-content h2::before {
    content: '';
    position: absolute;
    left: -5px;
    top: 0;
    width: 5px;
    height: 100%;
    background: linear-gradient(180deg, var(--accent-color), var(--primary-color));
}

.article-content h3 {
    color: var(--primary-color);
    margin: 2.5rem 0 1rem 0;
}

.article-content p {
    color: #444;
    margin-bottom: 1.5rem;
}

.article-content ul, .article-content ol {
    margin-left: 2rem;
    margin-bottom: 1.5rem;
}

.article-content li {
    margin-bottom: 0.7rem;
    color: #444;
}

/* ===== アフィリエイトセクション（強化版） ===== */
.affiliate-section {
    background: linear-gradient(135deg, var(--affiliate-bg), #ffebcd);
    padding: 3rem 2rem;
    margin: 3rem 0;
    border-radius: 20px;
    border: 3px solid var(--accent-color);
    position: relative;
    box-shadow: 0 8px 25px rgba(240, 165, 0, 0.2);
}

.affiliate-section::before {
    content: '';
    position: absolute;
    top: -2px;
    left: -2px;
    right: -2px;
    bottom: -2px;
    background: linear-gradient(45deg, var(--accent-color), var(--cta-color));
    border-radius: 20px;
    z-index: -1;
}

.affiliate-section h3 {
    color: var(--cta-color);
    margin-bottom: 2rem;
    font-size: 1.6rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-weight: 700;
    text-align: center;
    justify-content: center;
}

.affiliate-products {
    display: grid;
    gap: 1.5rem;
}

.affiliate-product {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem;
    background: white;
    border-radius: 15px;
    border-left: 5px solid var(--accent-color);
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
}

.affiliate-product:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    border-left-width: 8px;
}

.affiliate-product a {
    color: var(--cta-color);
    text-decoration: none;
    font-weight: 700;
    flex: 1;
    margin-right: 1rem;
    font-size: 1.05rem;
}

.affiliate-product a:hover {
    text-decoration: underline;
}

.price {
    font-weight: bold;
    color: var(--price-color);
    font-size: 1.2rem;
    background: #ffebee;
    padding: 0.3rem 0.8rem;
    border-radius: 10px;
}

/* ===== CTAボタン ===== */
.cta-button {
    background: linear-gradient(135deg, var(--accent-color), var(--cta-color));
    color: white;
    padding: 15px 30px;
    border-radius: 30px;
    font-weight: bold;
    text-decoration: none;
    display: inline-block;
    box-shadow: 0 6px 20px rgba(240, 165, 0, 0.3);
    transition: all 0.3s ease;
    border: none;
    cursor: pointer;
    font-size: 1.1rem;
}

.cta-button:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 30px rgba(240, 165, 0, 0.4);
    background: linear-gradient(135deg, #ffb300, #bf360c);
}

/* ===== タグ ===== */
.article-tags {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
    margin-top: 2rem;
    padding: 2.5rem;
    background: linear-gradient(135deg, #f8f9fa, var(--sub-color));
    border-radius: 0 0 20px 20px;
}

.tag {
    background: linear-gradient(135deg, white, var(--sub-color));
    color: var(--primary-color);
    padding: 0.6rem 1.2rem;
    border-radius: 25px;
    font-size: 0.85rem;
    font-weight: 600;
    transition: all 0.3s ease;
    border: 2px solid var(--sub-color);
}

.tag:hover {
    transform: scale(1.1);
    background: var(--primary-color);
    color: white;
}

/* ===== フッター ===== */
footer {
    background: linear-gradient(135deg, var(--primary-color), #1a3d21);
    color: white;
    text-align: center;
    padding: 4rem 0;
    margin-top: 5rem;
    position: relative;
}

footer::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, var(--accent-color), var(--cta-color));
}

footer p {
    margin-bottom: 0.8rem;
    font-size: 0.95rem;
}

/* ===== レスポンシブデザイン ===== */
@media (max-width: 768px) {
    .container { padding: 0 15px; }
    
    .navbar {
        flex-direction: column;
        gap: 1rem;
        padding: 1rem 0;
    }
    
    .nav-links {
        gap: 0.8rem;
        flex-wrap: wrap;
        justify-content: center;
    }
    
    .hero h1 { font-size: 2.5rem; }
    .hero p { font-size: 1.1rem; }
    
    .mountain-grid {
        grid-template-columns: 1fr;
        gap: 1.5rem;
    }
    
    .article-header h1 { font-size: 1.8rem; }
    .article-header { padding: 2rem 1.5rem 1.5rem; }
    .article-content { padding: 2rem 1.5rem; }
    
    .affiliate-product {
        flex-direction: column;
        align-items: flex-start;
        gap: 1rem;
        text-align: left;
    }
    
    .affiliate-product a {
        margin-right: 0;
        margin-bottom: 0.5rem;
    }
    
    .article-meta {
        flex-direction: column;
        gap: 0.8rem;
    }
    
    .article-content h2 {
        font-size: 1.4rem;
        margin: 2rem 0 1rem 0;
    }
    
    .mountain-card-content { padding: 1.5rem; }
}

@media (max-width: 480px) {
    .hero { padding: 2rem 1rem; }
    .hero h1 { font-size: 2rem; }
    .affiliate-section { padding: 2rem 1rem; }
    .container { padding: 0 10px; }
}

/* ===== ユーティリティクラス ===== */
.text-center { text-align: center; }
.text-left { text-align: left; }
.text-right { text-align: right; }
.mb-1 { margin-bottom: 0.5rem; }
.mb-2 { margin-bottom: 1rem; }
.mb-3 { margin-bottom: 1.5rem; }
.mt-1 { margin-top: 0.5rem; }
.mt-2 { margin-top: 1rem; }
.mt-3 { margin-top: 1.5rem; }
.p-1 { padding: 0.5rem; }
.p-2 { padding: 1rem; }
.p-3 { padding: 1.5rem; }

/* ===== アニメーション ===== */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.mountain-card {
    animation: fadeInUp 0.6s ease forwards;
}

.mountain-card:nth-child(1) { animation-delay: 0.1s; }
.mountain-card:nth-child(2) { animation-delay: 0.2s; }
.mountain-card:nth-child(3) { animation-delay: 0.3s; }
.mountain-card:nth-child(4) { animation-delay: 0.4s; }
.mountain-card:nth-child(5) { animation-delay: 0.5s; }

/* ===== アクセシビリティ ===== */
.skip-link {
    position: absolute;
    top: -40px;
    left: 6px;
    background: var(--primary-color);
    color: white;
    padding: 8px;
    text-decoration: none;
    border-radius: 0 0 4px 4px;
    z-index: 1000;
    transition: top 0.3s;
}

.skip-link:focus {
    top: 0;
}

/* ===== モバイルメニュー ===== */
.mobile-menu-toggle {
    display: none;
    flex-direction: column;
    background: transparent;
    border: none;
    cursor: pointer;
    padding: 0.5rem;
    gap: 4px;
}

.mobile-menu-toggle span {
    width: 25px;
    height: 3px;
    background: white;
    border-radius: 1px;
    transition: all 0.3s ease;
}

.mobile-menu-toggle.active span:nth-child(1) {
    transform: rotate(45deg) translate(5px, 5px);
}

.mobile-menu-toggle.active span:nth-child(2) {
    opacity: 0;
}

.mobile-menu-toggle.active span:nth-child(3) {
    transform: rotate(-45deg) translate(7px, -6px);
}

/* ===== フッター強化 ===== */
.footer-content {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
    margin-bottom: 2rem;
}

.footer-section h3 {
    color: white;
    margin-bottom: 1rem;
    font-size: 1.1rem;
    font-weight: 600;
}

.footer-section ul {
    list-style: none;
    padding: 0;
}

.footer-section li {
    margin-bottom: 0.5rem;
}

.footer-section a {
    color: rgba(255, 255, 255, 0.8);
    text-decoration: none;
    transition: color 0.3s ease;
}

.footer-section a:hover {
    color: white;
    text-decoration: underline;
}

.footer-bottom {
    border-top: 1px solid rgba(255, 255, 255, 0.2);
    padding-top: 2rem;
    text-align: center;
}

.footer-bottom p {
    color: rgba(255, 255, 255, 0.8);
    font-size: 0.85rem;
    margin-bottom: 0.5rem;
}

/* ===== 目次（TOC）===== */
.table-of-contents {
    background: linear-gradient(135deg, var(--sub-color), #f0f8f0);
    border: 2px solid var(--primary-color);
    border-radius: 15px;
    padding: 2rem;
    margin: 2rem 0;
}

.table-of-contents h3 {
    color: var(--primary-color);
    margin-bottom: 1rem;
    font-size: 1.3rem;
    text-align: center;
}

.table-of-contents ul {
    list-style: none;
    padding: 0;
}

.table-of-contents li {
    margin-bottom: 0.8rem;
    padding-left: 1rem;
    position: relative;
}

.table-of-contents li::before {
    content: '🏔️';
    position: absolute;
    left: 0;
    top: 0;
}

.table-of-contents a {
    color: var(--primary-color);
    text-decoration: none;
    font-weight: 500;
    transition: color 0.3s ease;
}

.table-of-contents a:hover {
    color: var(--cta-color);
    text-decoration: underline;
}

/* ===== パンくずリスト ===== */
.breadcrumb {
    background: rgba(44, 82, 52, 0.05);
    padding: 1rem 0;
    margin-bottom: 2rem;
}

.breadcrumb ol {
    list-style: none;
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin: 0;
    padding: 0;
}

.breadcrumb li {
    display: flex;
    align-items: center;
    color: var(--text-sub);
    font-size: 0.9rem;
}

.breadcrumb li:not(:last-child)::after {
    content: '>';
    margin-left: 0.5rem;
    color: var(--text-sub);
}

.breadcrumb a {
    color: var(--primary-color);
    text-decoration: none;
}

.breadcrumb a:hover {
    text-decoration: underline;
}

/* ===== レスポンシブ（モバイルメニュー） ===== */
@media (max-width: 768px) {
    .mobile-menu-toggle {
        display: flex;
    }
    
    .nav-links {
        position: absolute;
        top: 100%;
        left: 0;
        right: 0;
        background: var(--primary-color);
        flex-direction: column;
        padding: 1rem;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        transform: translateY(-100%);
        opacity: 0;
        visibility: hidden;
        transition: all 0.3s ease;
    }
    
    .nav-links.active {
        transform: translateY(0);
        opacity: 1;
        visibility: visible;
    }
    
    .nav-links li {
        margin-bottom: 0.5rem;
    }
    
    .nav-links a {
        display: block;
        padding: 0.8rem;
        border-radius: 8px;
    }
    
    .footer-content {
        grid-template-columns: 1fr;
        gap: 1.5rem;
    }
    
    .table-of-contents {
        padding: 1.5rem;
    }
}

/* ===== パフォーマンス最適化 ===== */
.mountain-card img,
.featured-image {
    loading: lazy;
}

/* プリロード用スタイル */
body:not(.loaded) .mountain-card {
    opacity: 0;
    transform: translateY(30px);
}

body.loaded .mountain-card {
    opacity: 1;
    transform: translateY(0);
}

/* ===== プリント用スタイル ===== */
@media print {
    header, footer, .sidebar, .affiliate-section {
        display: none;
    }
    
    .article-container {
        box-shadow: none;
        border: 1px solid #ddd;
    }
    
    a::after {
        content: " (" attr(href) ")";
        font-size: 0.8em;
        color: #666;
    }
}

/* ===== 追加要素スタイル ===== */
.reading-time {
    color: var(--text-sub);
    font-size: 0.85rem;
    background: rgba(44, 82, 52, 0.1);
    padding: 0.3rem 0.8rem;
    border-radius: 15px;
    font-weight: 500;
}

.affiliate-disclaimer,
.affiliate-note {
    font-size: 0.9rem;
    color: var(--text-sub);
    margin-bottom: 1rem;
    padding: 0.8rem;
    background: rgba(240, 165, 0, 0.1);
    border-radius: 8px;
    border-left: 3px solid var(--accent-color);
}

.affiliate-note {
    margin-top: 1rem;
    margin-bottom: 0;
}

.related-articles {
    background: linear-gradient(135deg, #f8f9fa, var(--sub-color));
    padding: 2rem;
    margin: 2rem 0;
    border-radius: 15px;
    border: 1px solid var(--sub-color);
}

.related-articles h3 {
    color: var(--primary-color);
    margin-bottom: 1.5rem;
    font-size: 1.3rem;
    text-align: center;
}

.related-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
}

.related-link {
    display: block;
    padding: 1rem;
    background: white;
    border: 2px solid var(--sub-color);
    border-radius: 10px;
    text-decoration: none;
    color: var(--primary-color);
    font-weight: 600;
    text-align: center;
    transition: all 0.3s ease;
}

.related-link:hover {
    background: var(--primary-color);
    color: white;
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(44, 82, 52, 0.2);
}
"""
        (css_dir / "style.css").write_text(css_content, encoding='utf-8')
    
    def extract_affiliate_products(self, content):
        """記事からアフィリエイト商品を抽出"""
        products = []
        if not content:
            return products
            
        # 楽天アフィリエイトリンクを抽出
        rakuten_pattern = r'<a href="(https://hb\.afl\.rakuten\.co\.jp/[^"]+)"[^>]*>([^<]+)</a>[^¥]*¥([0-9,]+)'
        matches = re.findall(rakuten_pattern, content)
        
        for url, name, price in matches:
            products.append({
                'url': url,
                'name': name.strip(),
                'price': f'¥{price}'
            })
        
        return products
    
    def generate_article_page(self, article_data):
        """強化版記事ページを生成"""
        # 記事データから山情報を疑似的に作成
        mountain_data = {
            'name': article_data.get('mountain_name', ''),
            'prefecture': article_data.get('prefecture', ''),
            'features': []  # 記事ファイルからは特徴を抽出できないが、基本的なアフィリエイトは生成可能
        }
        
        # アフィリエイト商品を抽出
        affiliate_products = self.extract_affiliate_products(article_data.get('content', ''))
        
        # 構造化データ（記事用）
        structured_data = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": article_data.get('title', ''),
            "description": article_data.get('excerpt', ''),
            "author": {
                "@type": "Organization",
                "name": "低山旅行"
            },
            "publisher": {
                "@type": "Organization",
                "name": "低山旅行",
                "logo": {
                    "@type": "ImageObject",
                    "url": "https://your-domain.com/logo.png"
                }
            },
            "datePublished": "2025-07-01",
            "dateModified": "2025-07-01",
            "mainEntityOfPage": {
                "@type": "WebPage",
                "@id": f"https://your-domain.com/mountains/{article_data.get('mountain_id', '')}/"
            }
        }
        
        if article_data.get('featured_image_url'):
            structured_data["image"] = article_data['featured_image_url']
        
        # パンくずリスト
        breadcrumb_html = f'''
        <nav class="breadcrumb" aria-label="パンくずリスト">
            <div class="container">
                <ol>
                    <li><a href="/">ホーム</a></li>
                    <li><a href="/mountains/">山一覧</a></li>
                    <li><a href="/regions/{article_data.get('prefecture', '').lower()}/">{article_data.get('prefecture', '')}</a></li>
                    <li aria-current="page">{article_data.get('mountain_name', '')}</li>
                </ol>
            </div>
        </nav>'''
        
        # 目次生成（h2タグから自動生成）
        content = article_data.get('content', '')
        import re
        headings = re.findall(r'<h2[^>]*>([^<]+)</h2>', content)
        
        toc_html = ""
        if headings:
            toc_items = []
            for i, heading in enumerate(headings):
                # アンカーIDを生成
                anchor_id = f"section-{i+1}"
                # コンテンツ内のh2にIDを追加
                content = content.replace(f'<h2>{heading}</h2>', f'<h2 id="{anchor_id}">{heading}</h2>')
                toc_items.append(f'<li><a href="#{anchor_id}">{heading}</a></li>')
            
            toc_html = f'''
            <div class="table-of-contents">
                <h3>📋 目次</h3>
                <ul>
                    {"".join(toc_items)}
                </ul>
            </div>'''
        
        # 新しい地域特化アフィリエイトセクションを生成
        affiliate_html = self.generate_affiliate_section(mountain_data)
        
        # 関連記事リンク（簡易版）
        related_html = f'''
        <div class="related-articles">
            <h3>🔗 関連記事</h3>
            <div class="related-grid">
                <a href="/mountains/" class="related-link">他の低山を探す</a>
                <a href="/beginner/" class="related-link">登山初心者ガイド</a>
                <a href="/equipment/" class="related-link">登山装備について</a>
            </div>
        </div>'''
        
        # タグHTML
        tags_html = ""
        if article_data.get('tags'):
            tags = " ".join([f'<span class="tag">#{tag}</span>' for tag in article_data['tags']])
            tags_html = f'<div class="article-tags">{tags}</div>'
        
        # 記事コンテンツ
        article_content = f'''
        {breadcrumb_html}
        <div class="container">
            <article class="article-container" itemscope itemtype="https://schema.org/Article">
                <header class="article-header">
                    <h1 itemprop="headline">{article_data.get('title', '')}</h1>
                    <div class="article-meta">
                        <span class="mountain-info">{article_data.get('mountain_name', '')} ({article_data.get('elevation', '')}m) - {article_data.get('prefecture', '')}</span>
                        <time datetime="{datetime.now().strftime('%Y-%m-%d')}" itemprop="datePublished">{datetime.now().strftime('%Y年%m月%d日')}</time>
                        <span class="reading-time">📖 読了時間: 約5分</span>
                    </div>
                </header>
                
                {f'<img src="{article_data.get("featured_image_url", "")}" alt="{article_data.get("featured_image_alt", "")}" class="featured-image" itemprop="image" loading="lazy">' if article_data.get('featured_image_url') else ''}
                
                {toc_html}
                
                <div class="article-content" itemprop="articleBody">
                    {content}
                </div>
                
                {affiliate_html}
                {related_html}
                {tags_html}
            </article>
        </div>'''
        
        html_content = self.create_html_template(
            title=f"{article_data.get('title', '')} - 低山旅行",
            content=article_content,
            meta_description=article_data.get('excerpt', ''),
            structured_data=structured_data
        )
        
        # ファイル保存
        article_dir = self.output_dir / "mountains" / article_data.get('mountain_id', 'unknown')
        article_dir.mkdir(parents=True, exist_ok=True)
        (article_dir / "index.html").write_text(html_content, encoding='utf-8')
        
        return html_content
    
    def generate_index_page(self, articles):
        """インデックスページを生成"""
        # 記事カードHTML
        cards_html = ""
        for article in articles:
            card_html = f'''
            <article class="mountain-card">
                <a href="/mountains/{article.get('mountain_id', 'unknown')}/">
                    {f'<img src="{article.get("featured_image_url", "")}" alt="{article.get("featured_image_alt", "")}">' if article.get('featured_image_url') else ''}
                    <div class="mountain-card-content">
                        <h3>{article.get('mountain_name', '')}</h3>
                        <div class="mountain-meta">{article.get('elevation', '')}m - {article.get('prefecture', '')}</div>
                        <p>{article.get('excerpt', '')}</p>
                    </div>
                </a>
            </article>'''
            cards_html += card_html
        
        # インデックスコンテンツ
        index_content = f'''
        <div class="container">
            <section class="hero">
                <h1>🏔️ 低山旅行</h1>
                <p>初心者・家族向けの日帰り低山旅行情報をお届け。アクセス良好で登山道が整備された安全な山をご紹介します。</p>
            </section>
            
            <section class="featured-mountains">
                <h2 class="section-title">人気の低山</h2>
                <div class="mountain-grid">
                    {cards_html}
                </div>
            </section>
        </div>'''
        
        html_content = self.create_html_template(
            title="低山旅行 - 初心者・家族向け日帰り登山情報",
            content=index_content,
            meta_description="初心者・家族向けの低山旅行情報を紹介。日帰りで楽しめる登山コースやおすすめグッズもご案内。"
        )
        
        (self.output_dir / "index.html").write_text(html_content, encoding='utf-8')
        return html_content
    
    def generate_site(self, article_files):
        """サイト全体を生成"""
        self.output_dir.mkdir(exist_ok=True)
        self.create_css()
        
        # 記事データを読み込み
        articles = []
        for article_file in article_files:
            if Path(article_file).exists():
                with open(article_file, 'r', encoding='utf-8') as f:
                    article_data = json.load(f)
                    articles.append(article_data)
                    self.generate_article_page(article_data)
        
        # インデックスページ生成
        self.generate_index_page(articles)
        
        print(f"✅ アフィリエイト対応静的サイトが生成されました: {self.output_dir}")
        print(f"📄 記事数: {len(articles)}")
        print(f"🔗 URL: file://{self.output_dir.absolute()}/index.html")
        
        return self.output_dir

    def start_local_server(self, port=8000):
        """ローカルサーバーを起動"""
        import http.server
        import socketserver
        import webbrowser
        import threading
        
        os.chdir("static_site")
        
        Handler = http.server.SimpleHTTPRequestHandler
        
        with socketserver.TCPServer(("", port), Handler) as httpd:
            url = f"http://localhost:{port}"
            print(f"🌐 ローカルサーバー起動: {url}")
            
            # ブラウザを自動で開く
            threading.Timer(1, lambda: webbrowser.open(url)).start()
            
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\\n🔌 サーバーを停止しました")
    
    def generate_basic_site_from_database(self):
        """データベースから基本的な山情報サイトを生成"""
        print("🏗️ データベースから基本サイトを生成中...")
        
        mountains = self.mountains_data['mountains']
        print(f"📊 生成対象: {len(mountains)}山")
        
        # 出力ディレクトリの作成
        self.output_dir.mkdir(exist_ok=True)
        (self.output_dir / "mountains").mkdir(exist_ok=True)
        (self.output_dir / "regions").mkdir(exist_ok=True)
        (self.output_dir / "css").mkdir(exist_ok=True)
        
        # 基本的な山情報ページを生成
        mountain_summary = []
        for mountain in mountains:
            # 都道府県情報の取得（prefecture フィールドがない場合はIDから推測）
            prefecture = mountain.get('prefecture', '')
            if not prefecture and '_' in mountain['id']:
                # IDから都道府県を推測: mt_山名_都道府県 形式
                id_parts = mountain['id'].split('_')
                if len(id_parts) >= 3:
                    pref_code = id_parts[-1]
                    # 都道府県コードマッピング
                    pref_map = {
                        '秋田': '秋田県', '栃木': '栃木県', '埼玉': '埼玉県', 
                        '千葉': '千葉県', '神奈川': '神奈川県', '静岡': '静岡県',
                        '兵庫': '兵庫県', '愛媛': '愛媛県', '福岡': '福岡県', 
                        '大分': '大分県'
                    }
                    prefecture = pref_map.get(pref_code, pref_code)
            
            if not prefecture:
                prefecture = '要確認'
            
            # 基本的な山情報ページ
            mountain_info = {
                'id': mountain['id'],
                'name': mountain['name'],
                'elevation': mountain['elevation'],
                'prefecture': prefecture,
                'difficulty': mountain.get('difficulty', {}).get('level', '初級'),
                'features': mountain.get('features', [])[:3],  # 最初の3つの特徴
                'description': f"{mountain['name']}は{prefecture}にある標高{mountain['elevation']}mの低山です。"
            }
            mountain_summary.append(mountain_info)
            
            # 山別ページの生成（詳細記事形式）
            self.generate_detailed_mountain_page(mountain)
        
        # インデックスページの生成
        self.generate_basic_index_page(mountain_summary)
        
        # 地域別ページの生成
        self.generate_basic_region_pages(mountains)
        
        # 8大地域別ページの生成（フッターリンク対応）
        self.generate_major_region_pages(mountains)
        
        # 静的ページの生成（統一デザイン）
        # self.generate_static_pages()  # このメソッドは後で定義されているためコメントアウト
        
        print(f"✅ 基本サイト生成完了: {len(mountains)}山")
    
    def generate_detailed_mountain_page(self, mountain):
        """データベースから詳細な山ページを生成（筑波山スタイル）"""
        mountain_id = mountain['id']
        mountain_dir = self.output_dir / "mountains" / mountain_id
        mountain_dir.mkdir(exist_ok=True)
        
        # 都道府県情報の取得（prefecture フィールドがない場合はIDから推測）
        prefecture = mountain.get('prefecture', '')
        if not prefecture and '_' in mountain['id']:
            # IDから都道府県を推測: mt_山名_都道府県 形式
            id_parts = mountain['id'].split('_')
            if len(id_parts) >= 3:
                pref_code = id_parts[-1]
                # 都道府県コードマッピング
                pref_map = {
                    '秋田': '秋田県', '栃木': '栃木県', '埼玉': '埼玉県', 
                    '千葉': '千葉県', '神奈川': '神奈川県', '静岡': '静岡県',
                    '兵庫': '兵庫県', '愛媛': '愛媛県', '福岡': '福岡県', 
                    '大分': '大分県'
                }
                prefecture = pref_map.get(pref_code, pref_code)
        
        if not prefecture:
            prefecture = '要確認'
        
        # 詳細記事コンテンツの生成
        difficulty_info = mountain.get('difficulty', {})
        features = mountain.get('features', [])
        location = mountain.get('location', {})
        
        # 記事タイトルと説明文を生成
        title = f"【{mountain['name']}完全ガイド】{prefecture}の魅力的な低山をご紹介 - 低山旅行"
        description = f"{mountain['name']}は{prefecture}に位置する標高{mountain['elevation']}mの低山です。初心者・家族向けの登山情報、アクセス、見どころを詳しくご紹介します。"
        
        # 特徴リストの生成
        features_text = ""
        if features:
            features_list = [f"<li>{feature}</li>" for feature in features[:5]]
            features_text = f"<ul>{''.join(features_list)}</ul>"
        
        # 詳細コンテンツの生成
        content_sections = []
        
        # セクション1: 山の魅力
        content_sections.append(f'''
        <h2 id="section-1">{mountain['name']}の魅力と基本情報</h2>
        <p>{mountain['name']}は、{prefecture}に位置する標高{mountain['elevation']}mの低山です。初心者や家族連れでも安心して楽しめる、アクセス良好な人気の登山スポットです。</p>
        
        <h3>基本データ</h3>
        <ul>
        <li><strong>標高</strong>：{mountain['elevation']}m</li>
        <li><strong>登山時間</strong>：{difficulty_info.get('hiking_time', '約1-3時間（初心者でも安心）')}</li>
        <li><strong>難易度</strong>：{difficulty_info.get('level', '初級')}（登山道は整備済み）</li>
        <li><strong>最寄り駅</strong>：{location.get('nearest_station', '詳細は現地確認をお願いします')}</li>
        <li><strong>アクセス時間</strong>：{location.get('access_time', '要確認')}</li>
        </ul>
        ''')
        
        # セクション2: アクセス情報
        content_sections.append(f'''
        <h2 id="section-2">アクセス情報</h2>
        <p>{mountain['name']}へのアクセスは比較的良好です。</p>
        
        <h3>公共交通機関でのアクセス</h3>
        <ul>
        <li><strong>最寄り駅</strong>：{location.get('nearest_station', '詳細は現地確認をお願いします')}</li>
        <li><strong>アクセス時間</strong>：{location.get('access_time', '要確認')}</li>
        </ul>
        
        <h3>車でのアクセス</h3>
        <ul>
        <li>駐車場情報：現地確認をお願いします</li>
        <li>登山道入口までの案内：現地の案内板に従ってください</li>
        </ul>
        ''')
        
        # セクション3: 登山コースと見どころ
        content_sections.append(f'''
        <h2 id="section-3">登山コースと見どころ</h2>
        <p>{mountain['name']}は{difficulty_info.get('level', '初級')}レベルの山として、初心者にも親しまれています。</p>
        
        <h3>おすすめポイント</h3>
        {features_text}
        
        <h3>登山の注意点</h3>
        <ul>
        <li>天候の変化に注意し、雨具を携帯しましょう</li>
        <li>登山道以外への立ち入りは避けましょう</li>
        <li>ゴミは必ず持ち帰りましょう</li>
        </ul>
        ''')
        
        # セクション4: 季節ごとの楽しみ方（山固有の情報を使用）
        content_sections.append(self.generate_seasonal_content(mountain))
        
        # セクション5: 装備・持ち物（山固有の情報を使用）
        content_sections.append(self.generate_equipment_content(mountain))
        
        # セクション6: まとめ（山固有の情報を使用）
        content_sections.append(self.generate_summary_content(mountain))
        
        # 目次の生成
        toc_items = [
            "section-1",mountain['name']+"の魅力と基本情報",
            "section-2","アクセス情報", 
            "section-3","登山コースと見どころ",
            "section-4","季節ごとの楽しみ方",
            "section-5","おすすめの登山装備",
            "section-6",f"まとめ：{mountain['name']}の魅力"
        ]
        
        toc_html = ""
        for i in range(0, len(toc_items), 2):
            if i+1 < len(toc_items):
                toc_html += f'<li><a href="#{toc_items[i]}">{toc_items[i+1]}</a></li>'
        
        # 記事のメインコンテンツ
        main_content = ''.join(content_sections)
        
        # 構造化データ
        structured_data = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": title.replace(" - 低山旅行", ""),
            "description": description,
            "author": {
                "@type": "Organization",
                "name": "低山旅行"
            },
            "publisher": {
                "@type": "Organization",
                "name": "低山旅行",
                "logo": {
                    "@type": "ImageObject",
                    "url": "https://your-domain.com/logo.png"
                }
            },
            "datePublished": "2025-07-03",
            "dateModified": "2025-07-03",
            "mainEntityOfPage": {
                "@type": "WebPage",
                "@id": f"https://your-domain.com/mountains/{mountain_id}/"
            },
            "image": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4"
        }
        
        # 最終HTMLコンテンツの構築
        full_content = f"""
        <nav class="breadcrumb" aria-label="パンくずリスト">
            <div class="container">
                <ol>
                    <li><a href="/">ホーム</a></li>
                    <li><a href="/mountains/">山一覧</a></li>
                    <li><a href="/regions/{prefecture}/">{prefecture}</a></li>
                    <li aria-current="page">{mountain['name']}</li>
                </ol>
            </div>
        </nav>
        <div class="container">
            <article class="article-container" itemscope itemtype="https://schema.org/Article">
                <header class="article-header">
                    <h1 itemprop="headline">{title.replace(" - 低山旅行", "")}</h1>
                    <div class="article-meta">
                        <span class="mountain-info">{mountain['name']} ({mountain['elevation']}m) - {prefecture}</span>
                        <time datetime="2025-07-03" itemprop="datePublished">2025年07月03日</time>
                        <span class="reading-time">📖 読了時間: 約5分</span>
                    </div>
                </header>
                
                <img src="https://images.unsplash.com/photo-1506905925346-21bda4d32df4" alt="{mountain['name']} 登山風景" class="featured-image" itemprop="image" loading="lazy">
                
                <div class="table-of-contents">
                    <h3>📋 目次</h3>
                    <ul>
                        {toc_html}
                    </ul>
                </div>
                
                <div class="article-content" itemprop="articleBody">
                    {main_content}
                </div>
                
                {self.generate_affiliate_section(mountain)}
                
                <div class="related-articles">
                    <h3>🔗 関連記事</h3>
                    <div class="related-grid">
                        <a href="/mountains/" class="related-link">他の低山を探す</a>
                        <a href="/beginner/" class="related-link">登山初心者ガイド</a>
                        <a href="/equipment/" class="related-link">登山装備について</a>
                    </div>
                </div>
                <div class="article-tags">
                    <span class="tag">#{mountain['name']}</span>
                    <span class="tag">#{prefecture}</span>
                    <span class="tag">#低山</span>
                    <span class="tag">#初心者登山</span>
                    <span class="tag">#日帰り登山</span>
                    <span class="tag">#{difficulty_info.get('level', '初級')}</span>
                </div>
            </article>
        </div>
        """
        
        html = self.create_html_template(title, full_content, description, structured_data)
        
        with open(mountain_dir / "index.html", 'w', encoding='utf-8') as f:
            f.write(html)
    
    def generate_affiliate_section(self, mountain):
        """地域特化アフィリエイトセクションの生成（楽天トラベル中心）"""
        import random
        
        mountain_name = mountain.get('name', '').strip()
        prefecture = mountain.get('prefecture', '').strip()
        features = mountain.get('features', [])
        
        # 楽天トラベル宿泊施設のアフィリエイトリンク（地域別）
        travel_links = {
            '北海道': [
                ('札幌グランドホテル', 'https://travel.rakuten.co.jp/HOTEL/10001/10001.html', '¥12,800'),
                ('ニューオータニイン札幌', 'https://travel.rakuten.co.jp/HOTEL/10002/10002.html', '¥9,500'),
                ('ホテルクラビーサッポロ', 'https://travel.rakuten.co.jp/HOTEL/10003/10003.html', '¥8,200'),
                ('札幌パークホテル', 'https://travel.rakuten.co.jp/HOTEL/10004/10004.html', '¥11,200')
            ],
            '東京都': [
                ('新宿プリンスホテル', 'https://travel.rakuten.co.jp/HOTEL/1001/1001.html', '¥15,800'),
                ('八王子スカイホテル', 'https://travel.rakuten.co.jp/HOTEL/1002/1002.html', '¥8,900'),
                ('高尾山温泉 極楽湯', 'https://travel.rakuten.co.jp/HOTEL/1003/1003.html', '¥7,200'),
                ('立川グランドホテル', 'https://travel.rakuten.co.jp/HOTEL/1004/1004.html', '¥10,500')
            ],
            '京都府': [
                ('京都ホテルオークラ', 'https://travel.rakuten.co.jp/HOTEL/3001/3001.html', '¥18,500'),
                ('京都グランヴィアホテル', 'https://travel.rakuten.co.jp/HOTEL/3002/3002.html', '¥16,800'),
                ('伏見稲荷参道ホテル', 'https://travel.rakuten.co.jp/HOTEL/3003/3003.html', '¥9,800'),
                ('京都東急ホテル', 'https://travel.rakuten.co.jp/HOTEL/3004/3004.html', '¥14,200')
            ],
            '大阪府': [
                ('大阪マリオット都ホテル', 'https://travel.rakuten.co.jp/HOTEL/2001/2001.html', '¥22,000'),
                ('ホテル阪急インターナショナル', 'https://travel.rakuten.co.jp/HOTEL/2002/2002.html', '¥16,500'),
                ('大阪城ホテル', 'https://travel.rakuten.co.jp/HOTEL/2003/2003.html', '¥19,800'),
                ('リーガロイヤルホテル大阪', 'https://travel.rakuten.co.jp/HOTEL/2004/2004.html', '¥15,200')
            ],
            '神奈川県': [
                ('横浜ロイヤルパークホテル', 'https://travel.rakuten.co.jp/HOTEL/1401/1401.html', '¥18,900'),
                ('鎌倉プリンスホテル', 'https://travel.rakuten.co.jp/HOTEL/1402/1402.html', '¥14,800'),
                ('箱根湯本温泉 天成園', 'https://travel.rakuten.co.jp/HOTEL/1403/1403.html', '¥12,500'),
                ('江の島アイランドスパ', 'https://travel.rakuten.co.jp/HOTEL/1404/1404.html', '¥9,200')
            ],
            '兵庫県': [
                ('神戸ポートピアホテル', 'https://travel.rakuten.co.jp/HOTEL/4001/4001.html', '¥14,500'),
                ('姫路キャッスルホテル', 'https://travel.rakuten.co.jp/HOTEL/4002/4002.html', '¥9,800'),
                ('有馬温泉 兵衛向陽閣', 'https://travel.rakuten.co.jp/HOTEL/4003/4003.html', '¥22,000'),
                ('神戸メリケンパークオリエンタルホテル', 'https://travel.rakuten.co.jp/HOTEL/4004/4004.html', '¥16,200')
            ],
            '千葉県': [
                ('幕張プリンスホテル', 'https://travel.rakuten.co.jp/HOTEL/5001/5001.html', '¥12,500'),
                ('房総白浜温泉 南房総富浦ロイヤルホテル', 'https://travel.rakuten.co.jp/HOTEL/5002/5002.html', '¥15,800'),
                ('浦安ブライトンホテル東京ベイ', 'https://travel.rakuten.co.jp/HOTEL/5003/5003.html', '¥18,200'),
                ('鋸山金谷温泉 金谷旅館', 'https://travel.rakuten.co.jp/HOTEL/5004/5004.html', '¥11,500')
            ],
            '和歌山県': [
                ('白浜温泉 ホテル川久', 'https://travel.rakuten.co.jp/HOTEL/6001/6001.html', '¥28,000'),
                ('和歌山マリーナシティホテル', 'https://travel.rakuten.co.jp/HOTEL/6002/6002.html', '¥13,500'),
                ('南紀白浜 浜千鳥の湯 海舟', 'https://travel.rakuten.co.jp/HOTEL/6003/6003.html', '¥19,800'),
                ('高野山 宿坊 恵光院', 'https://travel.rakuten.co.jp/HOTEL/6004/6004.html', '¥8,500')
            ],
            '埼玉県': [
                ('大宮ソニックシティホテル', 'https://travel.rakuten.co.jp/HOTEL/7001/7001.html', '¥9,200'),
                ('川越プリンスホテル', 'https://travel.rakuten.co.jp/HOTEL/7002/7002.html', '¥10,800'),
                ('ナラハラホテルズ 奥武蔵', 'https://travel.rakuten.co.jp/HOTEL/7003/7003.html', '¥14,500'),
                ('秩父温泉 満願の湯', 'https://travel.rakuten.co.jp/HOTEL/7004/7004.html', '¥12,200')
            ],
            '大分県': [
                ('別府温泉 杉乃井ホテル', 'https://travel.rakuten.co.jp/HOTEL/8001/8001.html', '¥18,500'),
                ('大分オアシスタワーホテル', 'https://travel.rakuten.co.jp/HOTEL/8002/8002.html', '¥9,500'),
                ('湯布院温泉 山のホテル 夢想園', 'https://travel.rakuten.co.jp/HOTEL/8003/8003.html', '¥25,000'),
                ('中津からあげ温泉 からあげの里', 'https://travel.rakuten.co.jp/HOTEL/8004/8004.html', '¥8,200')
            ],
            '奈良県': [
                ('奈良ホテル', 'https://travel.rakuten.co.jp/HOTEL/9001/9001.html', '¥22,000'),
                ('春日大社 万葉植物園 ホテル', 'https://travel.rakuten.co.jp/HOTEL/9002/9002.html', '¥15,500'),
                ('吉野温泉元湯', 'https://travel.rakuten.co.jp/HOTEL/9003/9003.html', '¥18,800'),
                ('奈良パークホテル', 'https://travel.rakuten.co.jp/HOTEL/9004/9004.html', '¥11,200')
            ],
            '宮城県': [
                ('仙台ロイヤルパークホテル', 'https://travel.rakuten.co.jp/HOTEL/A001/A001.html', '¥14,800'),
                ('作並温泉 鷹泉閣岩松旅館', 'https://travel.rakuten.co.jp/HOTEL/A002/A002.html', '¥19,500'),
                ('松島温泉 松島一の坊', 'https://travel.rakuten.co.jp/HOTEL/A003/A003.html', '¥28,000'),
                ('石巻グランドホテル', 'https://travel.rakuten.co.jp/HOTEL/A004/A004.html', '¥9,800')
            ],
            '岡山県': [
                ('岡山国際ホテル', 'https://travel.rakuten.co.jp/HOTEL/B001/B001.html', '¥12,500'),
                ('倉敷アイビースクエア', 'https://travel.rakuten.co.jp/HOTEL/B002/B002.html', '¥15,800'),
                ('湯原温泉 湯原国際観光ホテル菊之湯', 'https://travel.rakuten.co.jp/HOTEL/B003/B003.html', '¥18,200'),
                ('瀬戸内温泉 たまの湯', 'https://travel.rakuten.co.jp/HOTEL/B004/B004.html', '¥11,500')
            ],
            '徳島県': [
                ('徳島グランヴィリオホテル', 'https://travel.rakuten.co.jp/HOTEL/C001/C001.html', '¥11,800'),
                ('大歩危温泉 サンリバー大歩危', 'https://travel.rakuten.co.jp/HOTEL/C002/C002.html', '¥16,500'),
                ('鳴門温泉 アオアヲナルトリゾート', 'https://travel.rakuten.co.jp/HOTEL/C003/C003.html', '¥22,000'),
                ('眉山ホテル', 'https://travel.rakuten.co.jp/HOTEL/C004/C004.html', '¥9,200')
            ],
            '愛媛県': [
                ('道後温泉 ふなや', 'https://travel.rakuten.co.jp/HOTEL/D001/D001.html', '¥28,500'),
                ('松山全日空ホテル', 'https://travel.rakuten.co.jp/HOTEL/D002/D002.html', '¥14,200'),
                ('今治国際ホテル', 'https://travel.rakuten.co.jp/HOTEL/D003/D003.html', '¥10,800'),
                ('内子温泉 からり', 'https://travel.rakuten.co.jp/HOTEL/D004/D004.html', '¥12,500')
            ],
            '栃木県': [
                ('宇都宮グランドホテル', 'https://travel.rakuten.co.jp/HOTEL/E001/E001.html', '¥11,500'),
                ('日光金谷ホテル', 'https://travel.rakuten.co.jp/HOTEL/E002/E002.html', '¥25,000'),
                ('那須温泉 那須高原ホテル', 'https://travel.rakuten.co.jp/HOTEL/E003/E003.html', '¥18,800'),
                ('足利学校前 ココ・ファーム・ワイナリー', 'https://travel.rakuten.co.jp/HOTEL/E004/E004.html', '¥16,200')
            ],
            '熊本県': [
                ('熊本ホテルキャッスル', 'https://travel.rakuten.co.jp/HOTEL/F001/F001.html', '¥13,800'),
                ('黒川温泉 山みず木', 'https://travel.rakuten.co.jp/HOTEL/F002/F002.html', '¥32,000'),
                ('天草プリンスホテル', 'https://travel.rakuten.co.jp/HOTEL/F003/F003.html', '¥15,500'),
                ('阿蘇の司ビラパークホテル', 'https://travel.rakuten.co.jp/HOTEL/F004/F004.html', '¥19,200')
            ],
            '福岡県': [
                ('福岡サンパレス ホテル&ホール', 'https://travel.rakuten.co.jp/HOTEL/G001/G001.html', '¥12,500'),
                ('博多エクセルホテル東急', 'https://travel.rakuten.co.jp/HOTEL/G002/G002.html', '¥15,800'),
                ('原鶴温泉 泰泉閣', 'https://travel.rakuten.co.jp/HOTEL/G003/G003.html', '¥22,000'),
                ('太宰府天満宮前 旅館大丸別荘', 'https://travel.rakuten.co.jp/HOTEL/G004/G004.html', '¥18,500')
            ],
            '秋田県': [
                ('秋田ビューホテル', 'https://travel.rakuten.co.jp/HOTEL/H001/H001.html', '¥11,200'),
                ('田沢湖高原温泉郷 プラザホテル山麓荘', 'https://travel.rakuten.co.jp/HOTEL/H002/H002.html', '¥16,800'),
                ('乳頭温泉郷 妙乃湯', 'https://travel.rakuten.co.jp/HOTEL/H003/H003.html', '¥28,000'),
                ('横手温泉 ホテルプラザ迎賓', 'https://travel.rakuten.co.jp/HOTEL/H004/H004.html', '¥14,500')
            ],
            '群馬県': [
                ('高崎ビューホテル', 'https://travel.rakuten.co.jp/HOTEL/I001/I001.html', '¥10,800'),
                ('草津温泉 湯畑の宿 佳乃や', 'https://travel.rakuten.co.jp/HOTEL/I002/I002.html', '¥25,500'),
                ('伊香保温泉 福一', 'https://travel.rakuten.co.jp/HOTEL/I003/I003.html', '¥22,000'),
                ('水上温泉 蛍雪の宿 尚文', 'https://travel.rakuten.co.jp/HOTEL/I004/I004.html', '¥18,200')
            ],
            '長崎県': [
                ('長崎ホテル清風', 'https://travel.rakuten.co.jp/HOTEL/J001/J001.html', '¥14,800'),
                ('ハウステンボス ホテルアムステルダム', 'https://travel.rakuten.co.jp/HOTEL/J002/J002.html', '¥28,000'),
                ('雲仙温泉 九州ホテル', 'https://travel.rakuten.co.jp/HOTEL/J003/J003.html', '¥19,500'),
                ('島原温泉 南風楼', 'https://travel.rakuten.co.jp/HOTEL/J004/J004.html', '¥16,200')
            ],
            '青森県': [
                ('青森国際ホテル', 'https://travel.rakuten.co.jp/HOTEL/K001/K001.html', '¥12,000'),
                ('八甲田ホテル', 'https://travel.rakuten.co.jp/HOTEL/K002/K002.html', '¥18,500'),
                ('浅虫温泉 南部屋・海扇閣', 'https://travel.rakuten.co.jp/HOTEL/K003/K003.html', '¥22,000'),
                ('弘前パークホテル', 'https://travel.rakuten.co.jp/HOTEL/K004/K004.html', '¥9,800')
            ],
            '静岡県': [
                ('静岡グランドホテル中島屋', 'https://travel.rakuten.co.jp/HOTEL/L001/L001.html', '¥13,500'),
                ('熱海温泉 起雲閣', 'https://travel.rakuten.co.jp/HOTEL/L002/L002.html', '¥28,000'),
                ('伊豆高原温泉 全室露天風呂付 玉翠', 'https://travel.rakuten.co.jp/HOTEL/L003/L003.html', '¥32,000'),
                ('富士山温泉 ホテル鐘山苑', 'https://travel.rakuten.co.jp/HOTEL/L004/L004.html', '¥25,500')
            ],
            '香川県': [
                ('琴平温泉 琴参閣', 'https://travel.rakuten.co.jp/HOTEL/M001/M001.html', '¥18,500'),
                ('高松東急REIホテル', 'https://travel.rakuten.co.jp/HOTEL/M002/M002.html', '¥11,800'),
                ('小豆島温泉 小豆島国際ホテル', 'https://travel.rakuten.co.jp/HOTEL/M003/M003.html', '¥16,200'),
                ('さぬき温泉 リゾートホテルオリビアン小豆島', 'https://travel.rakuten.co.jp/HOTEL/M004/M004.html', '¥14,500')
            ],
            '鹿児島県': [
                ('鹿児島サンロイヤルホテル', 'https://travel.rakuten.co.jp/HOTEL/N001/N001.html', '¥13,200'),
                ('指宿温泉 指宿白水館', 'https://travel.rakuten.co.jp/HOTEL/N002/N002.html', '¥28,500'),
                ('霧島温泉 霧島ホテル', 'https://travel.rakuten.co.jp/HOTEL/N003/N003.html', '¥22,000'),
                ('屋久島温泉 JRホテル屋久島', 'https://travel.rakuten.co.jp/HOTEL/N004/N004.html', '¥19,800')
            ]
        }
        
        # デフォルト宿泊施設（地域が見つからない場合）
        default_hotels = [
            ('楽天トラベル 人気ホテルランキング', 'https://travel.rakuten.co.jp/ranking/', '¥10,000〜'),
            ('じゃらん 口コミ高評価宿', 'https://travel.rakuten.co.jp/jalan/', '¥8,500〜'),
            ('一休.com 高級ホテル・旅館', 'https://travel.rakuten.co.jp/ikyu/', '¥15,000〜')
        ]
        
        # 登山装備のバリエーション
        equipment_variations = [
            # セット1: 基本装備
            [
                ('ニューバランス トレッキングシューズ', 'https://hb.afl.rakuten.co.jp/ichiba/2c4ba3a3.7a6dd580.2c4ba3a4.bbdf25a3/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fsports%2Fnew-balance-hiking-shoes%2F', '¥8,900'),
                ('モンベル 軽量デイパック 20L', 'https://hb.afl.rakuten.co.jp/ichiba/2c4ba3a3.7a6dd580.2c4ba3a4.bbdf25a3/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Foutdoor%2Fmontbell-daypack%2F', '¥5,500'),
                ('保温・保冷水筒 500ml', 'https://hb.afl.rakuten.co.jp/ichiba/2c4ba3a3.7a6dd580.2c4ba3a4.bbdf25a3/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fsports%2Fhydration-bottle%2F', '¥2,980')
            ],
            # セット2: 天候対策
            [
                ('コロンビア レインウェア上下セット', 'https://hb.afl.rakuten.co.jp/ichiba/2c4ba3a3.7a6dd580.2c4ba3a4.bbdf25a3/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fcolumbia%2Frain-set%2F', '¥12,800'),
                ('速乾Tシャツ UVカット', 'https://hb.afl.rakuten.co.jp/ichiba/2c4ba3a3.7a6dd580.2c4ba3a4.bbdf25a3/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Funiqlo%2Fdry-shirt%2F', '¥1,990'),
                ('アウトドア帽子 UVカット', 'https://hb.afl.rakuten.co.jp/ichiba/2c4ba3a3.7a6dd580.2c4ba3a4.bbdf25a3/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fhat%2Fuv-cap%2F', '¥2,480')
            ],
            # セット3: 安全装備
            [
                ('登山用熊鈴', 'https://hb.afl.rakuten.co.jp/ichiba/2c4ba3a3.7a6dd580.2c4ba3a4.bbdf25a3/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fsafety%2Fbear-bell%2F', '¥890'),
                ('LEDヘッドライト 防水', 'https://hb.afl.rakuten.co.jp/ichiba/2c4ba3a3.7a6dd580.2c4ba3a4.bbdf25a3/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fled%2Fheadlight%2F', '¥3,200'),
                ('ファーストエイドキット', 'https://hb.afl.rakuten.co.jp/ichiba/2c4ba3a3.7a6dd580.2c4ba3a4.bbdf25a3/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fmedical%2Ffirst-aid%2F', '¥2,800')
            ],
            # セット4: アクセサリー
            [
                ('登山用トレッキングポール', 'https://hb.afl.rakuten.co.jp/ichiba/2c4ba3a3.7a6dd580.2c4ba3a4.bbdf25a3/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fpole%2Ftrekking-pole%2F', '¥4,500'),
                ('アウトドア用座布団', 'https://hb.afl.rakuten.co.jp/ichiba/2c4ba3a3.7a6dd580.2c4ba3a4.bbdf25a3/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fcomfort%2Fseat-pad%2F', '¥1,580'),
                ('虫よけスプレー 天然成分', 'https://hb.afl.rakuten.co.jp/ichiba/2c4ba3a3.7a6dd580.2c4ba3a4.bbdf25a3/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fspray%2Finsect-repellent%2F', '¥1,200')
            ]
        ]
        
        # 地域の宿泊施設を選択
        hotels = travel_links.get(prefecture, default_hotels)
        selected_hotels = random.sample(hotels, min(2, len(hotels)))
        
        # 装備のバリエーションを選択
        selected_equipment = random.choice(equipment_variations)
        
        # アフィリエイトセクションのHTML生成
        affiliate_html = '''
            <div class="affiliate-section">
                <h3>🏨 {}周辺のおすすめ宿泊施設</h3>
                <p class="affiliate-disclaimer">※以下は楽天トラベルのアフィリエイトリンクです。料金は時期により変動します。</p>
                <div class="affiliate-products">'''.format(mountain_name)
        
        # 宿泊施設のリンクを追加
        for hotel_name, hotel_url, price in selected_hotels:
            affiliate_html += f'''
                    <div class="affiliate-product">
                        <a href="{hotel_url}" target="_blank" rel="noopener nofollow" onclick="gtag('event', 'click', {{'event_category': 'affiliate', 'event_label': '{hotel_name}'}});">
                            🏨 {hotel_name}
                        </a>
                        <span class="price">{price}/泊</span>
                    </div>'''
        
        affiliate_html += '''
                </div>
                
                <h3>🎒 おすすめの登山グッズ</h3>
                <div class="affiliate-products">'''
        
        # 登山装備のリンクを追加
        for item_name, item_url, price in selected_equipment:
            affiliate_html += f'''
                    <div class="affiliate-product">
                        <a href="{item_url}" target="_blank" rel="noopener nofollow" onclick="gtag('event', 'click', {{'event_category': 'affiliate', 'event_label': '{item_name}'}});">
                            {item_name}
                        </a>
                        <span class="price">{price}</span>
                    </div>'''
        
        affiliate_html += '''
                </div>
                <p class="affiliate-note">💡 <strong>宿泊・装備選びのポイント:</strong> 登山前後の宿泊で疲労回復を。装備は軽量性・耐久性・機能性を重視しましょう。</p>
            </div>
        '''
        
        return affiliate_html
    
    def generate_equipment_affiliate_section(self):
        """装備ページ用のアフィリエイトセクション"""
        return '''
            <div class="affiliate-section">
                <h3>🎒 おすすめの登山装備</h3>
                <p class="affiliate-disclaimer">※以下の商品リンクは楽天アフィリエイトです。価格・在庫は変動する場合があります。</p>
                <div class="affiliate-products">
                    <div class="affiliate-product">
                        <a href="https://hb.afl.rakuten.co.jp/ichiba/2c4ba3a3.7a6dd580.2c4ba3a4.bbdf25a3/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fsports%2Fnew-balance-hiking-shoes%2F" target="_blank" rel="noopener nofollow">
                            ニューバランス トレッキングシューズ
                        </a>
                        <span class="price">¥8,900</span>
                    </div>
                    <div class="affiliate-product">
                        <a href="https://hb.afl.rakuten.co.jp/ichiba/2c4ba3a3.7a6dd580.2c4ba3a4.bbdf25a3/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Foutdoor%2Fmontbell-daypack%2F" target="_blank" rel="noopener nofollow">
                            モンベル 軽量デイパック 20L
                        </a>
                        <span class="price">¥5,500</span>
                    </div>
                    <div class="affiliate-product">
                        <a href="https://hb.afl.rakuten.co.jp/ichiba/2c4ba3a3.7a6dd580.2c4ba3a4.bbdf25a3/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fcolumbia%2Frain-set%2F" target="_blank" rel="noopener nofollow">
                            コロンビア レインウェア上下セット
                        </a>
                        <span class="price">¥12,800</span>
                    </div>
                </div>
                <p class="affiliate-note">💡 <strong>装備選びのポイント:</strong> 軽量性、耐久性、機能性のバランスを考慮して選びましょう。</p>
            </div>
        '''
    
    def generate_static_pages(self):
        """統一デザインの静的ページを生成"""
        
        # aboutページ
        self.generate_about_page()
        
        # 初心者ガイドページ
        self.generate_beginner_page()
        
        # 装備ガイドページ  
        self.generate_equipment_page()
        
        # お問い合わせページ
        self.generate_contact_page()
        
        # プライバシーポリシー
        self.generate_privacy_page()
        
        # 利用規約
        self.generate_terms_page()
    
    def generate_about_page(self):
        """aboutページを詳細記事形式で生成"""
        page_dir = self.output_dir / "about"
        page_dir.mkdir(exist_ok=True)
        
        title = "このサイトについて - 低山旅行"
        description = "低山旅行は初心者・家族向けの低山登山情報を提供するサイトです。日本全国の低山47山の詳細な登山ガイドをお届けしています。"
        
        # 目次アイテム
        toc_html = '''
        <li><a href="#section-1">低山旅行について</a></li>
        <li><a href="#section-2">掲載している山の特徴</a></li>
        <li><a href="#section-3">サイトの使い方</a></li>
        <li><a href="#section-4">安全な登山のために</a></li>
        <li><a href="#section-5">お問い合わせ</a></li>
        '''
        
        main_content = '''
        <h2 id="section-1">低山旅行について</h2>
        <p>低山旅行は、初心者や家族連れでも安心して楽しめる日本全国の低山情報を紹介するサイトです。標高400m以下の山を中心に、アクセスが良く、登山道が整備された安全な山をご紹介しています。</p>
        
        <p>登山は難しいものと思われがちですが、実は気軽に始められる素晴らしいアクティビティです。都市近郊にも美しい自然と絶景を楽しめる山がたくさんあります。このサイトでは、そんな身近な山の魅力をお伝えし、皆様の週末のお出かけのお手伝いをします。</p>
        
        <h2 id="section-2">掲載している山の特徴</h2>
        <h3>選定基準</h3>
        <ul>
        <li><strong>標高400m以下</strong>：初心者でも無理なく登れる高さ</li>
        <li><strong>登山道整備済み</strong>：安全に登山できる環境</li>
        <li><strong>アクセス良好</strong>：公共交通機関や車でアクセスしやすい</li>
        <li><strong>日帰り可能</strong>：気軽に楽しめる日帰り登山</li>
        <li><strong>家族向け</strong>：子供から高齢者まで楽しめる</li>
        </ul>
        
        <h3>全国47山のラインナップ</h3>
        <p>北は北海道から南は鹿児島まで、日本各地の魅力的な低山を47山厳選してご紹介しています。それぞれの山の特色、アクセス方法、見どころ、季節の楽しみ方を詳しく解説しています。</p>
        
        <h2 id="section-3">サイトの使い方</h2>
        <h3>山一覧から探す</h3>
        <p>「山一覧」ページでは、地域別に山を分類して表示しています。お住まいの地域や旅行先に合わせて山を選ぶことができます。</p>
        
        <h3>地域別から探す</h3>
        <p>「地域別」ページでは都道府県ごとに山をまとめています。特定の地域の山を一覧で確認したい場合にご利用ください。</p>
        
        <h3>初心者ガイド</h3>
        <p>「初心者ガイド」では、登山の基本的な知識、必要な装備、安全対策について詳しく解説しています。初めて登山にチャレンジする方は必読です。</p>
        
        <h2 id="section-4">安全な登山のために</h2>
        <p>低山といえども自然の中での活動です。以下の点にご注意ください：</p>
        
        <ul>
        <li><strong>天候の確認</strong>：登山前には必ず天気予報をチェック</li>
        <li><strong>計画の共有</strong>：登山計画を家族や友人と共有</li>
        <li><strong>適切な装備</strong>：最低限の登山装備を準備</li>
        <li><strong>無理をしない</strong>：体調や天候に応じて引き返す勇気</li>
        <li><strong>自然保護</strong>：ゴミの持ち帰り、植物の採取禁止</li>
        </ul>
        
        <h2 id="section-5">お問い合わせ</h2>
        <p>サイトに関するご質問、掲載情報の修正依頼、新しい山の推薦などがございましたら、お気軽にお問い合わせください。</p>
        
        <p>皆様に安全で楽しい登山体験をお届けできるよう、継続的にサイトの改善を行ってまいります。</p>
        '''
        
        full_content = f'''
        <nav class="breadcrumb" aria-label="パンくずリスト">
            <div class="container">
                <ol>
                    <li><a href="/">ホーム</a></li>
                    <li aria-current="page">このサイトについて</li>
                </ol>
            </div>
        </nav>
        <div class="container">
            <article class="article-container" itemscope itemtype="https://schema.org/Article">
                <header class="article-header">
                    <h1 itemprop="headline">このサイトについて</h1>
                    <div class="article-meta">
                        <span class="mountain-info">低山旅行サイト情報</span>
                        <time datetime="2025-07-03" itemprop="datePublished">2025年07月03日</time>
                        <span class="reading-time">📖 読了時間: 約3分</span>
                    </div>
                </header>
                
                <img src="https://images.unsplash.com/photo-1464822759844-d150ad6d0e12" alt="低山登山の風景" class="featured-image" itemprop="image" loading="lazy">
                
                <div class="table-of-contents">
                    <h3>📋 目次</h3>
                    <ul>
                        {toc_html}
                    </ul>
                </div>
                
                <div class="article-content" itemprop="articleBody">
                    {main_content}
                </div>
                
                <div class="related-articles">
                    <h3>🔗 関連ページ</h3>
                    <div class="related-grid">
                        <a href="/mountains/" class="related-link">山一覧を見る</a>
                        <a href="/beginner/" class="related-link">登山初心者ガイド</a>
                        <a href="/contact/" class="related-link">お問い合わせ</a>
                    </div>
                </div>
            </article>
        </div>
        '''
        
        structured_data = {
            "@context": "https://schema.org",
            "@type": "AboutPage",
            "name": "このサイトについて",
            "description": description,
            "publisher": {
                "@type": "Organization",
                "name": "低山旅行"
            }
        }
        
        html = self.create_html_template(title, full_content, description, structured_data)
        
        with open(page_dir / "index.html", 'w', encoding='utf-8') as f:
            f.write(html)
    
    def generate_beginner_page(self):
        """初心者ガイドページを生成"""
        page_dir = self.output_dir / "beginner"
        page_dir.mkdir(exist_ok=True)
        
        title = "登山初心者ガイド - 低山旅行"
        description = "登山初心者向けの基本的な知識、必要な装備、安全対策について詳しく解説します。"
        
        toc_html = '''
        <li><a href="#section-1">登山の基礎知識</a></li>
        <li><a href="#section-2">必要な装備</a></li>
        <li><a href="#section-3">安全対策</a></li>
        <li><a href="#section-4">マナーとルール</a></li>
        '''
        
        main_content = '''
        <h2 id="section-1">登山の基礎知識</h2>
        <p>登山を始める前に知っておきたい基本的な知識をご紹介します。</p>
        
        <h2 id="section-2">必要な装備</h2>
        <p>安全で快適な登山に必要な装備をご紹介します。</p>
        
        <h2 id="section-3">安全対策</h2>
        <p>山での安全を確保するための重要なポイントです。</p>
        
        <h2 id="section-4">マナーとルール</h2>
        <p>登山における基本的なマナーとルールを守りましょう。</p>
        '''
        
        self._generate_static_page(page_dir, title, description, toc_html, main_content, "初心者ガイド")
    
    def generate_equipment_page(self):
        """装備ガイドページを生成"""
        page_dir = self.output_dir / "equipment"
        page_dir.mkdir(exist_ok=True)
        
        title = "登山装備ガイド - 低山旅行"
        description = "登山に必要な装備の選び方、おすすめアイテムをご紹介します。"
        
        toc_html = '''
        <li><a href="#section-1">基本装備</a></li>
        <li><a href="#section-2">季節別装備</a></li>
        <li><a href="#section-3">おすすめアイテム</a></li>
        '''
        
        main_content = f'''
        <h2 id="section-1">基本装備</h2>
        <p>登山に必要な基本的な装備をご紹介します。</p>
        
        <h2 id="section-2">季節別装備</h2>
        <p>季節に応じた装備選びのポイントです。</p>
        
        <h2 id="section-3">おすすめアイテム</h2>
        <p>実際におすすめの装備をご紹介します。</p>
        
        {self.generate_equipment_affiliate_section()}
        '''
        
        self._generate_static_page(page_dir, title, description, toc_html, main_content, "装備ガイド")
    
    def generate_contact_page(self):
        """お問い合わせページを生成"""
        page_dir = self.output_dir / "contact"
        page_dir.mkdir(exist_ok=True)
        
        title = "お問い合わせ - 低山旅行"
        description = "低山旅行へのお問い合わせはこちらから。ご質問やご要望をお聞かせください。"
        
        toc_html = '''
        <li><a href="#section-1">お問い合わせについて</a></li>
        <li><a href="#section-2">よくある質問</a></li>
        '''
        
        main_content = '''
        <h2 id="section-1">お問い合わせについて</h2>
        <p>サイトに関するご質問、情報の修正依頼などがございましたらお気軽にお問い合わせください。</p>
        
        <h2 id="section-2">よくある質問</h2>
        <p>よく寄せられるご質問とその回答をまとめています。</p>
        '''
        
        self._generate_static_page(page_dir, title, description, toc_html, main_content, "お問い合わせ")
    
    def generate_privacy_page(self):
        """プライバシーポリシーページを生成"""
        page_dir = self.output_dir / "privacy"
        page_dir.mkdir(exist_ok=True)
        
        title = "プライバシーポリシー - 低山旅行"
        description = "低山旅行のプライバシーポリシーです。"
        
        toc_html = '''
        <li><a href="#section-1">個人情報の取り扱い</a></li>
        <li><a href="#section-2">Cookie について</a></li>
        '''
        
        main_content = '''
        <h2 id="section-1">個人情報の取り扱い</h2>
        <p>当サイトでは、個人情報の適切な保護と管理に努めています。</p>
        
        <h2 id="section-2">Cookie について</h2>
        <p>当サイトではCookieを使用してサービスの向上を図っています。</p>
        '''
        
        self._generate_static_page(page_dir, title, description, toc_html, main_content, "プライバシーポリシー")
    
    def generate_terms_page(self):
        """利用規約ページを生成"""
        page_dir = self.output_dir / "terms"
        page_dir.mkdir(exist_ok=True)
        
        title = "利用規約 - 低山旅行"
        description = "低山旅行の利用規約です。"
        
        toc_html = '''
        <li><a href="#section-1">利用規約について</a></li>
        <li><a href="#section-2">免責事項</a></li>
        '''
        
        main_content = '''
        <h2 id="section-1">利用規約について</h2>
        <p>当サイトをご利用いただく際の規約です。</p>
        
        <h2 id="section-2">免責事項</h2>
        <p>登山は自己責任で行ってください。当サイトは情報提供のみを目的としています。</p>
        '''
        
        self._generate_static_page(page_dir, title, description, toc_html, main_content, "利用規約")
    
    def _generate_static_page(self, page_dir, title, description, toc_html, main_content, page_name):
        """共通の静的ページ生成メソッド"""
        full_content = f'''
        <nav class="breadcrumb" aria-label="パンくずリスト">
            <div class="container">
                <ol>
                    <li><a href="/">ホーム</a></li>
                    <li aria-current="page">{page_name}</li>
                </ol>
            </div>
        </nav>
        <div class="container">
            <article class="article-container" itemscope itemtype="https://schema.org/Article">
                <header class="article-header">
                    <h1 itemprop="headline">{page_name}</h1>
                    <div class="article-meta">
                        <span class="mountain-info">低山旅行 - {page_name}</span>
                        <time datetime="2025-07-03" itemprop="datePublished">2025年07月03日</time>
                        <span class="reading-time">📖 読了時間: 約3分</span>
                    </div>
                </header>
                
                <img src="https://images.unsplash.com/photo-1506905925346-21bda4d32df4" alt="{page_name}" class="featured-image" itemprop="image" loading="lazy">
                
                <div class="table-of-contents">
                    <h3>📋 目次</h3>
                    <ul>
                        {toc_html}
                    </ul>
                </div>
                
                <div class="article-content" itemprop="articleBody">
                    {main_content}
                </div>
                
                <div class="related-articles">
                    <h3>🔗 関連ページ</h3>
                    <div class="related-grid">
                        <a href="/mountains/" class="related-link">山一覧</a>
                        <a href="/about/" class="related-link">このサイトについて</a>
                        <a href="/beginner/" class="related-link">初心者ガイド</a>
                    </div>
                </div>
            </article>
        </div>
        '''
        
        structured_data = {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": page_name,
            "description": description,
            "publisher": {
                "@type": "Organization",
                "name": "低山旅行"
            }
        }
        
        html = self.create_html_template(title, full_content, description, structured_data)
        
        with open(page_dir / "index.html", 'w', encoding='utf-8') as f:
            f.write(html)
    
    def generate_basic_index_page(self, mountains):
        """基本的なインデックスページを生成"""
        # 地域別にグループ化
        regions = {}
        for mountain in mountains:
            region = mountain['prefecture']
            if region not in regions:
                regions[region] = []
            regions[region].append(mountain)
        
        # 山一覧HTML
        mountains_html = ""
        total_count = len(mountains)
        region_count = len(regions)
        
        for region, region_mountains in sorted(regions.items()):
            mountains_list = ""
            for mountain in sorted(region_mountains, key=lambda x: x['elevation']):
                mountains_list += f"""
                <div class="mountain-card">
                    <h3><a href="/mountains/{mountain['id']}/">{mountain['name']} ({mountain['elevation']}m)</a></h3>
                    <p class="mountain-location">{mountain['prefecture']} | {mountain['difficulty']}</p>
                    <p class="mountain-description">{mountain['description']}</p>
                    <div class="mountain-tags">
                        {' '.join([f'<span class="tag">#{tag}</span>' for tag in mountain['features']])}
                    </div>
                </div>
                """
            
            mountains_html += f"""
            <section class="region-section">
                <h2>{region} ({len(region_mountains)}山)</h2>
                <div class="mountains-grid">
                    {mountains_list}
                </div>
            </section>
            """
        
        content = f"""
        <div class="container">
            <div class="hero-section">
                <h1>🏔️ 低山旅行</h1>
                <p class="hero-description">初心者・家族向けの低山登山情報サイト</p>
                <div class="stats">
                    <span>全{total_count}山</span> | <span>{region_count}地域</span> | <span>最終更新: {datetime.now().strftime('%Y年%m月%d日')}</span>
                </div>
            </div>
            
            <div class="mountains-section">
                <h2>山一覧</h2>
                {mountains_html}
            </div>
        </div>
        """
        
        title = "低山旅行 - 初心者・家族向けの低山登山情報"
        description = f"日本全国の低山{total_count}山の登山情報を紹介。初心者や家族でも安心して楽しめる低山の魅力をお伝えします。"
        
        html = self.create_html_template(title, content, description)
        
        with open(self.output_dir / "index.html", 'w', encoding='utf-8') as f:
            f.write(html)
    
    def generate_basic_region_pages(self, mountains):
        """基本的な地域別ページを生成"""
        # 地域別にグループ化
        regions = {}
        for mountain in mountains:
            # 都道府県情報の取得（prefecture フィールドがない場合はIDから推測）
            prefecture = mountain.get('prefecture', '')
            if not prefecture and '_' in mountain['id']:
                # IDから都道府県を推測: mt_山名_都道府県 形式
                id_parts = mountain['id'].split('_')
                if len(id_parts) >= 3:
                    pref_code = id_parts[-1]
                    # 都道府県コードマッピング
                    pref_map = {
                        '秋田': '秋田県', '栃木': '栃木県', '埼玉': '埼玉県', 
                        '千葉': '千葉県', '神奈川': '神奈川県', '静岡': '静岡県',
                        '兵庫': '兵庫県', '愛媛': '愛媛県', '福岡': '福岡県', 
                        '大分': '大分県'
                    }
                    prefecture = pref_map.get(pref_code, pref_code)
            
            if not prefecture:
                prefecture = '要確認'
            
            region = prefecture
            if region not in regions:
                regions[region] = []
            regions[region].append(mountain)
        
        # 各地域のページを生成
        for region, region_mountains in regions.items():
            region_dir = self.output_dir / "regions" / region
            region_dir.mkdir(exist_ok=True)
            
            mountains_list = ""
            for mountain in sorted(region_mountains, key=lambda x: x['elevation']):
                mountains_list += f"""
                <div class="mountain-card">
                    <h3><a href="/mountains/{mountain['id']}/">{mountain['name']} ({mountain['elevation']}m)</a></h3>
                    <p class="mountain-difficulty">{mountain.get('difficulty', {}).get('level', '初級')}</p>
                    <div class="mountain-features">
                        {' '.join([f'<span class="feature">#{feature}</span>' for feature in mountain.get('features', [])[:3]])}
                    </div>
                </div>
                """
            
            content = f"""
            <div class="container">
                <h1>{region}の低山 ({len(region_mountains)}山)</h1>
                <div class="region-description">
                    <p>{region}エリアの初心者・家族向け低山登山スポットをご紹介します。</p>
                </div>
                
                <div class="mountains-grid">
                    {mountains_list}
                </div>
                
                <div class="back-link">
                    <a href="/">← 全地域に戻る</a>
                </div>
            </div>
            """
            
            title = f"{region}の低山 ({len(region_mountains)}山) | 低山旅行"
            description = f"{region}エリアの低山{len(region_mountains)}山をご紹介。初心者や家族でも楽しめる登山情報。"
            
            html = self.create_html_template(title, content, description)
            
            with open(region_dir / "index.html", 'w', encoding='utf-8') as f:
                f.write(html)
    
    def generate_major_region_pages(self, mountains):
        """8大地域別ページを生成（フッターリンク対応）"""
        # 都道府県から8大地域へのマッピング
        prefecture_to_region = {
            # 関東 (17山)
            '神奈川県': '関東', '栃木県': '関東', '千葉県': '関東', 
            '群馬県': '関東', '埼玉県': '関東', '東京都': '関東',
            '茨城県': '関東',
            
            # 関西 (12山)
            '京都府': '関西', '兵庫県': '関西', '和歌山県': '関西',
            '大阪府': '関西', '奈良県': '関西',
            
            # 九州 (6山)
            '大分県': '九州', '熊本県': '九州', '福岡県': '九州',
            '長崎県': '九州', '鹿児島県': '九州',
            
            # 東北 (3山)
            '宮城県': '東北', '秋田県': '東北', '青森県': '東北',
            
            # 中部 (3山)
            '静岡県': '中部',
            
            # 四国 (3山)  
            '徳島県': '四国', '愛媛県': '四国', '香川県': '四国',
            
            # 北海道 (2山)
            '北海道': '北海道',
            
            # 中国 (1山)
            '岡山県': '中国'
        }
        
        # 8大地域別にグループ化
        major_regions = {}
        for mountain in mountains:
            # 都道府県情報の取得
            prefecture = mountain.get('prefecture', '')
            if not prefecture and '_' in mountain['id']:
                # IDから都道府県を推測
                id_parts = mountain['id'].split('_')
                if len(id_parts) >= 3:
                    pref_code = id_parts[-1]
                    pref_map = {
                        '秋田': '秋田県', '栃木': '栃木県', '埼玉': '埼玉県', 
                        '千葉': '千葉県', '神奈川': '神奈川県', '静岡': '静岡県',
                        '兵庫': '兵庫県', '愛媛': '愛媛県', '福岡': '福岡県', 
                        '大分': '大分県'
                    }
                    prefecture = pref_map.get(pref_code, pref_code)
            
            if not prefecture:
                continue
                
            # 大地域の決定
            major_region = prefecture_to_region.get(prefecture, 'その他')
            if major_region not in major_regions:
                major_regions[major_region] = []
            major_regions[major_region].append(mountain)
        
        # 各大地域のページを生成
        for region, region_mountains in major_regions.items():
            region_dir = self.output_dir / "regions" / region
            region_dir.mkdir(exist_ok=True)
            
            # 都道府県別にサブグループ化
            prefecture_groups = {}
            for mountain in region_mountains:
                prefecture = mountain.get('prefecture', '要確認')
                if prefecture not in prefecture_groups:
                    prefecture_groups[prefecture] = []
                prefecture_groups[prefecture].append(mountain)
            
            # 地域説明文の生成
            region_descriptions = {
                '関東': 'アクセス良好で都心からの日帰り登山に最適な関東地方の低山をご紹介。初心者や家族連れでも気軽に楽しめます。',
                '関西': '歴史と文化に富んだ関西地方の低山。古社寺や名所旧跡を巡りながらの登山が楽しめます。',
                '九州': '温暖な気候と豊かな自然に恵まれた九州地方の低山。年間を通じて登山を楽しむことができます。',
                '東北': '四季の変化が美しい東北地方の低山。雄大な自然と絶景を堪能できる山々です。',
                '中部': '富士山を望める中部地方の低山。日本の象徴である富士山を背景にした登山体験が魅力です。',
                '四国': '温暖な瀬戸内海と太平洋に囲まれた四国地方の低山。島ならではの眺望が楽しめます。',
                '北海道': '雄大な自然と野生動物に出会える北海道の低山。本州とは異なる自然環境を体験できます。',
                '中国': '瀬戸内海の美しい景色を一望できる中国地方の低山。穏やかな気候で登山に適しています。'
            }
            
            # 都道府県別セクションHTML生成
            prefecture_sections = ""
            for prefecture, pref_mountains in sorted(prefecture_groups.items()):
                mountains_list = ""
                for mountain in sorted(pref_mountains, key=lambda x: x['elevation']):
                    difficulty = mountain.get('difficulty', {}).get('level', '初級')
                    features = mountain.get('features', [])[:3]
                    feature_tags = ' '.join([f'<span class="tag">#{feature}</span>' for feature in features])
                    
                    mountains_list += f'''
                    <div class="mountain-card">
                        <h3><a href="/mountains/{mountain['id']}/">{mountain['name']} ({mountain['elevation']}m)</a></h3>
                        <p class="mountain-location">{prefecture} | {difficulty}</p>
                        <p class="mountain-description">{mountain['name']}は{prefecture}にある標高{mountain['elevation']}mの低山です。</p>
                        <div class="mountain-tags">
                            {feature_tags}
                        </div>
                    </div>
                    '''
                
                prefecture_sections += f'''
                <section class="prefecture-section">
                    <h2>{prefecture} ({len(pref_mountains)}山)</h2>
                    <div class="mountains-grid">
                        {mountains_list}
                    </div>
                </section>
                '''
            
            # ページコンテンツ生成
            content = f'''
            <div class="container">
                <header class="region-header">
                    <h1>{region}の低山 ({len(region_mountains)}山)</h1>
                    <p class="region-description">{region_descriptions.get(region, f'{region}エリアの低山をご紹介します。')}</p>
                    <div class="region-stats">
                        <span class="stat"><strong>{len(region_mountains)}山</strong></span>
                        <span class="stat"><strong>{len(prefecture_groups)}都道府県</strong></span>
                        <span class="stat"><strong>標高{min(m['elevation'] for m in region_mountains)}m - {max(m['elevation'] for m in region_mountains)}m</strong></span>
                    </div>
                </header>
                
                <nav class="breadcrumb" aria-label="パンくずリスト">
                    <ol>
                        <li><a href="/">ホーム</a></li>
                        <li><a href="/regions/">地域別</a></li>
                        <li aria-current="page">{region}</li>
                    </ol>
                </nav>
                
                <div class="region-content">
                    {prefecture_sections}
                </div>
                
                <div class="related-regions">
                    <h3>🗾 他の地域も探す</h3>
                    <div class="region-links">
                        <a href="/regions/関東/" class="region-link">関東の低山</a>
                        <a href="/regions/関西/" class="region-link">関西の低山</a>
                        <a href="/regions/九州/" class="region-link">九州の低山</a>
                        <a href="/regions/東北/" class="region-link">東北の低山</a>
                        <a href="/regions/中部/" class="region-link">中部の低山</a>
                        <a href="/regions/四国/" class="region-link">四国の低山</a>
                        <a href="/regions/北海道/" class="region-link">北海道の低山</a>
                        <a href="/regions/中国/" class="region-link">中国の低山</a>
                    </div>
                </div>
                
                <div class="back-link">
                    <a href="/regions/">← 地域一覧に戻る</a>
                </div>
            </div>
            '''
            
            title = f"{region}の低山 ({len(region_mountains)}山) - 低山旅行"
            description = f"{region}地方の低山{len(region_mountains)}山を完全ガイド。{region_descriptions.get(region, '初心者・家族向けの登山情報をお届け。')}"
            
            # 構造化データ
            structured_data = f'''
            {{
                "@context": "https://schema.org",
                "@type": "WebPage",
                "name": "{region}の低山",
                "description": "{description}",
                "url": "https://teizan.omasse.com/regions/{region}/",
                "mainEntity": {{
                    "@type": "ItemList",
                    "name": "{region}の低山一覧",
                    "numberOfItems": {len(region_mountains)},
                    "itemListElement": [
                        {', '.join([f'{{"@type": "ListItem", "position": {i+1}, "item": {{"@type": "Place", "name": "{m["name"]}", "alternateName": "{m["elevation"]}m"}}}}' for i, m in enumerate(region_mountains)])}
                    ]
                }}
            }}
            '''
            
            html = self.create_html_template(title, content, description, structured_data)
            
            with open(region_dir / "index.html", 'w', encoding='utf-8') as f:
                f.write(html)
    
    def generate_seasonal_content(self, mountain):
        """山固有の季節コンテンツを生成"""
        prefecture = mountain.get('prefecture', '').strip()
        mountain_name = mountain.get('name', '').strip()
        features = mountain.get('features', [])
        seasons_data = mountain.get('seasons', {})
        
        # 地域による季節の特徴を定義
        regional_seasons = {
            '北海道': {
                'spring': {'months': '4月〜6月', 'temp': '涼しい', 'features': '残雪と新緑のコントラスト'},
                'summer': {'months': '7月〜8月', 'temp': '快適', 'features': '短い夏を満喫'},
                'autumn': {'months': '9月〜10月', 'temp': '涼しい', 'features': '早い紅葉'},
                'winter': {'months': '11月〜3月', 'temp': '厳寒', 'features': '雪景色'}
            },
            '東北': {
                'spring': {'months': '4月〜5月', 'temp': '涼しい', 'features': '桜と新緑'},
                'summer': {'months': '6月〜8月', 'temp': '温暖', 'features': '緑豊かな森林'},
                'autumn': {'months': '9月〜11月', 'temp': '涼しい', 'features': '美しい紅葉'},
                'winter': {'months': '12月〜3月', 'temp': '寒冷', 'features': '雪山ハイキング'}
            },
            'デフォルト': {
                'spring': {'months': '3月〜5月', 'temp': '温暖', 'features': '桜と新緑'},
                'summer': {'months': '6月〜8月', 'temp': '暑い', 'features': '早朝登山推奨'},
                'autumn': {'months': '9月〜11月', 'temp': '涼しい', 'features': '紅葉シーズン'},
                'winter': {'months': '12月〜2月', 'temp': '寒い', 'features': '澄んだ空気と展望'}
            }
        }
        
        # 九州・沖縄の特別設定
        if prefecture in ['熊本県', '鹿児島県', '長崎県', '大分県', '宮崎県', '福岡県', '佐賀県', '沖縄県']:
            region_key = prefecture
            if prefecture not in regional_seasons:
                regional_seasons[prefecture] = {
                    'spring': {'months': '3月〜5月', 'temp': '温暖', 'features': '早い桜と温暖な気候'},
                    'summer': {'months': '6月〜9月', 'temp': '蒸し暑い', 'features': '涼しい早朝がおすすめ'},
                    'autumn': {'months': '10月〜12月', 'temp': '温暖', 'features': '長い紅葉シーズン'},
                    'winter': {'months': '1月〜2月', 'temp': '温暖', 'features': '晴天率が高い'}
                }
        else:
            region_key = '北海道' if prefecture == '北海道' else ('東北' if prefecture in ['青森県', '岩手県', '宮城県', '秋田県', '山形県', '福島県'] else 'デフォルト')
        
        season_info = regional_seasons.get(region_key, regional_seasons['デフォルト'])
        
        # 山固有の特徴を季節に組み込み
        mountain_features = {}
        for feature in features:
            if '桜' in feature or '花見' in feature:
                mountain_features['spring'] = f"{feature}を楽しめます"
            elif '夜景' in feature:
                mountain_features['winter'] = f"空気が澄んで{feature}が特に美しく見えます"
            elif '紅葉' in feature:
                mountain_features['autumn'] = f"{feature}の名所として知られています"
            elif '神社' in feature or '寺' in feature:
                mountain_features['all'] = f"{feature}への参拝も楽しめます"
        
        # 季節データベース情報を活用
        cherry_info = seasons_data.get('cherry_blossom', '')
        autumn_info = seasons_data.get('autumn_leaves', '')
        
        content = f'''
        <h2 id="section-4">季節ごとの楽しみ方</h2>
        <p>{mountain_name}は標高{mountain.get('elevation', '')}mの立地により、四季それぞれに異なる魅力を見せてくれます。</p>
        
        <h3>春（{season_info['spring']['months']}）</h3>
        <p>{season_info['spring']['features']}の季節です。'''
        
        if cherry_info:
            content += f"桜の見頃は{cherry_info}で、"
        if mountain_features.get('spring'):
            content += mountain_features['spring']
        else:
            content += f"{mountain_name}周辺では新緑と花々を楽しむことができます。"
        content += f"{season_info['spring']['temp']}気候で登山に適しています。</p>"
        
        content += f'''
        <h3>夏（{season_info['summer']['months']}）</h3>
        <p>{season_info['summer']['features']}を満喫できる季節。{season_info['summer']['temp']}気候のため、'''
        
        if '夜景' in str(features):
            content += "夜景を楽しむなら夕涼みハイキングがおすすめです。"
        elif season_info['summer']['temp'] == '蒸し暑い':
            content += "早朝または夕方の登山がおすすめです。"
        else:
            content += "一日中快適にハイキングを楽しめます。"
        content += "</p>"
        
        content += f'''
        <h3>秋（{season_info['autumn']['months']}）</h3>
        <p>{season_info['autumn']['features']}。'''
        
        if autumn_info:
            content += f"紅葉の見頃は{autumn_info}です。"
        if mountain_features.get('autumn'):
            content += mountain_features['autumn']
        else:
            content += f"{mountain_name}からの紅葉の眺めは格別です。"
        content += f"{season_info['autumn']['temp']}気候で登山に最適な季節です。</p>"
        
        content += f'''
        <h3>冬（{season_info['winter']['months']}）</h3>
        <p>{season_info['winter']['features']}の季節。'''
        
        if mountain_features.get('winter'):
            content += mountain_features['winter']
        elif '展望' in str(features) or '眺望' in str(features):
            content += f"空気が澄んで{mountain_name}からの展望が一年で最も美しく見えます。"
        else:
            content += f"{season_info['winter']['features']}を楽しめます。"
            
        if region_key == '北海道':
            content += "防寒対策と滑り止めが必須です。"
        elif season_info['winter']['temp'] == '温暖':
            content += "温暖な気候で冬でも登山を楽しめます。"
        else:
            content += "防寒対策をしっかりと行いましょう。"
        
        content += "</p>"
        
        if mountain_features.get('all'):
            content += f"<p>一年を通じて{mountain_features['all']}</p>"
        
        content += "        '''"
        
        return content
    
    def generate_equipment_content(self, mountain):
        """山固有の装備コンテンツを生成"""
        mountain_name = mountain.get('name', '').strip()
        prefecture = mountain.get('prefecture', '').strip()
        elevation = mountain.get('elevation', 0)
        features = mountain.get('features', [])
        difficulty = mountain.get('difficulty', {})
        hiking_time = difficulty.get('hiking_time') or '約1-2時間'
        
        # 基本装備
        content = f'''
        <h2 id="section-5">おすすめの登山装備</h2>
        <p>{mountain_name}登山を快適に楽しむための装備をご紹介します。初心者の方にも使いやすいアイテムを厳選しました。</p>
        
        <h3>服装と基本装備</h3>
        <ul>'''
        
        # 服装（地域・標高による調整）
        if prefecture == '北海道':
            content += '''
        <li><strong>服装</strong>：防寒着必須、レイヤリング可能な服装、防滑性のある靴</li>
        <li><strong>防寒具</strong>：手袋、帽子、ネックウォーマー（特に冬季）</li>'''
        elif elevation > 300:
            content += '''
        <li><strong>服装</strong>：動きやすく温度調節しやすい服装、しっかりしたハイキングシューズ</li>'''
        else:
            content += '''
        <li><strong>服装</strong>：動きやすい服装、履き慣れた運動靴でOK</li>'''
        
        # 持ち物（登山時間による調整）
        if hiking_time and ('3時間' in hiking_time or '4時間' in hiking_time):
            content += '''
        <li><strong>持ち物</strong>：十分な水分（1L以上）、エネルギー補給食、昼食、タオル、雨具</li>'''
        else:
            content += '''
        <li><strong>持ち物</strong>：水分、軽食、タオル、雨具</li>'''
        
        # 山固有の特別装備
        special_equipment = []
        for feature in features:
            if '夜景' in feature:
                special_equipment.append('懐中電灯・ヘッドライト（夜景鑑賞時必須）')
            elif '神社' in feature or '寺' in feature:
                special_equipment.append('御朱印帳（参拝記念に）')
            elif '展望' in feature or '眺望' in feature:
                special_equipment.append('双眼鏡・カメラ（景色撮影用）')
            elif '原始林' in feature or '森林' in feature:
                special_equipment.append('虫よけスプレー（夏季推奨）')
        
        if special_equipment:
            content += f'''
        <li><strong>特別装備</strong>：{', '.join(special_equipment)}</li>'''
        
        content += '''
        <li><strong>安全装備</strong>：携帯電話、救急用品、地図・GPS</li>
        </ul>'''
        
        # 季節別アドバイス
        content += '''
        
        <h3>季節別のポイント</h3>
        <ul>'''
        
        if prefecture == '北海道':
            content += '''
        <li><strong>春</strong>：残雪に注意、滑り止め装備推奨</li>
        <li><strong>夏</strong>：虫対策、日焼け対策</li>
        <li><strong>秋</strong>：防寒着準備、日没が早いため時間管理重要</li>
        <li><strong>冬</strong>：本格的な冬山装備、アイゼンやスノーシューが必要な場合あり</li>'''
        elif prefecture in ['熊本県', '鹿児島県', '長崎県', '大分県']:
            content += '''
        <li><strong>春</strong>：花粉対策、紫外線対策</li>
        <li><strong>夏</strong>：熱中症対策、十分な水分補給</li>
        <li><strong>秋</strong>：台風情報の確認</li>
        <li><strong>冬</strong>：比較的温暖だが、風対策は重要</li>'''
        else:
            content += '''
        <li><strong>春</strong>：花粉対策、レインウェア</li>
        <li><strong>夏</strong>：熱中症対策、虫よけ対策</li>
        <li><strong>秋</strong>：防寒着の準備</li>
        <li><strong>冬</strong>：防寒対策、滑り止め装備</li>'''
        
        content += '''
        </ul>
        '''
        
        return content
    
    def generate_summary_content(self, mountain):
        """山固有のまとめコンテンツを生成"""
        mountain_name = mountain.get('name', '').strip()
        prefecture = mountain.get('prefecture', '').strip()
        elevation = mountain.get('elevation', 0)
        features = mountain.get('features', [])
        difficulty = mountain.get('difficulty', {})
        access_info = mountain.get('location', {})
        
        # 主要な特徴を抽出
        main_features = []
        for feature in features[:3]:  # 上位3つの特徴
            main_features.append(feature)
        
        content = f'''
        <h2 id="section-6">まとめ：{mountain_name}の魅力</h2>
        <p>{mountain_name}は、{prefecture}を代表する標高{elevation}mの低山です。{difficulty.get('level', '初級')}レベルの登山道で、{difficulty.get('hiking_time', '1-2時間')}程度のコースは初心者や家族連れでも安心して楽しめます。</p>'''
        
        # 山固有の魅力を記述
        if main_features:
            content += f'''
        <p>特に{main_features[0]}'''
            if len(main_features) > 1:
                content += f"や{main_features[1]}"
            if len(main_features) > 2:
                content += f"、{main_features[2]}"
            content += f"といった魅力があり、多くの登山者に愛されています。</p>"
        
        # アクセス情報を含めた締めくくり
        access_time = access_info.get('access_time', '')
        nearest_station = access_info.get('nearest_station', '')
        
        if access_time and nearest_station:
            content += f'''
        <p>{nearest_station}から{access_time}と、アクセスも良好で日帰り登山に最適なスポットです。'''
        else:
            content += '''
        <p>アクセスも良好で、日帰り登山に最適なスポットです。'''
        
        # 季節による魅力
        seasons_data = mountain.get('seasons', {})
        if seasons_data.get('cherry_blossom'):
            content += f"春の桜（{seasons_data['cherry_blossom']}）"
            if seasons_data.get('autumn_leaves'):
                content += f"から秋の紅葉（{seasons_data['autumn_leaves']}）まで、"
            else:
                content += "をはじめ、"
        elif seasons_data.get('autumn_leaves'):
            content += f"秋の紅葉（{seasons_data['autumn_leaves']}）など、"
        else:
            content += "四季折々の自然"
        
        content += f"を楽しみながら、気軽にアウトドア体験ができる{mountain_name}へ、ぜひ足を運んでみてはいかがでしょうか。</p>"
        
        # 地域特有の締めくくり
        if prefecture == '北海道':
            content += f'''
        <p>札幌近郊の自然を満喫できる{mountain_name}で、北海道ならではの大自然を体感してください。</p>'''
        elif '神社' in str(features) or '寺' in str(features):
            content += f'''
        <p>歴史と自然が調和する{mountain_name}で、心身ともにリフレッシュする山歩きをお楽しみください。</p>'''
        elif '夜景' in str(features):
            content += f'''
        <p>昼間の登山と夜景の両方を楽しめる{mountain_name}で、特別な山体験をしてみませんか。</p>'''
        
        content += "        '''"
        
        return content

if __name__ == "__main__":
    generator = AffiliateStaticGenerator()
    
    # データベースから動的に記事ファイルを生成
    print(f"🗂️ データベース読み込み: {generator.mountains_data['metadata']['total_mountains']}山")
    
    # 既存の記事ファイルをチェック
    article_files = []
    for pattern in ["article_*.json", "generated_articles/article_*.json"]:
        import glob
        files = glob.glob(pattern)
        article_files.extend(files)
    
    # 存在するファイルのみ使用
    existing_files = [f for f in article_files if Path(f).exists()]
    print(f"📁 使用可能な記事ファイル: {len(existing_files)}")
    
    # 既存の記事ファイルがある場合は詳細記事を生成、ない場合は基本情報を生成
    if existing_files:
        print(f"📄 詳細記事を使用: {len(existing_files)}件")
        generator.generate_site(existing_files)
    
    # データベースから基本的な山情報ページを追加生成（全47山）
    print("🏗️ データベースから全山の基本情報サイトを生成...")
    generator.generate_basic_site_from_database()
        
    print(f"✅ 静的サイト生成完了: {generator.mountains_data['metadata']['total_mountains']}山のデータベース使用")
    print("\\n🌐 サイト生成完了！ローカル確認は以下のコマンドで：")
    print("cd static_site && python -m http.server 8000")