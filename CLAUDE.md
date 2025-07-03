# Claude作業履歴・再開ガイド

## 📋 現在の作業状況（2025-07-02）

### 🌐 サイト情報
- **メインURL**: https://teizan.omasse.com/
- **FTPパス**: https://omasse.pupu.jp/as_teizan/ (同一サイト)
- **デプロイ先**: /as_teizan ディレクトリ

## 📋 前回作業状況（2025-06-30）

### ✅ 完了項目（2025-07-02更新）
1. **BE-PAL記事統合ワークフロー** - 外部記事から山データ自動抽出システム
2. **山と溪谷記事データ統合** - 日本百低山から16山抽出、12山をデータベースに追加
3. **データベース拡充** - 47山の低山データベース（v5.2）完成
4. **静的サイトジェネレーター** - HTMLサイト生成・FTPデプロイシステム実装済み
5. **円山記事充実化** - 空だった記事を詳細コンテンツ+アフィリエイトリンク付きで完全リニューアル
6. **全ページ品質向上** - HTMLの\nゴミ除去、レイアウト最適化
7. **FTPデプロイ自動化** - teizan.omasse.com (= omasse.pupu.jp/as_teizan) への自動デプロイ完了

### 🎯 データベース詳細
- **版数**: v5.2
- **総山数**: 47山
- **標高範囲**: 20m - 400m（競秀峰131m ← 鷲頭山392m）
- **データソース**: BE-PAL記事 + 山と溪谷日本百低山
- **特徴**: 初心者・家族向け・日帰り・アクセス良好

### 📁 重要ファイル
- `data/mountains_japan_expanded.json` - メインデータベース
- `data/article_metadata.json` - 記事メタデータ（画像URL、タイトル等）
- `bepal_integration_workflow.py` - BE-PAL記事統合ツール
- `update_database_yamatokaikoku.py` - 山と溪谷データ統合ツール
- `enhanced_article_generator.py` - 記事生成システム
- `sync_article_images.py` - 記事画像同期ツール
- `BEPAL_INTEGRATION_GUIDE.md` - 統合ガイド
- `DEPLOYMENT_CHECKLIST.md` - デプロイ前チェックリスト

## 🚀 次回すぐに実行可能なタスク

### 1. 記事生成テスト
```bash
python enhanced_article_generator.py
```

### 2. 新規データソース統合
- 新しい記事ファイルがあれば：
```bash
python bepal_integration_workflow.py [記事ファイル名] [タイトル] [URL]
```

### 3. 静的サイト生成・公開
**⚠️ 重要: デプロイ前に必ずDEPLOYMENT_CHECKLIST.mdを確認してください！**
```bash
# 1. 事前チェック（必須）
python check_layout_issues.py
python check_affiliate_sections.py
python analyze_missing_pages.py

# 2. 問題がなければ静的サイト生成
python affiliate_static_generator.py

# 3. デプロイ実行
python deploy_all_pages.py
```

### 4. データベース拡充作業
- GPS座標の手動補完
- アクセス情報の詳細化
- 登山時間・距離の追加

## 📊 現在の進捗状況
- [x] データベース基盤構築
- [x] 記事統合ワークフロー完成
- [x] 複数データソース統合完了
- [ ] 記事生成テスト・検証
- [ ] サイト公開
- [ ] データ詳細化

## 💡 開発のポイント
- 標高400m以下の低山に特化
- 初心者・家族向けコンテンツ重視
- 複数記事ソースの統合機能
- 自動記事生成 + 手動カスタマイズ
- 静的サイト + FTP自動デプロイ

## ⚠️ デプロイ時の注意事項
**DEPLOYMENT_CHECKLIST.md を必ず確認！**
過去の不具合：
- 404エラー（必須ページの欠落）
- ヘッダー重なり（z-index問題）
- アフィリエイトセクション欠落
- HTMLテンプレート崩れ

## 📝 記事生成ルール（2025-07-03更新）

### ⚠️ 重要：外部API使用禁止
- **Claude Code**による記事生成のみ使用
- Anthropic API、WordPress API等の外部API呼び出しは禁止
- APIエラー回避・安定性確保のため

### 🎯 記事生成フロー
1. **Claude Code**で記事内容を直接生成
2. 生成した記事をHTMLファイルとして保存
3. 静的サイトジェネレーターでサイト構築
4. FTPデプロイで公開

## 🔄 再開時の最初のコマンド
```bash
cd /home/qthisa/abg_teizan/mountain_blog_generator
ls -la data/
cat data/mountains_japan_expanded.json | head -20
```