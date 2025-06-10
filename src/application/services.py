"""
アプリケーションサービス実装
"""
import time
from typing import Dict, List, Optional, Any
from datetime import datetime

from config.settings import get_settings
from config.logging_config import LoggerMixin
from src.domain.entities import (
    Mountain, Article, ArticleContent, ArticleFactory, ImageInfo,
    GenerationRequest, GenerationResult, AffiliateProduct, AffiliateHotel
)
from src.infrastructure.api_clients import (
    APIClientFactory, APIClientError
)
from src.infrastructure.repositories import (
    RepositoryFactory, RepositoryError
)


class ServiceError(Exception):
    """サービスエラー"""
    pass


class ArticleGenerationService(LoggerMixin):
    """記事生成サービス"""
    
    def __init__(self):
        self.settings = get_settings()
        self.claude_client = APIClientFactory.create_claude_client()
        self.mountain_repo = RepositoryFactory.get_mountain_repository()
    
    def generate_article(self, request: GenerationRequest) -> GenerationResult:
        """記事を生成"""
        start_time = time.time()
        
        try:
            self.log_info(f"Starting article generation for mountain: {request.mountain_id}")
            
            # 山データを取得
            mountain = self.mountain_repo.get_by_id(request.mountain_id)
            if not mountain:
                raise ServiceError(f"山が見つかりません: {request.mountain_id}")
            
            # Claude APIで記事を生成
            mountain_dict = self._mountain_to_dict(mountain)
            import os
            if os.getenv('DEBUG_CLAUDE', '').lower() in ['true', '1', 'yes']:
                print(f"🏔️ GENERATING ARTICLE FOR: {mountain.name} ({mountain.elevation}m)")
                print(f"📝 THEME: {request.theme}")
                print(f"📏 TARGET LENGTH: {request.target_length}")
            
            title, content, excerpt, tags = self.claude_client.generate_article(
                mountain_dict,
                request.theme,
                request.target_length
            )
            
            if os.getenv('DEBUG_CLAUDE', '').lower() in ['true', '1', 'yes']:
                print(f"✅ GENERATED ARTICLE:")
                print(f"   📌 Title: {title}")
                print(f"   📊 Content length: {len(content)} chars")
                print(f"   📋 Excerpt: {excerpt[:100]}...")
                print(f"   🏷️ Tags: {tags}")
            
            # 記事エンティティを作成
            article = ArticleFactory.create_article_with_content(
                mountain=mountain,
                title=title,
                content=content,
                excerpt=excerpt,
                tags=tags,
                categories=self.settings.WP_DEFAULT_CATEGORIES
            )
            
            generation_time = time.time() - start_time
            
            self.log_info(f"Article generation completed in {generation_time:.2f}s")
            
            return GenerationResult(
                success=True,
                article=article,
                generation_time=generation_time
            )
            
        except (APIClientError, RepositoryError, ServiceError) as e:
            self.log_error("Article generation failed", e)
            return GenerationResult(
                success=False,
                error_message=str(e),
                generation_time=time.time() - start_time
            )
    
    def _mountain_to_dict(self, mountain: Mountain) -> Dict[str, Any]:
        """山エンティティを辞書に変換"""
        return {
            "id": mountain.id,
            "name": mountain.name,
            "name_en": mountain.name_en,
            "prefecture": mountain.prefecture,
            "region": mountain.region,
            "elevation": mountain.elevation,
            "difficulty": {
                "level": mountain.difficulty.level.value,
                "hiking_time": mountain.difficulty.hiking_time,
                "distance": mountain.difficulty.distance,
                "elevation_gain": mountain.difficulty.elevation_gain
            },
            "features": mountain.features,
            "keywords": mountain.keywords,
            "article_themes": mountain.article_themes
        }


