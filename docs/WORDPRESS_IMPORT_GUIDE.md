# WordPress インポート機能ガイド

## 概要

WordPressの標準インポート機能を使って、生成した記事を一括で投稿できます。

## メリット

- 🚀 **一括投稿** - 複数記事を一度にインポート
- 📅 **予約投稿対応** - 指定日時での自動公開
- 🛡️ **安全性** - WordPress標準機能なので安心
- 📝 **下書き保存可能** - 公開前に確認・編集可能

## 使い方

### 1. 即時公開用のインポートファイル生成

```bash
# 仮想環境で実行
source venv/bin/activate

# 複数の山を指定
python wordpress_import_generator.py mt_takao mt_tsukuba mt_fuji_shizuoka
```

### 2. 予約投稿用のインポートファイル生成

```bash
# 24時間間隔で予約投稿
python wordpress_import_generator.py --scheduled mt_takao mt_tsukuba mt_fuji_shizuoka
```

### 3. WordPressへのインポート手順

1. **WordPress管理画面にログイン**

2. **ツール → インポート**
   - 「WordPress」を選択
   - インポーターがない場合は「今すぐインストール」

3. **XMLファイルをアップロード**
   - 生成された `wordpress_import_YYYYMMDD_HHMMSS.xml` を選択
   - 「ファイルをアップロードしてインポート」をクリック

4. **投稿者の割り当て**
   - 記事の投稿者を選択
   - 「添付ファイルのインポート」にチェック（画像も含める場合）
   - 「実行」をクリック

## 生成されるXMLファイルの特徴

- **WXR形式** - WordPress eXtended RSS
- **完全な記事データ** - タイトル、本文、タグ、カテゴリー
- **アイキャッチ画像** - URLとして含まれる（要プラグイン）
- **予約投稿情報** - 日時指定済み

## アイキャッチ画像の設定

インポート後、以下のプラグインで自動設定可能：
- **Featured Image from URL** プラグイン
- インストール後、記事編集画面で画像URLを設定

## 注意事項

1. **大量インポート時**
   - 一度に100記事以上は避ける
   - サーバーのタイムアウトに注意

2. **予約投稿**
   - WP-Cronが有効であることを確認
   - タイムゾーン設定を確認

3. **重複チェック**
   - 同じ記事を再インポートすると重複する
   - 事前に既存記事を確認

## トラブルシューティング

### インポートが失敗する場合
- PHPのメモリ制限を確認（php.ini）
- アップロードファイルサイズ制限を確認
- XMLファイルのエンコーディング（UTF-8）を確認

### 予約投稿が機能しない場合
- WordPressのタイムゾーン設定を確認
- WP-Cronの動作を確認
- サーバーの時刻設定を確認

## 活用例

### 1週間分の記事を予約投稿
```bash
# 7つの山を選んで、毎日1記事ずつ公開
python wordpress_import_generator.py --scheduled \
  mt_takao mt_tsukuba mt_fuji_shizuoka \
  mt_mitake mt_jinba mt_nokogiri mt_oyama
```

### テーマ別記事の一括生成
```bash
# 家族向けテーマで複数記事を生成（要カスタマイズ）
python wordpress_import_generator.py \
  mt_takao mt_tsukuba mt_mitake
```