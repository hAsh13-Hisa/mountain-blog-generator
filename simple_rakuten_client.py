#!/usr/bin/env python3
"""
シンプルな楽天APIクライアント（標準ライブラリのみ使用）
"""

import json
import urllib.request
import urllib.parse
import urllib.error
from typing import List, Dict, Any

class SimpleRakutenClient:
    """シンプルな楽天APIクライアント"""
    
    def __init__(self):
        # .envファイルから設定を読み込み
        self.app_id = "1099421053709374278"
        self.affiliate_id = "139b96cc.29d2cd62.139b96cd.e6b1673a"
        self.base_url = "https://app.rakuten.co.jp/services/api"
    
    def search_products(self, keyword: str, max_results: int = 3) -> List[Dict[str, Any]]:
        """商品を検索"""
        try:
            params = {
                'applicationId': self.app_id,
                'affiliateId': self.affiliate_id,
                'keyword': keyword,
                'hits': max_results,
                'minPrice': 1000,
                'maxPrice': 50000,
                'sort': 'standard',
                'format': 'json'
            }
            
            url = f"{self.base_url}/IchibaItem/Search/20170706"
            query_string = urllib.parse.urlencode(params)
            full_url = f"{url}?{query_string}"
            
            print(f"  🔍 楽天API呼び出し: {keyword}")
            
            with urllib.request.urlopen(full_url, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))
            
            products = []
            for item in data.get('Items', []):
                item_data = item['Item']
                
                product = {
                    'name': item_data['itemName'],
                    'price': int(item_data['itemPrice']),
                    'url': item_data['affiliateUrl'],
                    'image_url': item_data['mediumImageUrls'][0]['imageUrl'] if item_data.get('mediumImageUrls') else '',
                    'description': item_data.get('itemCaption', '')[:150],
                    'shop_name': item_data.get('shopName', '')
                }
                products.append(product)
            
            print(f"    ✅ {len(products)}件の商品を取得")
            return products
            
        except Exception as e:
            print(f"    ⚠️ 楽天API呼び出しエラー: {e}")
            return []
    
    def search_hotels(self, station_name: str, max_results: int = 3) -> List[Dict[str, Any]]:
        """最寄り駅名で宿泊施設を検索"""
        try:
            params = {
                'applicationId': self.app_id,
                'affiliateId': self.affiliate_id,
                'keyword': f"{station_name} ホテル",
                'hits': max_results,
                'sort': 'standard',
                'format': 'json'
            }
            
            url = f"{self.base_url}/Travel/SimpleHotelSearch/20170426"
            query_string = urllib.parse.urlencode(params)
            full_url = f"{url}?{query_string}"
            
            print(f"  🏨 楽天トラベル検索: {station_name}")
            
            with urllib.request.urlopen(full_url, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))
            
            hotels = []
            for item in data.get('hotels', []):
                hotel_data = item[0]['hotel'][0]
                
                # 直接予約URLを生成（楽天トラベルの実際の予約ページ）
                hotel_no = hotel_data.get('hotelNo', '')
                booking_url = f"https://travel.rakuten.co.jp/HOTEL/{hotel_no}/{hotel_no}.html?f_tn=1&f_camp_id={self.affiliate_id}"
                
                hotel = {
                    'name': hotel_data['hotelName'],
                    'url': booking_url,  # 直接予約URLに変更
                    'image_url': hotel_data.get('hotelThumbnailUrl', ''),
                    'description': hotel_data.get('hotelSpecial', '')[:100],
                    'location': hotel_data.get('address1', '') + hotel_data.get('address2', ''),
                    'min_charge': hotel_data.get('hotelMinCharge', 0)
                }
                hotels.append(hotel)
            
            print(f"    ✅ {len(hotels)}件のホテルを取得")
            return hotels
            
        except Exception as e:
            print(f"    ⚠️ 楽天トラベル検索エラー: {e}")
            return []

