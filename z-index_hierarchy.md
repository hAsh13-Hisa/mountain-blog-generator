# Z-Index 階層構造

## 現在の設定値（修正後）

1. **Skip Link (アクセシビリティ)**: `z-index: 10000`
   - 最上位レイヤー
   - キーボード操作時に表示

2. **Site Header `header[role="banner"]`**: `z-index: 9999`
   - サイト全体のナビゲーション要素
   - 常に最前面に固定表示

3. **Hero セクション要素**: `z-index: 2`
   - ランディングページの要素

4. **Article Header `.article-header`**: `z-index: 1`
   - 記事内のヘッダー（タイトル部分）
   - 通常のコンテンツレイヤー

5. **装飾要素**: `z-index: -1`
   - 背景装飾等

## 重要な修正

**問題**: 以前は `header` セレクタがすべてのheaderタグに適用
**解決**: `header[role="banner"]` で**サイトヘッダーのみ**に高いz-indexを適用
**結果**: 記事ヘッダーがサイトヘッダーと重ならない