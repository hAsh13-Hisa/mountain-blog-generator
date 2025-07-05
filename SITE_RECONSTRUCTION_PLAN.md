# 🎨 低山アフィリエイトサイト再構築計画書
## 💰 収益最大化を目的とした山紹介特化サイト

## 📋 デザイン分析結果

### 🌸 Template Party「桜ピンク」テンプレート特徴
- **テーマ**: 旅行・観光サイト向け → **低山・ハイキング特化**に適用
- **対象**: 観光業、旅行代理店 → **登山初心者・ファミリー層**
- **デザイン**: 清潔感のあるモダンレイアウト → **アフィリエイト最適化**
- **多言語対応**: 日本語/英語 → **日本語特化**
- **参考URL**: https://template-party.com/template/tp_travel1/tp_travel1_sakura_pink/

### 🎯 サイト目的の再定義
- **主目的**: アフィリエイト収益最大化
- **ターゲット**: 登山初心者・ファミリー層（購買意欲が高い）
- **収益源**: 登山装備・アウトドアグッズ・旅行関連商品
- **コンテンツ**: 山紹介 + 装備レビュー + 旅行情報

## 🧩 必要コンポーネント一覧

### 1. ヘッダー部分（アフィリエイト最適化）
```
✓ サイトロゴ（左上）- 「低山マスター」ブランド
✓ 収益化ナビゲーション - 装備レビュー・ランキング優先
✓ 検索機能（山名・装備検索）
✓ 人気記事へのクイックリンク
✓ CTA（初心者ガイド・おすすめ装備）
```

### 2. メインコンテンツ（収益最大化レイアウト）
```
✓ ヒーローエリア（山の魅力 + 装備CTAボタン）
✓ 収益記事グリッド（装備レビュー・ランキング記事）
✓ 山紹介カード（装備紹介付き）
✓ 季節別おすすめ装備セクション
✓ 地域別山紹介 + 周辺観光・宿泊情報
✓ 最新レビュー・体験談
```

### 3. サイドバー（アフィリエイト重点）
```
✓ おすすめ装備ランキング（固定）
✓ 季節のおすすめ商品
✓ 人気記事ランキング
✓ カテゴリー別商品一覧
✓ 読者の購入報告・レビュー
```

### 4. フッター（信頼性 + 収益化）
```
✓ 運営者情報（専門性アピール）
✓ サイトマップ（SEO強化）
✓ 免責事項・アフィリエイト表記
✓ お問い合わせ・レビュー依頼
```

## 🎨 色彩設計（アフィリエイト最適化）

### 基本カラーパレット
```css
:root {
  /* 自然・山をイメージした基本色 */
  --primary-green: #2c5234;    /* 深緑（山・自然） */
  --secondary-green: #e8f5e8;  /* 淡緑（背景・区切り） */
  --accent-orange: #f0a500;    /* オレンジ（行動喚起） */
  
  /* テキスト・基本色 */
  --text-dark: #333333;        /* メインテキスト */
  --text-light: #666666;       /* サブテキスト */
  --background: #fafafa;       /* 背景色 */
  --border: #e0e0e0;          /* ボーダー */
  
  /* アフィリエイト専用色 */
  --affiliate-bg: #fff3e0;     /* 商品紹介背景 */
  --price-red: #e53935;        /* 価格表示（緊急性） */
  --cta-orange: #d84315;       /* CTAボタン（濃オレンジ） */
  --sale-yellow: #ffd54f;      /* セール・割引表示 */
}
```

## 🏗️ レイアウト構造設計

### 1. ヘッダー（sticky・アフィリエイト最適化）
```html
<header role="banner" class="site-header">
  <div class="container">
    <div class="logo">🏔️ 低山マスター</div>
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
    <div class="header-cta">
      <a href="/equipment/essential/" class="cta-button">必需品チェック</a>
    </div>
  </div>
</header>
```

### 2. メインコンテンツ（収益最大化レイアウト）
```html
<main class="main-content">
  <!-- ヒーローエリア -->
  <section class="hero">
    <div class="hero-content">
      <h1>安全で楽しい低山ハイキング</h1>
      <p>初心者・家族向け 47都道府県の厳選低山 + 必要装備を完全ガイド</p>
      <div class="hero-cta">
        <a href="/equipment/beginner/" class="cta-button primary">初心者向け装備</a>
        <a href="/mountains/ranking/" class="cta-button secondary">人気の山</a>
      </div>
    </div>
  </section>
  
  <!-- おすすめ装備セクション -->
  <section class="featured-equipment">
    <div class="container">
      <h2>🎒 今月のおすすめ装備</h2>
      <div class="equipment-grid">
        <!-- 装備カード × 3（アフィリエイト） -->
      </div>
    </div>
  </section>
  
  <!-- 山紹介 + 装備セット -->
  <section class="mountain-with-gear">
    <div class="container">
      <h2>⛰️ 山別おすすめ装備セット</h2>
      <div class="mountain-gear-grid">
        <!-- 山 + 装備セット × 3 -->
      </div>
    </div>
  </section>
</main>
```

