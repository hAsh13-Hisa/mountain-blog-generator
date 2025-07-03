#!/usr/bin/env python3
"""
未作成ページを一括生成
"""
import json
from pathlib import Path
from datetime import datetime

def create_base_template(title, content, description="低山旅行の情報サイト"):
    """基本HTMLテンプレート"""
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - 低山旅行</title>
    <meta name="description" content="{description}">
    <meta name="keywords" content="低山, 登山, ハイキング, 初心者, 家族旅行, 日帰り, アウトドア">
    <meta name="author" content="低山旅行">
    
    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://teizan.omasse.com/">
    <meta property="og:title" content="{title} - 低山旅行">
    <meta property="og:description" content="{description}">
    <meta property="og:image" content="https://teizan.omasse.com/images/og-image.jpg">
    
    <!-- Twitter -->
    <meta property="twitter:card" content="summary_large_image">
    <meta property="twitter:url" content="https://teizan.omasse.com/">
    <meta property="twitter:title" content="{title} - 低山旅行">
    <meta property="twitter:description" content="{description}">
    <meta property="twitter:image" content="https://teizan.omasse.com/images/og-image.jpg">
    
    <!-- Favicon -->
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <link rel="apple-touch-icon" href="/apple-touch-icon.png">
    
    <!-- CSS -->
    <link rel="stylesheet" href="/css/style.css">
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
        <div class="container">
            {content}
        </div>
    </main>
    
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

