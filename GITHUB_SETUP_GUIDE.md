# GitHub セットアップガイド

## 📋 事前準備

1. **GitHubアカウント**が必要です（無料）
2. **FTP接続情報**を手元に用意してください
   - FTPホスト名
   - FTPユーザー名
   - FTPパスワード

## 🚀 セットアップ手順

### 1. GitHubでリポジトリを作成

1. https://github.com にログイン
2. 右上の「+」→「New repository」をクリック
3. 以下を入力:
   - Repository name: `mountain-blog-generator`
   - Description: `低山旅行記事生成システム - Git-Based CMS統合`
   - **Private**を選択（無料で利用可能）
   - 他はデフォルトのまま
4. 「Create repository」をクリック

### 2. ローカルリポジトリをGitHubに接続

ターミナルで以下のコマンドを実行：

```bash
cd /home/qthisa/abg_teizan/mountain_blog_generator

# Gitリポジトリとして初期化（既に初期化済みの場合はスキップ）
git init

# GitHubリポジトリをリモートとして追加
git remote add origin https://github.com/[your-username]/mountain-blog-generator.git

# 設定ファイルのユーザー名を更新
sed -i 's/\[your-username\]/YOUR_GITHUB_USERNAME/g' static/admin/config.yml
```

### 3. FTP認証情報をGitHub Secretsに登録

1. GitHubのリポジトリページを開く
2. 「Settings」タブをクリック
3. 左メニューの「Secrets and variables」→「Actions」をクリック
4. 「New repository secret」をクリック
5. 以下の3つのシークレットを追加：

   **FTP_HOST**
   - Name: `FTP_HOST`
   - Secret: `あなたのFTPホスト名`（例: ftp.lolipop.jp）
   
   **FTP_USER**
   - Name: `FTP_USER`
   - Secret: `あなたのFTPユーザー名`
   
   **FTP_PASSWORD**
   - Name: `FTP_PASSWORD`
   - Secret: `あなたのFTPパスワード`

### 4. 初回コミット＆プッシュ

```bash
# すべてのファイルをステージング
git add .

# 初回コミット
git commit -m "初期セットアップ: Git-Based CMS統合

- Netlify CMS設定追加
- GitHub Actions自動デプロイ設定
- 静的サイト生成システム統合"

# メインブランチに名前を変更（必要な場合）
git branch -M main

# GitHubにプッシュ
git push -u origin main
```

### 5. Netlify Identity設定（CMS認証用）

1. https://app.netlify.com/ にアクセス
2. 無料アカウントを作成
3. 「Add new site」→「Import an existing project」
4. GitHubと連携し、作成したリポジトリを選択
5. デプロイ設定:
   - Build command: 空欄
   - Publish directory: `static`
6. 「Deploy site」をクリック

デプロイ後：
1. 「Site settings」→「Identity」タブ
2. 「Enable Identity」をクリック
3. 「Registration」→「Invite only」を選択
4. 「Identity」→「Invite users」で自分のメールアドレスを招待
5. メールが届いたら認証を完了

### 6. CMSアクセス設定

1. Netlifyでサイトがデプロイされたら、URLをコピー
2. `https://[your-netlify-site].netlify.app/admin/` にアクセス
3. 招待メールで設定したアカウントでログイン

### 7. ローカル開発環境（オプション）

CMSをローカルで使う場合：

```bash
# Decap CMSのローカルプロキシをインストール
npm install -g @decap-cms/proxy-server

# プロキシサーバーを起動
npx decap-server

# 別ターミナルで静的サーバーを起動
python3 -m http.server 8000

# ブラウザで http://localhost:8000/admin/ にアクセス
```

## 🔧 トラブルシューティング

### GitHub Actions が失敗する場合

1. **Secrets設定を確認**
   - FTP_HOST, FTP_USER, FTP_PASSWORD が正しく設定されているか
   
2. **FTPサーバーの設定確認**
   - FTPSが有効になっているか
   - ポート21が開いているか

3. **ワークフローログを確認**
   - GitHubリポジトリの「Actions」タブでエラー詳細を確認

### CMSにログインできない場合

1. **Netlify Identity設定を確認**
   - Identityが有効になっているか
   - 招待メールが届いているか

2. **config.yml の設定確認**
   - GitHubユーザー名が正しく設定されているか
   - リポジトリ名が一致しているか

## 📝 日常的な使い方

### コンテンツ編集

1. `https://[your-site].netlify.app/admin/` または `https://teizan.omasse.com/admin/` にアクセス
2. GitHubアカウントでログイン
3. 山情報や記事を編集
4. 「公開」ボタンで保存

### 手動デプロイ

GitHubの「Actions」タブから：
1. 「Build and Deploy to Lolipop」を選択
2. 「Run workflow」→「Run workflow」をクリック

## 🎉 セットアップ完了！

これで、Git-Based CMSシステムが稼働します。
編集→自動ビルド→自動デプロイの流れが確立されました。