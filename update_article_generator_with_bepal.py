#!/usr/bin/env python3
"""
記事生成システムにBE-PAL記事の参考情報を統合
"""
import json
from pathlib import Path

def integrate_bepal_references():
    """BE-PAL記事情報を山データベースに統合"""
    
    # 既存の山データ読み込み
    with open('data/mountains_japan_expanded.json', 'r', encoding='utf-8') as f:
        mountains_data = json.load(f)
    
    # BE-PAL記事参考情報読み込み
    with open('data/bepal_article_references.json', 'r', encoding='utf-8') as f:
        bepal_data = json.load(f)
    
    # BE-PAL記事を山IDでインデックス化
    bepal_by_id = {}
    for article in bepal_data['mountain_articles']:
        bepal_by_id[article['mountain_id']] = article['bepal_article']
    
    # 各山データにBE-PAL記事情報を追加
    updated_count = 0
    for mountain in mountains_data['mountains']:
        mountain_id = mountain['id']
        if mountain_id in bepal_by_id:
            mountain['bepal_reference'] = bepal_by_id[mountain_id]
            updated_count += 1
    
    # メタデータ更新
    mountains_data['metadata']['version'] = "5.1"
    mountains_data['metadata']['last_updated'] = "2025-06-30"
    mountains_data['metadata']['bepal_integration'] = {
        "status": "integrated",
        "updated_mountains": updated_count,
        "source": "BE-PAL記事「全国のおすすめ低山58選！登山初心者も楽しめる人気の山を紹介」",
        "url": "https://www.bepal.net/archives/536937",
        "copyright_notice": "BE-PAL記事内容の引用時は出典を明記すること"
    }
    
    # 更新されたデータを保存
    with open('data/mountains_japan_expanded.json', 'w', encoding='utf-8') as f:
        json.dump(mountains_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ BE-PAL記事参考情報の統合完了")
    print(f"📊 統合された山: {updated_count}山")
    print(f"📚 参考情報: 専門家コメント、詳細説明、参考記事タイトル")
    print(f"⚖️ 著作権: 引用時は出典明記が必要")
    
    return updated_count

def create_article_generation_template():
    """記事生成時のBE-PAL参考情報活用テンプレート作成"""
    
    template = """
# BE-PAL記事参考情報の活用方法

## 記事生成時の参照手順

1. **山データ取得時に確認**
   ```python
   if 'bepal_reference' in mountain_data:
       bepal_info = mountain_data['bepal_reference']
       description = bepal_info['description']
       expert_comment = bepal_info.get('expert_comment')
       expert_name = bepal_info.get('expert_name')
   ```

2. **記事本文での活用**
   - BE-PAL記事の説明を参考にして、より詳細で魅力的な山の紹介文を作成
   - 専門家コメントがある場合は、その視点を取り入れた記事構成
   - 特徴的なポイント（眺望、花、歴史など）を重点的に紹介

3. **出典明記（必須）**
   記事末尾に以下の出典情報を必ず記載：
   ```
   【参考文献】
   BE-PAL「全国のおすすめ低山58選！登山初心者も楽しめる人気の山を紹介」
   https://www.bepal.net/archives/536937
   ```

## 活用例

### 神成山の場合
**BE-PAL情報:**
- 「龍の背のような九連峰」
- 「日本一のハイキングコース」
- 「上信電鉄の懐かしい風景」

**記事での活用:**
→ これらの特徴を詳しく解説し、実際の登山体験として描写

### 専門家コメント活用例
四角友里さんのコメント「山と街が近い鎌倉。衣張山からは...」
→ この表現を参考に、鎌倉の山と海の魅力を具体的に紹介

## 注意事項
- 直接的な引用は最小限に留める
- BE-PAL記事を「参考」として、オリジナルの表現で記事を作成
- 必ず出典を明記する
- 専門家のコメントは「〜という専門家の指摘もあります」として間接的に活用
"""
    
    with open('BEPAL_REFERENCE_GUIDE.md', 'w', encoding='utf-8') as f:
        f.write(template)
    
    print(f"📝 BE-PAL参考情報活用ガイドを作成: BEPAL_REFERENCE_GUIDE.md")

if __name__ == "__main__":
    updated_count = integrate_bepal_references()
    create_article_generation_template()
    
    print(f"\n🎯 次のステップ:")
    print(f"1. 記事生成時にbepal_referenceフィールドを参照")
    print(f"2. 出典明記を忘れずに記載")
    print(f"3. BE-PALの表現を参考にしたオリジナル記事作成")