class ImageService(LoggerMixin):
    """画像サービス"""
    
    def __init__(self):
        self.settings = get_settings()
        self.unsplash_client = APIClientFactory.create_unsplash_client()
    
    def get_featured_image(self, mountain: Mountain) -> Optional[ImageInfo]:
        """アイキャッチ画像を取得"""
        try:
            self.log_info(f"Fetching featured image for: {mountain.name}")
            
            # キーワードを構築
            keywords = [mountain.name, mountain.prefecture, "山", "登山"]
            search_keyword = " ".join(keywords[:2])
            
            images = self.unsplash_client.search_images(
                keyword=search_keyword,
                count=1,
                orientation="landscape"
            )
            
            if images:
                image = images[0]
                image.title = f"{mountain.name}の風景"
                image.description = f"{mountain.name}（{mountain.prefecture}）の美しい景色"
                image.alt_text = f"{mountain.name} 登山 風景"
                return image
            
            return None
            
        except APIClientError as e:
            self.log_error("Failed to fetch featured image", e)
            return None
    
    def get_inline_images(self, mountain: Mountain, count: int = 2) -> List[ImageInfo]:
        """記事内画像を取得"""
        try:
            self.log_info(f"Fetching {count} inline images for: {mountain.name}")
            
            images = []
            keywords = [
                f"{mountain.name} 登山道",
                f"{mountain.name} 山頂",
                f"{mountain.prefecture} ハイキング"
            ]
            
            for i, keyword in enumerate(keywords[:count]):
                image_list = self.unsplash_client.search_images(
                    keyword=keyword,
                    count=1
                )
                
                if image_list:
                    image = image_list[0]
                    image.title = f"{mountain.name}の登山風景{i+1}"
                    image.description = f"{mountain.name}での登山の様子"
                    image.alt_text = f"{mountain.name} 登山風景"
                    images.append(image)
            
            return images
            
        except APIClientError as e:
            self.log_error("Failed to fetch inline images", e)
            return []


class AffiliateService(LoggerMixin):
    """アフィリエイトサービス"""
    
    def __init__(self):
        self.settings = get_settings()
        self.rakuten_client = APIClientFactory.create_rakuten_client()
        self.area_repo = RepositoryFactory.get_area_code_repository()
    
    def get_hiking_products(self, mountain: Mountain) -> List[AffiliateProduct]:
        """登山用品を取得"""
        try:
            self.log_info(f"Fetching hiking products for: {mountain.name}")
            
            # 山の特徴に応じたキーワード
            keywords = self._get_product_keywords(mountain)
            
            all_products = []
            for keyword in keywords[:2]:  # 最大2つのキーワードで検索
                products = self.rakuten_client.search_products(
                    keyword=keyword,
                    max_results=3,
                    min_price=self.settings.PRODUCT_PRICE_MIN,
                    max_price=self.settings.PRODUCT_PRICE_MAX
                )
                all_products.extend(products)
            
            # 重複を除去し、価格でソート
            unique_products = []
            seen_names = set()
            
            for product in all_products:
                if product.name not in seen_names:
                    unique_products.append(product)
                    seen_names.add(product.name)
            
            # 最大商品数まで制限
            unique_products.sort(key=lambda x: x.price)
            return unique_products[:self.settings.MAX_AFFILIATE_PRODUCTS]
            
        except APIClientError as e:
            self.log_error("Failed to fetch hiking products", e)
            return []
    
    def get_nearby_hotels(self, mountain: Mountain) -> List[AffiliateHotel]:
        """近隣の宿泊施設を取得"""
        try:
            self.log_info(f"Fetching hotels near: {mountain.name}")
            
            # 都道府県から地域コードを取得
            area_code = self.area_repo.get_area_code(mountain.prefecture)
            
            hotels = self.rakuten_client.search_hotels(
                area_code=area_code,
                max_results=self.settings.MAX_AFFILIATE_HOTELS
            )
            
            return hotels
            
        except APIClientError as e:
            self.log_error("Failed to fetch nearby hotels", e)
            return []
    
    def _get_product_keywords(self, mountain: Mountain) -> List[str]:
        """山の特徴に応じた商品キーワードを生成"""
        keywords = []
        
        # 山の名前をハッシュして、山ごとに異なる商品を選択
        import hashlib
        mountain_hash = int(hashlib.md5(mountain.name.encode()).hexdigest(), 16) % 100
        
        # 基本キーワードプール
        basic_keywords = [
            ["登山靴", "トレッキングシューズ"],
            ["ハイキング ウェア", "アウトドア ジャケット", "登山 パンツ"],
            ["リュック", "バックパック", "デイパック"],
            ["水筒", "ボトル", "ハイドレーション"],
            ["レインウェア", "雨具", "ポンチョ"],
            ["帽子", "キャップ", "ハット"],
            ["グローブ", "手袋", "軍手"],
            ["タオル", "手ぬぐい", "バンダナ"]
        ]
        
        # 山のハッシュ値を使って異なる組み合わせを選択
        selected_basic = basic_keywords[mountain_hash % len(basic_keywords)]
        keywords.extend(selected_basic[:2])  # 各カテゴリから2つ選択
        
        # 追加で別のカテゴリからも選択
        second_category = basic_keywords[(mountain_hash + 1) % len(basic_keywords)]
        keywords.extend(second_category[:1])
        
        # 難易度に応じたキーワード
        if mountain.is_beginner_friendly():
            beginner_keywords = ["初心者 登山", "ハイキング", "軽登山", "散策"]
            keywords.append(beginner_keywords[mountain_hash % len(beginner_keywords)])
        else:
            advanced_keywords = ["登山 装備", "トレッキング ポール", "本格登山", "山岳装備"]
            keywords.append(advanced_keywords[mountain_hash % len(advanced_keywords)])
        
        # 標高に応じたキーワード
        if mountain.elevation > 1500:
            high_altitude_keywords = ["高山 装備", "アルパイン", "高地 対応"]
            keywords.append(high_altitude_keywords[mountain_hash % len(high_altitude_keywords)])
        elif mountain.elevation < 500:
            low_mountain_keywords = ["低山 ハイキング", "里山 散策", "ウォーキング"]
            keywords.append(low_mountain_keywords[mountain_hash % len(low_mountain_keywords)])
        
        # 地域特性を考慮
        if "北海道" in mountain.prefecture:
            keywords.append("防寒")
        elif "沖縄" in mountain.prefecture:
            keywords.append("日焼け対策")
        elif "関東" in mountain.prefecture or "東京" in mountain.prefecture:
            keywords.append("都市近郊 ハイキング")
        
        # 重複を除去してシャッフル
        unique_keywords = list(set(keywords))
        # 山ごとに固定だが異なる順序で返す
        import random
        random.seed(mountain_hash)  # 山ごとに固定のシード
        random.shuffle(unique_keywords)
        
        return unique_keywords[:5]  # 最大5つのキーワード


