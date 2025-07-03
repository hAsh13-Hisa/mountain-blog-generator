# Git-Based CMS導入・運用ガイド

## 📋 概要
ロリポップサーバーでNode.jsが使えない制約を回避し、Git-Based CMS（Netlify CMS/Decap CMS）を使用してコンテンツ管理を実現する方法です。

## 🏗️ システム構成

```
GitHub Repository
├── 山データ (JSON)
├── 記事コンテンツ
└── Netlify CMS
    ↓ 編集
GitHub Actions
├── 静的サイト生成
└── FTPアップロード
    ↓ 自動デプロイ
ロリポップサーバー
└── teizan.omasse.com
```

## 🚀 導入手順

### Step 1: GitHubリポジトリの準備

1. **既存プロジェクトをGitHubにプッシュ**
```bash
cd /home/qthisa/abg_teizan/mountain_blog_generator
git remote add origin https://github.com/[username]/mountain-blog-generator.git
git push -u origin main
```

2. **ブランチ戦略の設定**
- `main`: 本番環境
- `develop`: 開発環境
- `cms/[feature]`: CMS編集用

### Step 2: Netlify CMS (Decap CMS)の設定

1. **必要なディレクトリ構造を作成**
```bash
mkdir -p static/admin
```

2. **CMS設定ファイルを作成**
```yaml
# static/admin/config.yml
backend:
  name: github
  repo: [username]/mountain-blog-generator
  branch: main
  base_url: https://api.netlify.com
  auth_endpoint: auth
  
# 日本語UI
locale: 'ja'

# メディアファイルの保存先
media_folder: "static/images/uploads"
public_folder: "/images/uploads"

# コンテンツコレクション
collections:
  # 山情報
  - name: "mountains"
    label: "山情報"
    label_singular: "山"
    description: "登山可能な低山の情報を管理"
    folder: "content/mountains"
    format: "json"
    create: true
    slug: "{{fields.id}}"
    identifier_field: "name"
    summary: "{{name}} ({{elevation}}m) - {{prefecture}}"
    
    fields:
      - {label: "ID", name: "id", widget: "string", hint: "例: mt_maruyama_hokkaido"}
      - {label: "山名", name: "name", widget: "string"}
      - {label: "山名（英語）", name: "name_en", widget: "string", required: false}
      - {label: "標高", name: "elevation", widget: "number", value_type: "int"}
      - {label: "都道府県", name: "prefecture", widget: "string"}
      - {label: "地域", name: "region", widget: "select", options: ["北海道", "東北", "関東", "中部", "近畿", "中国", "四国", "九州"]}
      
      - label: "位置情報"
        name: "location"
        widget: "object"
        fields:
          - {label: "緯度", name: "latitude", widget: "number", value_type: "float"}
          - {label: "経度", name: "longitude", widget: "number", value_type: "float"}
          - {label: "最寄り駅", name: "nearest_station", widget: "string"}
          - {label: "アクセス時間", name: "access_time", widget: "string"}
      
      - label: "難易度"
        name: "difficulty"
        widget: "object"
        fields:
          - {label: "レベル", name: "level", widget: "select", options: ["初級", "中級", "上級"]}
          - {label: "登山時間", name: "hiking_time", widget: "string"}
          - {label: "距離", name: "distance", widget: "string"}
          - {label: "標高差", name: "elevation_gain", widget: "string"}
      
      - {label: "特徴", name: "features", widget: "list", field: {label: "特徴", name: "feature", widget: "string"}}
      
      - label: "シーズン情報"
        name: "seasons"
        widget: "object"
        fields:
          - {label: "ベストシーズン", name: "best", widget: "list", field: {label: "月", name: "month", widget: "string"}}
          - {label: "避けるべき時期", name: "avoid", widget: "list", field: {label: "月", name: "month", widget: "string"}}
      
      - {label: "メイン画像", name: "main_image", widget: "image", required: false}
      
  # 記事
  - name: "articles"
    label: "記事"
    label_singular: "記事"
    folder: "content/articles"
    format: "frontmatter"
    create: true
    slug: "{{year}}-{{month}}-{{day}}-{{slug}}"
    
    fields:
      - {label: "タイトル", name: "title", widget: "string"}
      - {label: "公開日", name: "date", widget: "datetime"}
      - {label: "説明", name: "description", widget: "text"}
      - {label: "関連する山", name: "mountain_id", widget: "relation", collection: "mountains", value_field: "id", search_fields: ["name"], display_fields: ["name"]}
      - {label: "本文", name: "body", widget: "markdown"}
      - {label: "アイキャッチ画像", name: "featured_image", widget: "image", required: false}
      
  # サイト設定
  - name: "settings"
    label: "サイト設定"
    files:
      - label: "基本設定"
        name: "general"
        file: "content/settings/general.json"
        fields:
          - {label: "サイト名", name: "site_title", widget: "string"}
          - {label: "サイト説明", name: "site_description", widget: "text"}
          - {label: "キーワード", name: "keywords", widget: "string"}
          - {label: "Google Analytics ID", name: "ga_id", widget: "string", required: false}
```

