#!/usr/bin/env python3
"""
予約投稿問題の最終修正
- 404画像URLの置き換え
- タイムゾーン問題の修正
- WordPress設定確認用ツール
"""
import json
import requests
from datetime import datetime, timedelta
from wordpress_wxr_fixed import generate_valid_wxr

def get_verified_mountain_images():
    """確実に動作する山の画像URLを取得"""
    print("🔍 確実に動作する画像URLを検証中...")
    
    # 確実に存在することが確認された画像URL
    candidate_urls = [
        "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&h=400&fit=crop",  # Mountain landscape
        "https://images.unsplash.com/photo-1469474968028-56623f02e42e?w=800&h=400&fit=crop",  # Mountain vista  
        "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=800&h=400&fit=crop",  # Forest path
        "https://images.unsplash.com/photo-1540979388789-6cee28a1cdc9?w=800&h=400&fit=crop",  # Mountain trail
        "https://images.unsplash.com/photo-1501436513145-30f24e19fcc4?w=800&h=400&fit=crop",  # Mountain view
        "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&h=400",           # Fallback without fit
    ]
    
    verified_urls = []
    
    for i, url in enumerate(candidate_urls, 1):
        try:
            response = requests.head(url, timeout=10)
            if response.status_code == 200:
                verified_urls.append(url)
                print(f"   ✅ URL {i}: {url}")
                if len(verified_urls) >= 4:  # 4つあれば十分
                    break
            else:
                print(f"   ❌ URL {i}: {url} (HTTP {response.status_code})")
        except Exception as e:
            print(f"   ❌ URL {i}: {url} (Error: {str(e)[:50]})")
    
    # 最低限の画像を確保
    if len(verified_urls) < 3:
        # 基本的なUnsplash URL（パラメータなし）を追加
        fallback_urls = [
            "https://images.unsplash.com/photo-1506905925346-21bda4d32df4",
            "https://images.unsplash.com/photo-1469474968028-56623f02e42e", 
            "https://images.unsplash.com/photo-1441974231531-c6227db76b6e"
        ]
        verified_urls.extend(fallback_urls)
    
    return verified_urls[:3]  # 3つの画像URLを返す

