"""
アプリケーション設定管理
"""
from typing import List, Optional
from pydantic import Field
from pydantic_settings import BaseSettings
import os
from pathlib import Path


class Settings(BaseSettings):
    """アプリケーション設定クラス"""
    
    # === API Keys ===
    ANTHROPIC_API_KEY: str = Field(
        ..., 
        description="Claude API キー"
    )
    
    RAKUTEN_APP_ID: str = Field(
        ..., 
        description="楽天アプリケーションID"
    )
    
    RAKUTEN_AFFILIATE_ID: str = Field(
        ..., 
        description="楽天アフィリエイトID"
    )
    
    # === WordPress Settings ===
    WP_URL: str = Field(
        ..., 
        description="WordPress サイトURL"
    )
    
    WP_USERNAME: str = Field(
        ..., 
        description="WordPress ユーザー名"
    )
    
    WP_APP_PASSWORD: str = Field(
        ..., 
        description="WordPress アプリケーションパスワード"
    )
    
    # === Claude API Settings ===
    CLAUDE_MODEL: str = Field(
        default="claude-3-5-sonnet-20241022",
        description="使用するClaudeモデル"
    )
    
    CLAUDE_MAX_TOKENS: int = Field(
        default=2500,
        description="Claude API 最大トークン数"
    )
    
    CLAUDE_TEMPERATURE: float = Field(
        default=0.7,
        description="Claude API 温度パラメータ"
    )
    
    # === Application Settings ===
    LOG_LEVEL: str = Field(
        default="INFO",
        description="ログレベル"
    )
    
    OUTPUT_DIR: str = Field(
        default="./output",
        description="記事出力ディレクトリ"
    )
    
    DATA_DIR: str = Field(
        default="./data",
        description="データディレクトリ"
    )
    
    LOGS_DIR: str = Field(
        default="./logs",
        description="ログディレクトリ"
    )
    
    # === Retry Settings ===
    MAX_RETRIES: int = Field(
        default=3,
        description="API呼び出しの最大リトライ回数"
    )
    
    RETRY_DELAY: int = Field(
        default=5,
        description="リトライ間隔（秒）"
    )
    
    API_TIMEOUT: int = Field(
        default=30,
        description="API タイムアウト（秒）"
    )
    
    # === Article Generation Settings ===
    ARTICLE_MIN_LENGTH: int = Field(
        default=1500,
        description="記事の最小文字数"
    )
    
    ARTICLE_MAX_LENGTH: int = Field(
        default=2500,
        description="記事の最大文字数"
    )
    
    # === Image Settings ===
    FEATURED_IMAGE_WIDTH: int = Field(
        default=1024,
        description="アイキャッチ画像の幅"
    )
    
    FEATURED_IMAGE_HEIGHT: int = Field(
        default=576,
        description="アイキャッチ画像の高さ"
    )
    
    INLINE_IMAGE_WIDTH: int = Field(
        default=800,
        description="記事内画像の幅"
    )
    
    INLINE_IMAGE_HEIGHT: int = Field(
        default=600,
        description="記事内画像の高さ"
    )
    
    # === Affiliate Settings ===
    MAX_AFFILIATE_PRODUCTS: int = Field(
        default=5,
        description="記事内の最大アフィリエイト商品数"
    )
    
    MAX_AFFILIATE_HOTELS: int = Field(
        default=3,
        description="記事内の最大宿泊施設数"
    )
    
    PRODUCT_PRICE_MIN: int = Field(
        default=1000,
        description="商品の最低価格"
    )
    
    PRODUCT_PRICE_MAX: int = Field(
        default=50000,
        description="商品の最高価格"
    )
    
    # === WordPress Settings ===
    WP_DEFAULT_STATUS: str = Field(
        default="draft",
        description="WordPressの投稿ステータス"
    )
    
    WP_DEFAULT_CATEGORIES: List[str] = Field(
        default=["エリア別"],
        description="デフォルトカテゴリ"
    )
    
    # === Scheduler Settings ===
    SCHEDULE_ENABLED: bool = Field(
        default=False,
        description="スケジューラーの有効/無効"
    )
    
    SCHEDULE_TIME: str = Field(
        default="09:00",
        description="記事生成時刻（HH:MM形式）"
    )
    
    ARTICLES_PER_DAY: int = Field(
        default=1,
        description="1日の記事生成数"
    )
    
    # === Development Settings ===
    DEBUG: bool = Field(
        default=False,
        description="デバッグモード"
    )
    
    TESTING: bool = Field(
        default=False,
        description="テストモード"
    )
    
    # === Validation ===
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._create_directories()
        self._validate_settings()
    
    def _create_directories(self):
        """必要なディレクトリを作成"""
        for dir_path in [self.OUTPUT_DIR, self.DATA_DIR, self.LOGS_DIR]:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    def _validate_settings(self):
        """設定値の検証"""
        # ログレベルの検証
        valid_log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if self.LOG_LEVEL not in valid_log_levels:
            raise ValueError(f"LOG_LEVEL must be one of {valid_log_levels}")
        
        # 記事長さの検証
        if self.ARTICLE_MIN_LENGTH >= self.ARTICLE_MAX_LENGTH:
            raise ValueError("ARTICLE_MIN_LENGTH must be less than ARTICLE_MAX_LENGTH")
        
        # 価格範囲の検証
        if self.PRODUCT_PRICE_MIN >= self.PRODUCT_PRICE_MAX:
            raise ValueError("PRODUCT_PRICE_MIN must be less than PRODUCT_PRICE_MAX")
        
        # WordPress ステータスの検証
        valid_statuses = ["draft", "publish", "private"]
        if self.WP_DEFAULT_STATUS not in valid_statuses:
            raise ValueError(f"WP_DEFAULT_STATUS must be one of {valid_statuses}")
    
    @property
    def is_development(self) -> bool:
        """開発環境かどうかを判定"""
        return self.DEBUG or self.TESTING
    
    @property
    def mountains_file_path(self) -> str:
        """山マスターデータファイルのパス"""
        return os.path.join(self.DATA_DIR, "mountains.json")
    
    @property
    def article_template_path(self) -> str:
        """記事テンプレートファイルのパス"""
        return os.path.join(self.DATA_DIR, "templates", "article_template.yaml")
    
    def get_log_file_path(self, log_name: str = "app") -> str:
        """ログファイルのパスを取得"""
        return os.path.join(self.LOGS_DIR, f"{log_name}.log")
    
    def get_output_file_path(self, filename: str) -> str:
        """出力ファイルのパスを取得"""
        return os.path.join(self.OUTPUT_DIR, filename)
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        
        # 環境変数プレフィックス（オプション）
        # env_prefix = "MOUNTAIN_BLOG_"


# シングルトンインスタンス
_settings_instance: Optional[Settings] = None


def get_settings() -> Settings:
    """設定インスタンスを取得（シングルトンパターン）"""
    global _settings_instance
    if _settings_instance is None:
        _settings_instance = Settings()
    return _settings_instance


def reload_settings() -> Settings:
    """設定を再読み込み"""
    global _settings_instance
    _settings_instance = None
    return get_settings()


# 便利な関数
def is_production() -> bool:
    """本番環境かどうかを判定"""
    return not get_settings().is_development


def get_api_timeout() -> int:
    """API タイムアウト値を取得"""
    return get_settings().API_TIMEOUT


def get_claude_config() -> dict:
    """Claude API 設定を取得"""
    settings = get_settings()
    return {
        "model": settings.CLAUDE_MODEL,
        "max_tokens": settings.CLAUDE_MAX_TOKENS,
        "temperature": settings.CLAUDE_TEMPERATURE,
    }