3. **管理画面HTMLを作成**
```html
<!-- static/admin/index.html -->
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>低山旅行CMS管理画面</title>
  <script src="https://identity.netlify.com/v1/netlify-identity-widget.js"></script>
</head>
<body>
  <script src="https://unpkg.com/decap-cms@^3.0.0/dist/decap-cms.js"></script>
  <script>
    // カスタムプレビューテンプレート（オプション）
    CMS.registerPreviewStyle('/css/style.css');
  </script>
</body>
</html>
```

### Step 3: GitHub Actionsワークフロー設定

1. **FTP認証情報をGitHub Secretsに登録**
- `FTP_HOST`: FTPサーバーアドレス
- `FTP_USER`: FTPユーザー名
- `FTP_PASSWORD`: FTPパスワード

2. **ワークフローファイルを作成**
```yaml
# .github/workflows/deploy.yml
name: Build and Deploy to Lolipop

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Convert CMS content to JSON
      run: |
        python scripts/cms_to_json.py
    
    - name: Generate static site
      run: |
        python affiliate_static_generator.py
    
    - name: Deploy to FTP
      uses: SamKirkland/FTP-Deploy-Action@4.3.3
      with:
        server: ${{ secrets.FTP_HOST }}
        username: ${{ secrets.FTP_USER }}
        password: ${{ secrets.FTP_PASSWORD }}
        local-dir: ./static_site/
        server-dir: /as_teizan/
```

### Step 4: コンテンツ変換スクリプト

```python
# scripts/cms_to_json.py
import json
import os
import glob
from pathlib import Path

def convert_cms_to_json():
    """CMSのコンテンツを既存のJSON形式に変換"""
    
    # 山データの変換
    mountains = []
    mountain_files = glob.glob('content/mountains/*.json')
    
    for file_path in mountain_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            mountain = json.load(f)
            mountains.append(mountain)
    
    # 既存のデータ構造に合わせる
    output_data = {
        "metadata": {
            "version": "5.3",
            "last_updated": datetime.now().isoformat(),
            "description": "Git-Based CMS管理データ",
            "total_mountains": len(mountains)
        },
        "mountains": mountains
    }
    
    # 既存のパスに保存
    with open('data/mountains_japan_expanded.json', 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    convert_cms_to_json()
```

### Step 5: 認証設定

1. **Netlify IDの設定**（無料）
- https://app.netlify.com/ でアカウント作成
- Site settings > Identity > Enable Identity
- Registration preferences > Invite only
- 管理者のメールアドレスを招待

2. **OAuth設定**
- GitHubのOAuthアプリを作成
- Callback URL: `https://api.netlify.com/auth/done`

## 📝 運用方法

### 日常的な編集作業

1. **CMSアクセス**
   - `https://[your-domain]/admin/` にアクセス
   - GitHubアカウントでログイン

2. **コンテンツ編集**
   - 山情報の追加・編集
   - 記事の作成・更新
   - 画像のアップロード

3. **公開フロー**
   - CMSで「公開」ボタンをクリック
   - GitHubにコミット
   - GitHub Actionsが自動実行
   - ロリポップに自動デプロイ

### 開発者向け作業

1. **ローカル開発**
```bash
# CMSをローカルで起動
npx decap-server

# 別ターミナルで
python -m http.server 8000
# http://localhost:8000/admin/ でアクセス
```

2. **バックアップ**
```bash
# 定期的にデータをバックアップ
git pull origin main
cp -r data/ backup/data_$(date +%Y%m%d)/
```

## 🔧 トラブルシューティング

### よくある問題

1. **認証エラー**
   - GitHub OAuthアプリの設定確認
   - Netlify Identity設定の確認

2. **FTPデプロイ失敗**
   - GitHub Secrets設定の確認
   - FTP接続情報の検証

3. **ビルドエラー**
   - requirements.txt確認
   - Pythonバージョン確認

## 📊 メリット・デメリット

### メリット
- ✅ 無料で運用可能
- ✅ バージョン管理完備
- ✅ 非技術者も編集可能
- ✅ ロリポップサーバーで動作

### デメリット
- ❌ リアルタイムプレビューなし
- ❌ 初期設定がやや複雑
- ❌ インターネット接続必須

## 🚀 次のステップ

1. GitHubリポジトリの作成
2. Netlify CMSの初期設定
3. テスト環境での動作確認
4. 本番環境への移行