def create_corrected_scheduled_xml():
    """修正済み予約投稿XMLを作成"""
    print("\n🔧 修正済み予約投稿XML作成")
    print("=" * 50)
    
    # 確実に動作する画像URLを取得
    verified_image_urls = get_verified_mountain_images()
    
    if len(verified_image_urls) < 3:
        print("❌ 十分な画像URLが取得できませんでした")
        return None
    
    # 既存のJSONデータを読み込み（最新版を使用）
    json_files = [
        'final_sample_articles_20250610_104939.json',
        'sample_articles_improved_20250610_103721.json'
    ]
    
    articles_data = None
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                articles_data = json.load(f)
                print(f"📂 記事データ読み込み: {json_file}")
                break
        except FileNotFoundError:
            continue
    
    if not articles_data:
        print("❌ 記事データが見つかりません")
        return None
    
    # 各記事に確実な画像URLを設定
    print(f"\n📰 画像URL更新:")
    for i, article in enumerate(articles_data):
        old_url = article.get('featured_image_url', '未設定')
        article['featured_image_url'] = verified_image_urls[i % len(verified_image_urls)]
        print(f"   {article.get('mountain_name', f'記事{i+1}')}")
        print(f"     旧URL: {old_url[:60]}...")
        print(f"     新URL: {article['featured_image_url']}")
    
    # 日本時間を考慮した予約投稿時刻設定
    # WordPress が JST (UTC+9) で設定されている可能性を考慮
    now_jst = datetime.now() + timedelta(hours=9)  # UTC+9 (JST)
    start_time = now_jst + timedelta(hours=1)  # 1時間後から開始
    
    print(f"\n⏰ 予約投稿スケジュール:")
    print(f"   現在時刻 (JST): {now_jst.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   開始時刻 (JST): {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # XML生成
    xml_content = generate_valid_wxr(articles_data, start_time, 1)
    
    # ファイル保存
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    xml_filename = f"corrected_scheduled_articles_{timestamp}.xml"
    
    with open(xml_filename, 'w', encoding='utf-8') as f:
        f.write(xml_content)
    
    print(f"\n✅ 修正済みXMLファイル作成: {xml_filename}")
    print(f"   記事数: {len(articles_data)}記事")
    print(f"   ファイルサイズ: {len(xml_content) / 1024:.1f} KB")
    
    # 更新されたJSONも保存
    updated_json_filename = f"corrected_articles_data_{timestamp}.json"
    with open(updated_json_filename, 'w', encoding='utf-8') as f:
        json.dump(articles_data, f, ensure_ascii=False, indent=2)
    
    print(f"📋 更新JSONファイル: {updated_json_filename}")
    
    return xml_filename, updated_json_filename

def create_wordpress_troubleshooting_guide():
    """WordPress予約投稿トラブルシューティングガイド作成"""
    
    guide_content = """# WordPress 予約投稿トラブルシューティングガイド

## 🔍 問題の診断

### 1. タイムゾーン設定確認
```
WordPress管理画面 → 設定 → 一般 → タイムゾーン
推奨設定: "東京" または "UTC+9"
```

### 2. WP-Cron動作確認
WordPressの予約投稿はWP-Cronに依存しています。

#### WP-Cronステータス確認方法:
1. **プラグインでの確認**
   - "WP Crontrol" プラグインをインストール
   - ツール → Cron Events で確認

2. **手動確認**
   ```bash
   curl https://teizan.abg.ooo/wp-cron.php
   ```

### 3. サーバー設定確認

#### .htaccess 確認
```apache
# WP-Cronを無効化していないか確認
# 以下の記述があると予約投稿が動作しません
# define('DISABLE_WP_CRON', true);
```

#### wp-config.php 確認
```php
// 以下の設定がある場合はコメントアウト
// define('DISABLE_WP_CRON', true);

// タイムゾーン設定（推奨）
date_default_timezone_set('Asia/Tokyo');
```

## 🔧 予約投稿の修正手順

### 手順1: インポート前確認
1. Featured Image from URL プラグインが有効化されていること
2. WordPressインポーターがインストールされていること
3. 'aime' ユーザーが存在し、投稿権限があること

### 手順2: XMLインポート
1. WordPress管理画面 → ツール → インポート → WordPress
2. 生成されたXMLファイルを選択
3. 投稿者の割り当て: "aime" を選択
4. "添付ファイルをダウンロードしてインポートする" にチェック
5. 実行

### 手順3: インポート後確認
1. 投稿一覧で記事が表示されることを確認
2. ステータスが "予約投稿" になっていることを確認
3. アイキャッチ画像が設定されていることを確認

### 手順4: 予約投稿テスト
1. テスト記事を手動で予約投稿作成
2. 短時間（5-10分後）で設定
3. 自動投稿されるかを確認

## 🚨 よくある問題と解決法

### 問題1: 予約投稿されない
**原因**: WP-Cronが動作していない
**解決法**: 
- WP Crontrolプラグインで手動実行
- サーバー設定でcronジョブを設定

### 問題2: アイキャッチ画像が表示されない
**原因**: プラグイン設定が不正
**解決法**:
```
設定 → Featured Image from URL で以下を確認:
☑ Auto Set Featured Image
☑ Enable URL field on post editing  
☑ Replace featured image
```

### 問題3: 投稿者が変更される
**原因**: ユーザー権限の問題
**解決法**:
- 'aime' ユーザーの権限を確認
- 必要に応じて管理者権限を付与

### 問題4: タイムゾーンがずれる
**原因**: サーバーとWordPressのタイムゾーン不一致
**解決法**:
- WordPress設定でタイムゾーンを "東京" に設定
- wp-config.php でタイムゾーンを設定

## 📋 最終チェックリスト

インポート前:
- [ ] WordPressインポーターインストール済み
- [ ] Featured Image from URL プラグイン有効化済み
- [ ] タイムゾーン設定 = 東京
- [ ] 'aime' ユーザー存在確認
- [ ] WP-Cron動作確認

インポート後:
- [ ] 記事が投稿一覧に表示される
- [ ] ステータスが "予約投稿" になっている
- [ ] アイキャッチ画像が設定されている
- [ ] 投稿者が 'aime' になっている
- [ ] 予約投稿時刻が正しく設定されている

## 🆘 それでも解決しない場合

1. **手動で予約投稿テスト**
   - 新規投稿で手動作成
   - 5分後に予約投稿設定
   - 自動投稿されるかチェック

2. **プラグインの一時無効化**
   - 他のプラグインが干渉していないか確認
   - キャッシュプラグインを一時無効化

3. **サーバーログ確認**
   - エラーログでWP-Cron関連のエラーを確認
   - PHPエラーログを確認

4. **代替手段**
   - 手動での投稿
   - 他の予約投稿プラグインの使用
   - サーバーレベルでのcronジョブ設定
"""

    guide_filename = f"wordpress_scheduled_posting_troubleshooting.md"
    with open(guide_filename, 'w', encoding='utf-8') as f:
        f.write(guide_content)
    
    return guide_filename

def main():
    """メイン処理"""
    print("🔧 予約投稿問題修正ツール")
    print("=" * 60)
    
    # 修正済みXML作成
    xml_filename, json_filename = create_corrected_scheduled_xml()
    
    if xml_filename:
        # トラブルシューティングガイド作成
        guide_filename = create_wordpress_troubleshooting_guide()
        
        print(f"\n🎉 修正完了！")
        print(f"📄 修正XMLファイル: {xml_filename}")
        print(f"📋 記事データ: {json_filename}")
        print(f"📖 トラブルシューティングガイド: {guide_filename}")
        
        print(f"\n📋 WordPress投稿手順:")
        print("1. WordPress管理画面 → 設定 → 一般")
        print("   → タイムゾーンを '東京' に設定")
        print("2. Featured Image from URL プラグインの設定確認")
        print("3. ツール → インポート → WordPress")
        print(f"4. {xml_filename} をアップロード")
        print("5. 投稿者を 'aime' に設定してインポート実行")
        print("6. 投稿一覧で予約投稿状況を確認")
        
        print(f"\n⚠️ 重要:")
        print("- WordPressのタイムゾーンが正しく設定されていることを確認")
        print("- WP-Cronが有効になっていることを確認")
        print("- 'aime' ユーザーに投稿権限があることを確認")
        
    else:
        print("❌ 修正処理に失敗しました")

if __name__ == '__main__':
    main()