
# Featured Image from URL プラグイン 手動設定ガイド

## 1. プラグイン設定確認

WordPress管理画面で以下を確認してください：

### Settings → Featured Image from URL
- ✅ **Enable Featured Image from URL** - 有効化
- ✅ **Auto Set Featured Image** - 自動設定を有効
- ✅ **Enable URL field on post editing** - 投稿編集画面にURL欄を表示

## 2. 各記事の手動設定

インポートした記事で画像が表示されない場合：

### 記事1: 札幌の円山登山ガイド
1. 投稿 → 編集画面を開く
2. 右サイドバーの「Featured Image from URL」セクション
3. 画像URL欄に貼り付け:
   ```
   https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&h=400&fit=crop
   ```
4. 「Set Featured Image」をクリック
5. 更新

### 記事2: 岩木山登山ガイド
1. 投稿 → 編集画面を開く
2. 画像URL欄に貼り付け:
   ```
   https://images.unsplash.com/photo-1464822759844-d150ad6ba46f?w=800&h=400&fit=crop
   ```
3. 「Set Featured Image」をクリック
4. 更新

### 記事3: 岩手山登山ガイド
1. 投稿 → 編集画面を開く
2. 画像URL欄に貼り付け:
   ```
   https://images.unsplash.com/photo-1469474968028-56623f02e42e?w=800&h=400&fit=crop
   ```
3. 「Set Featured Image」をクリック
4. 更新

## 3. プラグイン代替方法

Featured Image from URLが動作しない場合：

### 方法1: 記事内に画像を追加
各記事の先頭に以下のHTMLを追加：

```html
<img src="画像URL" alt="アイキャッチ画像" style="width:100%; height:400px; object-fit:cover; margin-bottom:20px;">
```

### 方法2: 別のプラグインを使用
- **Auto Featured Image from URL**
- **External Featured Image**
- **WP Featured Image Generator**

## 4. SEO設定

Yoast SEOを使用している場合：
1. 各記事の編集画面
2. Yoast SEOセクション
3. ソーシャル → Facebook/Twitter画像を設定

## 5. 確認方法

設定後の確認：
1. フロントエンドで記事一覧表示
2. 個別記事ページで画像表示確認
3. SNSシェア時の画像確認

## トラブルシューティング

### 画像が表示されない場合：
1. 画像URLが有効か確認（ブラウザで直接アクセス）
2. WordPressのメディア設定確認
3. テーマがアイキャッチ画像に対応しているか確認
4. プラグインの競合確認

### キャッシュクリア：
1. WordPressキャッシュプラグインのクリア
2. ブラウザキャッシュのクリア
3. CDNキャッシュのクリア（使用している場合）

## 最終手段：直接データベース更新

phpMyAdminでの直接更新（上級者向け）：
```sql
UPDATE wp_postmeta 
SET meta_value = '画像URL' 
WHERE meta_key = '_thumbnail_url' 
AND post_id = 記事ID;
```
