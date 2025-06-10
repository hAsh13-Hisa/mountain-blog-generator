# WP-Cron 設定・有効化ガイド

## 🔍 WP-Cronとは？

WP-Cron（WordPressクーロン）は、WordPressの内蔵スケジューラーです。
予約投稿、自動更新、プラグインの定期実行などに使用されます。

**重要**: WP-Cronが無効になっていると予約投稿が動作しません。

---

## 📍 WP-Cronの設定場所と確認方法

### 1. wp-config.php での確認・設定

WordPressのルートディレクトリにある `wp-config.php` ファイルを確認します。

**ファイル場所**: `/public_html/wp-config.php` (通常)

#### ❌ 無効化されている場合（これがあると予約投稿が動かない）
```php
define('DISABLE_WP_CRON', true);
```

#### ✅ 有効化する場合
```php
// 以下の行をコメントアウトまたは削除
// define('DISABLE_WP_CRON', true);

// または明示的に有効化
define('DISABLE_WP_CRON', false);
```

### 2. .htaccess での確認

WordPress ルートディレクトリの `.htaccess` ファイルを確認

**避けるべき設定**:
```apache
# これがあるとWP-Cronが動作しない可能性
RewriteRule ^wp-cron\.php$ - [F,L]
```

---

## 🔧 WP-Cron 設定手順

### 手順1: ファイルアクセス方法

#### A. cPanel（レンタルサーバーの場合）
1. cPanel にログイン
2. "ファイルマネージャー" をクリック
3. `public_html` フォルダを開く
4. `wp-config.php` を右クリック → "編集"

#### B. FTP/SFTP（上級者向け）
1. FTPクライアント（FileZilla等）でサーバーに接続
2. WordPressがインストールされているディレクトリに移動
3. `wp-config.php` をダウンロード → 編集 → アップロード

#### C. SSH（上級者向け）
```bash
# サーバーにSSH接続後
cd /path/to/wordpress
nano wp-config.php
```

### 手順2: wp-config.php の編集

1. **バックアップ作成**（重要！）
   ```
   wp-config.php のコピーを作成
   例: wp-config.php.backup
   ```

2. **ファイルを開いて確認**
   ```php
   // この行を探す
   define('DISABLE_WP_CRON', true);
   ```

3. **修正方法**
   ```php
   // パターン1: コメントアウト
   // define('DISABLE_WP_CRON', true);
   
   // パターン2: false に変更
   define('DISABLE_WP_CRON', false);
   
   // パターン3: 削除する
   ```

4. **ファイルを保存**

### 手順3: 設定確認

#### WordPress管理画面での確認
1. プラグイン → 新規追加
2. "WP Crontrol" で検索してインストール・有効化
3. ツール → Cron Events で確認

#### 手動でのテスト
```bash
# ブラウザまたはコマンドで実行
curl https://teizan.abg.ooo/wp-cron.php
```

---

## 🔍 WP-Cron 動作確認方法

### 方法1: WP Crontrol プラグイン使用

1. **プラグインインストール**
   ```
   WordPress管理画面 → プラグイン → 新規追加
   → "WP Crontrol" を検索 → インストール → 有効化
   ```

2. **確認手順**
   ```
   ツール → Cron Events
   → スケジュールされたイベントが表示されるか確認
   ```

3. **テスト実行**
   ```
   "wp_scheduled_post" イベントを探す
   → "Run Now" で手動実行テスト
   ```

### 方法2: 手動テスト（コマンド）

```bash
# WP-Cronエンドポイントに直接アクセス
curl -I https://teizan.abg.ooo/wp-cron.php

# レスポンスが200 OKなら正常
HTTP/1.1 200 OK
```

### 方法3: 予約投稿テスト

1. **テスト記事作成**
   ```
   投稿 → 新規追加
   → タイトル: "WP-Cronテスト"
   → 公開日時を5-10分後に設定
   → "予約投稿" をクリック
   ```

2. **結果確認**
   ```
   設定時刻に自動で公開されるか確認
   ```

---

## 🚨 よくある問題と解決法

### 問題1: wp-config.php が見つからない
**解決法**:
- WordPressのルートディレクトリを確認
- 隠しファイルの表示を有効化
- サーバー管理者に確認

### 問題2: ファイル編集権限がない
**解決法**:
- ファイルの権限を確認（644 または 664）
- FTPで所有者権限を確認
- レンタルサーバーの場合は管理画面から編集

### 問題3: 編集後にサイトが表示されない
**解決法**:
- すぐにバックアップファイルで復元
- PHP構文エラーをチェック
- 余分な文字や改行を削除

### 問題4: WP-Cronは有効だが予約投稿されない
**解決法**:
- タイムゾーン設定確認
- サーバー時刻とWordPress時刻の確認
- 他のプラグインとの競合確認

---

## 📋 teizan.abg.ooo での設定確認手順

### 1. 現在の設定確認
```bash
# WP-Cronの動作確認
curl -I https://teizan.abg.ooo/wp-cron.php
```

### 2. wp-config.php の場所
```
一般的な場所:
/public_html/wp-config.php
/var/www/html/wp-config.php
/home/ユーザー名/public_html/wp-config.php
```

### 3. 必要に応じてレンタルサーバー管理画面で確認
- cPanel → ファイルマネージャー
- WordPress管理機能がある場合はそちらで確認

---

## ⚡ 緊急時の代替手段

### 1. プラグインでの代替
```
"WP Scheduled Posts" プラグインをインストール
→ 独自のスケジューラーを使用
```

### 2. サーバーレベルでのCron設定
```bash
# サーバーのcrontabに追加（上級者向け）
*/15 * * * * curl https://teizan.abg.ooo/wp-cron.php >/dev/null 2>&1
```

### 3. 手動投稿
```
予約投稿時刻に手動で公開ステータスに変更
```

---

## ✅ 最終チェックリスト

設定前の確認:
- [ ] wp-config.php のバックアップ作成済み
- [ ] ファイル編集権限の確認済み
- [ ] WordPress管理画面へのアクセス可能

設定後の確認:
- [ ] wp-config.php にDISABLE_WP_CRON=true がない
- [ ] WP Crontrol でイベント一覧が表示される
- [ ] curl テストで200 OKが返る
- [ ] テスト予約投稿が正常動作する

---

## 🆘 サポート

設定でお困りの場合:
1. 使用しているレンタルサーバーのサポートに問い合わせ
2. WordPressコミュニティフォーラムで質問
3. WP-Cronプラグインのドキュメント参照
