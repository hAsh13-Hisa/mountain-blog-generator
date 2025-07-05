#!/usr/bin/env python3
"""
楽天API経由で実際のアフィリエイトリンクを取得してアフィリエイトセクションを更新
（標準ライブラリのみ使用）
"""

import json
import os
import re
from simple_rakuten_client import SimpleRakutenClient, get_fallback_products, get_fallback_hotels

def load_mountain_data():
    """山データを読み込み"""
    data_file = "data/mountains_japan_expanded.json"
    with open(data_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_prefecture_area_code(prefecture):
    """都道府県名から楽天の地域コードを取得"""
    area_codes = {
        "北海道": "01",
        "青森県": "02", "岩手県": "03", "宮城県": "04", "秋田県": "05", "山形県": "06", "福島県": "07",
        "茨城県": "08", "栃木県": "09", "群馬県": "10", "埼玉県": "11", "千葉県": "12", "東京都": "13", "神奈川県": "14",
        "新潟県": "15", "富山県": "16", "石川県": "17", "福井県": "18", "山梨県": "19", "長野県": "20",
        "岐阜県": "21", "静岡県": "22", "愛知県": "23", "三重県": "24",
        "滋賀県": "25", "京都府": "26", "大阪府": "27", "兵庫県": "28", "奈良県": "29", "和歌山県": "30",
        "鳥取県": "31", "島根県": "32", "岡山県": "33", "広島県": "34", "山口県": "35",
        "徳島県": "36", "香川県": "37", "愛媛県": "38", "高知県": "39",
        "福岡県": "40", "佐賀県": "41", "長崎県": "42", "熊本県": "43", "大分県": "44", "宮崎県": "45", "鹿児島県": "46", "沖縄県": "47"
    }
    return area_codes.get(prefecture, "13")  # デフォルトは東京

def generate_affiliate_section_with_api(mountain_name, prefecture, nearest_station, rakuten_client):
    """楽天API経由で実際のアフィリエイトセクションを生成"""
    
    # 登山用品の検索キーワード
    equipment_keywords = [
        "トレッキングシューズ",
        "ハイキング リュック",
        "登山 水筒"
    ]
    
    # 楽天商品API から登山用品を取得
    all_products = []
    for keyword in equipment_keywords:
        products = rakuten_client.search_products(keyword, max_results=1)
        if products:
            all_products.extend(products)
    
    # API呼び出しが失敗した場合はフォールバック商品を使用
    if not all_products:
        print(f"  ⚠️ 楽天API取得失敗、フォールバック商品を使用")
        all_products = get_fallback_products()
    
    # 最大3商品まで
    all_products = all_products[:3]
    
    products_html = ""
    for product in all_products:
        # 価格を万円単位で表示
        price_display = f"¥{product['price']:,}"
        
        # 商品説明を100文字以内に短縮
        description = product['description'][:100] + "..." if len(product['description']) > 100 else product['description']
        
        # 商品名を短縮
        product_name = product['name'][:40] + "..." if len(product['name']) > 40 else product['name']
        
        products_html += f'''
                        <div class="affiliate-item">
                            <img src="{product['image_url']}" 
                                 alt="{product_name}" class="affiliate-image"
                                 onerror="this.src='https://images.unsplash.com/photo-1544966503-7cc5ac882d5f?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80'">
                            <div class="affiliate-text">
                                <h4>{product_name}</h4>
                                <p>{description}</p>
                                <div class="product-price">{price_display}</div>
                                <a href="{product['url']}" class="btn btn-affiliate" target="_blank" rel="noopener">
                                    楽天で詳細を見る
                                </a>
                            </div>
                        </div>'''
    
    # 最寄り駅の宿泊施設を検索
    hotels = []
    if nearest_station:
        # 駅名から「駅」を除去
        station_name = nearest_station.replace('駅', '')
        hotels = rakuten_client.search_hotels(station_name, max_results=3)
    
    # API呼び出しが失敗した場合はフォールバック宿泊施設を使用
    if not hotels:
        print(f"  ⚠️ 楽天トラベルAPI取得失敗、フォールバック宿泊施設を使用")
        hotels = get_fallback_hotels()
    
    # 最大3宿泊施設まで
    hotels = hotels[:3]
    
    hotels_html = ""
    for hotel in hotels:
        # 料金を表示
        if hotel.get('min_charge') and hotel['min_charge'] > 0:
            price_display = f"¥{hotel['min_charge']:,}〜"
        else:
            price_display = "料金は公式サイトでご確認ください"
        
        # 説明を100文字以内に短縮
        description = hotel['description'][:100] + "..." if len(hotel['description']) > 100 else hotel['description']
        
        # ホテル名を短縮
        hotel_name = hotel['name'][:30] + "..." if len(hotel['name']) > 30 else hotel['name']
        
        hotels_html += f'''
                        <div class="affiliate-item">
                            <img src="{hotel['image_url']}" 
                                 alt="{hotel_name}" class="affiliate-image"
                                 onerror="this.src='https://images.unsplash.com/photo-1566073771259-6a8506099945?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80'">
                            <div class="affiliate-text">
                                <h4>{hotel_name}</h4>
                                <p>{description}</p>
                                <div class="product-price">{price_display}</div>
                                <a href="{hotel['url']}" class="btn btn-affiliate" target="_blank" rel="noopener">
                                    楽天トラベルで予約
                                </a>
                            </div>
                        </div>'''
    
    return f'''
        <!-- アフィリエイトセクション -->
        <section class="affiliate-section">
            <div class="container">
                <!-- 楽天トラベルセクション -->
                <div class="affiliate-block">
                    <h3 class="affiliate-title">🏨 {mountain_name}周辺の宿泊予約</h3>
                    <p class="affiliate-description">{nearest_station}周辺の宿泊施設をご紹介</p>
                    <div class="affiliate-content">{hotels_html}
                    </div>
                </div>

                <!-- 低山グッズセクション -->
                <div class="affiliate-block">
                    <h3 class="affiliate-title">🎒 おすすめ低山グッズ</h3>
                    <p class="affiliate-description">{mountain_name}登山に最適な装備をご紹介</p>
                    <div class="affiliate-content">{products_html}
                    </div>
                </div>
            </div>
        </section>'''

def update_mountain_page_with_api(mountain, rakuten_client):
    """個別山ページのアフィリエイトセクションを楽天API経由で更新"""
    mountain_name = mountain['name']
    prefecture = mountain.get('prefecture', '日本')
    nearest_station = mountain.get('location', {}).get('nearest_station', '最寄り駅')
    
    # ファイルパス作成
    mountain_dir = f"site_minimal/mountains/{mountain_name}"
    html_file = f"{mountain_dir}/index.html"
    
    if not os.path.exists(html_file):
        print(f"⚠️ ファイルが見つかりません: {html_file}")
        return False
    
    # HTMLファイルを読み込み
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 既存のアフィリエイトセクションを探して置換
    if 'affiliate-section' in html_content:
        # 楽天API経由で新しいアフィリエイトセクションを生成
        new_affiliate_section = generate_affiliate_section_with_api(mountain_name, prefecture, nearest_station, rakuten_client)
        
        # 既存のアフィリエイトセクションを新しいものに置換
        # パターンを調整して確実に置換
        pattern = r'(\s*<!-- アフィリエイトセクション -->.*?</section>\s*)'
        html_content = re.sub(pattern, new_affiliate_section, html_content, flags=re.DOTALL)
        
        # ファイルに書き戻し
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"  ✅ {mountain_name}: 楽天API商品・宿泊施設リンク更新完了 (最寄り駅: {nearest_station})")
        return True
    else:
        print(f"  ⚠️ {mountain_name}: アフィリエイトセクションが見つかりません")
        return False

