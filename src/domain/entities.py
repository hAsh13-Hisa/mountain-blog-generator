"""
ドメインエンティティ定義
"""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


class DifficultyLevel(str, Enum):
    """登山難易度レベル"""
    BEGINNER = "初級"
    BEGINNER_INTERMEDIATE = "初級-中級"
    INTERMEDIATE = "中級"
    ADVANCED = "上級"


class ArticleStatus(str, Enum):
    """記事のステータス"""
    DRAFT = "draft"
    PUBLISH = "publish"
    PRIVATE = "private"


@dataclass
class Location:
    """位置情報"""
    latitude: float
    longitude: float
    nearest_station: str
    access_time: str


@dataclass
class Difficulty:
    """登山難易度情報"""
    level: DifficultyLevel
    hiking_time: str
    distance: str
    elevation_gain: str


@dataclass
class Trail:
    """登山コース"""
    name: str
    description: str
    time: str


@dataclass
class Seasons:
    """季節情報"""
    best: List[str]
    cherry_blossom: Optional[str] = None
    autumn_leaves: Optional[str] = None


@dataclass
class Facilities:
    """施設情報"""
    restrooms: bool = False
    restaurant: bool = False
    parking: bool = False
    cable_car: bool = False
    visitor_center: bool = False


@dataclass
class Mountain:
    """山エンティティ"""
    id: str
    name: str
    name_en: str
    prefecture: str
    region: str
    elevation: int
    location: Location
    difficulty: Difficulty
    features: List[str]
    trails: List[Trail] = field(default_factory=list)
    seasons: Optional[Seasons] = None
    facilities: Optional[Facilities] = None
    nearby_attractions: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    article_themes: List[str] = field(default_factory=list)
    
    def is_beginner_friendly(self) -> bool:
        """初心者向けかどうかを判定"""
        return self.difficulty.level in [DifficultyLevel.BEGINNER, DifficultyLevel.BEGINNER_INTERMEDIATE]
    
    def has_cable_car(self) -> bool:
        """ケーブルカーがあるかどうかを判定"""
        return self.facilities and self.facilities.cable_car
    
    def get_hiking_hours(self) -> float:
        """登山時間を時間単位で取得（概算）"""
        import re
        time_str = self.difficulty.hiking_time
        match = re.search(r'(\d+)', time_str)
        return float(match.group(1)) if match else 3.0


@dataclass
class ImageInfo:
    """画像情報"""
    url: str
    title: str
    description: str
    photographer: str
    source: str = "unsplash"
    width: Optional[int] = None
    height: Optional[int] = None
    alt_text: Optional[str] = None
    
    def get_wordpress_media_data(self) -> Dict[str, Any]:
        """WordPress用のメディアデータを生成"""
        return {
            "title": self.title,
            "description": self.description,
            "alt_text": self.alt_text or self.title,
            "caption": f"Photo by {self.photographer} on Unsplash"
        }


@dataclass
class AffiliateProduct:
    """アフィリエイト商品"""
    name: str
    price: int
    url: str
    image_url: str
    description: str
    category: str
    rating: Optional[float] = None
    review_count: Optional[int] = None
    shop_name: Optional[str] = None
    
    def get_formatted_price(self) -> str:
        """フォーマットされた価格文字列を取得"""
        return f"¥{self.price:,}"
    
    def is_reasonably_priced(self, max_price: int = 50000) -> bool:
        """適正価格かどうかを判定"""
        return self.price <= max_price


@dataclass
class AffiliateHotel:
    """アフィリエイト宿泊施設"""
    name: str
    price: int
    url: str
    image_url: str
    description: str
    location: str
    rating: Optional[float] = None
    review_count: Optional[int] = None
    
    def get_formatted_price(self) -> str:
        """フォーマットされた価格文字列を取得"""
        return f"¥{self.price:,}/泊"


@dataclass
class ArticleContent:
    """記事コンテンツ"""
    title: str
    content: str
    excerpt: str
    featured_image: Optional[ImageInfo] = None
    inline_images: List[ImageInfo] = field(default_factory=list)
    affiliate_products: List[AffiliateProduct] = field(default_factory=list)
    affiliate_hotels: List[AffiliateHotel] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    categories: List[str] = field(default_factory=list)
    
    def get_word_count(self) -> int:
        """記事の文字数を取得"""
        return len(self.content.replace(' ', '').replace('\n', ''))
    
    def has_minimum_length(self, min_length: int = 1500) -> bool:
        """最小文字数を満たしているかチェック"""
        return self.get_word_count() >= min_length


