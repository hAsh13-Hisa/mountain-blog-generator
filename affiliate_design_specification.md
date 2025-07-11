# 人気アフィリエイトサイト デザイン仕様書
## 2024年版 - 低山ハイキングサイト向け設計指針

---

## 📋 概要

この仕様書は2024年の人気アフィリエイトサイトの分析結果に基づき、低山ハイキングサイトに最適化されたデザイン指針をまとめています。

---

## 🎯 基本設計思想

### 1. ユーザーファースト設計
- **第一印象の重要性**: 3秒以内にサイトの価値を伝える
- **可読性重視**: 読みやすさを最優先
- **直感的操作**: 迷わないナビゲーション

### 2. コンバージョン最適化
- **キラーページ導線**: 収益記事への自然な誘導
- **信頼性構築**: 専門性・権威性・信頼性の表現
- **アクション喚起**: 明確なCTAボタン配置

---

## 🖥️ ページレイアウト構成

### トップページ構成

```
┌─────────────────────────────────┐
│           ヘッダー               │ ← ナビゲーション、ロゴ
├─────────────────────────────────┤
│         ヒーローセクション         │ ← キャッチコピー、メインビジュアル
├─────────────────────────────────┤
│      人気記事カードグリッド        │ ← 3-4列グリッド、画像付き
├─────────────────────────────────┤
│        カテゴリ別おすすめ         │ ← 地域別、難易度別
├─────────────────────────────────┤
│       新着記事 & ランキング       │ ← 更新頻度をアピール
├─────────────────────────────────┤
│         サイト紹介・信頼性        │ ← 運営者情報、実績
├─────────────────────────────────┤
│           フッター               │ ← リンク集、著作権表示
└─────────────────────────────────┘
```

### 記事ページ構成

```
┌─────────────────────────────────┐
│           ヘッダー               │
├─────────────────────────────────┤
│         記事タイトル             │ ← SEOタイトル、h1タグ
├─────────────────────────────────┤
│    メタ情報 + アイキャッチ        │ ← 日付、カテゴリ、メイン画像
├─────────────────────────────────┤
│          目次（TOC）            │ ← ジャンプリンク
├─────────────────────────────────┤
│         メインコンテンツ         │ ← h2-h3構造、画像多用
├─────────────────────────────────┤
│      アフィリエイトボックス       │ ← 商品紹介セクション
├─────────────────────────────────┤
│         関連記事リンク           │ ← 内部リンク強化
├─────────────────────────────────┤
│           フッター               │
└─────────────────────────────────┘
```

---

## 🎨 デザインシステム

### カラーパレット

#### プライマリーカラー
- **メインカラー**: `#2c5234` (深緑) - 自然・安心感
- **アクセントカラー**: `#f0a500` (オレンジ) - 活力・行動喚起
- **サブカラー**: `#e8f5e8` (淡緑) - 背景・区切り

#### セカンダリーカラー
- **テキスト**: `#333333` (濃グレー) - 可読性重視
- **サブテキスト**: `#666666` (中グレー) - 補足情報
- **背景**: `#fafafa` (極薄グレー) - 清潔感

#### アフィリエイト専用カラー
- **商品紹介背景**: `#fff3e0` (淡オレンジ) - 注目度向上
- **価格表示**: `#e53935` (赤) - 緊急性・重要性
- **CTAボタン**: `#d84315` (濃オレンジ) - クリック誘導

### タイポグラフィ

#### フォントファミリー
```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 
             Roboto, 'Noto Sans JP', sans-serif;
```

#### フォントサイズ階層
- **大見出し（h1）**: `2.2rem` (35px) - 記事タイトル
- **中見出し（h2）**: `1.6rem` (26px) - セクション区切り
- **小見出し（h3）**: `1.3rem` (21px) - サブセクション
- **本文**: `1rem` (16px) - 読みやすさ重視
- **キャプション**: `0.85rem` (14px) - 補足情報

#### 行間・余白
- **行間**: `1.7` - 読みやすさを重視
- **段落間**: `1.2rem` - 適度な区切り
- **セクション間**: `2.5rem` - 明確な区分

---

## 🧭 ナビゲーション設計

### グローバルナビゲーション
```html
[ロゴ] [ホーム] [山一覧] [地域別] [初心者ガイド] [装備レビュー] [このサイトについて]
```

### パンくずリスト
```
ホーム > 関東地方 > 茨城県 > 筑波山登山ガイド
```

### サイドバー構成（記事ページ）
1. **検索ボックス** - サイト内検索
2. **人気記事ランキング** - PV上位5記事
3. **カテゴリ一覧** - 地域・難易度別
4. **おすすめ商品** - 固定アフィリエイト
5. **新着記事** - 更新情報
6. **プロフィール** - 運営者紹介

---

## 📱 レスポンシブデザイン

### ブレークポイント
- **モバイル**: `〜768px`
- **タブレット**: `769px〜1024px`
- **デスクトップ**: `1025px〜`

