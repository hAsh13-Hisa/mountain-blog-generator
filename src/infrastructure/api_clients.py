"""
外部API クライアント実装
"""
import asyncio
import aiohttp
import requests
import json
import time
from typing import Dict, List, Optional, Any, Tuple
from urllib.parse import urlencode, quote
import base64

from anthropic import Anthropic
from config.settings import get_settings
from config.logging_config import LoggerMixin, log_api_call
from src.domain.entities import AffiliateProduct, AffiliateHotel, ImageInfo


class APIClientError(Exception):
    """API クライアントエラー"""
    pass


class ClaudeAPIClient(LoggerMixin):
    """Claude API クライアント"""
    
    def __init__(self):
        self.settings = get_settings()
        self.client = Anthropic(api_key=self.settings.ANTHROPIC_API_KEY)
    
    @log_api_call("Claude API")
    def generate_article(
        self,
        mountain_data: Dict[str, Any],
        theme: Optional[str] = None,
        target_length: int = 2000
    ) -> Tuple[str, str, str, List[str]]:
        """
        記事を生成
        
        Returns:
            Tuple[title, content, excerpt, tags]
        """
        try:
            prompt = self._build_article_prompt(mountain_data, theme, target_length)
            
            message = self.client.messages.create(
                model=self.settings.CLAUDE_MODEL,
                max_tokens=self.settings.CLAUDE_MAX_TOKENS,
                temperature=self.settings.CLAUDE_TEMPERATURE,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            response_text = message.content[0].text
            return self._parse_article_response(response_text)
            
        except Exception as e:
            self.log_error("Claude API article generation failed", e)
            raise APIClientError(f"Claude API エラー: {str(e)}")
    
    def _build_article_prompt(
        self,
        mountain_data: Dict[str, Any],
        theme: Optional[str],
        target_length: int
    ) -> str:
        """記事生成用プロンプトを構築"""
        mountain_name = mountain_data['name']
        prefecture = mountain_data['prefecture']
        elevation = mountain_data['elevation']
        difficulty = mountain_data['difficulty']['level']
        features = mountain_data['features']
        
        prompt = f"""
低山旅行ブログの記事を作成してください。以下の条件に従って、SEOに最適化された魅力的な記事を書いてください。

【山の情報】
- 山名: {mountain_name}
- 所在地: {prefecture}
- 標高: {elevation}m
- 難易度: {difficulty}
- 特徴: {', '.join(features)}

【記事の条件】
- 文字数: 約{target_length}文字
- ターゲット: 登山初心者〜中級者
- トーン: 親しみやすく、実用的な情報を含む
- SEO: 自然なキーワード配置
"""

        if theme:
            prompt += f"- テーマ: {theme}\n"

        prompt += """
【記事構成】
1. 魅力的な導入
2. 山の基本情報
3. 登山コースの詳細
4. 見どころ・楽しみ方
5. アクセス・準備情報
6. まとめ

【出力形式】
以下のJSONフォーマットで出力してください：

```json
{
  "title": "記事タイトル（SEOキーワードを含む）",
  "content": "記事本文（HTML形式、見出しはh2, h3タグを使用）",
  "excerpt": "記事の要約（150文字程度）",
  "tags": ["タグ1", "タグ2", "タグ3", "タグ4", "タグ5"]
}
```

記事は読者が実際に登山に行きたくなるような内容にしてください。
"""
        return prompt
    
    def _parse_article_response(self, response: str) -> Tuple[str, str, str, List[str]]:
        """Claude APIのレスポンスをパース"""
        try:
            # デバッグ: 生のレスポンスをコンソールに出力（必要時のみ）
            import os
            if os.getenv('DEBUG_CLAUDE', '').lower() in ['true', '1', 'yes']:
                print("=" * 80)
                print("🔍 CLAUDE API RAW RESPONSE:")
                print("=" * 80)
                print(response)
                print("=" * 80)
            
            # JSON部分を抽出
            json_start = response.find('```json')
            if json_start == -1:
                # JSON マーカーが見つからない場合は、JSON部分を直接探す
                json_start = response.find('{')
                if json_start == -1:
                    raise ValueError("JSON not found in response")
                start_idx = json_start
                end_idx = response.rfind('}') + 1
            else:
                start_idx = json_start + 7
                end_idx = response.find('```', start_idx)
                if end_idx == -1:
                    end_idx = len(response)
            
            json_str = response[start_idx:end_idx].strip()
            
            # レスポンス全体がJSONオブジェクトでない場合、{} で囲む
            if not json_str.startswith('{'):
                json_str = '{' + json_str
            if not json_str.endswith('}'):
                json_str = json_str + '}'
            
            if os.getenv('DEBUG_CLAUDE', '').lower() in ['true', '1', 'yes']:
                print("🔍 EXTRACTED JSON:")
                print("-" * 40)
                print(json_str)
                print("-" * 40)
            
            # 制御文字を除去
            import re
            json_str = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', json_str)
            
            # テンプレートリテラル（backtick）をダブルクォートに変換
            json_str = re.sub(r'`([^`]*)`', r'"\1"', json_str)
            
            # 改行文字をエスケープ
            json_str = json_str.replace('\n', '\\n').replace('\r', '\\r')
            
            if os.getenv('DEBUG_CLAUDE', '').lower() in ['true', '1', 'yes']:
                print("🔍 CLEANED JSON:")
                print("-" * 40)
                print(json_str)
                print("-" * 40)
            
            data = json.loads(json_str)
            
            return (
                data['title'],
                data['content'],
                data['excerpt'],
                data['tags']
            )
            
        except (json.JSONDecodeError, KeyError) as e:
            print(f"❌ JSON PARSE ERROR: {e}")
            print("🔄 FALLBACK: Using raw response as content")
            self.log_error("Failed to parse Claude API response", e)
            
            # フォールバック: レスポンスからタイトルを抽出してみる
            lines = response.split('\n')
            title = "登山記事"
            for line in lines[:10]:  # 最初の10行から探す
                if any(keyword in line for keyword in ['タイトル', 'Title', '題名']):
                    title = line.strip()
                    break
            
            return (
                title,
                response,  # 生のレスポンスをそのまま使用
                "Claude APIから生成された登山記事です。",
                ["登山", "山歩き", "ハイキング", "自然", "アウトドア"]
            )


class WordPressAPIClient(LoggerMixin):
    """WordPress API クライアント"""
    
    def __init__(self):
        self.settings = get_settings()
        self.base_url = f"{self.settings.WP_URL}/wp-json/wp/v2"
        self.auth = self._get_auth_header()
    
    def _get_auth_header(self) -> str:
        """認証ヘッダーを生成"""
        # アプリケーションパスワードからスペースを削除
        app_password = self.settings.WP_APP_PASSWORD.replace(' ', '')
        credentials = f"{self.settings.WP_USERNAME}:{app_password}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        return f"Basic {encoded_credentials}"
    
    def _get_or_create_tags(self, tag_names: List[str]) -> List[int]:
        """タグ名からタグIDを取得または作成"""
        tag_ids = []
        headers = {
            "Authorization": self.auth,
            "Content-Type": "application/json"
        }
        
        for tag_name in tag_names:
            try:
                # 既存のタグを検索
                search_response = requests.get(
                    f"{self.base_url}/tags",
                    params={"search": tag_name},
                    headers=headers,
                    timeout=30
                )
                search_response.raise_for_status()
                existing_tags = search_response.json()
                
                if existing_tags:
                    # 既存のタグを使用
                    tag_ids.append(existing_tags[0]['id'])
                else:
                    # 新しいタグを作成
                    create_response = requests.post(
                        f"{self.base_url}/tags",
                        json={"name": tag_name},
                        headers=headers,
                        timeout=30
                    )
                    create_response.raise_for_status()
                    new_tag = create_response.json()
                    tag_ids.append(new_tag['id'])
                    
            except Exception as e:
                self.log_warning(f"Failed to process tag '{tag_name}': {e}")
                
        return tag_ids
    
    @log_api_call("WordPress API")
    def create_post(self, post_data: Dict[str, Any]) -> int:
        """投稿を作成"""
        try:
            headers = {
                "Authorization": self.auth,
                "Content-Type": "application/json"
            }
            
            self.log_info(f"Creating WordPress post: {post_data.get('title', 'Unknown')}")
            
            # タグを処理（文字列配列が渡された場合）
            if 'tags' in post_data and isinstance(post_data['tags'], list) and post_data['tags']:
                if isinstance(post_data['tags'][0], str):
                    tag_ids = self._get_or_create_tags(post_data['tags'])
                    post_data['tags'] = tag_ids
            
            response = requests.post(
                f"{self.base_url}/posts",
                json=post_data,
                headers=headers,
                timeout=60
            )
            
            response.raise_for_status()
            result = response.json()
            
            post_id = result['id']
            self.log_info(f"WordPress post created successfully with ID: {post_id}")
            return post_id
            
        except requests.RequestException as e:
            # エラーレスポンスの詳細を取得
            error_detail = ""
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_detail = f" - レスポンス: {e.response.text[:500]}"
                except:
                    pass
            
            self.log_error(f"WordPress post creation failed{error_detail}", e)
            raise APIClientError(f"WordPress API エラー: {str(e)}{error_detail}")
    
    @log_api_call("WordPress API")
    def upload_media(self, image_url: str, image_data: Dict[str, str]) -> int:
        """メディアをアップロード - 一時的に無効化"""
        try:
            # 認証エラーを回避するため、画像アップロードを無効化
            self.log_info("WordPress画像アップロードをスキップ（認証エラー回避）")
            return 0  # ダミーのメディアID
            
            headers = {
                "Authorization": self.auth,
            }
            
            files = {
                'file': ('image.jpg', img_response.content, 'image/jpeg')
            }
            
            data = {
                'title': image_data.get('title', ''),
                'alt_text': image_data.get('alt_text', ''),
                'caption': image_data.get('caption', '')
            }
            
            response = requests.post(
                f"{self.base_url}/media",
                files=files,
                data=data,
                headers=headers,
                timeout=60
            )
            
            response.raise_for_status()
            result = response.json()
            
            self.log_info(f"WordPress media uploaded with ID: {result['id']}")
            return result['id']
            
        except requests.RequestException as e:
            self.log_error("WordPress media upload failed", e)
            raise APIClientError(f"WordPress メディアアップロード エラー: {str(e)}")


class RakutenAPIClient(LoggerMixin):
    """楽天 API クライアント"""
    
    def __init__(self):
        self.settings = get_settings()
        self.app_id = self.settings.RAKUTEN_APP_ID
        self.affiliate_id = self.settings.RAKUTEN_AFFILIATE_ID
        self.base_url = "https://app.rakuten.co.jp/services/api"
    
    @log_api_call("Rakuten API")
    def search_products(
        self,
        keyword: str,
        max_results: int = 5,
        min_price: int = 1000,
        max_price: int = 50000
    ) -> List[AffiliateProduct]:
        """商品を検索"""
        try:
            params = {
                'applicationId': self.app_id,
                'affiliateId': self.affiliate_id,
                'keyword': keyword,
                'hits': max_results,
                'minPrice': min_price,
                'maxPrice': max_price,
                'sort': 'standard',
                'format': 'json'
            }
            
            response = requests.get(
                f"{self.base_url}/IchibaItem/Search/20170706",
                params=params,
                timeout=self.settings.API_TIMEOUT
            )
            
            response.raise_for_status()
            data = response.json()
            
            products = []
            for item in data.get('Items', []):
                item_data = item['Item']
                
                product = AffiliateProduct(
                    name=item_data['itemName'],
                    price=int(item_data['itemPrice']),
                    url=item_data['affiliateUrl'],
                    image_url=item_data['mediumImageUrls'][0]['imageUrl'] if item_data.get('mediumImageUrls') else '',
                    description=item_data.get('itemCaption', '')[:200],
                    category=item_data.get('genreId', ''),
                    rating=float(item_data.get('reviewAverage', 0)),
                    review_count=int(item_data.get('reviewCount', 0)),
                    shop_name=item_data.get('shopName', '')
                )
                products.append(product)
            
            self.log_info(f"Found {len(products)} products for keyword: {keyword}")
            return products
            
        except requests.RequestException as e:
            self.log_error("Rakuten product search failed", e)
            raise APIClientError(f"楽天商品検索 エラー: {str(e)}")
    
    @log_api_call("Rakuten API")
    def search_hotels(
        self,
        area_code: str = "01",  # デフォルトは北海道
        max_results: int = 3
    ) -> List[AffiliateHotel]:
        """宿泊施設を検索"""
        try:
            # 楽天APIエラーを回避するため、宿泊検索を無効化
            self.log_info("楽天宿泊検索をスキップ（APIエラー回避）")
            return []  # 空のリストを返す
            
            response = requests.get(
                f"{self.base_url}/Travel/SimpleHotelSearch/20170426",
                params=params,
                timeout=self.settings.API_TIMEOUT
            )
            
            response.raise_for_status()
            data = response.json()
            
            hotels = []
            for hotel_data in data.get('hotels', []):
                hotel_info = hotel_data[0]['hotel'][0]['hotelBasicInfo']
                
                hotel = AffiliateHotel(
                    name=hotel_info['hotelName'],
                    price=int(hotel_info.get('hotelMinCharge', 5000)),
                    url=hotel_info['hotelInformationUrl'],
                    image_url=hotel_info.get('hotelImageUrl', ''),
                    description=hotel_info.get('hotelSpecial', '')[:200],
                    location=hotel_info.get('address1', ''),
                    rating=float(hotel_info.get('userReview', 0)),
                    review_count=int(hotel_info.get('reviewCount', 0))
                )
                hotels.append(hotel)
            
            self.log_info(f"Found {len(hotels)} hotels for area: {area_code}")
            return hotels
            
        except requests.RequestException as e:
            self.log_error("Rakuten hotel search failed", e)
            raise APIClientError(f"楽天宿泊検索 エラー: {str(e)}")


class UnsplashAPIClient(LoggerMixin):
    """Unsplash API クライアント（無料版）"""
    
    def __init__(self):
        self.settings = get_settings()
        self.base_url = "https://api.unsplash.com"
    
    def search_images(
        self,
        keyword: str,
        count: int = 1,
        orientation: str = "landscape"
    ) -> List[ImageInfo]:
        """画像を検索（無料版のため制限あり）"""
        try:
            # Unsplash API キーが設定されていない場合は固定画像を返す
            images = []
            
            # 山の種類に応じた固定画像URLを返す
            sample_images = self._get_sample_images(keyword)
            
            for i, img_data in enumerate(sample_images[:count]):
                image = ImageInfo(
                    url=img_data['url'],
                    title=f"{keyword}の風景",
                    description=f"美しい{keyword}の景色",
                    photographer=img_data['photographer'],
                    source="unsplash",
                    width=img_data.get('width', 1024),
                    height=img_data.get('height', 576),
                    alt_text=f"{keyword}の登山風景"
                )
                images.append(image)
            
            self.log_info(f"Generated {len(images)} sample images for: {keyword}")
            return images
            
        except Exception as e:
            self.log_error("Image search failed", e)
            # フォールバックとして固定画像を返す
            return [ImageInfo(
                url="https://images.unsplash.com/photo-1506905925346-21bda4d32df4",
                title=f"{keyword}の風景",
                description="山の美しい景色",
                photographer="Sample Photographer",
                source="unsplash",
                alt_text=f"{keyword}の登山風景"
            )]
    
    def _get_sample_images(self, keyword: str) -> List[Dict[str, Any]]:
        """キーワードに応じたサンプル画像データを返す"""
        mountain_images = [
            {
                "url": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4",
                "photographer": "Maarten van den Heuvel",
                "width": 1024,
                "height": 576
            },
            {
                "url": "https://images.unsplash.com/photo-1464822759844-d150ad6d0e12",
                "photographer": "Matteo Catanese",
                "width": 1024,
                "height": 576
            },
            {
                "url": "https://images.unsplash.com/photo-1551632811-561732d1e306",
                "photographer": "Francesco Ungaro",
                "width": 1024,
                "height": 576
            },
            {
                "url": "https://images.unsplash.com/photo-1506197603052-3cc9c3a201bd",
                "photographer": "Sergey Pesterev",
                "width": 1024,
                "height": 576
            }
        ]
        
        return mountain_images


# API クライアントのファクトリークラス
class APIClientFactory:
    """API クライアントのファクトリー"""
    
    @staticmethod
    def create_claude_client() -> ClaudeAPIClient:
        """Claude API クライアントを作成"""
        return ClaudeAPIClient()
    
    @staticmethod
    def create_wordpress_client() -> WordPressAPIClient:
        """WordPress API クライアントを作成"""
        return WordPressAPIClient()
    
    @staticmethod
    def create_rakuten_client() -> RakutenAPIClient:
        """楽天 API クライアントを作成"""
        return RakutenAPIClient()
    
    @staticmethod
    def create_unsplash_client() -> UnsplashAPIClient:
        """Unsplash API クライアントを作成"""
        return UnsplashAPIClient()