# 既知の問題・制限事項

## アイキャッチ画像関連

### 問題の詳細
- **編集画面**: Featured Image from URLプラグインで正常に表示される
- **予約投稿**: 公開記事にアイキャッチ画像が反映されない
- **即時投稿**: 未検証

### 現在の対応状況
- XMLファイルには正しくメタデータが含まれている
- `fifu_image_url`、`fifu_image_alt`、`_thumbnail_id`フィールドが設定済み
- 編集画面では画像URLが正しく表示される

### 一時的な回避策
1. **手動で再保存**: 公開後に記事を編集画面で再保存
2. **即時投稿を使用**: 予約投稿ではなく即時投稿を使用
3. **プラグイン設定確認**: Featured Image from URLプラグインの予約投稿対応設定

### 保留理由
- 予約投稿とプラグインの互換性問題の可能性
- WordPressのフック処理タイミングの問題の可能性
- より詳細な調査が必要

## その他の制限事項

### 楽天API商品取得
- 商品が少ない場合がある（地域や山によって差異）
- 一部のキーワードで商品が見つからない場合がある

### 山データ
- 一部の山で`mt_tsukuba`など存在しないIDがある
- 山一覧の表示機能で確認が必要

## 今後の改善予定
- [ ] アイキャッチ画像の予約投稿対応
- [ ] 楽天API商品取得の改善
- [ ] 山データの整備・検証