## 📱 レスポンシブ対応

### ブレイクポイント
```css
/* モバイル */
@media (max-width: 768px) {
  .mountains-grid { grid-template-columns: 1fr; }
  .main-nav { display: none; }
  .mobile-menu { display: block; }
}

/* タブレット */
@media (min-width: 769px) and (max-width: 1024px) {
  .mountains-grid { grid-template-columns: repeat(2, 1fr); }
}

/* デスクトップ */
@media (min-width: 1025px) {
  .mountains-grid { grid-template-columns: repeat(3, 1fr); }
}
```

## 🔗 現在データとの対応関係（アフィリエイト活用）

### 山データ活用（47山 → 収益化構造）
```
✓ 47都道府県の低山 → 地域別ページ + 地域別装備
✓ 標高20m-400m → 難易度別必要装備
✓ 初心者向け → ビギナー装備セット
✓ アクセス情報 → 交通手段別装備
✓ BE-PAL記事 → 詳細コンテンツ + 関連商品
✓ 季節情報 → 季節別装備・ウェア
```

### 既存ファイル活用
- `data/mountains_japan_expanded.json` - メインデータベース（47山）
- `data/article_metadata.json` - 記事メタデータ
- `archive/generators/affiliate_static_generator.py` - 静的サイト生成器（要改修）
- `static_site/` - 現在のサイト構造
- `affiliate_design_specification.md` - アフィリエイト設計指針

### 💰 収益化マッピング
```
山の特徴 → 推奨装備カテゴリ
├── 低山（〜200m）→ 軽装備・スニーカー・日帰り用品
├── 中級山（200-400m）→ 本格装備・登山靴・ザック
├── 季節別 → ウェア・防寒具・レインウェア
├── 地域別 → 交通手段・宿泊・観光
└── 初心者向け → 入門セット・安全装備
```

## 🚀 実装計画

### Phase 1: アフィリエイト基盤構築（1-2日）
1. **HTMLテンプレート作成**
   - ヘッダー/フッター共通化（アフィリエイト最適化）
   - アフィリエイトボックス・CTAボタン設計
   - 商品紹介セクション統合

2. **CSS設計**
   - 自然色テーマ適用（緑・オレンジ）
   - アフィリエイト専用スタイル
   - レスポンシブ対応

### Phase 2: 収益化機能実装（2-3日）
1. **静的サイト生成器改修**
   - 新テンプレート対応
   - アフィリエイトリンク自動挿入
   - 商品データ統合

2. **コンテンツ統合**
   - 47山データ → 装備推奨システム
   - 記事 + 商品紹介の自動生成
   - 季節・地域別装備マッピング

### Phase 3: 収益最大化調整（1日）
1. **コンバージョン最適化**
   - CTAボタン配置調整
   - 商品紹介の効果測定
   - ユーザー導線改善

2. **品質管理**
   - アフィリエイト表記確認
   - 法的コンプライアンス
   - デプロイ前チェック

## 📋 技術仕様

### 使用技術
- **HTML5** + **CSS3** + **JavaScript**
- **Python** 静的サイト生成
- **FTP** 自動デプロイ
- **レスポンシブデザイン**

### ファイル構成（アフィリエイト最適化）
```
templates/
├── base.html                    # 基本テンプレート（アフィリエイト対応）
├── index.html                   # トップページ（収益重視レイアウト）
├── mountain_detail.html         # 山詳細 + 装備紹介
├── mountain_list.html           # 山一覧 + カテゴリ別装備
├── equipment_review.html        # 装備レビューページ
├── equipment_ranking.html       # 装備ランキングページ
├── affiliate_components/        # アフィリエイト部品
│   ├── product_box.html        # 商品紹介ボックス
│   ├── cta_buttons.html        # CTAボタンセット
│   └── equipment_set.html      # 装備セット紹介
└── region_index.html           # 地域別 + 地域装備

static/
├── css/
│   ├── mountain_affiliate_theme.css  # 山アフィリエイト専用CSS
│   ├── components.css               # 再利用可能コンポーネント
│   └── affiliate.css               # アフィリエイト要素専用
├── js/
│   ├── affiliate_tracking.js      # クリック追跡・分析
│   ├── product_recommendations.js # 商品推奨システム
│   └── site.js                    # 基本機能
└── images/
    ├── equipment/                 # 装備画像
    ├── mountains/                 # 山画像
    └── affiliate/                # アフィリエイト用素材
```

## ⚠️ 重要な制約・注意事項