### モバイル最適化
```css
/* モバイルファースト設計 */
.container {
  padding: 0 15px;
}

.mountain-grid {
  grid-template-columns: 1fr; /* 1列表示 */
}

.affiliate-product {
  flex-direction: column; /* 縦積み */
}
```

---

## 💼 アフィリエイト要素設計

### 商品紹介ボックス
```html
<div class="affiliate-section">
  <h3>🎒 おすすめの登山グッズ</h3>
  <div class="affiliate-products">
    <div class="affiliate-product">
      <div class="product-info">
        <a href="[アフィリエイトURL]">商品名</a>
        <p class="product-description">商品説明</p>
      </div>
      <div class="product-price">¥3,980</div>
    </div>
  </div>
</div>
```

### CTAボタンデザイン
```css
.cta-button {
  background: linear-gradient(135deg, #f0a500, #d84315);
  color: white;
  padding: 12px 24px;
  border-radius: 25px;
  font-weight: bold;
  box-shadow: 0 4px 15px rgba(240, 165, 0, 0.3);
  transition: transform 0.2s ease;
}

.cta-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(240, 165, 0, 0.4);
}
```

---

## 📊 コンテンツ戦略

### 記事構成パターン

#### 1. 登山ガイド記事
```
1. 山の概要・魅力
2. 基本情報（標高、アクセス等）
3. 登山コース詳細
4. 見どころ・楽しみ方
5. 季節別情報
6. アクセス・準備情報
7. おすすめ装備（アフィリエイト）
8. まとめ
```

#### 2. 装備レビュー記事
```
1. 製品概要
2. 実際の使用感
3. メリット・デメリット
4. 他製品との比較
5. おすすめ度・評価
6. 購入リンク（アフィリエイト）
```

#### 3. 比較・ランキング記事
```
1. 比較基準の説明
2. ランキング一覧
3. 各製品の詳細レビュー
4. 用途別おすすめ
5. 購入ガイド
```

---

## 🔍 SEO・UI/UX最適化

### SEO要素
- **titleタグ**: 32文字以内、キーワード含有
- **meta description**: 120文字以内、魅力的な説明
- **h1-h6**: 階層構造を明確に
- **alt属性**: 画像の説明文
- **内部リンク**: 関連記事への誘導

### ページ表示速度最適化
- **画像最適化**: WebP形式、遅延読み込み
- **CSS/JS圧縮**: ファイルサイズ削減
- **CDN活用**: 配信速度向上

### ユーザビリティ
- **読み込み時間**: 3秒以内を目標
- **クリック領域**: 44px以上のタップエリア
- **コントラスト**: WCAG 2.1 AA準拠
- **フォーカス管理**: キーボード操作対応

---

## 📈 コンバージョン最適化

### A/Bテスト対象要素
1. **CTAボタンの色・文言**
2. **商品紹介ボックスの位置**
3. **価格表示の方法**
4. **画像とテキストの比率**

### ヒートマップ分析ポイント
1. **スクロール到達率**: コンテンツ長の最適化
2. **クリック分布**: リンク配置の改善
3. **離脱ポイント**: コンテンツ改善箇所特定

---

## 🛠️ 技術仕様

### 推奨技術スタック
- **CMS**: WordPress (テーマ: SWELL/SANGO推奨)
- **CSS Framework**: 独自CSS + Bootstrap Grid
- **JavaScript**: Vanilla JS + 必要最小限のライブラリ
- **画像**: WebP対応、Lazy Loading
- **アナリティクス**: Google Analytics 4 + Search Console

### パフォーマンス目標
- **PageSpeed Insights**: 90点以上
- **First Contentful Paint**: 1.5秒以内
- **Largest Contentful Paint**: 2.5秒以内
- **Cumulative Layout Shift**: 0.1以下

---

## 📋 実装チェックリスト

### デザイン実装
- [ ] カラーパレット適用
- [ ] タイポグラフィ設定
- [ ] レスポンシブ対応
- [ ] アフィリエイトボックス作成

### コンテンツ
- [ ] 記事テンプレート作成
- [ ] 画像最適化
- [ ] 内部リンク構造構築
- [ ] メタ情報設定

### 機能
- [ ] 検索機能実装
- [ ] 関連記事表示
- [ ] SNS共有ボタン
- [ ] お問い合わせフォーム

### SEO・分析
- [ ] Google Analytics設定
- [ ] Search Console登録
- [ ] sitemap.xml生成
- [ ] robots.txt設定

---

## 📚 参考情報

### 成功サイト分析例
1. **特化型アフィリエイトサイト**: 専門性重視
2. **比較・レビューサイト**: 客観的評価
3. **ブログ型サイト**: 個人の体験談重視

### 継続改善のポイント
1. **定期的なコンテンツ更新**
2. **ユーザーフィードバック収集**
3. **競合サイト分析**
4. **新トレンドの取り入れ**

---

*最終更新: 2025年7月1日*
*作成者: Claude (Anthropic)*