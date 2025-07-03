#!/usr/bin/env python3
"""
CMS管理コンテンツを既存のJSON形式に変換するスクリプト
Netlify CMS/Decap CMSで管理されるコンテンツを統合
"""

import json
import os
import glob
from datetime import datetime
from pathlib import Path
import frontmatter
import re
import html

class CMStoJSONConverter:
    def __init__(self):
        self.content_dir = Path("content")
        self.data_dir = Path("data")
        self.ensure_directories()
    
    def ensure_directories(self):
        """必要なディレクトリを作成"""
        self.content_dir.mkdir(exist_ok=True)
        (self.content_dir / "mountains").mkdir(exist_ok=True)
        (self.content_dir / "articles").mkdir(exist_ok=True)
        (self.content_dir / "settings").mkdir(exist_ok=True)
        self.data_dir.mkdir(exist_ok=True)
    
    def convert_mountains(self):
        """山データをCMS形式から既存JSON形式に変換"""
        mountains = []
        mountain_files = glob.glob(str(self.content_dir / "mountains" / "*.json"))
        
        for file_path in sorted(mountain_files):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    mountain = json.load(f)
                    
                # データ形式の検証と補完
                mountain = self.validate_mountain_data(mountain)
                mountains.append(mountain)
                print(f"✅ 変換完了: {mountain['name']}")
                
            except Exception as e:
                print(f"❌ エラー: {file_path} - {str(e)}")
        
        return mountains
    
    def sanitize_html_content(self, content: str) -> str:
        """HTMLコンテンツのサニタイズ"""
        if not content:
            return ""
        
        # 危険なHTMLタグの除去
        content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)
        content = re.sub(r'<iframe[^>]*>.*?</iframe>', '', content, flags=re.DOTALL | re.IGNORECASE)
        content = re.sub(r'on\w+="[^"]*"', '', content, flags=re.IGNORECASE)  # イベントハンドラ除去
        
        return content
    
    def validate_mountain_data(self, mountain):
        """山データの検証と必要なフィールドの補完（セキュリティ強化版）"""
        # 文字列長制限
        if len(mountain.get('name', '')) > 100:
            raise ValueError("山名が長すぎます（100文字以内）")
        
        # HTMLエスケープ処理
        text_fields = ['name', 'name_en', 'safety_info']
        for field in text_fields:
            if field in mountain and mountain[field]:
                mountain[field] = html.escape(str(mountain[field]))
        
        # リスト内文字列のエスケープ
        if 'features' in mountain and isinstance(mountain['features'], list):
            mountain['features'] = [html.escape(str(f)) for f in mountain['features']]
        
        # ネストされたオブジェクトの処理
        if 'location' in mountain:
            for key in ['nearest_station', 'access_time']:
                if key in mountain['location'] and mountain['location'][key]:
                    mountain['location'][key] = html.escape(str(mountain['location'][key]))
        # 必須フィールドのデフォルト値
        defaults = {
            "name_en": "",
            "location": {
                "latitude": None,
                "longitude": None,
                "nearest_station": "",
                "access_time": ""
            },
            "difficulty": {
                "level": "初級",
                "hiking_time": "",
                "distance": "",
                "elevation_gain": ""
            },
            "features": [],
            "seasons": {
                "best": [],
                "avoid": [],
                "features": {}
            },
            "trails": [],
            "access": {},
            "facilities": [],
            "nearby_attractions": [],
            "wildlife": [],
            "safety_info": "",
            "equipment_rental": "",
            "guided_tours": "",
            "emergency_contacts": {},
            "weather_info": "",
            "trail_conditions": "",
            "water_sources": [],
            "camping_allowed": False,
            "dogs_allowed": True,
            "night_hiking": False,
            "winter_hiking": True
        }
        
        # デフォルト値で不足フィールドを補完
        for key, default_value in defaults.items():
            if key not in mountain:
                mountain[key] = default_value
        
        return mountain
    
    def convert_articles(self):
        """記事データをCMS形式から処理"""
        articles = []
        article_files = glob.glob(str(self.content_dir / "articles" / "*.md"))
        
        metadata = {}
        
        for file_path in sorted(article_files):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    post = frontmatter.load(f)
                
                # 記事メタデータの抽出
                article_id = Path(file_path).stem
                metadata[article_id] = {
                    "title": post.get('title', ''),
                    "description": post.get('description', ''),
                    "mountain_id": post.get('mountain_id', ''),
                    "date": post.get('date', '').isoformat() if hasattr(post.get('date', ''), 'isoformat') else '',
                    "featured_image": post.get('featured_image', '')
                }
                
                print(f"✅ 記事変換完了: {post.get('title', article_id)}")
                
            except Exception as e:
                print(f"❌ 記事エラー: {file_path} - {str(e)}")
        
        return metadata
    
    def load_existing_data(self):
        """既存のJSONデータを読み込み"""
        existing_file = self.data_dir / "mountains_japan_expanded.json"
        if existing_file.exists():
            with open(existing_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    
    def merge_data(self, cms_mountains, existing_data):
        """CMSデータと既存データをマージ"""
        if not existing_data:
            return cms_mountains
        
        # 既存データの山をIDでインデックス化
        existing_mountains = {m['id']: m for m in existing_data.get('mountains', [])}
        
        # CMSデータでアップデート
        for mountain in cms_mountains:
            if mountain['id'] in existing_mountains:
                # 既存データを更新
                existing_mountains[mountain['id']].update(mountain)
            else:
                # 新規追加
                existing_mountains[mountain['id']] = mountain
        
        return list(existing_mountains.values())
    
    def save_json(self, mountains, article_metadata):
        """統合データを保存"""
        # 既存データの読み込み
        existing_data = self.load_existing_data()
        
        # データのマージ
        if existing_data:
            merged_mountains = self.merge_data(mountains, existing_data)
        else:
            merged_mountains = mountains
        
        # 出力データ構造
        output_data = {
            "metadata": {
                "version": "5.3",
                "last_updated": datetime.now().isoformat(),
                "description": "Git-Based CMS管理データ - 日本全国の低山マスターデータ",
                "total_mountains": len(merged_mountains),
                "coverage": "全47都道府県",
                "elevation_range": "20m - 400m",
                "focus": "初心者・家族向け・日帰り登山・アクセス良好・登山道整備済み",
                "cms_integration": {
                    "type": "Decap CMS (Netlify CMS)",
                    "last_sync": datetime.now().isoformat()
                }
            },
            "mountains": sorted(merged_mountains, key=lambda x: x['elevation'])
        }
        
        # メインデータファイルの保存
        output_file = self.data_dir / "mountains_japan_expanded.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ データ保存完了: {output_file}")
        print(f"   総山数: {len(merged_mountains)}山")
        
        # 記事メタデータの保存
        if article_metadata:
            metadata_file = self.data_dir / "article_metadata_cms.json"
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(article_metadata, f, ensure_ascii=False, indent=2)
            print(f"✅ 記事メタデータ保存: {metadata_file}")
    
    def run(self):
        """変換処理のメイン実行"""
        print("🔄 CMS to JSON 変換開始...\n")
        
        # 山データの変換
        print("📊 山データ変換中...")
        mountains = self.convert_mountains()
        
        # 記事データの変換
        print("\n📝 記事データ変換中...")
        article_metadata = self.convert_articles()
        
        # データの保存
        print("\n💾 データ保存中...")
        self.save_json(mountains, article_metadata)
        
        print("\n✨ 変換処理完了！")


def main():
    """メイン処理"""
    converter = CMStoJSONConverter()
    converter.run()


if __name__ == "__main__":
    main()