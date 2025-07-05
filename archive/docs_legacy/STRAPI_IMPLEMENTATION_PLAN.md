# Strapi実装計画書 - 低山旅行記事生成システム

## 📋 概要
現在の静的サイトジェネレーターシステムにStrapiヘッドレスCMSを統合し、コンテンツ管理の効率化とレイアウトの統一性を実現する。

## 🎯 実装目標
1. **レイアウトの完全統一化** - テンプレート管理の一元化
2. **コンテンツ管理の効率化** - 非技術者でも更新可能
3. **既存データの完全移行** - 47山のデータを損失なく移行
4. **API駆動の静的サイト生成** - 現在のFTPデプロイシステムを維持

## 📊 データモデル設計

### 1. Mountain（山）コレクション
```javascript
{
  // 基本情報
  id: "String (Unique)",
  name: "String (Required)",
  name_en: "String",
  elevation: "Number (Required)",
  
  // 位置情報
  prefecture: "String (Required)",
  region: "Relation to Region",
  location: {
    latitude: "Float",
    longitude: "Float",
    nearest_station: "String",
    access_time: "String"
  },
  
  // 難易度情報
  difficulty: {
    level: "Enum ['初級', '中級', '上級']",
    hiking_time: "String",
    distance: "String",
    elevation_gain: "String"
  },
  
  // 特徴
  features: "JSON (Array)",
  
  // シーズン情報
  seasons: {
    best: "JSON (Array)",
    avoid: "JSON (Array)",
    features: "JSON (Object)"
  },
  
  // メディア
  images: "Media (Multiple)",
  main_image: "Media (Single)",
  
  // SEO
  seo_title: "String",
  seo_description: "Text",
  
  // リレーション
  articles: "Relation to Article (One to Many)",
  affiliate_links: "Component (Repeatable)"
}
```

### 2. Article（記事）コレクション
```javascript
{
  title: "String (Required)",
  slug: "String (Unique)",
  content: "Rich Text",
  excerpt: "Text",
  published_at: "DateTime",
  
  // リレーション
  mountain: "Relation to Mountain",
  author: "Relation to User",
  
  // メタデータ
  metadata: {
    reading_time: "Number",
    difficulty_level: "Enum",
    season: "String"
  },
  
  // SEO
  seo: "Component"
}
```

### 3. Region（地域）コレクション
```javascript
{
  name: "String (Required)",
  slug: "String (Unique)",
  description: "Text",
  
  // リレーション
  mountains: "Relation to Mountain (One to Many)",
  
  // メタデータ
  climate_info: "Text",
  access_info: "Text"
}
```

### 4. コンポーネント

#### AffiliateLink
```javascript
{
  platform: "Enum ['Amazon', '楽天', 'Yahoo']",
  product_name: "String",
  url: "String",
  image_url: "String",
  price: "String",
  description: "Text"
}
```

#### SEO
```javascript
{
  meta_title: "String",
  meta_description: "Text",
  keywords: "String",
  og_image: "Media",
  canonical_url: "String"
}
```

## 🔄 移行計画

### Phase 1: 環境構築（1-2日）
1. **Strapiインストール**
   ```bash
   npx create-strapi-app@latest mountain-cms --quickstart
   cd mountain-cms
   npm run develop
   ```

2. **コンテンツタイプ作成**
   - 管理画面からGUIで作成
   - または`api/`ディレクトリに直接定義

3. **日本語化**
   ```bash
   npm install strapi-plugin-i18n
   ```

### Phase 2: データ移行（2-3日）

#### 移行スクリプト概要
```python
# strapi_migration.py
import json
import requests
from typing import Dict, List

class StrapiMigration:
    def __init__(self, strapi_url: str, api_token: str):
        self.base_url = strapi_url
        self.headers = {
            'Authorization': f'Bearer {api_token}',
            'Content-Type': 'application/json'
        }
    
    def migrate_mountains(self, json_file: str):
        """既存のJSONデータをStrapiに移行"""
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for mountain in data['mountains']:
            # データ変換
            strapi_data = self.transform_mountain_data(mountain)
            
            # Strapi APIにPOST
            response = requests.post(
                f"{self.base_url}/api/mountains",
                json={"data": strapi_data},
                headers=self.headers
            )
            
    def transform_mountain_data(self, mountain: Dict) -> Dict:
        """データ形式をStrapi用に変換"""
        return {
            "name": mountain['name'],
            "name_en": mountain.get('name_en', ''),
            "elevation": mountain['elevation'],
            "prefecture": mountain['prefecture'],
            # ... その他のフィールドマッピング
        }
```

