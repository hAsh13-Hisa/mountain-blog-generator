# Git使用ガイド

## 基本的なGitコマンド

### 変更の確認
```bash
git status          # 変更されたファイルを確認
git diff            # 変更内容を確認
```

### 変更の保存
```bash
git add .           # 全ての変更をステージング
git add <file>      # 特定のファイルをステージング
git commit -m "メッセージ"  # コミット
```

### 履歴の確認
```bash
git log --oneline   # コミット履歴を簡潔に表示
git log -p          # 変更内容付きで表示
```

## ブランチの使い方

### 新機能開発時
```bash
git branch feature/新機能名     # ブランチ作成
git checkout feature/新機能名   # ブランチ切り替え
# または
git checkout -b feature/新機能名  # 作成と切り替えを同時に
```

### マージ
```bash
git checkout master
git merge feature/新機能名
```

## GitHubへのプッシュ（リモートリポジトリを設定した場合）

```bash
# リモートリポジトリを追加
git remote add origin https://github.com/ユーザー名/mountain_blog_generator.git

# プッシュ
git push -u origin master
```

## .gitignoreについて

以下のファイル/ディレクトリは自動的に無視されます：
- `.env` - 環境変数（APIキーなど）
- `venv/` - Python仮想環境
- `logs/` - ログファイル
- `generated_articles/` - 生成された記事
- `__pycache__/` - Pythonキャッシュ

## 推奨ワークフロー

1. 作業前に最新状態を確認
   ```bash
   git status
   git pull  # リモートがある場合
   ```

2. 新機能はブランチで開発
   ```bash
   git checkout -b feature/機能名
   ```

3. こまめにコミット
   ```bash
   git add .
   git commit -m "実装内容を説明"
   ```

4. 完成したらマージ
   ```bash
   git checkout master
   git merge feature/機能名
   ```