def get_fallback_products():
    """フォールバック用の固定商品データ（実際の楽天商品リンク）"""
    return [
        {
            'name': 'トレッキングシューズ ドイツの撥水・防汚の技術を使用 登山靴 防水 スニーカー ...',
            'price': 4680,
            'url': 'https://hb.afl.rakuten.co.jp/hgc/g00q2ud5.fuu30885.g00q2ud5.fuu31a6d/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fvanilla-vague%2Fladshoes004%2F&m=http%3A%2F%2Fm.rakuten.co.jp%2Fvanilla-vague%2Fi%2F10522079%2F&rafcid=wsc_i_is_1099421053709374278',
            'image_url': 'https://thumbnail.image.rakuten.co.jp/@0_gold/vanilla-vague/images/thumb/ladshoes004-thum740-001.jpg?_ex=128x128',
            'description': 'メーカー希望小売価格はメーカーサイトに基づいて掲載しています※概要はキャンペーンページをご確認ください。LAD WEATHER ドイツの撥水・防汚の技術を使用 防水トレッキングシューズ ladshoe...',
            'shop_name': 'vanilla vague'
        },
        {
            'name': '【ポイント10倍】QUECHUA ケシュア 登山 ハイキング 普段使い バックパ...',
            'price': 3990,
            'url': 'https://hb.afl.rakuten.co.jp/hgc/g00u1zy5.fuu306b0.g00u1zy5.fuu31365/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fdecathlon-japan%2F4287298535504%2F&m=http%3A%2F%2Fm.rakuten.co.jp%2Fdecathlon-japan%2Fi%2F10002656%2F&rafcid=wsc_i_is_1099421053709374278',
            'image_url': 'https://thumbnail.image.rakuten.co.jp/@0_mall/decathlon-japan/cabinet/thumb250704/4287298535504_thumb.jpg?_ex=128x128',
            'description': '※ブラックカラー（モデルコード: 8529024）は、商品デザインの変更により、お届けされる製品は動画や画像とロゴや細部デザインが異なる場合がございます。 晴れた日の低地、森林、海岸などへの2時間ほど...',
            'shop_name': 'Decathlon Japan 楽天市場店'
        },
        {
            'name': '【SALE Max20%OFF】【全23色】ナルゲン 広口1.0L トライタンリ...',
            'price': 2268,
            'url': 'https://hb.afl.rakuten.co.jp/hgc/g00r4jv5.fuu30cec.g00r4jv5.fuu313de/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fcanpanera%2Fn16002%2F&m=http%3A%2F%2Fm.rakuten.co.jp%2Fcanpanera%2Fi%2F10003969%2F&rafcid=wsc_i_is_1099421053709374278',
            'image_url': 'https://thumbnail.image.rakuten.co.jp/@0_mall/canpanera/cabinet/item206/item_n16002_0.jpg?_ex=128x128',
            'description': 'メーカー希望小売価格はメーカーサイトに基づいて掲載しています純度の高いプラスチックの高性能と高い気密性が世界中のバックパッカー、キャンパーらに愛されています。 キャンプ、トレッキング、フィットネス、ス...',
            'shop_name': 'CAMPANERAオンラインストア'
        }
    ]

def get_fallback_hotels():
    """フォールバック用の固定ホテルデータ（実際の楽天トラベル予約リンク）"""
    return [
        {
            'name': 'ホテルフランクス',
            'url': 'https://travel.rakuten.co.jp/HOTEL/4929/4929.html?f_tn=1&f_camp_id=139b96cc.29d2cd62.139b96cd.e6b1673a',
            'image_url': 'https://images.unsplash.com/photo-1566073771259-6a8506099945?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80',
            'description': '接客サービス高評価♪全室禁煙で快適滞在。幕張メッセ徒歩5分の便利な立地。',
            'location': '海浜幕張駅徒歩4分',
            'min_charge': 8800
        },
        {
            'name': '旭屋旅館＜香川県・小豆島＞',
            'url': 'https://travel.rakuten.co.jp/HOTEL/13651/13651.html?f_tn=1&f_camp_id=139b96cc.29d2cd62.139b96cd.e6b1673a',
            'image_url': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80',
            'description': '土庄港高速艇乗り場から徒歩1分。小豆島観光の拠点として最適な立地。',
            'location': '土庄港徒歩1分',
            'min_charge': 6800
        },
        {
            'name': 'ロヂテ・サンボア（聖なる森）',
            'url': 'https://travel.rakuten.co.jp/HOTEL/2950/2950.html?f_tn=1&f_camp_id=139b96cc.29d2cd62.139b96cd.e6b1673a',
            'image_url': 'https://images.unsplash.com/photo-1564501049412-61c2a3083791?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80',
            'description': '男体山一望の静かな一軒宿。杉木立の眺めに癒される岩風呂で登山の疲れを癒やします。',
            'location': 'JR日光駅より車で3分',
            'min_charge': 7500
        }
    ]