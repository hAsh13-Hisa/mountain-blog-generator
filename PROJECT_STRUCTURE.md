# 📁 プロジェクト構造整理完了報告

## 🔄 整理実施内容

### 整理前の状況
- **ルートディレクトリ**: 132個のファイル
- **Python スクリプト**: 44個
- **JSON ファイル**: 53個
- **Markdown ファイル**: 14個

### 整理後の構造
```
/home/qthisa/abg_teizan/mountain_blog_generator/
├── 📁 archive/                    # アーカイブ（過去のファイル）
│   ├── articles/                  # 記事JSONファイル（article_*.json）
│   ├── docs_legacy/               # 旧ドキュメント（BEPAL_*.md等）
│   ├── generators/                # 記事生成器（enhanced_article_generator.py等）
│   └── scripts/                   # 統合スクリプト（bepal_integration_workflow.py等）
├── 📁 tools/                      # 開発ツール
│   ├── deployment/                # デプロイ関連（deploy_*.py）
│   ├── analysis/                  # 分析ツール（check_*.py, analyze_*.py）
│   └── utilities/                 # ユーティリティ（fix_*.py, update_*.py）
├── 📁 data/                       # データファイル
│   ├── mountains_japan_expanded.json
│   ├── article_metadata.json
│   ├── BE-PAL記事,txt
│   └── 山と溪谷記事,txt
├── 📁 static_site/                # 静的サイト出力
├── 📁 src/                        # ソースコード
├── 📁 config/                     # 設定ファイル
├── 📁 content/                    # コンテンツ
├── 📁 docs/                       # ドキュメント
├── 📁 logs/                       # ログファイル
├── 📁 tests/                      # テストコード
├── 📁 utils/                      # ユーティリティ
└── 📁 venv/                       # 仮想環境
```

### ルートディレクトリ残存ファイル（22個）
```
✅ 必須設定ファイル
- .env, .env.example
- .gitignore, .netlifyignore
- pyproject.toml, setup.py
- requirements.txt.backup
- Makefile, netlify.toml

✅ 重要ドキュメント
- CLAUDE.md（作業履歴）
- DEPLOYMENT_CHECKLIST.md（デプロイ前チェック）
- SITE_RECONSTRUCTION_PLAN.md（再構築計画）
- affiliate_design_specification.md
- z-index_hierarchy.md
- クイックスタート.md
- デプロイ仕様書.md
- 運用マニュアル.md

✅ 実行可能ファイル
- serve.py
- gui_launcher.py
- static_site_config.js
- php_dynamic_site.php
```

## 🔧 移動したファイルの主な用途

### archive/generators/
- `enhanced_article_generator.py` - メイン記事生成器
- `affiliate_static_generator.py` - 現在の静的サイト生成器
- `simple_article_generator*.py` - 簡易記事生成器

### archive/scripts/
- `bepal_integration_workflow.py` - BE-PAL記事統合
- `sync_article_images.py` - 画像同期
- `wordpress_*.py` - WordPress関連

### tools/deployment/
- `deploy_all_pages.py` - 全ページデプロイ
- `ftp_deploy.py` - FTPデプロイ
- `full_deploy.py` - 完全デプロイ

### tools/analysis/
- `check_*.py` - 各種チェックツール
- `analyze_*.py` - 分析ツール

## 🎯 整理の効果

1. **ルートディレクトリ**: 132個 → 22個（83%削減）
2. **視認性向上**: 重要ファイルが見つけやすくなった
3. **機能別分類**: 用途別にファイルが整理された
4. **メンテナンス性**: 関連ファイルがまとまった

## 🚀 今後の運用方針

### 新規ファイル作成ルール
1. **スクリプト**: 用途に応じて`tools/`配下に配置
2. **アーカイブ**: 古いファイルは`archive/`に移動
3. **ドキュメント**: 重要なものはルート、詳細は`docs/`
4. **一時ファイル**: 作業後は適切な場所に移動

### 定期整理
- 月1回のファイル整理
- 不要ファイルの削除
- archive内の古いファイル見直し

## 📝 更新履歴

- **2025-07-05**: 大規模ファイル整理実施
- **整理担当**: Claude Code
- **対象**: 132個のファイル → 22個に削減

---

**✅ プロジェクト構造整理完了**