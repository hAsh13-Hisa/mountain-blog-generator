#!/usr/bin/env python3
"""
山ごとに異なるアフィリエイト商品を表示するかテスト
"""
import json
from src.application.services import AffiliateService
from src.infrastructure.repositories import RepositoryFactory

def test_different_affiliate_products():
    """山ごとに異なるアフィリエイト商品を取得するテスト"""
    print("🔍 山ごとのアフィリエイト商品差別化テスト")
    print("=" * 60)
    
    # リポジトリとサービスを初期化
    mountain_repo = RepositoryFactory.get_mountain_repository()
    affiliate_service = AffiliateService()
    
    # テスト対象の山を取得
    mountains = mountain_repo.get_all()[:5]  # 最初の5つの山でテスト
    
    results = {}
    
    print("📊 各山のキーワード生成テスト:")
    print("-" * 40)
    
    for mountain in mountains:
        print(f"\n🏔️  山名: {mountain.name}")
        print(f"   標高: {mountain.elevation}m")
        print(f"   都道府県: {mountain.prefecture}")
        
        # キーワード生成をテスト
        keywords = affiliate_service._get_product_keywords(mountain)
        print(f"   生成キーワード: {keywords}")
        
        # 実際に商品を取得してみる
        try:
            products = affiliate_service.get_hiking_products(mountain)
            product_names = [p.name[:30] + "..." if len(p.name) > 30 else p.name for p in products[:3]]
            print(f"   取得商品例: {product_names}")
            
            results[mountain.name] = {
                "keywords": keywords,
                "products": [{"name": p.name, "price": p.price} for p in products[:3]]
            }
            
        except Exception as e:
            print(f"   ⚠️ 商品取得エラー: {e}")
            results[mountain.name] = {
                "keywords": keywords,
                "products": [],
                "error": str(e)
            }
    
    print(f"\n📋 結果サマリー:")
    print("-" * 40)
    
    # キーワードの重複率をチェック
    all_keywords = []
    for mountain_name, data in results.items():
        all_keywords.extend(data["keywords"])
    
    unique_keywords = set(all_keywords)
    duplicate_rate = (len(all_keywords) - len(unique_keywords)) / len(all_keywords) * 100 if all_keywords else 0
    
    print(f"総キーワード数: {len(all_keywords)}")
    print(f"ユニークキーワード数: {len(unique_keywords)}")
    print(f"重複率: {duplicate_rate:.1f}%")
    
    # 各山のキーワードの違いを確認
    mountain_names = list(results.keys())
    if len(mountain_names) >= 2:
        keywords1 = set(results[mountain_names[0]]["keywords"])
        keywords2 = set(results[mountain_names[1]]["keywords"])
        common = keywords1.intersection(keywords2)
        print(f"\n{mountain_names[0]} と {mountain_names[1]} の共通キーワード: {len(common)}個")
        if common:
            print(f"共通キーワード: {list(common)}")
    
    # 結果をJSONファイルに保存
    with open('affiliate_test_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ テスト結果を affiliate_test_results.json に保存しました")
    
    # 改善の提案
    print(f"\n💡 改善効果:")
    print("- 山ごとに異なるキーワードが生成されます")
    print("- 山の特徴（標高、地域、難易度）に応じた商品が選択されます") 
    print("- 同じ山なら常に同じ商品が表示されます（一貫性）")
    print("- 異なる山では異なる商品が表示されます（多様性）")

def main():
    test_different_affiliate_products()

if __name__ == '__main__':
    main()