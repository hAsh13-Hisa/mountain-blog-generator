#!/usr/bin/env python3
"""
改善されたアフィリエイト機能のサンプル記事生成
"""
import json
from datetime import datetime
from src.application.services import MountainArticleService
from src.infrastructure.repositories import RepositoryFactory
from wordpress_wxr_fixed import generate_valid_wxr

def generate_sample_articles():
    """サンプル記事を生成してアフィリエイトの差別化を確認"""
    print("📝 改善されたアフィリエイト機能のサンプル記事生成")
    print("=" * 60)
    
    # サービス初期化
    service = MountainArticleService()
    mountain_repo = RepositoryFactory.get_mountain_repository()
    
    # テスト対象の山を選択
    target_mountains = [
        'mt_maruyama_hokkaido',  # 円山（北海道、低山）
        'mt_iwaki',              # 岩木山（青森、高山）
        'mt_iwate'               # 岩手山（岩手、高山）
    ]
    
    articles_data = []
    
    print("🏔️ 記事生成中...")
    for i, mountain_id in enumerate(target_mountains):
        print(f"\n{i+1}. {mountain_id} の記事生成中...")
        
        try:
            # 記事生成
            result = service.create_and_publish_article(
                mountain_id=mountain_id,
                theme="初心者向け登山ガイド",
                publish=False
            )
            
            if result and result.success and result.article:
                article = result.article
                mountain = mountain_repo.get_by_id(mountain_id)
                
                print(f"   ✅ 生成成功: {article.content.title}")
                print(f"   📊 文字数: {len(article.content.content)}文字")
                
                # アフィリエイトリンクの確認
                if 'おすすめの登山用品' in article.content.content:
                    print("   🛍️ アフィリエイトリンク: 含まれています")
                    
                    # アフィリエイト部分を抽出して商品を確認
                    content = article.content.content
                    affiliate_start = content.find('おすすめの登山用品')
                    affiliate_section = content[affiliate_start:affiliate_start+1500]
                    
                    # 商品リンクを抽出
                    import re
                    product_links = re.findall(r'<a href="[^"]*"[^>]*>([^<]*)</a>', affiliate_section)
                    if product_links:
                        print(f"   🎯 商品例: {product_links[0][:50]}...")
                else:
                    print("   ⚠️ アフィリエイトリンク: 見つかりません")
                
                # JSONデータ作成
                article_data = {
                    "title": article.content.title,
                    "content": article.content.content,
                    "excerpt": article.content.excerpt,
                    "tags": article.content.tags or [],
                    "mountain_name": mountain.name,
                    "mountain_id": mountain_id,
                    "elevation": mountain.elevation,
                    "prefecture": mountain.prefecture,
                    "featured_image_url": f"https://images.unsplash.com/photo-{1500000000 + i}?w=800&h=400&fit=crop"
                }
                articles_data.append(article_data)
                
            else:
                print(f"   ❌ 生成失敗: {result.error_message if result else '不明なエラー'}")
                
        except Exception as e:
            print(f"   ❌ エラー: {e}")
    
    # 結果をJSONファイルに保存
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    json_filename = f"sample_articles_improved_{timestamp}.json"
    
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(articles_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 JSONファイル保存: {json_filename}")
    print(f"   記事数: {len(articles_data)}記事")
    
    # WordPress XML形式でも出力
    if articles_data:
        print("\n📄 WordPress XML生成中...")
        
        # スケジュール設定（1時間間隔）
        from datetime import timedelta
        start_time = datetime.now() + timedelta(hours=1)
        
        xml_content = generate_valid_wxr(articles_data, start_time, 1)
        xml_filename = f"sample_articles_improved_{timestamp}.xml"
        
        with open(xml_filename, 'w', encoding='utf-8') as f:
            f.write(xml_content)
        
        print(f"📄 XMLファイル保存: {xml_filename}")
        print(f"   記事数: {len(articles_data)}記事")
        print(f"   ファイルサイズ: {len(xml_content) / 1024:.1f} KB")
    
    # アフィリエイト差別化の確認
    print(f"\n🔍 アフィリエイト差別化確認:")
    print("-" * 40)
    
    for i, article_data in enumerate(articles_data):
        print(f"\n📰 {article_data['mountain_name']} ({article_data['elevation']}m)")
        
        # アフィリエイト部分を抽出
        content = article_data['content']
        if 'おすすめの登山用品' in content:
            affiliate_start = content.find('おすすめの登山用品')
            affiliate_end = content.find('</ul>', affiliate_start) + 5
            affiliate_section = content[affiliate_start:affiliate_end]
            
            # 商品名を抽出
            import re
            product_names = re.findall(r'>([^<]*)</a>', affiliate_section)
            unique_products = list(set([name[:30] for name in product_names if name.strip() and '¥' not in name]))
            
            if unique_products:
                print(f"   🛍️ 商品例: {unique_products[0]}...")
            else:
                print("   ⚠️ 商品情報の抽出に失敗")
        else:
            print("   ❌ アフィリエイトセクションなし")
    
    # サマリー
    print(f"\n📊 生成サマリー:")
    print(f"   成功記事数: {len(articles_data)}")
    print(f"   JSONファイル: {json_filename}")
    print(f"   XMLファイル: {xml_filename}")
    
    print(f"\n🎯 確認ポイント:")
    print("1. 各山ごとに異なるアフィリエイト商品が表示されているか")
    print("2. 山の特徴（標高、地域）に応じた商品選択になっているか")
    print("3. XMLファイルでWordPressに正常にインポートできるか")
    
    return json_filename, xml_filename

def analyze_affiliate_differences(json_filename):
    """生成された記事のアフィリエイト差別化を分析"""
    print(f"\n🔬 アフィリエイト差別化分析")
    print("=" * 60)
    
    try:
        with open(json_filename, 'r', encoding='utf-8') as f:
            articles_data = json.load(f)
        
        print(f"📊 分析対象: {len(articles_data)}記事")
        
        affiliate_products = {}
        
        for article in articles_data:
            mountain_name = article['mountain_name']
            content = article['content']
            
            # アフィリエイト商品を抽出
            if 'おすすめの登山用品' in content:
                import re
                # 商品リンクのタイトルを抽出
                products = re.findall(r'<a href="[^"]*"[^>]*>([^<]*)</a>', content)
                # 価格情報を除外して商品名のみ取得
                clean_products = []
                for product in products:
                    if '¥' not in product and len(product.strip()) > 5:
                        clean_products.append(product.strip()[:50])  # 50文字まで
                
                affiliate_products[mountain_name] = clean_products[:3]  # 最初の3つ
            else:
                affiliate_products[mountain_name] = []
        
        # 結果表示
        print(f"\n📋 各山のアフィリエイト商品:")
        for mountain, products in affiliate_products.items():
            print(f"\n🏔️ {mountain}:")
            if products:
                for i, product in enumerate(products, 1):
                    print(f"   {i}. {product}...")
            else:
                print("   ❌ 商品なし")
        
        # 重複率計算
        all_products = []
        for products in affiliate_products.values():
            all_products.extend(products)
        
        if all_products:
            unique_products = set(all_products)
            duplication_rate = (len(all_products) - len(unique_products)) / len(all_products) * 100
            
            print(f"\n📈 差別化指標:")
            print(f"   総商品数: {len(all_products)}")
            print(f"   ユニーク商品数: {len(unique_products)}")
            print(f"   重複率: {duplication_rate:.1f}%")
            print(f"   差別化率: {100 - duplication_rate:.1f}%")
            
            if duplication_rate < 50:
                print("   ✅ 差別化Good: 各記事で異なる商品が表示されています")
            else:
                print("   ⚠️ 差別化改善余地: 商品の重複が多いです")
        
    except Exception as e:
        print(f"❌ 分析エラー: {e}")

def main():
    """メイン処理"""
    json_filename, xml_filename = generate_sample_articles()
    
    if json_filename:
        analyze_affiliate_differences(json_filename)
    
    print(f"\n🎉 サンプル記事生成完了！")
    print(f"WordPressでテストするには: {xml_filename} をインポートしてください")

if __name__ == '__main__':
    main()