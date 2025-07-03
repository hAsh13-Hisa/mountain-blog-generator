#!/usr/bin/env python3
"""
テスト用記事を生成
"""
import json
import hashlib
from datetime import datetime

# テスト用の山リスト
test_mountains = [
    {
        "name": "高尾山",
        "id": "mt_takao",
        "elevation": 599,
        "prefecture": "東京都"
    },
    {
        "name": "筑波山",
        "id": "mt_tsukuba_ibaraki",
        "elevation": 877,
        "prefecture": "茨城県"
    },
    {
        "name": "函館山",
        "id": "mt_hakodate_hokkaido",
        "elevation": 334,
        "prefecture": "北海道"
    },
    {
        "name": "円山",
        "id": "mt_maruyama_hokkaido",
        "elevation": 225,
        "prefecture": "北海道"
    },
    {
        "name": "讃岐富士",
        "id": "mt_sanuki_kagawa",
        "elevation": 422,
        "prefecture": "香川県"
    }
]

# 画像URLリスト
image_urls = [
    "https://images.unsplash.com/photo-1506905925346-21bda4d32df4",
    "https://images.unsplash.com/photo-1464822759844-d150ad6d0e12",
    "https://images.unsplash.com/photo-1551632811-561732d1e306",
    "https://images.unsplash.com/photo-1506197603052-3cc9c3a201bd",
    "https://images.unsplash.com/photo-1578662996442-48f60103fc96",
    "https://images.unsplash.com/photo-1519904981063-b0cf448d479e",
    "https://images.unsplash.com/photo-1483728642387-6c3bdd6c93e5",
    "https://images.unsplash.com/photo-1544558635-667480601430",
    "https://images.unsplash.com/photo-1524712245354-2c4e5e7121c0",
    "https://images.unsplash.com/photo-1516655855035-d5215bcb5604"
]

# 各山の記事を生成
for mountain in test_mountains:
    article = {
        "mountain_name": mountain["name"],
        "mountain_id": mountain["id"],
        "elevation": mountain["elevation"],
        "prefecture": mountain["prefecture"],
        "title": f"【{mountain['name']}完全ガイド】初心者向け登山コース",
        "excerpt": f"{mountain['name']}は{mountain['prefecture']}の人気の山。初心者でも安心して登れます。",
        "content": f"<h2>{mountain['name']}の魅力</h2><p>{mountain['name']}は標高{mountain['elevation']}mの低山です。</p>",
        "tags": [mountain['name'], mountain['prefecture'], "初心者登山"],
        "featured_image_url": image_urls[int(hashlib.md5(mountain['id'].encode()).hexdigest(), 16) % len(image_urls)],
        "featured_image_alt": f"{mountain['name']} 登山風景",
        "products_count": 5,
        "created_at": datetime.now().isoformat()
    }
    
    filename = f"article_{mountain['name']}_{datetime.now().strftime('%Y%m%d')}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(article, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 生成: {filename}")

print("\n📝 記事生成完了！")