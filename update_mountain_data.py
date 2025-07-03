#!/usr/bin/env python3
"""
BE-PAL記事から抽出した新しい山データを既存データベースに統合
"""
import json
from datetime import datetime

def merge_mountain_data():
    """BE-PAL記事の山データを既存データベースにマージ"""
    
    # 既存データ読み込み
    with open('data/mountains_japan_expanded.json', 'r', encoding='utf-8') as f:
        existing_data = json.load(f)
    
    # 新規追加データ読み込み
    with open('data/mountains_bepal_additions.json', 'r', encoding='utf-8') as f:
        new_data = json.load(f)
    
    # 新しい山データを既存リストに追加
    for new_mountain in new_data['new_mountains']:
        existing_data['mountains'].append(new_mountain)
    
    # メタデータ更新
    existing_data['metadata']['version'] = "5.0"
    existing_data['metadata']['last_updated'] = datetime.now().strftime("%Y-%m-%d")
    existing_data['metadata']['total_mountains'] = len(existing_data['mountains'])
    existing_data['metadata']['description'] = "日本全国の低山マスターデータ（標高400m以下・登山道整備済み）+ BE-PAL記事追加分"
    
    # 地域別山リスト更新
    region_mountains = {
        "北海道": [],
        "東北": [],
        "関東": [],
        "中部": [],
        "関西": [],
        "中国": [],
        "四国": [],
        "九州": []
    }
    
    # 都道府県別山リスト更新
    prefecture_mountains = {}
    
    # 各山を地域・都道府県別に分類
    for mountain in existing_data['mountains']:
        region = mountain['region']
        prefecture = mountain['prefecture']
        mountain_id = mountain['id']
        
        if region in region_mountains:
            region_mountains[region].append(mountain_id)
        
        if prefecture not in prefecture_mountains:
            prefecture_mountains[prefecture] = []
        prefecture_mountains[prefecture].append(mountain_id)
    
    # 地域情報更新
    existing_data['regions']['北海道']['mountains'] = region_mountains['北海道']
    existing_data['regions']['東北']['mountains'] = region_mountains['東北']
    existing_data['regions']['関東']['mountains'] = region_mountains['関東']
    existing_data['regions']['関東']['description'] = "首都圏からアクセス良好な多様な低山（神奈川県を中心に大幅拡充）"
    
    # 中国地域を新規追加
    existing_data['regions']['中国'] = {
        "description": "風光明媚な縦走路と地元に愛される里山",
        "mountains": region_mountains['中国'],
        "characteristics": ["縦走", "岩場", "鉄道風景", "吉井川", "里山", "地元愛"]
    }
    
    # 中部地域更新
    existing_data['regions']['中部']['mountains'] = region_mountains['中部']
    
    # 関西地域更新
    existing_data['regions']['関西']['mountains'] = region_mountains['関西']
    existing_data['regions']['関西']['description'] = "歴史と文化に彩られた親しみやすい山々（和歌山県の巨岩群を追加）"
    existing_data['regions']['関西']['characteristics'].extend(["巨岩群", "360度絶景", "みかん畑", "夜景"])
    
    # 四国地域更新
    existing_data['regions']['四国']['mountains'] = region_mountains['四国']
    
    # 九州地域更新
    existing_data['regions']['九州']['mountains'] = region_mountains['九州']
    existing_data['regions']['九州']['description'] = "夜景名所と歴史散策の山々（天草・大分の奇岩群を追加）"
    existing_data['regions']['九州']['characteristics'].extend(["奇岩", "断崖", "島の山", "岩峰群"])
    
    # 都道府県別データ更新
    existing_data['prefectures'] = prefecture_mountains
    
    # 検索タグ更新
    search_tags = existing_data['search_tags']
    
    # 新しいタグカテゴリ追加
    search_tags.update({
        "駅近": ["mt_ryogaisan_tochigi", "mt_kannariyama_gunma", "mt_azumayama_kanagawa", "mt_takatoriyama_kanagawa", "mt_wake_alps_okayama"],
        "縦走": ["mt_kannariyama_gunma", "mt_komayama_kanagawa", "mt_wake_alps_okayama"],
        "巨岩・奇岩": ["mt_takatoriyama_kanagawa", "mt_hikiiwagusa_wakayama", "mt_nakayamasenkyo_oita"],
        "磨崖仏": ["mt_takatoriyama_kanagawa"],
        "城跡": ["mt_ryogaisan_tochigi"],
        "三浦半島": ["mt_ogusuyama_kanagawa"],
        "湘南": ["mt_kinuhariyama_kanagawa", "mt_takatoriyama_kanagawa", "mt_komayama_kanagawa"],
        "鎌倉": ["mt_kinuhariyama_kanagawa"],
        "和歌山": ["mt_hikiiwagusa_wakayama", "mt_iwagamiyama_wakayama"],
        "天草": ["mt_jiromarudake_kumamoto"],
        "360度絶景": ["mt_hikiiwagusa_wakayama"],
        "みかん畑": ["mt_hikiiwagusa_wakayama"],
        "断崖絶壁": ["mt_jiromarudake_kumamoto"],
        "岩峰群": ["mt_nakayamasenkyo_oita"]
    })
    
    # 既存タグ更新
    search_tags["富士山展望"].extend(["mt_ryogaisan_tochigi", "mt_ogusuyama_kanagawa", "mt_komayama_kanagawa"])
    search_tags["家族向け"].extend(["mt_azumayama_kanagawa"])
    search_tags["手軽"].extend(["mt_kinuhariyama_kanagawa", "mt_azumayama_kanagawa", "mt_hikiiwagusa_wakayama"])
    search_tags["夜景"].extend(["mt_iwagamiyama_wakayama"])
    search_tags["歴史"].extend(["mt_ryogaisan_tochigi", "mt_kinuhariyama_kanagawa", "mt_komayama_kanagawa"])
    
    # 更新されたデータを保存
    with open('data/mountains_japan_expanded.json', 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 山データベース更新完了")
    print(f"📊 総山数: {len(existing_data['mountains'])}山")
    print(f"🗾 地域数: {len(existing_data['regions'])}地域")
    print(f"🏔️ 新規追加: {len(new_data['new_mountains'])}山")
    print(f"📅 更新日: {existing_data['metadata']['last_updated']}")
    
    # 地域別集計表示
    print("\n🌍 地域別山数:")
    for region, data in existing_data['regions'].items():
        print(f"  {region}: {len(data['mountains'])}山")
    
    # 新規追加山の詳細
    print("\n🆕 新規追加された山:")
    for mountain in new_data['new_mountains']:
        print(f"  • {mountain['name']} ({mountain['prefecture']}, {mountain['elevation']}m)")

if __name__ == "__main__":
    merge_mountain_data()