### 1. z-index階層管理（CLAUDE.mdに従う）
```css
/* z-index階層定義（絶対遵守） */
Skip Link:                 z-index: 10000
サイトヘッダー（ナビ）:      z-index: 9999   ← header[role="banner"]
モーダル・ドロップダウン:    z-index: 1000-8999
記事ヘッダー:              z-index: 1       ← .article-header  
通常コンテンツ:            z-index: auto (0)
背景装飾:                  z-index: -1
```

### 2. HTMLテンプレート命名ルール
- **サイトヘッダー**: `<header role="banner">` （ナビゲーション用）
- **記事ヘッダー**: `<header class="article-header">` （記事タイトル用）
- **セクションヘッダー**: `<div class="section-header">` （その他用）

### 3. 必須レイアウト設定
```css
/* sticky/fixedヘッダー使用時は必ずbodyにpadding-top設定 */
body {
    padding-top: 70px; /* ヘッダー実測高さ分を確保 */
}

header[role="banner"] {
    position: sticky;
    top: 0;
    z-index: 9999;
    padding: 1rem 0;
}
```

### 4. 開発制約
- **外部API使用禁止**（Claude Code直接生成のみ）
- **既存データ活用必須**（47山データベース）
- **デプロイ前チェック必須**（DEPLOYMENT_CHECKLIST.md）

### 5. アフィリエイト関連制約
- **法的表記必須**（アフィリエイト広告である旨を明記）
- **ステマ規制対応**（PR表記・広告表記の徹底）
- **コンプライアンス**（薬機法・景表法の遵守）
- **収益最適化**（CVR測定・A/Bテスト実装）

## 🎯 実装開始時のコマンド

### 1. 現在のサイト構造確認
```bash
cd /home/qthisa/abg_teizan/mountain_blog_generator
ls -la static_site/
cat data/mountains_japan_expanded.json | head -20
```

### 2. 新テンプレート開発
```bash
# 新しいテンプレートディレクトリ作成
mkdir -p templates_new/
mkdir -p static_new/css/
mkdir -p static_new/js/
```

### 3. 既存生成器のバックアップ
```bash
cp archive/generators/affiliate_static_generator.py archive/generators/affiliate_static_generator_backup.py
```

## 📊 期待される成果

### 1. 収益向上（最重要目標）
- **アフィリエイト収益の大幅向上**（現在の3-5倍を目標）
- **CVR最適化**（訪問者→購入者の転換率向上）
- **客単価向上**（装備セット販売・高額商品誘導）

### 2. デザイン向上
- **自然・山テーマ**による親しみやすさ
- **アフィリエイト要素の自然な統合**
- **レスポンシブ対応**でモバイル収益化

### 3. コンテンツ戦略
- **山紹介 + 装備推奨**の自然な結合
- **季節・地域別装備**の体系的紹介
- **初心者向け装備ガイド**による市場拡大

### 4. SEO・集客最適化
- **購買意図キーワード**の強化
- **商品レビュー記事**でのロングテール獲得
- **地域×装備**での複合キーワード対応

## 💡 重要なアフィリエイト戦略

### 1. 商品カテゴリ別収益性
```
高収益カテゴリ:
├── 登山靴・トレッキングシューズ（5,000-30,000円）
├── ザック・バックパック（3,000-20,000円）
├── レインウェア・アウター（5,000-25,000円）
├── 登山用品セット（10,000-50,000円）
└── キャンプ・宿泊グッズ（2,000-15,000円）

中収益カテゴリ:
├── 小物・アクセサリー（500-3,000円）
├── 水筒・食料（1,000-5,000円）
└── 書籍・ガイドブック（1,000-3,000円）
```

### 2. ターゲット別アプローチ
```
初心者（最重要）:
- 装備選びに不安→「失敗しない」「初心者向け」
- 予算重視→「コスパ最強」「エントリーモデル」
- 安全重視→「専門家おすすめ」「実績豊富」

ファミリー層:
- 子供の安全→「子供用装備」「ファミリー向け」
- 荷物の軽量化→「軽量」「コンパクト」
- 楽しさ重視→「楽しい」「思い出作り」
```

### 3. 季節別キャンペーン
```
春（3-5月）: 新緑ハイキング装備
夏（6-8月）: 暑さ対策・虫対策グッズ
秋（9-11月）: 紅葉装備・防寒具
冬（12-2月）: 来年準備・室内トレーニング
```

## 📝 更新履歴

- **2025-07-05**: アフィリエイト特化版に全面改訂
- **2025-07-04**: 初版作成
- **参考サイト**: Template Party 桜ピンクテンプレート + アフィリエイト設計指針
- **データベース**: v5.2（47山）+ 装備マッピング
- **作成者**: Claude Code

---

**⚠️ 実装前に必ずCLAUDE.md、affiliate_design_specification.md、DEPLOYMENT_CHECKLIST.mdを確認してください**

**💰 最重要: アフィリエイト収益最大化を常に念頭に置いた実装を行うこと**