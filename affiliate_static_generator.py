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
    <link rel="stylesheet" href="/css/style.css">
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

/* ===== ヘッダー ===== */
header {
    background: linear-gradient(135deg, var(--primary-color), #3d6b47);
    color: white;
    padding: 1rem 0;
    box-shadow: 0 4px 20px rgba(44, 82, 52, 0.3);
    position: sticky;
    top: 0;
    z-index: 100;
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
        
        # アフィリエイトセクションHTML（強化版）
        affiliate_html = ""
        if affiliate_products:
            products_html = "\n".join([
                f'''<div class="affiliate-product">
                    <a href="{product['url']}" target="_blank" rel="noopener nofollow" onclick="gtag('event', 'click', {{'event_category': 'affiliate', 'event_label': '{product['name']}'}});">
                        {product['name']}
                    </a>
                    <span class="price">{product['price']}</span>
                </div>''' for product in affiliate_products
            ])
            
            affiliate_html = f'''
            <div class="affiliate-section">
                <h3>🎒 おすすめの登山グッズ</h3>
                <p class="affiliate-disclaimer">※以下の商品リンクは楽天アフィリエイトです。価格・在庫は変動する場合があります。</p>
                <div class="affiliate-products">
                    {products_html}
                </div>
                <p class="affiliate-note">💡 <strong>登山装備選びのポイント:</strong> 軽量性、耐久性、機能性のバランスを考慮して選びましょう。</p>
            </div>'''
        
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
            
            # 山別ページの生成
            self.generate_basic_mountain_page(mountain)
        
        # インデックスページの生成
        self.generate_basic_index_page(mountain_summary)
        
        # 地域別ページの生成
        self.generate_basic_region_pages(mountains)
        
        print(f"✅ 基本サイト生成完了: {len(mountains)}山")
    
    def generate_basic_mountain_page(self, mountain):
        """データベースから基本的な山ページを生成"""
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
        
        # 基本的な山情報HTML
        features_html = ""
        if mountain.get('features'):
            features_list = "".join([f"<li>{feature}</li>" for feature in mountain['features'][:5]])
            features_html = f"<ul>{features_list}</ul>"
        
        difficulty_info = mountain.get('difficulty', {})
        
        content = f"""
        <div class="container">
            <article class="mountain-article">
                <h1>{mountain['name']} ({mountain['elevation']}m)</h1>
                <div class="mountain-meta">
                    <span class="location">📍 {prefecture}</span>
                    <span class="elevation">⛰️ {mountain['elevation']}m</span>
                    <span class="difficulty">🎯 {difficulty_info.get('level', '初級')}</span>
                </div>
                
                <div class="mountain-description">
                    <h2>山の特徴</h2>
                    <p>{mountain['name']}は{prefecture}に位置する標高{mountain['elevation']}mの低山です。</p>
                    {features_html}
                </div>
                
                <div class="access-info">
                    <h2>アクセス情報</h2>
                    <p>最寄り駅: {mountain.get('location', {}).get('nearest_station', '要確認')}</p>
                    <p>アクセス時間: {mountain.get('location', {}).get('access_time', '要確認')}</p>
                </div>
                
                <div class="difficulty-info">
                    <h2>登山情報</h2>
                    <p>難易度: {difficulty_info.get('level', '初級')}</p>
                    <p>登山時間: {difficulty_info.get('hiking_time', '要確認')}</p>
                </div>
            </article>
        </div>
        """
        
        title = f"{mountain['name']} ({mountain['elevation']}m) - {prefecture} | 低山旅行"
        description = f"{mountain['name']}は{prefecture}にある標高{mountain['elevation']}mの低山です。初心者でも楽しめる登山情報をご紹介。"
        
        html = self.create_html_template(title, content, description)
        
        with open(mountain_dir / "index.html", 'w', encoding='utf-8') as f:
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