class PublishingService(LoggerMixin):
    """記事公開サービス"""
    
    def __init__(self):
        self.settings = get_settings()
        self.wordpress_client = APIClientFactory.create_wordpress_client()
        self.image_service = ImageService()
        self.affiliate_service = AffiliateService()
    
    def enhance_article(self, article: Article) -> Article:
        """記事に画像とアフィリエイトリンクを追加"""
        try:
            self.log_info(f"Enhancing article: {article.content.title}")
            
            # アイキャッチ画像を取得
            if not article.content.featured_image:
                featured_image = self.image_service.get_featured_image(article.mountain)
                if featured_image:
                    article.content.featured_image = featured_image
            
            # 記事内画像を取得
            if not article.content.inline_images:
                inline_images = self.image_service.get_inline_images(article.mountain, 2)
                article.content.inline_images = inline_images
            
            # アフィリエイト商品を取得
            if not article.content.affiliate_products:
                products = self.affiliate_service.get_hiking_products(article.mountain)
                article.content.affiliate_products = products
            
            # 宿泊施設を取得
            if not article.content.affiliate_hotels:
                hotels = self.affiliate_service.get_nearby_hotels(article.mountain)
                article.content.affiliate_hotels = hotels
            
            # コンテンツにアフィリエイト情報を埋め込み
            enhanced_content = self._embed_affiliates_in_content(
                article.content.content,
                article.content.affiliate_products,
                article.content.affiliate_hotels
            )
            article.content.content = enhanced_content
            
            self.log_info("Article enhancement completed")
            return article
            
        except Exception as e:
            self.log_error("Article enhancement failed", e)
            return article
    
    def publish_to_wordpress(self, article: Article) -> int:
        """WordPressに記事を公開"""
        try:
            self.log_info(f"Publishing article to WordPress: {article.content.title}")
            
            # アイキャッチ画像をアップロード
            featured_image_id = None
            if article.content.featured_image:
                try:
                    featured_image_id = self.wordpress_client.upload_media(
                        article.content.featured_image.url,
                        article.content.featured_image.get_wordpress_media_data()
                    )
                except APIClientError as e:
                    self.log_warning(f"Failed to upload featured image: {e}")
            
            # 投稿データを準備
            post_data = article.get_wordpress_data()
            if featured_image_id:
                post_data['featured_media'] = featured_image_id
            
            # WordPressに投稿
            post_id = self.wordpress_client.create_post(post_data)
            
            # 記事エンティティを更新
            article.wordpress_id = post_id
            article.updated_at = datetime.now()
            
            self.log_info(f"Article published with WordPress ID: {post_id}")
            return post_id
            
        except APIClientError as e:
            self.log_error("WordPress publishing failed", e)
            raise ServiceError(f"WordPress公開エラー: {str(e)}")
    
    def _embed_affiliates_in_content(
        self,
        content: str,
        products: List[AffiliateProduct],
        hotels: List[AffiliateHotel]
    ) -> str:
        """コンテンツにアフィリエイトリンクを埋め込み"""
        if not products and not hotels:
            return content
        
        affiliate_section = "\n\n<h3>おすすめの登山用品・宿泊施設</h3>\n"
        
        # 商品セクション
        if products:
            affiliate_section += "\n<h4>登山用品</h4>\n<ul>\n"
            for product in products[:3]:  # 最大3つまで
                affiliate_section += f'<li><a href="{product.url}" target="_blank" rel="noopener">{product.name}</a> - {product.get_formatted_price()}</li>\n'
            affiliate_section += "</ul>\n"
        
        # 宿泊施設セクション
        if hotels:
            affiliate_section += "\n<h4>近隣の宿泊施設</h4>\n<ul>\n"
            for hotel in hotels:
                affiliate_section += f'<li><a href="{hotel.url}" target="_blank" rel="noopener">{hotel.name}</a> - {hotel.get_formatted_price()}</li>\n'
            affiliate_section += "</ul>\n"
        
        # コンテンツの最後に追加
        return content + affiliate_section


