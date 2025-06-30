# 低山旅行自動記事作成アプリ - クイックスタートガイド

## セットアップ

### 1. 環境設定
```bash
# .envファイルを作成
cp .env.example .env

# .envファイルを編集してAPIキーを設定
# 必須: ANTHROPIC_API_KEY
# オプション: RAKUTEN_APP_ID, RAKUTEN_AFFILIATE_ID
```

### 2. 依存関係のインストール
```bash
# 仮想環境を作成・有効化
python3 -m venv venv
source venv/bin/activate

# パッケージをインストール
pip install -r requirements.txt
```

## 使い方

### 単発記事生成（推奨）
```bash
# スクリプトを使用（簡単）
./generate_article.sh mt_takao

# または直接実行
source venv/bin/activate
python simple_article_generator.py mt_takao
```

### 利用可能な山を確認
```bash
./generate_article.sh --list
```

### テーマを指定して生成
```bash
./generate_article.sh mt_fuji_shizuoka "家族登山"
```

## 生成されるファイル

- `generated_articles/article_山名_日時.json` - 記事データ
- `generated_articles/preview_山名_日時.html` - ブラウザで確認用

## ディレクトリ構成

```
mountain_blog_generator/
├── simple_article_generator.py  # メインスクリプト
├── generate_article.sh         # 実行用スクリプト
├── generated_articles/         # 生成された記事
├── src/                       # ソースコード
├── data/                      # 山データ
├── logs/                      # ログファイル
├── utils/                     # ユーティリティスクリプト
├── old_versions/              # 過去のバージョン
└── docs/                      # ドキュメント
```

## よく使う山ID

- `mt_takao` - 高尾山（東京）
- `mt_fuji_shizuoka` - 富士山（静岡・山梨）
- `mt_tsukuba` - 筑波山（茨城）
- `mt_mitake` - 御岳山（東京）

## トラブルシューティング

### APIキーエラーの場合
`.env`ファイルにANTHROPIC_API_KEYが正しく設定されているか確認

### 仮想環境のエラー
```bash
deactivate  # 一度終了
rm -rf venv  # 削除
python3 -m venv venv  # 再作成
```