def create_missing_pages():
    """未作成ページを生成"""
    
    pages = {
        # 一般ページ
        '/mountains/': {
            'title': '山一覧',
            'description': '初心者・家族向けの低山一覧。標高400m以下の登りやすい山をご紹介します。',
            'content': '''
            <div class="page-header">
                <h1>🏔️ 山一覧</h1>
                <p class="page-description">初心者・家族向けの低山を厳選してご紹介。標高400m以下で登山道が整備された、安全で楽しめる山々です。</p>
            </div>
            
            <div class="mountain-grid">
                <a href="/mountains/mt_takao/" class="mountain-card">
                    <img src="https://images.unsplash.com/photo-1506905925346-21bda4d32df4" alt="高尾山" loading="lazy">
                    <div class="mountain-card-content">
                        <h3>高尾山</h3>
                        <div class="mountain-meta">東京都 - 標高599m</div>
                        <p>東京近郊で最も人気の低山。ケーブルカーでのアクセスも可能で、初心者から上級者まで楽しめます。</p>
                    </div>
                </a>
                
                <a href="/mountains/mt_tsukuba_ibaraki/" class="mountain-card">
                    <img src="https://images.unsplash.com/photo-1564121071929-ad2b78ca5b80" alt="筑波山" loading="lazy">
                    <div class="mountain-card-content">
                        <h3>筑波山</h3>
                        <div class="mountain-meta">茨城県 - 標高877m</div>
                        <p>日本百名山の中でも登りやすく、関東の名峰として親しまれています。ロープウェイもあり家族連れにも人気。</p>
                    </div>
                </a>
                
                <a href="/mountains/mt_maruyama_hokkaido/" class="mountain-card">
                    <img src="https://images.unsplash.com/photo-1483728642387-6c3bdd6c93e5" alt="円山" loading="lazy">
                    <div class="mountain-card-content">
                        <h3>円山</h3>
                        <div class="mountain-meta">北海道 - 標高225m</div>
                        <p>札幌市内からアクセス抜群。原始林が残る都市型登山の代表格で、野生動物観察も楽しめます。</p>
                    </div>
                </a>
                
                <a href="/mountains/mt_hakodate_hokkaido/" class="mountain-card">
                    <img src="https://images.unsplash.com/photo-1578662996442-48f60103fc96" alt="函館山" loading="lazy">
                    <div class="mountain-card-content">
                        <h3>函館山</h3>
                        <div class="mountain-meta">北海道 - 標高334m</div>
                        <p>函館の夜景で有名な山。ロープウェイの他、登山道も整備されており、ハイキングコースとしても人気。</p>
                    </div>
                </a>
                
                <a href="/mountains/mt_sanuki_kagawa/" class="mountain-card">
                    <img src="https://images.unsplash.com/photo-1571197300840-5c1fd64e4c89" alt="讃岐富士" loading="lazy">
                    <div class="mountain-card-content">
                        <h3>讃岐富士（飯野山）</h3>
                        <div class="mountain-meta">香川県 - 標高422m</div>
                        <p>美しい形から讃岐富士と呼ばれる名峰。瀬戸内海の絶景を望める初心者向けの山です。</p>
                    </div>
                </a>
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
            '''
        },
        
        '/beginner/': {
            'title': '初心者ガイド',
            'description': '登山初心者向けの基本知識、装備、安全対策をわかりやすく解説します。',
            'content': '''
            <div class="page-header">
                <h1>🥾 初心者ガイド</h1>
                <p class="page-description">登山を始めたい方のための基本情報をまとめました。安全で楽しい山行のための知識とコツをお伝えします。</p>
            </div>
            
            <div class="section">
                <h2>📚 登山の基本知識</h2>
                
                <h3>🎯 登山計画の立て方</h3>
                <ul>
                    <li><strong>目標設定</strong>：体力と経験に合った山を選ぶ</li>
                    <li><strong>天気確認</strong>：登山日の天気予報を必ずチェック</li>
                    <li><strong>コース研究</strong>：地図やガイドブックで事前にルートを確認</li>
                    <li><strong>時間配分</strong>：余裕をもったスケジュールを組む</li>
                </ul>
                
                <h3>🎒 基本装備リスト</h3>
                <div class="equipment-list">
                    <h4>必需品</h4>
                    <ul>
                        <li>登山靴（トレッキングシューズ）</li>
                        <li>リュックサック（20-30L程度）</li>
                        <li>レインウェア（上下セット）</li>
                        <li>防寒具（フリースやダウン）</li>
                        <li>帽子・手袋</li>
                        <li>水筒・ハイドレーション</li>
                        <li>行動食・非常食</li>
                        <li>ヘッドライト・予備電池</li>
                        <li>救急セット</li>
                        <li>地図・コンパス</li>
                    </ul>
                </div>
            </div>
            
            <div class="section">
                <h2>⚠️ 安全対策</h2>
                <div class="safety-tips">
                    <div class="safety-tip">
                        <h3>🗺️ 道迷い防止</h3>
                        <p>登山道の分岐点では必ず地図で現在地を確認。不安になったら引き返す勇気も大切です。</p>
                    </div>
                    <div class="safety-tip">
                        <h3>🌡️ 体調管理</h3>
                        <p>水分補給をこまめに行い、疲労を感じたら無理をせず休憩を取りましょう。</p>
                    </div>
                    <div class="safety-tip">
                        <h3>📱 連絡手段</h3>
                        <p>登山届の提出と、家族への行程連絡を忘れずに。携帯電話の電池切れにも注意。</p>
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h2>🏔️ おすすめ初心者コース</h2>
                <p><a href="/mountains/">山一覧ページ</a>で紹介している低山は、すべて初心者向けに厳選されています。まずは標高300m以下の山から始めることをおすすめします。</p>
            </div>
            '''
        },
        
        '/equipment/': {
            'title': '登山装備ガイド',
            'description': '登山に必要な装備の選び方、使い方を詳しく解説。初心者向けのおすすめ商品もご紹介します。',
            'content': '''
            <div class="page-header">
                <h1>🎒 登山装備ガイド</h1>
                <p class="page-description">安全で快適な登山のための装備選びをサポート。初心者向けのおすすめアイテムから上級者向けの装備まで詳しく解説します。</p>
            </div>
            
            <div class="section">
                <h2>👕 ウェア（服装）</h2>
                
                <h3>レイヤリングシステム</h3>
                <div class="layering-system">
                    <div class="layer">
                        <h4>ベースレイヤー（肌着）</h4>
                        <p>吸汗速乾性の高い化繊やメリノウール素材がおすすめ。綿は避けましょう。</p>
                    </div>
                    <div class="layer">
                        <h4>ミドルレイヤー（中間着）</h4>
                        <p>保温性のあるフリースやダウンジャケット。気温に応じて脱着調整。</p>
                    </div>
                    <div class="layer">
                        <h4>アウターレイヤー（外着）</h4>
                        <p>防水透湿性のあるレインウェア。風や雨から身を守ります。</p>
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h2>🥾 フットウェア（靴）</h2>
                
                <h3>登山靴の選び方</h3>
                <ul>
                    <li><strong>ローカット</strong>：軽量で歩きやすい。平坦な山道や日帰りハイキングに</li>
                    <li><strong>ミドルカット</strong>：足首をサポート。石や木の根が多い山道に</li>
                    <li><strong>ハイカット</strong>：しっかりしたサポート力。重装備や長期縦走に</li>
                </ul>
                
                <h3>サイズ選びのポイント</h3>
                <p>午後の足が膨らんだ状態で試着し、つま先に1cm程度の余裕があるサイズを選びましょう。</p>
            </div>
            
            <div class="section">
                <h2>🎒 バックパック</h2>
                
                <h3>容量の目安</h3>
                <ul>
                    <li><strong>20-30L</strong>：日帰りハイキング</li>
                    <li><strong>30-50L</strong>：小屋泊登山</li>
                    <li><strong>50L以上</strong>：テント泊や長期縦走</li>
                </ul>
                
                <h3>フィッティングのポイント</h3>
                <p>背面長を正しく測り、ウエストベルトが腰骨の上に来るように調整しましょう。</p>
            </div>
            
            <div class="section">
                <h2>🔦 その他の重要装備</h2>
                
                <div class="equipment-grid">
                    <div class="equipment-item">
                        <h3>ヘッドライト</h3>
                        <p>早朝出発や日没後の下山に必須。予備電池も忘れずに。</p>
                    </div>
                    <div class="equipment-item">
                        <h3>レインウェア</h3>
                        <p>防水透湿性素材（ゴアテックスなど）がおすすめ。上下セットで用意。</p>
                    </div>
                    <div class="equipment-item">
                        <h3>救急用品</h3>
                        <p>絆創膏、包帯、痛み止めなど基本的な応急処置用品を携帯。</p>
                    </div>
                    <div class="equipment-item">
                        <h3>地図・コンパス</h3>
                        <p>スマートフォンアプリと併用して、アナログの地図とコンパスも携帯。</p>
                    </div>
                </div>
            </div>
            '''
        },
        
        '/about/': {
            'title': 'このサイトについて',
            'description': '低山旅行は初心者・家族向けの低山登山情報を提供するサイトです。',
            'content': '''
            <div class="page-header">
                <h1>🏔️ このサイトについて</h1>
                <p class="page-description">低山旅行は、登山初心者や家族連れの方々に向けて、安全で楽しい低山登山の情報をお届けするサイトです。</p>
            </div>
            
            <div class="section">
                <h2>📋 サイトの目的</h2>
                <p>このサイトは、以下の目的で運営されています：</p>
                <ul>
                    <li>登山初心者が安心して始められる低山情報の提供</li>
                    <li>家族や友人と気軽に楽しめる山の紹介</li>
                    <li>安全な登山のための基礎知識の共有</li>
                    <li>登山装備や準備に関する実用的な情報提供</li>
                </ul>
            </div>
            
            <div class="section">
                <h2>🎯 対象とする読者</h2>
                <ul>
                    <li>これから登山を始めたい初心者の方</li>
                    <li>家族や子供と一緒に山を楽しみたい方</li>
                    <li>日帰りで気軽にハイキングを楽しみたい方</li>
                    <li>低山の魅力を再発見したい方</li>
                </ul>
            </div>
            
            <div class="section">
                <h2>⛰️ 掲載基準</h2>
                <p>当サイトでは、以下の基準で山を選定しています：</p>
                <ul>
                    <li><strong>標高</strong>：主に400m以下の低山</li>
                    <li><strong>アクセス</strong>：公共交通機関でアクセス可能</li>
                    <li><strong>安全性</strong>：登山道が整備されている</li>
                    <li><strong>初心者適正</strong>：特別な技術や装備を必要としない</li>
                    <li><strong>季節対応</strong>：年間を通じて楽しめる</li>
                </ul>
            </div>
            
            <div class="section">
                <h2>ℹ️ 情報について</h2>
                <p>掲載している情報は、各種登山ガイドブック、公式サイト、実地調査に基づいています。ただし、自然環境や登山道の状況は常に変化するため、実際の登山前には最新の情報を現地や関係機関で確認することをお勧めします。</p>
                
                <h3>⚠️ 免責事項</h3>
                <p>当サイトの情報を利用した登山で発生した事故や損害について、当サイトは一切の責任を負いかねます。登山は自己責任で行い、十分な準備と安全対策をお願いします。</p>
            </div>
            
            <div class="section">
                <h2>📧 お問い合わせ</h2>
                <p>サイトに関するご質問やご意見は、<a href="/contact/">お問い合わせページ</a>からお送りください。</p>
            </div>
            '''
        },
        
        '/contact/': {
            'title': 'お問い合わせ',
            'description': 'サイトに関するご質問・ご意見をお待ちしています。',
            'content': '''
            <div class="page-header">
                <h1>📧 お問い合わせ</h1>
                <p class="page-description">サイトに関するご質問、ご意見、山の情報提供などお気軽にお送りください。</p>
            </div>
            
            <div class="section">
                <h2>📝 お問い合わせ内容</h2>
                <p>以下のような内容についてお気軽にご連絡ください：</p>
                <ul>
                    <li>サイトの使い方に関するご質問</li>
                    <li>掲載されている山の情報について</li>
                    <li>おすすめの低山情報の提供</li>
                    <li>登山装備に関するご相談</li>
                    <li>サイトの改善提案</li>
                    <li>その他、登山に関するご質問</li>
                </ul>
            </div>
            
            <div class="section">
                <h2>✉️ 連絡方法</h2>
                <div class="contact-info">
                    <p>現在、お問い合わせフォームを準備中です。しばらくお待ちください。</p>
                    <p>緊急のお問い合わせがございましたら、各山の管理事務所または最寄りの観光案内所にお問い合わせください。</p>
                </div>
            </div>
            
            <div class="section">
                <h2>⏰ 回答について</h2>
                <ul>
                    <li>お問い合わせをいただいてから、3-5営業日以内にご回答いたします</li>
                    <li>内容によっては回答にお時間をいただく場合があります</li>
                    <li>登山の安全に関わる緊急のご質問については、必ず現地の管理事務所にもご確認ください</li>
                </ul>
            </div>
            
            <div class="section">
                <h2>🔒 個人情報の取り扱い</h2>
                <p>お送りいただいた個人情報は、お問い合わせへの回答のみに使用し、他の目的には使用いたしません。詳しくは<a href="/privacy/">プライバシーポリシー</a>をご確認ください。</p>
            </div>
            '''
        },
        
        '/privacy/': {
            'title': 'プライバシーポリシー',
            'description': '当サイトの個人情報保護方針について説明します。',
            'content': '''
            <div class="page-header">
                <h1>🔒 プライバシーポリシー</h1>
                <p class="page-description">当サイト「低山旅行」における個人情報の取り扱いについて説明します。</p>
            </div>
            
            <div class="section">
                <h2>📋 基本方針</h2>
                <p>当サイトは、ユーザーの個人情報保護を重要と考え、個人情報保護法を遵守し、適切な取り扱いを行います。</p>
            </div>
            
            <div class="section">
                <h2>📊 収集する情報</h2>
                
                <h3>アクセス情報</h3>
                <ul>
                    <li>IPアドレス</li>
                    <li>ブラウザの種類</li>
                    <li>アクセス日時</li>
                    <li>閲覧ページ</li>
                    <li>リファラー情報</li>
                </ul>
                
                <h3>お問い合わせ情報</h3>
                <ul>
                    <li>お名前</li>
                    <li>メールアドレス</li>
                    <li>お問い合わせ内容</li>
                </ul>
            </div>
            
            <div class="section">
                <h2>🎯 利用目的</h2>
                <ul>
                    <li>サイトの運営・改善</li>
                    <li>お問い合わせへの回答</li>
                    <li>アクセス解析によるサービス向上</li>
                    <li>不正アクセスの防止</li>
                </ul>
            </div>
            
            <div class="section">
                <h2>🔐 第三者への提供</h2>
                <p>以下の場合を除き、個人情報を第三者に提供することはありません：</p>
                <ul>
                    <li>ユーザーの同意がある場合</li>
                    <li>法令により提供が求められる場合</li>
                    <li>人の生命・身体・財産の保護のために必要な場合</li>
                </ul>
            </div>
            
            <div class="section">
                <h2>🍪 Cookieの使用</h2>
                <p>当サイトでは、ユーザーの利便性向上のためCookieを使用する場合があります：</p>
                <ul>
                    <li>アクセス解析（Google Analytics等）</li>
                    <li>広告配信の最適化</li>
                    <li>サイトの機能改善</li>
                </ul>
                <p>Cookieの使用を望まない場合は、ブラウザの設定で無効にできます。</p>
            </div>
            
            <div class="section">
                <h2>🔄 アフィリエイトプログラム</h2>
                <p>当サイトは、楽天アフィリエイトプログラムに参加しています。これらのプログラムでは、商品やサービスの紹介を目的としてCookieが使用される場合があります。</p>
            </div>
            
            <div class="section">
                <h2>📝 免責事項</h2>
                <ul>
                    <li>当サイトの情報は、登山の安全を保証するものではありません</li>
                    <li>登山は自己責任で行い、十分な準備をお願いします</li>
                    <li>情報の正確性については努めていますが、完全性を保証するものではありません</li>
                    <li>当サイトの利用により生じた損害について、一切責任を負いません</li>
                </ul>
            </div>
            
            <div class="section">
                <h2>📞 お問い合わせ</h2>
                <p>プライバシーポリシーに関するご質問は、<a href="/contact/">お問い合わせページ</a>からお送りください。</p>
                
                <p><strong>最終更新日：2025年7月2日</strong></p>
            </div>
            '''
        },
        
        '/terms/': {
            'title': '利用規約',
            'description': '当サイトの利用規約について説明します。',
            'content': '''
            <div class="page-header">
                <h1>📜 利用規約</h1>
                <p class="page-description">当サイト「低山旅行」をご利用いただく前に、必ずお読みください。</p>
            </div>
            
            <div class="section">
                <h2>📋 総則</h2>
                <p>本利用規約は、当サイト「低山旅行」（以下「当サイト」）の利用条件を定めるものです。ユーザーは当サイトを利用することで、本規約に同意したものとみなします。</p>
            </div>
            
            <div class="section">
                <h2>🎯 サイトの目的</h2>
                <p>当サイトは、登山初心者や家族連れの方々に向けて、低山登山に関する情報を提供することを目的としています。</p>
            </div>
            
            <div class="section">
                <h2>⚠️ 利用上の注意</h2>
                
                <h3>情報の利用について</h3>
                <ul>
                    <li>登山情報は参考程度にとどめ、実際の登山前には最新情報を確認してください</li>
                    <li>気象条件、登山道の状況等は常に変化するため、現地での最新情報収集を怠らないでください</li>
                    <li>登山は自己責任で行い、十分な準備と安全対策をお願いします</li>
                </ul>
                
                <h3>禁止事項</h3>
                <ul>
                    <li>法令に違反する行為</li>
                    <li>他のユーザーや第三者の権利を侵害する行為</li>
                    <li>当サイトの運営を妨げる行為</li>
                    <li>虚偽の情報を提供する行為</li>
                    <li>商用目的での無断利用</li>
                </ul>
            </div>
            
            <div class="section">
                <h2>📝 免責事項</h2>
                
                <h3>情報の正確性</h3>
                <p>当サイトは情報の正確性に努めていますが、完全性や最新性を保証するものではありません。</p>
                
                <h3>登山の安全</h3>
                <p>当サイトの情報を利用した登山において発生した事故、損害について、当サイトは一切の責任を負いません。</p>
                
                <h3>外部リンク</h3>
                <p>当サイトからリンクされた外部サイトの内容については、当サイトは責任を負いません。</p>
            </div>
            
            <div class="section">
                <h2>📸 著作権</h2>
                <ul>
                    <li>当サイトの文章、画像等の著作権は当サイトに帰属します</li>
                    <li>個人の範囲を超えた複製、転載は禁止します</li>
                    <li>引用する場合は、出典を明記してください</li>
                </ul>
            </div>
            
            <div class="section">
                <h2>🛒 アフィリエイトについて</h2>
                <p>当サイトは、楽天アフィリエイトプログラムに参加しています：</p>
                <ul>
                    <li>紹介する商品の価格・在庫は変動する場合があります</li>
                    <li>最新情報は各販売サイトでご確認ください</li>
                    <li>商品の購入は各ユーザーの判断と責任で行ってください</li>
                </ul>
            </div>
            
            <div class="section">
                <h2>🔄 規約の変更</h2>
                <p>当サイトは、必要に応じて本利用規約を変更する場合があります。変更後の規約は、当サイトに掲載した時点で効力を生じます。</p>
            </div>
            
            <div class="section">
                <h2>📞 お問い合わせ</h2>
                <p>利用規約に関するご質問は、<a href="/contact/">お問い合わせページ</a>からお送りください。</p>
                
                <p><strong>最終更新日：2025年7月2日</strong></p>
            </div>
            '''
        },
        
        # 地域ページ
        '/regions/': {
            'title': '地域別山一覧',
            'description': '日本全国の低山を地域別にご紹介。お住まいの地域やお出かけ先で楽しめる山を見つけてください。',
            'content': '''
            <div class="page-header">
                <h1>🗾 地域別山一覧</h1>
                <p class="page-description">日本全国の低山を地域別に整理しました。お住まいの地域やお出かけ先で楽しめる山を見つけてください。</p>
            </div>
            
            <div class="regions-grid">
                <a href="/regions/北海道/" class="region-card">
                    <img src="https://images.unsplash.com/photo-1483728642387-6c3bdd6c93e5" alt="北海道の山" loading="lazy">
                    <div class="region-card-content">
                        <h3>🏔️ 北海道</h3>
                        <p>雄大な自然と原始林が魅力。札幌近郊でアクセスの良い低山をご紹介。</p>
                        <div class="region-mountains">円山、函館山</div>
                    </div>
                </a>
                
                <a href="/regions/東京都/" class="region-card">
                    <img src="https://images.unsplash.com/photo-1506905925346-21bda4d32df4" alt="関東の山" loading="lazy">
                    <div class="region-card-content">
                        <h3>🗼 東京都</h3>
                        <p>都心からアクセス良好。電車で行ける身近な低山をご紹介。</p>
                        <div class="region-mountains">高尾山</div>
                    </div>
                </a>
                
                <a href="/regions/茨城県/" class="region-card">
                    <img src="https://images.unsplash.com/photo-1564121071929-ad2b78ca5b80" alt="関東の山" loading="lazy">
                    <div class="region-card-content">
                        <h3>🌸 茨城県</h3>
                        <p>百名山にも選ばれた名峰と、穏やかな里山が魅力の茨城県の低山。</p>
                        <div class="region-mountains">筑波山</div>
                    </div>
                </a>
                
                <a href="/regions/香川県/" class="region-card">
                    <img src="https://images.unsplash.com/photo-1571197300840-5c1fd64e4c89" alt="四国の山" loading="lazy">
                    <div class="region-card-content">
                        <h3>🌊 香川県</h3>
                        <p>瀬戸内海を望む美しい山々。うどん県ならではの観光も楽しめる。</p>
                        <div class="region-mountains">讃岐富士（飯野山）</div>
                    </div>
                </a>
            </div>
            
            <div class="section">
                <h2>🎯 地域選びのポイント</h2>
                <div class="tips-grid">
                    <div class="tip-card">
                        <h3>🚗 アクセス重視</h3>
                        <p>自宅からの距離や交通手段を考慮して、無理のない範囲で選びましょう。</p>
                    </div>
                    <div class="tip-card">
                        <h3>🌸 季節の特色</h3>
                        <p>各地域の気候や季節の見どころを調べて、ベストシーズンに訪れましょう。</p>
                    </div>
                    <div class="tip-card">
                        <h3>🏪 周辺施設</h3>
                        <p>温泉や観光地など、登山以外の楽しみも合わせて計画を立てましょう。</p>
                    </div>
                </div>
            </div>
            '''
        },
        
        '/difficulty/beginner/': {
            'title': '初心者向けの山',
            'description': '登山初心者でも安心して登れる、標高が低く登山道が整備された山をご紹介します。',
            'content': '''
            <div class="page-header">
                <h1>🥾 初心者向けの山</h1>
                <p class="page-description">登山経験がない方でも安心して楽しめる山をご紹介。標高が低く、登山道がしっかり整備された山を厳選しました。</p>
            </div>
            
            <div class="section">
                <h2>🎯 初心者向け山の特徴</h2>
                <div class="features-grid">
                    <div class="feature-card">
                        <h3>📏 低標高</h3>
                        <p>標高400m以下で、体力に自信がない方でも登頂可能。高山病の心配もありません。</p>
                    </div>
                    <div class="feature-card">
                        <h3>🛤️ 整備された登山道</h3>
                        <p>道迷いの心配が少なく、階段や手すりが設置された安全なルート。</p>
                    </div>
                    <div class="feature-card">
                        <h3>🚌 アクセス良好</h3>
                        <p>公共交通機関でアクセス可能。駐車場も完備されている山が多数。</p>
                    </div>
                    <div class="feature-card">
                        <h3>⏰ 短時間登山</h3>
                        <p>往復2-4時間程度で完登可能。日帰りで気軽に楽しめます。</p>
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h2>🏔️ おすすめの初心者向け低山</h2>
                
                <div class="mountain-list">
                    <div class="mountain-item">
                        <h3><a href="/mountains/mt_maruyama_hokkaido/">円山（北海道）</a></h3>
                        <div class="mountain-meta">標高225m / 登山時間：往復1-2時間</div>
                        <p>札幌市内からアクセス抜群。都市型登山の代表格で、原始林の自然を楽しめます。</p>
                    </div>
                    
                    <div class="mountain-item">
                        <h3><a href="/mountains/mt_hakodate_hokkaido/">函館山（北海道）</a></h3>
                        <div class="mountain-meta">標高334m / 登山時間：往復2-3時間</div>
                        <p>ロープウェイもありますが、登山道も整備されています。夜景スポットとしても有名。</p>
                    </div>
                    
                    <div class="mountain-item">
                        <h3><a href="/mountains/mt_takao/">高尾山（東京都）</a></h3>
                        <div class="mountain-meta">標高599m / 登山時間：往復3-4時間</div>
                        <p>東京近郊で最もポピュラーな山。ケーブルカーもあり、様々なコースが楽しめます。</p>
                    </div>
                    
                    <div class="mountain-item">
                        <h3><a href="/mountains/mt_sanuki_kagawa/">讃岐富士（香川県）</a></h3>
                        <div class="mountain-meta">標高422m / 登山時間：往復2-3時間</div>
                        <p>美しい円錐形で「讃岐富士」と呼ばれる山。瀬戸内海の眺望が素晴らしい。</p>
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h2>🎒 初心者に必要な装備</h2>
                <div class="equipment-checklist">
                    <h3>最低限の装備</h3>
                    <ul>
                        <li>歩きやすい靴（運動靴でも可）</li>
                        <li>リュックサック（20L程度）</li>
                        <li>水分（500ml以上）</li>
                        <li>軽食・行動食</li>
                        <li>レインウェア</li>
                        <li>防寒着（フリースなど）</li>
                        <li>帽子</li>
                        <li>タオル</li>
                    </ul>
                </div>
            </div>
            
            <div class="section">
                <h2>⚠️ 初心者が注意すべきポイント</h2>
                <ul>
                    <li>天気予報を必ず確認し、悪天候の日は避ける</li>
                    <li>登山計画を家族や友人に伝えておく</li>
                    <li>無理のないペースで歩く</li>
                    <li>水分補給をこまめに行う</li>
                    <li>道迷いしたら無理をせず引き返す</li>
                    <li>登山道以外には立ち入らない</li>
                </ul>
            </div>
            '''
        }
    }
    
    # 地域別ページ
    regions = {
        '北海道': {
            'mountains': [
                {'name': '円山', 'elevation': '225m', 'link': '/mountains/mt_maruyama_hokkaido/', 'description': '札幌市内から15分。原始林が残る都市型登山の代表格。'},
                {'name': '函館山', 'elevation': '334m', 'link': '/mountains/mt_hakodate_hokkaido/', 'description': '函館の夜景で有名。登山道も整備されている。'}
            ],
            'description': '北海道は雄大な自然と豊かな原生林が魅力。札幌や函館などの都市部からアクセスできる低山も多く、観光と合わせて楽しめます。'
        },
        '東京都': {
            'mountains': [
                {'name': '高尾山', 'elevation': '599m', 'link': '/mountains/mt_takao/', 'description': '東京近郊で最も人気の山。ケーブルカーでのアクセスも可能。'}
            ],
            'description': '東京都内には高尾山をはじめとする、都心からアクセスしやすい山々があります。電車で気軽に行ける身近な自然を楽しめます。'
        },
        '茨城県': {
            'mountains': [
                {'name': '筑波山', 'elevation': '877m', 'link': '/mountains/mt_tsukuba_ibaraki/', 'description': '日本百名山の中でも登りやすい名峰。ロープウェイもあり。'}
            ],
            'description': '茨城県には筑波山をはじめとする、関東地方を代表する山々があります。比較的標高が低く、初心者にも優しい山が多いのが特徴です。'
        },
        '香川県': {
            'mountains': [
                {'name': '讃岐富士（飯野山）', 'elevation': '422m', 'link': '/mountains/mt_sanuki_kagawa/', 'description': '美しい円錐形で讃岐富士と呼ばれる。瀬戸内海の絶景。'}
            ],
            'description': '香川県は瀬戸内海に面した美しい景観が楽しめる山々があります。うどんグルメと合わせて観光も楽しめるのが魅力です。'
        }
    }
    
    for region_name, region_data in regions.items():
        mountains_html = ''
        for mountain in region_data['mountains']:
            mountains_html += f'''
            <div class="mountain-item">
                <h3><a href="{mountain['link']}">{mountain['name']}</a></h3>
                <div class="mountain-meta">標高{mountain['elevation']}</div>
                <p>{mountain['description']}</p>
            </div>'''
        
        pages[f'/regions/{region_name}/'] = {
            'title': f'{region_name}の低山',
            'description': f'{region_name}の初心者向け低山をご紹介。アクセス情報や周辺観光情報も掲載。',
            'content': f'''
            <div class="page-header">
                <h1>🏔️ {region_name}の低山</h1>
                <p class="page-description">{region_data['description']}</p>
            </div>
            
            <div class="section">
                <h2>⛰️ {region_name}の山一覧</h2>
                <div class="mountain-list">
                    {mountains_html}
                </div>
            </div>
            
            <div class="section">
                <h2>🎯 {region_name}登山のポイント</h2>
                <ul>
                    <li>気候の特徴を事前に調べて、適切な装備を準備する</li>
                    <li>公共交通機関のアクセス方法を確認する</li>
                    <li>地域の観光情報もチェックして、登山と合わせて楽しむ</li>
                    <li>地元の山小屋や観光案内所で最新情報を収集する</li>
                </ul>
            </div>
            
            <div class="section">
                <h2>🔗 関連リンク</h2>
                <ul>
                    <li><a href="/regions/">他の地域の山を探す</a></li>
                    <li><a href="/beginner/">初心者向けガイド</a></li>
                    <li><a href="/equipment/">登山装備について</a></li>
                </ul>
            </div>
            '''
        }
    
    # 他の地域ページ（関東、関西、九州）
    other_regions = ['kanto', 'kansai', 'kyushu']
    region_names = {'kanto': '関東地方', 'kansai': '関西地方', 'kyushu': '九州地方'}
    
    for region_code in other_regions:
        region_name = region_names[region_code]
        pages[f'/regions/{region_code}/'] = {
            'title': f'{region_name}の低山',
            'description': f'{region_name}の初心者向け低山情報。準備中です。',
            'content': f'''
            <div class="page-header">
                <h1>🏔️ {region_name}の低山</h1>
                <p class="page-description">{region_name}の低山情報を準備中です。</p>
            </div>
            
            <div class="section">
                <h2>📝 準備中</h2>
                <p>{region_name}の低山情報は現在準備中です。しばらくお待ちください。</p>
                
                <h3>🔗 他の地域もチェック</h3>
                <ul>
                    <li><a href="/regions/北海道/">北海道の低山</a></li>
                    <li><a href="/regions/東京都/">東京都の低山</a></li>
                    <li><a href="/regions/茨城県/">茨城県の低山</a></li>
                    <li><a href="/regions/香川県/">香川県の低山</a></li>
                </ul>
            </div>
            
            <div class="section">
                <h2>💌 情報提供のお願い</h2>
                <p>{region_name}でおすすめの低山情報をお持ちの方は、<a href="/contact/">お問い合わせページ</a>からお気軽にお知らせください。</p>
            </div>
            '''
        }
    
    return pages

def create_all_pages():
    """全ページを作成"""
    pages = create_missing_pages()
    
    print(f"📝 {len(pages)}個のページを作成中...")
    
    for path, page_data in pages.items():
        # パスからディレクトリ構造を作成
        file_path = Path('static_site') / path.strip('/') / 'index.html'
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # HTMLを生成
        html_content = create_base_template(
            title=page_data['title'],
            content=page_data['content'],
            description=page_data['description']
        )
        
        # ファイルに保存
        file_path.write_text(html_content, encoding='utf-8')
        print(f"✅ {path}")
    
    print(f"\n🎉 {len(pages)}個のページを作成完了！")

if __name__ == "__main__":
    create_all_pages()