# セキュリティ改善実装計画

## 🔒 セキュリティ監査結果サマリー

**セキュリティスコア: 6.5/10**

主な問題：
- XSS対策不足（HTMLエスケープ、CSP未実装）
- 入力値検証の不完全性
- ユーザー権限管理の粗さ

## 🔥 緊急対応（セットアップ前に実装）

### 1. HTMLエスケープ処理の実装

#### A. cms_to_json.py の改良
```python
import html
import re

def sanitize_html_content(content: str) -> str:
    """HTMLコンテンツのサニタイズ"""
    if not content:
        return ""
    
    # HTMLタグの除去（基本的なもの）
    content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'<iframe[^>]*>.*?</iframe>', '', content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'on\w+="[^"]*"', '', content, flags=re.IGNORECASE)  # イベントハンドラ除去
    
    return content

def validate_mountain_data(self, mountain):
    """山データの検証とサニタイズ（強化版）"""
    # 文字列長制限
    if len(mountain.get('name', '')) > 100:
        raise ValueError("山名が長すぎます（100文字以内）")
    
    # HTMLエスケープ処理
    for field in ['name', 'name_en', 'safety_info']:
        if field in mountain and mountain[field]:
            mountain[field] = html.escape(str(mountain[field]))
    
    # リスト内文字列のエスケープ
    if 'features' in mountain and isinstance(mountain['features'], list):
        mountain['features'] = [html.escape(str(f)) for f in mountain['features']]
    
    return mountain
```

#### B. affiliate_static_generator.py の改良
```python
import html
from markupsafe import Markup, escape

def escape_user_content(content):
    """ユーザー入力コンテンツのエスケープ"""
    if not content:
        return ""
    return html.escape(str(content))

# HTMLテンプレート生成時
def generate_mountain_page(self, mountain_data):
    # ... 既存コード ...
    
    # ユーザー入力データのエスケープ
    safe_name = escape_user_content(mountain_data['name'])
    safe_description = escape_user_content(mountain_data.get('description', ''))
    
    # テンプレート内で使用
    html_content = f"""
    <h1>{safe_name}</h1>
    <p>{safe_description}</p>
    """
```

### 2. Content Security Policy の実装

#### HTMLテンプレートヘッダーに追加
```html
<!-- セキュリティヘッダーをHTMLテンプレートに追加 -->
<meta http-equiv="Content-Security-Policy" 
      content="default-src 'self'; 
               script-src 'self' 'unsafe-inline' https://www.googletagmanager.com https://www.google-analytics.com; 
               style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; 
               img-src 'self' data: https:; 
               connect-src 'self';">
<meta http-equiv="X-Content-Type-Options" content="nosniff">
<meta http-equiv="X-Frame-Options" content="DENY">
<meta http-equiv="X-XSS-Protection" content="1; mode=block">
<meta http-equiv="Referrer-Policy" content="strict-origin-when-cross-origin">
```

### 3. Netlify CMS設定の強化

#### config.yml セキュリティ改善
```yaml
# static/admin/config.yml に追加
collections:
  - name: "mountains"
    # ... 既存設定 ...
    fields:
      - label: "山名"
        name: "name"
        widget: "string"
        pattern: ['^[^<>&"]*$', '特殊文字（<>&"）は使用できません']
        hint: "100文字以内、HTMLタグ使用不可"
      
      - label: "説明"
        name: "description"
        widget: "text"
        pattern: ['^[^<script]*$', 'scriptタグは使用できません']
        
      # ファイルサイズ制限追加
      - label: "メイン画像"
        name: "main_image"
        widget: "image"
        max_file_size: 5242880  # 5MB制限
        required: false
```

## 📊 段階的実装計画

### Phase 1: 緊急対応（セットアップ前）
- [ ] HTMLエスケープ処理実装
- [ ] CSPヘッダー追加
- [ ] 入力値検証強化

### Phase 2: 運用開始後1週間以内
- [ ] ログ監視システム構築
- [ ] セキュリティテスト実施
- [ ] 不正アクセス検知

### Phase 3: 運用開始後1ヶ月以内
- [ ] ユーザー権限管理細分化
- [ ] セキュリティ監査自動化
- [ ] 依存関係脆弱性スキャン

## 🛡️ 運用時セキュリティガイドライン

### 管理者向けガイドライン
1. **定期的なパスワード変更**（3ヶ月毎）
2. **不審な編集履歴の監視**
3. **ファイルアップロード内容の確認**
4. **外部リンクの検証**

### 編集者向けガイドライン
1. **HTMLタグの直接入力禁止**
2. **外部スクリプトの埋め込み禁止**
3. **個人情報の記載禁止**
4. **著作権侵害コンテンツの禁止**

## 🚨 インシデント対応手順

### 1. 不正アクセス検知時
- GitHubアクセスログ確認
- Netlify Identity ログ確認
- 該当アカウントの無効化

### 2. 不正コンテンツ発見時
- 即座にコンテンツ削除
- Git履歴から完全削除
- 影響範囲の調査

### 3. システム脆弱性発見時
- 緊急パッチ適用
- セキュリティレビュー実施
- ドキュメント更新

## 📋 セキュリティチェックリスト

### デプロイ前チェック
- [ ] HTMLエスケープ処理実装済み
- [ ] CSPヘッダー設定済み
- [ ] 入力値検証実装済み
- [ ] .gitignore設定確認
- [ ] Secrets設定確認

### 運用中定期チェック（月次）
- [ ] アクセスログ確認
- [ ] 依存関係アップデート
- [ ] セキュリティパッチ適用
- [ ] バックアップ確認
- [ ] 脆弱性スキャン実行

## 🔧 推奨セキュリティツール

### 開発時
- **bandit**: Pythonセキュリティ問題検出
- **safety**: 依存関係脆弱性チェック
- **semgrep**: 静的解析ツール

### 運用時
- **GitHub Security Alerts**: 依存関係監視
- **Netlify Analytics**: アクセス解析
- **Cloudflare**: DDoS保護（オプション）

## ⚠️ 重要な注意事項

1. **段階的実装**: すべてを一度に実装せず、重要度順に対応
2. **テスト環境**: 本番前に必ずテスト環境で検証
3. **バックアップ**: セキュリティ更新前に必ずバックアップ
4. **監視**: 実装後は異常な動作がないか監視

このセキュリティ改善計画に従って実装することで、Git-Based CMSシステムの安全性を大幅に向上させることができます。