@dataclass
class Article:
    """記事エンティティ"""
    id: Optional[str]
    mountain: Mountain
    content: ArticleContent
    status: ArticleStatus = ArticleStatus.DRAFT
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    wordpress_id: Optional[int] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
    
    def is_publishable(self) -> bool:
        """公開可能かどうかを判定"""
        return (
            self.content.has_minimum_length() and
            self.content.featured_image is not None and
            len(self.content.tags) > 0
        )
    
    def get_wordpress_data(self) -> Dict[str, Any]:
        """WordPress投稿用データを生成"""
        # WordPressではcategoriesとtagsはIDの配列である必要がある
        # タグは文字列配列で送信し、APIクライアント側で処理
        return {
            "title": self.content.title,
            "content": self.content.content,
            "excerpt": self.content.excerpt,
            "status": self.status.value,
            "tags": self.content.tags  # 文字列配列として送信
            # categoriesは一時的に除外（既存のカテゴリIDの取得が必要）
            # "categories": self.content.categories,
        }


class GenerationRequest(BaseModel):
    """記事生成リクエスト"""
    mountain_id: str = Field(..., description="山のID")
    theme: Optional[str] = Field(None, description="記事テーマ")
    target_length: int = Field(2000, description="目標文字数")
    include_affiliates: bool = Field(True, description="アフィリエイトリンクを含むか")
    max_products: int = Field(5, description="最大商品数")
    max_hotels: int = Field(3, description="最大宿泊施設数")
    
    class Config:
        use_enum_values = True


class GenerationResult(BaseModel):
    """記事生成結果"""
    success: bool
    article: Optional[Article] = None
    error_message: Optional[str] = None
    generation_time: Optional[float] = None
    
    class Config:
        arbitrary_types_allowed = True


# ファクトリークラス
class MountainFactory:
    """山エンティティのファクトリークラス"""
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> Mountain:
        """辞書データから山エンティティを生成"""
        location = Location(
            latitude=data['location']['latitude'],
            longitude=data['location']['longitude'],
            nearest_station=data['location']['nearest_station'],
            access_time=data['location']['access_time']
        )
        
        difficulty = Difficulty(
            level=DifficultyLevel(data['difficulty']['level']),
            hiking_time=data['difficulty']['hiking_time'],
            distance=data['difficulty']['distance'],
            elevation_gain=data['difficulty']['elevation_gain']
        )
        
        trails = [
            Trail(
                name=trail['name'],
                description=trail['description'],
                time=trail['time']
            )
            for trail in data.get('trails', [])
        ]
        
        seasons = None
        if 'seasons' in data:
            seasons = Seasons(
                best=data['seasons']['best'],
                cherry_blossom=data['seasons'].get('cherry_blossom'),
                autumn_leaves=data['seasons'].get('autumn_leaves')
            )
        
        facilities = None
        if 'facilities' in data:
            facilities = Facilities(
                restrooms=data['facilities'].get('restrooms', False),
                restaurant=data['facilities'].get('restaurant', False),
                parking=data['facilities'].get('parking', False),
                cable_car=data['facilities'].get('cable_car', False),
                visitor_center=data['facilities'].get('visitor_center', False)
            )
        
        return Mountain(
            id=data['id'],
            name=data['name'],
            name_en=data['name_en'],
            prefecture=data['prefecture'],
            region=data['region'],
            elevation=data['elevation'],
            location=location,
            difficulty=difficulty,
            features=data['features'],
            trails=trails,
            seasons=seasons,
            facilities=facilities,
            nearby_attractions=data.get('nearby_attractions', []),
            keywords=data.get('keywords', []),
            article_themes=data.get('article_themes', [])
        )


class ArticleFactory:
    """記事エンティティのファクトリークラス"""
    
    @staticmethod
    def create_empty_article(mountain: Mountain) -> Article:
        """空の記事エンティティを生成"""
        content = ArticleContent(
            title="",
            content="",
            excerpt="",
            categories=["エリア別"]
        )
        
        return Article(
            id=None,
            mountain=mountain,
            content=content
        )
    
    @staticmethod
    def create_article_with_content(
        mountain: Mountain,
        title: str,
        content: str,
        excerpt: str,
        tags: List[str],
        categories: List[str] = None
    ) -> Article:
        """コンテンツ付きの記事エンティティを生成"""
        if categories is None:
            categories = ["エリア別"]
        
        article_content = ArticleContent(
            title=title,
            content=content,
            excerpt=excerpt,
            tags=tags,
            categories=categories
        )
        
        return Article(
            id=None,
            mountain=mountain,
            content=article_content
        )