class MountainArticleService(LoggerMixin):
    """山記事総合サービス"""
    
    def __init__(self):
        self.generation_service = ArticleGenerationService()
        self.publishing_service = PublishingService()
        self.mountain_repo = RepositoryFactory.get_mountain_repository()
    
    def create_and_publish_article(
        self,
        mountain_id: str,
        theme: Optional[str] = None,
        publish: bool = False
    ) -> GenerationResult:
        """記事作成から公開までの一連の処理"""
        try:
            self.log_info(f"Starting full article workflow for: {mountain_id}")
            
            # 記事生成
            request = GenerationRequest(
                mountain_id=mountain_id,
                theme=theme,
                include_affiliates=True
            )
            
            result = self.generation_service.generate_article(request)
            
            if not result.success or not result.article:
                return result
            
            # 記事を拡張（画像・アフィリエイト追加）
            enhanced_article = self.publishing_service.enhance_article(result.article)
            
            # 公開処理
            if publish:
                try:
                    wordpress_id = self.publishing_service.publish_to_wordpress(enhanced_article)
                    self.log_info(f"Article published successfully with ID: {wordpress_id}")
                except ServiceError as e:
                    self.log_error("Publishing failed", e)
                    result.error_message = str(e)
                    result.success = False
            
            result.article = enhanced_article
            return result
            
        except Exception as e:
            self.log_error("Full article workflow failed", e)
            return GenerationResult(
                success=False,
                error_message=str(e)
            )
    
    def get_mountain_suggestions(self, count: int = 5) -> List[Mountain]:
        """記事作成におすすめの山を取得"""
        try:
            # 様々な難易度・地域からバランスよく選択
            suggestions = []
            
            # 初心者向けの山
            beginner_mountains = self.mountain_repo.get_beginner_friendly()
            if beginner_mountains:
                suggestions.extend(beginner_mountains[:2])
            
            # ケーブルカーがある山
            cable_car_mountains = self.mountain_repo.get_with_cable_car()
            if cable_car_mountains:
                suggestions.extend([m for m in cable_car_mountains if m not in suggestions][:2])
            
            # その他の山をランダムに追加
            remaining_count = count - len(suggestions)
            if remaining_count > 0:
                other_mountains = [m for m in self.mountain_repo.get_all() if m not in suggestions]
                suggestions.extend(other_mountains[:remaining_count])
            
            return suggestions[:count]
            
        except RepositoryError as e:
            self.log_error("Failed to get mountain suggestions", e)
            return []