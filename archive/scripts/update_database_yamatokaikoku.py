#!/usr/bin/env python3
"""
山と溪谷記事から抽出した低山データをメインデータベースに統合するスクリプト
"""

import json
import os
from datetime import datetime

class YamatoKaikokuIntegrator:
    def __init__(self):
        self.source_file = "yamatokaikoku_low_mountains_under_400m.json"
        self.database_file = "data/mountains_japan_expanded.json"
        
    def load_source_data(self):
        """山と溪谷データを読み込み"""
        with open(self.source_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def load_database(self):
        """既存データベースを読み込み"""
        with open(self.database_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def convert_to_full_mountain_data(self, mountain):
        """山と溪谷データを完全な山データ構造に変換"""
        
        # 地域マッピング
        region_map = {
            '北海道': '北海道',
            '青森県': '東北', '岩手県': '東北', '宮城県': '東北', '秋田県': '東北', 
            '山形県': '東北', '福島県': '東北',
            '茨城県': '関東', '栃木県': '関東', '群馬県': '関東', '埼玉県': '関東',
            '千葉県': '関東', '東京都': '関東', '神奈川県': '関東',
            '新潟県': '中部', '富山県': '中部', '石川県': '中部', '福井県': '中部',
            '山梨県': '中部', '長野県': '中部', '岐阜県': '中部', '静岡県': '中部', '愛知県': '中部',
            '三重県': '関西', '滋賀県': '関西', '京都府': '関西', '大阪府': '関西',
            '兵庫県': '関西', '奈良県': '関西', '和歌山県': '関西',
            '鳥取県': '中国', '島根県': '中国', '岡山県': '中国', '広島県': '中国', '山口県': '中国',
            '徳島県': '四国', '香川県': '四国', '愛媛県': '四国', '高知県': '四国',
            '福岡県': '九州', '佐賀県': '九州', '長崎県': '九州', '熊本県': '九州',
            '大分県': '九州', '宮崎県': '九州', '鹿児島県': '九州', '沖縄県': '沖縄'
        }
        
        prefecture = mountain['prefecture'].split('・')[0]  # 複数県の場合は最初を使用
        region = region_map.get(prefecture, '不明')
        
        # 山IDを生成
        mountain_id = f"mt_{mountain['name'].lower().replace('山', '').replace('岳', '').replace('峰', '')}_{prefecture.replace('県', '').replace('府', '').replace('都', '').lower()}"
        
        return {
            "id": mountain_id,
            "name": mountain['name'],
            "location": {
                "prefecture": prefecture,
                "region": region,
                "latitude": None,  # 手動更新必要
                "longitude": None,  # 手動更新必要
                "nearest_station": None,  # 手動更新必要
                "access_time": None  # 手動更新必要
            },
            "elevation": mountain['elevation'],
            "difficulty": {
                "level": "初級",
                "hiking_time": None,  # 手動更新必要
                "distance": None  # 手動更新必要
            },
            "description": f"{mountain['name']}は{prefecture}にある標高{mountain['elevation']}mの低山です。山と溪谷編集部選定の日本百低山の一つとして選ばれており、登山初心者にも親しまれています。",
            "features": [],  # 手動更新必要
            "seasons": {
                "cherry_blossom": None,  # 手動更新必要
                "autumn_leaves": None   # 手動更新必要
            },
            "keywords": [mountain['name'], prefecture, "低山", "初心者向け", "日帰り登山"],
            "article_themes": ["初心者におすすめの低山", "日帰りハイキング", f"{region}地方の山歩き"],
            "yamatokaikoku_reference": {
                "source": "山と溪谷編集部選定 日本百低山",
                "description": f"山と溪谷編集部が選定した日本百低山の一つ。標高{mountain['elevation']}mで日帰り登山が可能な魅力的な山として紹介されています。",
                "url": "https://www.yamakei.co.jp/yk/article/hyakuteizan",
                "source_line": mountain['source_line']
            }
        }
    
    def integrate_data(self):
        """データを統合"""
        print("🔄 山と溪谷データベース統合開始")
        
        # データ読み込み
        source_data = self.load_source_data()
        database = self.load_database()
        
        new_mountains = []
        skipped_count = 0
        
        # 既存の山名リストを作成
        existing_names = [mountain['name'] for mountain in database['mountains']]
        
        for mountain in source_data['extracted_mountains']:
            if mountain['name'] in existing_names:
                print(f"🔄 SKIP: {mountain['name']} - 既存データに存在")
                skipped_count += 1
                continue
                
            full_mountain_data = self.convert_to_full_mountain_data(mountain)
            new_mountains.append(full_mountain_data)
            print(f"🔄 ADD: {mountain['name']} ({mountain['prefecture']}, {mountain['elevation']}m)")
        
        # データベース更新
        if new_mountains:
            database['mountains'].extend(new_mountains)
            
            # メタデータ更新
            database['metadata']['total_mountains'] = len(database['mountains'])
            database['metadata']['last_updated'] = datetime.now().isoformat()
            version_parts = database['metadata']['version'].split('.')
            version_parts[-1] = str(int(version_parts[-1]) + 1)
            database['metadata']['version'] = '.'.join(version_parts)
            # sources フィールドがない場合は追加
            if 'sources' not in database['metadata']:
                database['metadata']['sources'] = []
            database['metadata']['sources'].append("山と溪谷編集部選定 日本百低山")
            
            # データベース保存
            with open(self.database_file, 'w', encoding='utf-8') as f:
                json.dump(database, f, ensure_ascii=False, indent=2)
                
            print(f"🔄 SAVE: データベース更新完了 (v{database['metadata']['version']})")
        
        # 結果サマリー
        print("\n" + "="*50)
        print("🏔️ 山と溪谷データベース統合結果")
        print("="*50)
        print(f"✅ 成功")
        print(f"📊 処理された山: {len(source_data['extracted_mountains'])}山")
        print(f"🆕 新規追加: {len(new_mountains)}山")
        print(f"⏭️ スキップ: {skipped_count}山")
        print(f"📄 データベース総山数: {database['metadata']['total_mountains']}山")
        print("="*50)

if __name__ == "__main__":
    integrator = YamatoKaikokuIntegrator()
    integrator.integrate_data()