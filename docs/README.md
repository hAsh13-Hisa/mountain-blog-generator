# Mountain Blog Generator

低山旅行記事を自動生成してWordPressに投稿するPythonアプリケーション

## 概要

このシステムは、日本の低山に関する高品質なハイキング・登山記事を自動生成し、楽天アフィリエイトリンクを含めてWordPressに投稿します。

### 主な機能

- 🤖 **Claude AI による高品質記事生成**
- 🛍️ **楽天アフィリエイトリンクの自動挿入**
- 📸 **Unsplashからの画像自動取得**
- 📝 **WordPress自動投稿**
- 🔍 **SEO最適化**

## 必要な環境

- Python 3.9以上
- WordPress (REST API有効)
- 各種APIキー
  - Anthropic (Claude) API
  - 楽天アプリケーションID
  - 楽天アフィリエイトID

## インストール

### 1. リポジトリのクローン

```bash
git clone https://github.com/yourusername/mountain-blog-generator.git
cd mountain-blog-generator
```

### 2. 仮想環境の作成と有効化

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# または
venv\Scripts\activate  # Windows
```

### 3. 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

### 4. 開発モードでのインストール

```bash
pip install -e .
```

## 設定

### 1. 環境変数の設定

`.env.example`をコピーして`.env`を作成し、必要な情報を入力:

```bash
cp .env.example .env
```

`.env`ファイルの内容:
```
# API Keys
ANTHROPIC_API_KEY=sk-ant-api03-xxxxx
RAKUTEN_APP_ID=1099421053709374278
RAKUTEN_AFFILIATE_ID=139b96cc.29d2cd62.139b96cd.e6b1673a

# WordPress Settings
WP_URL=https://teizan.abg.ooo
WP_USERNAME=your_username
WP_APP_PASSWORD=your_app_password

# Application Settings
LOG_LEVEL=INFO
OUTPUT_DIR=./output
```

### 2. 山データの設定

`data/mountains.json`に山の情報を追加:

```json
{
  "mountains": [
    {
      "id": "takao",
      "name": "高尾山",
      "elevation": 599,
      "prefecture": "東京都",
      ...
    }
  ]
}
```

## 使用方法

### 基本的な使用方法

```bash
# 単一の山の記事を生成
mountain-blog generate --mountain takao

# 複数の山の記事を一括生成
mountain-blog generate --all

# ドラフトとして投稿
mountain-blog generate --mountain takao --draft

# ヘルプの表示
mountain-blog --help
```

### Pythonスクリプトとして実行

```python
from src.application.use_cases import GenerateArticleUseCase
from src.infrastructure.api import ClaudeClient, WordPressClient
from config.settings import Settings

# 設定を読み込み
settings = Settings()

# クライアントを初期化
claude_client = ClaudeClient(settings)
wp_client = WordPressClient(settings)

# ユースケースを実行
use_case = GenerateArticleUseCase(claude_client, wp_client)
result = use_case.execute("takao")
```

## プロジェクト構造

```
mountain_blog_generator/
├── config/              # 設定ファイル
├── src/
│   ├── domain/         # ドメイン層
│   ├── application/    # アプリケーション層
│   ├── infrastructure/ # インフラストラクチャ層
│   └── presentation/   # プレゼンテーション層
├── data/               # 山データ・テンプレート
├── logs/               # ログファイル
├── output/             # 生成された記事
└── tests/              # テストコード
```

## テスト

```bash
# 全テストを実行
pytest

# カバレッジレポート付きでテスト
pytest --cov=src

# 特定のテストのみ実行
pytest tests/unit/test_article_generator.py
```

## 開発

### コードフォーマット

```bash
# Black でフォーマット
black src/

# isort でインポートを整理
isort src/

# flake8 でリント
flake8 src/

# mypy で型チェック
mypy src/
```

### pre-commit の設定

```bash
pip install pre-commit
pre-commit install
```

## トラブルシューティング

### よくある問題

1. **APIキーエラー**
   - `.env`ファイルが正しく設定されているか確認
   - APIキーの権限を確認

2. **WordPress投稿エラー**
   - アプリケーションパスワードが有効か確認
   - REST APIが有効になっているか確認

3. **画像取得エラー**
   - インターネット接続を確認
   - Unsplashのサービス状態を確認

## ライセンス

MIT License

## 貢献

プルリクエストを歓迎します。大きな変更の場合は、まずissueを作成して変更内容を議論してください。

## サポート

問題が発生した場合は、[Issues](https://github.com/yourusername/mountain-blog-generator/issues)で報告してください。