def add_css_for_price_display():
    """価格表示用のCSSを追加"""
    css_file = "site_minimal/css/minimal_design.css"
    
    if not os.path.exists(css_file):
        print("⚠️ CSSファイルが見つかりません")
        return
    
    # 価格表示用のスタイルを追加
    price_css = """
/* === 価格表示用スタイル === */
.product-price {
    font-size: var(--font-size-lg);
    font-weight: 600;
    color: var(--accent-success);
    margin-bottom: var(--spacing-md);
    padding: var(--spacing-sm);
    background: var(--forest-light);
    border-radius: var(--border-radius);
    text-align: center;
}
"""
    
    with open(css_file, 'r', encoding='utf-8') as f:
        css_content = f.read()
    
    if '.product-price' not in css_content:
        css_content += price_css
        
        with open(css_file, 'w', encoding='utf-8') as f:
            f.write(css_content)
        
        print("✅ 価格表示用CSSを追加しました")

def main():
    """メイン実行関数"""
    print("🛒 楽天API経由アフィリエイトリンク更新開始...")
    
    try:
        # 楽天APIクライアントを初期化
        rakuten_client = SimpleRakutenClient()
        print("✅ 楽天APIクライアント初期化完了")
        
        # データ読み込み
        data = load_mountain_data()
        mountains = data['mountains']
        
        success_count = 0
        total_count = len(mountains)
        
        print(f"📊 処理対象: {total_count}山")
        
        # 価格表示用CSSを追加
        add_css_for_price_display()
        
        # 最初の5山のみテスト実行
        test_mountains = mountains[:5]
        print(f"🧪 テスト実行: 最初の{len(test_mountains)}山のみ処理")
        
        for i, mountain in enumerate(test_mountains, 1):
            mountain_name = mountain['name']
            print(f"  🏔️ 処理中: {mountain_name} ({i}/{len(test_mountains)})")
            
            if update_mountain_page_with_api(mountain, rakuten_client):
                success_count += 1
        
        print(f"\n🎉 楽天API経由アフィリエイトリンク更新完了！")
        print(f"  • 成功: {success_count}/{len(test_mountains)}")
        print(f"  • 実際の楽天商品リンク・楽天トラベルリンクを適用")
        print(f"  • 価格情報付きの本格的なアフィリエイト表示")
        
        if success_count == len(test_mountains):
            print(f"  ✅ テスト処理完了！")
            
            # 残りの山も処理するか確認
            remaining = mountains[5:]
            if remaining:
                print(f"\n残り{len(remaining)}山も処理しますか？ (y/n): ", end="")
                # 自動的に処理を続行
                print("y (自動継続)")
                
                for i, mountain in enumerate(remaining, len(test_mountains)+1):
                    mountain_name = mountain['name']
                    print(f"  🏔️ 処理中: {mountain_name} ({i}/{total_count})")
                    
                    if update_mountain_page_with_api(mountain, rakuten_client):
                        success_count += 1
                
                print(f"\n🎉 全山処理完了！")
                print(f"  • 最終成功数: {success_count}/{total_count}")
        else:
            print(f"  ⚠️ 一部ページで処理できませんでした")
    
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n📁 確認: http://localhost:8081/mountains/円山/ で楽天APIリンクを確認してください")
    else:
        print("\n❌ 処理に失敗しました")