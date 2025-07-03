# デプロイ前チェックリスト

## 🔍 過去の不具合から学んだ重要チェックポイント

### 1. ❌ 404エラー対策
**問題**: サイト内リンクが404エラーになる
- [ ] **全内部リンクの存在確認**
  ```bash
  python analyze_missing_pages.py
  ```
- [ ] **必須ページの存在確認**
  - `/about/`
  - `/beginner/`
  - `/contact/`
  - `/equipment/`
  - `/mountains/`
  - `/privacy/`
  - `/terms/`
  - `/regions/`
  - `/difficulty/beginner/`
- [ ] **地域別ページの確認**
  - 都道府県ページ（例: `/regions/北海道/`）
  - 地方ページ（例: `/regions/kanto/`）

### 2. 🎨 CSS・レイアウト問題
**問題**: ヘッダーがコンテンツに重なる、表示崩れ

#### z-index階層チェック
- [ ] **サイトヘッダー**: `header[role="banner"]` のみに高いz-index
- [ ] **記事ヘッダー**: `.article-header` は低いz-index
- [ ] **階層構造の確認**:
  - Skip Link: 10000
  - サイトヘッダー: 9999
  - 記事ヘッダー: 1

#### padding/margin確認
- [ ] **body**: `padding-top: 140px` が設定されているか
- [ ] **ヘッダー**: `position: fixed` で固定されているか
- [ ] **パンくずナビ**: 適切なmargin-topがあるか

#### キャッシュ対策
- [ ] **CSSバージョニング**: `/css/style.css?v=YYYYMMDDHHMM`
  ```bash
  python add_css_version.py
  ```

### 3. 💰 アフィリエイト欠落
**問題**: 山ページにアフィリエイトセクションがない
- [ ] **全山ページのアフィリエイト確認**
  ```bash
  python check_affiliate_sections.py
  ```
- [ ] **必須要素の確認**:
  - `<div class="affiliate-section">`
  - 楽天アフィリエイトリンク（最低5個）
  - 商品名と価格表示

### 4. 📁 FTPデプロイ問題
**問題**: ファイルが正しくアップロードされない
- [ ] **ディレクトリ作成エラー対策**
  - 階層的にディレクトリを作成しているか
  - `difficulty/beginner/` のような深い階層も考慮
- [ ] **文字エンコーディング**
  - UTF-8で保存されているか
  - 日本語ファイル名の扱い

### 5. 🖼️ HTMLテンプレート崩れ
**問題**: mainタグ内の不要な空行、改行
- [ ] **テンプレート整合性**
  ```bash
  python fix_mountain_templates.py
  ```
- [ ] **不要な改行・空行のチェック**
  - `<main>` 直後の改行
  - "No newline at end of file" の除去

### 6. ⚡ その他の重要ポイント
- [ ] **文字化け対策**: `\n` が `\\n` として表示されていないか
- [ ] **リンク切れ**: 外部リンクも含めて確認
- [ ] **モバイル表示**: レスポンシブデザインの確認
- [ ] **ブラウザ互換性**: Chrome, Firefox, Safari, Edge

## 📝 デプロイ手順

1. **ローカルチェック**
   ```bash
   python check_layout_issues.py
   python check_affiliate_sections.py
   python analyze_missing_pages.py
   ```

2. **問題修正**
   - 見つかった問題を個別に修正

3. **静的サイト生成**
   ```bash
   python affiliate_static_generator.py
   ```

4. **デプロイ**
   ```bash
   python deploy_all_pages.py
   ```

5. **本番環境確認**
   - 主要ページの表示確認
   - リンクのクリックテスト
   - アフィリエイトリンクの動作確認

## 🚨 緊急時の対処法

### CSSが反映されない場合
1. CSSバージョンパラメータを更新
2. ブラウザキャッシュをクリア（Ctrl+F5）
3. FTPで直接CSSファイルを確認

### 404エラーが発生した場合
1. FTPでファイルの存在を確認
2. パスの大文字小文字を確認
3. 必要に応じて手動でファイルをアップロード

### レイアウトが崩れた場合
1. 開発者ツール（F12）でエラーを確認
2. z-indexの競合をチェック
3. padding/marginの設定を確認