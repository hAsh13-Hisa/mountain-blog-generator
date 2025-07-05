# 🎨 低山アフィリエイト特化サイト - フレッシュデザイン仕様書

## 💰 アフィリエイト収益最大化に特化した完全新設計

### 🎯 基本コンセプト
- **Template Party継承を完全破棄**
- **アフィリエイト収益最大化**に特化した独自設計
- **山×装備**の自然な結合による高CVR設計
- **初心者・ファミリー層**をターゲットとした親しみやすいデザイン

## 🌈 独自カラーシステム

### 🍃 自然調和カラーパレット
```css
:root {
  /* === 基本色系（自然・山をイメージ） === */
  --mountain-deep: #1a4d2e;       /* 深い森の緑 */
  --mountain-medium: #27662d;     /* 中間の山緑 */
  --mountain-light: #e8f5e8;      /* 薄い新緑 */
  --mountain-mist: #f4f9f4;       /* 山霧のような背景 */
  
  /* === アクセント色系（行動喚起・収益化） === */
  --sunrise-orange: #ff6b35;      /* 山の日の出オレンジ */
  --sunset-red: #d73035;          /* 夕日の赤（緊急性） */
  --autumn-gold: #f0a500;         /* 秋の黄金色 */
  --sky-blue: #4a90e2;            /* 高原の空 */
  
  /* === 機能色系（UI要素） === */
  --text-primary: #2d3436;        /* 濃いグレー */
  --text-secondary: #636e72;      /* 中グレー */
  --text-light: #b2bec3;          /* 薄いグレー */
  --border-light: #ddd;           /* 薄いボーダー */
  --shadow-subtle: rgba(0,0,0,0.1); /* 微細な影 */
  
  /* === アフィリエイト特化色系 === */
  --affiliate-bg: #fff8e1;        /* 商品紹介背景 */
  --price-highlight: #d73035;     /* 価格強調 */
  --discount-bg: #ffeb3b;         /* 割引背景 */
  --cta-gradient-start: #ff6b35;  /* CTAグラデーション開始 */
  --cta-gradient-end: #d73035;    /* CTAグラデーション終了 */
  --success-green: #27ae60;       /* 成功・安全表示 */
}
```

## 🏗️ レイアウト設計原則

### 1. 収益最大化レイアウト構造
```
┌─────────────────────────────────────────────────────────────┐
│ 🏔️ ヘッダー（sticky）- 装備CTAボタン常時表示                │
├─────────────────────────────────────────────────────────────┤
│ 🌅 ヒーローエリア - 山の魅力 + 装備誘導                      │
├─────────────────────────────────────────────────────────────┤
│ 🎒 今月のおすすめ装備 - 高収益商品3つ                        │
├─────────────────────────────────────────────────────────────┤
│ ⛰️ 山別装備セット - 山紹介 + 装備セット販売                 │
├─────────────────────────────────────────────────────────────┤
│ 🗾 地域別ガイド - 地域×装備のマッピング                     │
├─────────────────────────────────────────────────────────────┤
│ 👨‍👩‍👧‍👦 初心者ガイド - 装備選び入門                               │
├─────────────────────────────────────────────────────────────┤
│ 📋 フッター - 信頼性 + 法的表記                             │
└─────────────────────────────────────────────────────────────┘
```

### 2. グリッドシステム
```css
/* フレッシュグリッドシステム */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

/* 装備グリッド（収益最適化） */
.equipment-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin: 2rem 0;
}

/* 山×装備グリッド */
.mountain-gear-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2.5rem;
  margin: 2rem 0;
}
```

## 📱 レスポンシブ戦略

### モバイルファーストアプローチ
```css
/* === ベース（モバイル） === */
.hero-title { font-size: 2rem; }
.equipment-grid { grid-template-columns: 1fr; }
.main-nav { display: none; }
.mobile-menu { display: block; }

/* === タブレット（768px+） === */
@media (min-width: 768px) {
  .hero-title { font-size: 2.5rem; }
  .equipment-grid { grid-template-columns: repeat(2, 1fr); }
  .main-nav { display: flex; }
  .mobile-menu { display: none; }
}

/* === デスクトップ（1024px+） === */
@media (min-width: 1024px) {
  .hero-title { font-size: 3rem; }
  .equipment-grid { grid-template-columns: repeat(3, 1fr); }
  .container { padding: 0 40px; }
}
```

## 🎨 UIコンポーネント設計

### 1. アフィリエイト特化CTAボタン
```css
.cta-button {
  background: linear-gradient(135deg, var(--cta-gradient-start), var(--cta-gradient-end));
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 600;
  text-decoration: none;
  display: inline-block;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(255, 107, 53, 0.3);
}

.cta-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 107, 53, 0.4);
}

.cta-button.large {
  padding: 16px 32px;
  font-size: 1.1rem;
}
```