### Phase 3: API統合（2-3日）

#### 静的サイトジェネレーター改修
```python
# enhanced_article_generator_strapi.py
class StrapiArticleGenerator:
    def __init__(self, strapi_url: str):
        self.api_url = f"{strapi_url}/api"
        
    async def fetch_mountains(self) -> List[Dict]:
        """Strapi APIから山データを取得"""
        response = await requests.get(
            f"{self.api_url}/mountains?populate=*"
        )
        return response.json()['data']
    
    def generate_static_site(self):
        """APIデータから静的サイトを生成"""
        mountains = self.fetch_mountains()
        
        for mountain in mountains:
            self.generate_mountain_page(mountain)
            
        self.generate_index_page(mountains)
        self.generate_region_pages(mountains)
```

### Phase 4: テンプレート統一（1-2日）

#### Strapiでのテンプレート管理
```javascript
// strapi/src/api/template/content-types/template/schema.json
{
  "kind": "collectionType",
  "collectionName": "templates",
  "info": {
    "singularName": "template",
    "pluralName": "templates",
    "displayName": "Template"
  },
  "attributes": {
    "name": {
      "type": "string",
      "required": true
    },
    "type": {
      "type": "enumeration",
      "enum": ["mountain", "article", "region", "index"],
      "required": true
    },
    "html_template": {
      "type": "text",
      "required": true
    },
    "css_version": {
      "type": "string",
      "default": "202507030000"
    }
  }
}
```

## 🚀 実装スケジュール

### Week 1: 基盤構築
- [ ] Strapi環境構築
- [ ] コンテンツタイプ定義
- [ ] 管理画面カスタマイズ
- [ ] API権限設定

### Week 2: データ移行
- [ ] 移行スクリプト開発
- [ ] テストデータ移行
- [ ] 本番データ移行
- [ ] データ検証

### Week 3: システム統合
- [ ] 静的サイトジェネレーター改修
- [ ] API連携実装
- [ ] テンプレート統一
- [ ] デプロイパイプライン構築

### Week 4: テスト・最適化
- [ ] 統合テスト
- [ ] パフォーマンス最適化
- [ ] ドキュメント作成
- [ ] 本番移行

## 🏗️ インフラ要件

### 推奨構成
1. **開発環境**
   - ローカルStrapi（SQLite）
   - Node.js 18以上

2. **本番環境オプション**
   - **Option A**: VPS（月額1,000円程度）
     - Ubuntu 22.04
     - PostgreSQL
     - Nginx
   
   - **Option B**: Strapi Cloud（月額$29〜）
     - マネージドサービス
     - 自動バックアップ
   
   - **Option C**: Heroku（無料〜）
     - PostgreSQLアドオン
     - 自動デプロイ

## 📝 移行時の注意点

1. **データバックアップ**
   - 現在のJSONデータを完全バックアップ
   - 生成済み静的サイトもバックアップ

2. **段階的移行**
   - まず開発環境で完全動作確認
   - 一部の山データでテスト運用
   - 問題なければ全データ移行

3. **既存システムとの並行運用**
   - 移行期間中は両システムを維持
   - 完全移行後に旧システム停止

## 🎨 期待される改善効果

1. **レイアウト統一**
   - 全ページで同一テンプレート使用
   - CSSバージョン管理の一元化
   - コンポーネントベースの開発

2. **運用効率化**
   - GUIでのコンテンツ編集
   - 画像アップロードの簡素化
   - プレビュー機能

3. **拡張性向上**
   - プラグインによる機能追加
   - 多言語対応の容易化
   - ユーザー権限管理

## 📚 参考リソース
- [Strapi公式ドキュメント](https://docs.strapi.io/)
- [Strapi日本語コミュニティ](https://strapi-japan.com/)
- [静的サイト生成ガイド](https://strapi.io/blog/how-to-create-a-static-site-with-strapi)

## 🔄 次のアクション
1. Strapi開発環境の構築開始
2. 詳細なデータモデルの最終確認
3. 移行スクリプトのプロトタイプ作成