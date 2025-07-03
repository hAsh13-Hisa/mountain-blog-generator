# BE-PAL記事統合ガイド

## 概要
新しいBE-PAL記事や外部の山関連記事を山データベースに自動統合するためのワークフローシステムです。

## 📋 準備手順

### 1. 記事テキストファイルの準備
```bash
# 記事をテキストファイルとして保存
# ファイル名例: BE-PAL新記事.txt, 山と溪谷記事.txt
```

### 2. 必要なディレクトリ確認
```bash
# ログディレクトリが存在することを確認
mkdir -p logs
```

## 🚀 基本的な使用方法

### 簡単実行（記事ファイルのみ）
```bash
python bepal_integration_workflow.py BE-PAL記事.txt
```

### 完全実行（ソース情報付き）
```bash
python bepal_integration_workflow.py BE-PAL新記事.txt "全国のおすすめ低山100選" "https://www.bepal.net/archives/example"
```

## 📊 ワークフロー処理内容

### ステップ1: 山データ抽出
- テキストから「都道府県｜山名」パターンを検索
- 標高情報（標高XXXm）を抽出
- 標高400m以下の山のみを対象
- 山の説明文を自動抽出

### ステップ2: データ変換
- 山IDの自動生成（例: `mt_takao_tokyo`）
- 地域の自動判定（関東、関西など）
- 完全な山データ構造に変換
- 重複チェック

### ステップ3: データベース統合
- 既存データベースとの重複排除
- バージョン自動更新
- メタデータ更新

### ステップ4: レポート生成
- 統合結果サマリーをJSONで出力
- 詳細ログを`logs/`ディレクトリに保存

## 📁 出力ファイル

### 更新されるファイル
- `data/mountains_japan_expanded.json` - メインデータベース

### 新規作成されるファイル
- `logs/integration_summary_YYYYMMDD_HHMMSS.json` - 統合結果サマリー

## 🔧 カスタマイズ

### 標高制限の変更
```python
# bepal_integration_workflow.py の __init__ メソッド
self.elevation_limit = 500  # 500m以下に変更
```

### 地域マッピングの追加
```python
# convert_to_full_mountain_data メソッド内の region_map に追加
region_map = {
    # 既存マッピング...
    '新しい県': '新しい地域'
}
```

## 📋 手動確認が必要な項目

統合後、以下の項目は手動で確認・更新してください：

### 必須更新項目
- `location.latitude` / `location.longitude` - GPS座標
- `location.nearest_station` - 最寄り駅
- `location.access_time` - アクセス時間
- `difficulty.hiking_time` - 登山時間
- `difficulty.distance` - 距離
- `features` - 山の特徴
- `seasons.cherry_blossom` - 桜の見頃
- `seasons.autumn_leaves` - 紅葉の見頃

### 推奨更新項目
- `keywords` - SEO用キーワード
- `article_themes` - 記事テーマ
- `difficulty.level` - 難易度（初級/初級-中級）

## 🎯 実行例

### 例1: BE-PAL記事の統合
```bash
# BE-PAL記事をダウンロードしてテキストファイルに保存
curl -s "https://www.bepal.net/archives/536937" > bepal_new.html
# HTMLからテキストを抽出（手動またはツール使用）

# ワークフロー実行
python bepal_integration_workflow.py bepal_new.txt "全国のおすすめ低山58選" "https://www.bepal.net/archives/536937"
```

### 例2: 山と溪谷記事の統合
```bash
python bepal_integration_workflow.py yamakei_article.txt "初心者向け低山ガイド" "https://www.yamakei.com/example"
```

## 📈 実行結果の確認

### コンソール出力例
```
🔄 [14:30:15] EXTRACT: 記事テキストから山データを抽出開始
🔄 [14:30:15] FOUND: 衣張山 (神奈川県, 121m)
🔄 [14:30:15] FOUND: 吾妻山 (神奈川県, 136m)
🔄 [14:30:15] EXTRACT: 抽出完了: 2山を発見
🔄 [14:30:16] CONVERT: 衣張山 データ変換完了
🔄 [14:30:16] SAVE: データベース更新完了 (v5.2)
🔄 [14:30:16] SUCCESS: 2山を新規追加

==================================================
🏔️ BE-PAL統合ワークフロー結果
==================================================
✅ 成功
📊 抽出された山: 2山
🆕 新規追加: 2山
📄 詳細レポート: integration_summary_20250630_143016.json
==================================================
```

## 🔍 トラブルシューティング

### よくあるエラー

#### ファイルが見つからない
```bash
FileNotFoundError: [Errno 2] No such file or directory: 'BE-PAL記事.txt'
```
**解決**: ファイルパスを確認し、正しい場所にファイルがあることを確認

#### JSONエラー
```bash
json.decoder.JSONDecodeError
```
**解決**: 既存のデータベースファイルが破損している可能性。バックアップから復元

#### 重複エラー
```bash
🔄 [14:30:16] SKIP: 衣張山 - 既存データに存在
```
**解決**: 正常な動作。重複する山は自動的にスキップされます

### デバッグ方法
```bash
# 詳細ログを確認
cat logs/integration_summary_20250630_143016.json | jq '.workflow_log'

# データベースの確認
cat data/mountains_japan_expanded.json | jq '.metadata'
```

## 📚 関連ファイル

- `bepal_integration_workflow.py` - メインワークフロー
- `data/mountains_japan_expanded.json` - 山データベース
- `logs/` - 統合ログとサマリー
- `BEPAL_INTEGRATION_GUIDE.md` - このガイド

## 🔄 継続的な更新

### 定期的なBE-PAL記事チェック
```bash
# 月1回程度の頻度で新しい記事をチェック
# 1. BE-PAL サイトで新しい低山記事を探す
# 2. テキストファイルとして保存
# 3. ワークフローを実行
```

### データベースバックアップ
```bash
# 統合前にバックアップを作成
cp data/mountains_japan_expanded.json data/mountains_japan_expanded_backup_$(date +%Y%m%d).json
```