### 2. 装備カード（収益最適化）
```css
.equipment-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 6px 24px var(--shadow-subtle);
  transition: transform 0.3s ease;
}

.equipment-card:hover {
  transform: translateY(-5px);
}

.equipment-card .price {
  color: var(--price-highlight);
  font-size: 1.5rem;
  font-weight: 700;
}

.equipment-card .discount {
  background: var(--discount-bg);
  color: var(--text-primary);
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 600;
}
```

### 3. 山紹介カード
```css
.mountain-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 20px var(--shadow-subtle);
  position: relative;
}

.mountain-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--mountain-deep), var(--sunrise-orange));
}

.mountain-meta {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  margin: 1rem 0;
}

.mountain-meta span {
  background: var(--mountain-light);
  color: var(--mountain-deep);
  padding: 4px 8px;
  border-radius: 16px;
  font-size: 0.9rem;
}
```

## 🌟 特徴的デザイン要素

### 1. 山テーマのアイコン統合
```css
/* 山アイコンの統合 */
.section-icon {
  font-size: 2rem;
  margin-right: 0.5rem;
  vertical-align: middle;
}

.mountain-difficulty::before {
  content: '🥾';
  margin-right: 0.5rem;
}

.equipment-category::before {
  content: '🎒';
  margin-right: 0.5rem;
}
```

### 2. 自然なグラデーション
```css
.hero-background {
  background: linear-gradient(135deg, var(--mountain-light) 0%, var(--mountain-mist) 100%);
  position: relative;
  overflow: hidden;
}

.hero-background::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><path d="M0,100 Q25,60 50,80 T100,70 L100,100 Z" fill="rgba(26,77,46,0.05)"/></svg>');
  background-size: cover;
  background-position: bottom;
}
```

### 3. 微細なアニメーション
```css
.float-animation {
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-10px); }
}

.pulse-cta {
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}
```

## 🎯 アフィリエイト最適化要素

### 1. 価格表示の最適化
```css
.price-display {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin: 1rem 0;
}

.price-current {
  font-size: 1.8rem;
  font-weight: 700;
  color: var(--price-highlight);
}

.price-original {
  font-size: 1.2rem;
  color: var(--text-secondary);
  text-decoration: line-through;
}

.price-discount {
  background: var(--discount-bg);
  color: var(--text-primary);
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.9rem;
  font-weight: 600;
}
```

### 2. 緊急性を演出するUI
```css
.urgency-indicator {
  background: var(--sunset-red);
  color: white;
  padding: 8px 16px;
  border-radius: 4px;
  font-size: 0.9rem;
  font-weight: 600;
  display: inline-block;
  animation: pulse 1.5s ease-in-out infinite;
}

.stock-warning {
  background: var(--autumn-gold);
  color: var(--text-primary);
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 600;
}
```

## 📊 パフォーマンス最適化

### 1. Critical CSS戦略
```css
/* Critical CSS（above the fold） */
.site-header, .hero, .featured-equipment {
  /* 最重要スタイル */
}

/* Non-critical CSS（lazy load） */
.footer, .detailed-content {
  /* 遅延読み込み対象 */
}
```

### 2. 画像最適化
```css
.lazy-image {
  opacity: 0;
  transition: opacity 0.3s ease;
}

.lazy-image.loaded {
  opacity: 1;
}

.equipment-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 8px 8px 0 0;
}
```

## 🔧 実装計画

### Phase 1: 基盤構築
1. **フレッシュHTML構造**
   - 完全新規base.html
   - アフィリエイト特化index.html
   - 山詳細テンプレート

2. **独自CSS設計**
   - 新カラーシステム
   - アフィリエイト最適化コンポーネント
   - レスポンシブ対応

### Phase 2: 機能実装
1. **JavaScript機能**
   - アフィリエイト追跡
   - 装備推奨システム
   - ユーザー導線最適化

2. **サイト生成器**
   - 新テンプレート対応
   - 装備データ統合
   - 自動アフィリエイトリンク

### Phase 3: 最適化
1. **CVR最適化**
   - A/Bテスト実装
   - ユーザー行動分析
   - 収益最大化調整

## ⚠️ 重要制約（CLAUDE.md準拠）

### z-index階層管理
```css
/* 絶対遵守階層 */
.skip-link { z-index: 10000; }
header[role="banner"] { z-index: 9999; }
.modal { z-index: 5000; }
.article-header { z-index: 1; }
```

### 必須レイアウト
```css
body {
  padding-top: 80px; /* ヘッダー高さ分 */
}

header[role="banner"] {
  position: sticky;
  top: 0;
  z-index: 9999;
}
```

## 🎉 完成イメージ

### 期待効果
1. **収益向上**: 現在の3-5倍のアフィリエイト収益
2. **CVR向上**: 訪問者→購入者転換率2倍
3. **UX向上**: 直感的で使いやすいUI
4. **SEO向上**: 構造化データ対応

### 差別化要素
1. **山×装備の自然結合**
2. **初心者特化の親しみやすさ**
3. **アフィリエイト要素の自然統合**
4. **モバイル最適化**

---

**🚀 実装開始準備完了 - 完全新規デザインによる収益最大化サイト構築**