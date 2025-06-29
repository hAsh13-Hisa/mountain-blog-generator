# アイキャッチ画像設定ガイド

## 問題

生成されたXMLファイルには画像URLが含まれていますが、WordPressにインポートした時にアイキャッチ画像として自動的に設定されません。

## 原因

WordPressの標準インポート機能では、外部URL画像を自動的にアイキャッチ画像として設定する機能がありません。

## 解決方法

### 方法1: Featured Image from URL プラグイン（推奨）

1. **プラグインをインストール**
   - WordPressに「Featured Image from URL」プラグインをインストール
   - プラグインを有効化

2. **設定手順**
   - 記事編集画面で「Featured Image from URL」セクションを確認
   - XMLファイルに含まれる画像URLをコピペ
   - 「Preview」で確認後、更新

### 方法2: 自動設定機能を追加

XMLファイルにより詳細な画像情報を含める改良版を作成：

```xml
<wp:postmeta>
    <wp:meta_key>_featured_image_from_url</wp:meta_key>
    <wp:meta_value><![CDATA[https://images.unsplash.com/photo-1506905925346-21bda4d32df4]]></wp:meta_value>
</wp:postmeta>
```

### 方法3: 手動設定

1. **記事をインポート後**
2. **各記事を編集**
3. **アイキャッチ画像を手動で設定**
   - 「アイキャッチ画像を設定」をクリック
   - 「URLから挿入」タブを選択
   - XMLに含まれる画像URLを入力

## 現在のXMLファイルの画像情報

```xml
<wp:postmeta>
    <wp:meta_key>featured_image_url</wp:meta_key>
    <wp:meta_value><![CDATA[画像URL]]></wp:meta_value>
</wp:postmeta>
```

この情報を使って、上記の方法でアイキャッチ画像を設定できます。

## おすすめ手順

1. 「Featured Image from URL」プラグインをインストール
2. 記事をインポート
3. 各記事のメタデータから画像URLをコピー
4. プラグインを使ってアイキャッチ画像を設定