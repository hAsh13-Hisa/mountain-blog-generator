#!/usr/bin/env python3
"""
最終修正スクリプト - 残った問題を一括修正
"""

import re
from pathlib import Path

class FinalFixer:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        
    def fix_onerror_attributes(self):
        """間違ったonerror属性を修正"""
        print("🔧 onerror属性を修正中...")
        
        html_files = list(self.base_dir.rglob("*.html"))
        for html_file in html_files:
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 間違ったonerror属性を修正
                content = re.sub(
                    r'onerror="this\.src=\'\{\}/images/hero_mountain_hiking\.svg\'\"\.format\(window\.location\.origin\)',
                    'onerror="this.src=\'images/hero_mountain_hiking.svg\'"',
                    content
                )
                
                # 相対パスを適切に修正
                content = re.sub(
                    r'onerror="this\.src=\'images/hero_mountain_hiking\.svg\'"',
                    lambda m: 'onerror="this.src=\'../images/hero_mountain_hiking.svg\'"' if 'mountains/' in str(html_file) or 'equipment/' in str(html_file) or 'beginner/' in str(html_file) else 'onerror="this.src=\'images/hero_mountain_hiking.svg\'"',
                    content
                )
                
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
            except Exception as e:
                print(f"❌ エラー: {html_file} - {e}")
        
        print("✅ onerror属性の修正完了")
    
    def fix_skip_link_detection(self):
        """スキップリンクの検出問題を修正"""
        print("♿ スキップリンク検出を修正中...")
        
        html_files = list(self.base_dir.rglob("*.html"))
        for html_file in html_files:
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 重複したスキップリンクを削除
                content = re.sub(
                    r'(\s*<!-- Skip Link -->\s*<a href="#main-content" class="sr-only">メインコンテンツへスキップ</a>\s*){2,}',
                    r'\1',
                    content
                )
                
                # スキップリンクがない場合は追加
                if 'skip-link' not in content and 'sr-only' not in content:
                    content = re.sub(
                        r'(<body[^>]*>)',
                        r'\1\n    <!-- Skip Link -->\n    <a href="#main-content" class="sr-only">メインコンテンツへスキップ</a>\n',
                        content
                    )
                
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
            except Exception as e:
                print(f"❌ エラー: {html_file} - {e}")
        
        print("✅ スキップリンクの修正完了")
    
    def create_missing_mountain_pages(self):
        """不足している山ページを作成"""
        print("⛰️ 不足している山ページを作成中...")
        
        missing_mountains = ["交野山", "若草山"]
        
        for mountain_name in missing_mountains:
            mountain_dir = self.base_dir / "mountains" / mountain_name
            mountain_dir.mkdir(parents=True, exist_ok=True)
            
            # 簡単な山ページを作成
            content = f'''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{mountain_name} | 山の詳細 - 低山旅行</title>
    <meta name="description" content="{mountain_name}の詳細情報。低山ハイキングに最適な山をご紹介します。">
    
    <link rel="stylesheet" href="../../css/minimal_design.css">
    
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "Place",
        "name": "{mountain_name}",
        "description": "{mountain_name}の詳細情報",
        "url": "https://teizan.omasse.com/mountains/{mountain_name}/"
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

        <!-- 山の詳細 -->
        <section class="section mountain-detail">
            <div class="container">
                <header class="section-header">
                    <h1 class="section-title">{mountain_name}</h1>
                    <p class="section-subtitle">
                        日本の美しい低山
                    </p>
                </header>
                
                <div class="mountain-content">
                    <div class="mountain-image">
                        <img src="../../images/hero_mountain_hiking.svg" 
                             alt="{mountain_name}の美しいイラスト" 
                             class="mountain-main-img">
                    </div>
                    
                    <div class="mountain-info">
                        <div class="info-grid">
                            <div class="info-card">
                                <h3>基本情報</h3>
                                <ul class="info-list">
                                    <li><strong>山名:</strong> {mountain_name}</li>
                                    <li><strong>難易度:</strong> 初級</li>
                                    <li><strong>登山時間:</strong> 約1-2時間</li>
                                </ul>
                            </div>
                            
                            <div class="info-card">
                                <h3>特徴</h3>
                                <p>初心者にもおすすめの美しい低山です。</p>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="mountain-actions">
                    <a href="../../mountains/" class="btn btn-secondary">
                        ← 山一覧に戻る
                    </a>
                    <a href="../../equipment/" class="btn btn-primary">
                        装備ガイドを見る
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
            
            with open(mountain_dir / "index.html", 'w', encoding='utf-8') as f:
                f.write(content)
        
        print(f"✅ {len(missing_mountains)}個の山ページを作成完了")
    
    def run_final_fixes(self):
        """最終修正を実行"""
        print("🔧 最終修正開始")
        print("=" * 50)
        
        self.fix_onerror_attributes()
        self.fix_skip_link_detection()
        self.create_missing_mountain_pages()
        
        print("=" * 50)
        print("🎉 最終修正完了！")

def main():
    fixer = FinalFixer()
    fixer.run_final_fixes()

if __name__ == "__main__":
    main()