"""
ログ設定
"""
import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Optional
import colorlog
from .settings import get_settings


def setup_logging(
    name: str = "mountain_blog",
    log_file: Optional[str] = None,
    console_output: bool = True,
    file_output: bool = True
) -> logging.Logger:
    """
    ログシステムをセットアップ
    
    Args:
        name: ロガー名
        log_file: ログファイル名（Noneの場合はデフォルト）
        console_output: コンソール出力の有効/無効
        file_output: ファイル出力の有効/無効
        
    Returns:
        設定済みのロガー
    """
    settings = get_settings()
    
    # ロガーを取得
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, settings.LOG_LEVEL))
    
    # 既存のハンドラーをクリア
    logger.handlers.clear()
    
    # フォーマッターの設定
    detailed_formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # コンソール用カラーフォーマッター
    color_formatter = colorlog.ColoredFormatter(
        fmt="%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%H:%M:%S",
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        }
    )
    
    # コンソールハンドラー
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO if not settings.DEBUG else logging.DEBUG)
        console_handler.setFormatter(color_formatter)
        logger.addHandler(console_handler)
    
    # ファイルハンドラー
    if file_output:
        if log_file is None:
            log_file = settings.get_log_file_path(name)
        
        # ログディレクトリの作成
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        
        # 回転ファイルハンドラー（最大10MB、5ファイルまでバックアップ）
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(detailed_formatter)
        logger.addHandler(file_handler)
    
    # プロパゲーションを無効化（重複ログを防ぐ）
    logger.propagate = False
    
    return logger


def get_logger(name: str = "mountain_blog") -> logging.Logger:
    """
    ロガーを取得（既に設定済みの場合はそのまま返す）
    
    Args:
        name: ロガー名
        
    Returns:
        ロガー
    """
    logger = logging.getLogger(name)
    
    # まだ設定されていない場合は設定
    if not logger.handlers:
        logger = setup_logging(name)
    
    return logger


def setup_api_logger() -> logging.Logger:
    """API通信専用のロガーをセットアップ"""
    return setup_logging("mountain_blog.api")


def setup_article_logger() -> logging.Logger:
    """記事生成専用のロガーをセットアップ"""
    return setup_logging("mountain_blog.article")


def setup_scheduler_logger() -> logging.Logger:
    """スケジューラー専用のロガーをセットアップ"""
    return setup_logging("mountain_blog.scheduler")


class LoggerMixin:
    """
    ロガーミックスイン（クラスにログ機能を追加）
    """
    
    @property
    def logger(self) -> logging.Logger:
        """クラス名に基づいたロガーを取得"""
        class_name = self.__class__.__name__
        return get_logger(f"mountain_blog.{class_name.lower()}")
    
    def log_info(self, message: str, **kwargs):
        """INFO レベルでログ出力"""
        self.logger.info(message, extra=kwargs)
    
    def log_debug(self, message: str, **kwargs):
        """DEBUG レベルでログ出力"""
        self.logger.debug(message, extra=kwargs)
    
    def log_warning(self, message: str, **kwargs):
        """WARNING レベルでログ出力"""
        self.logger.warning(message, extra=kwargs)
    
    def log_error(self, message: str, error: Exception = None, **kwargs):
        """ERROR レベルでログ出力"""
        if error:
            kwargs['error_type'] = type(error).__name__
            kwargs['error_message'] = str(error)
        self.logger.error(message, extra=kwargs, exc_info=error is not None)
    
    def log_critical(self, message: str, error: Exception = None, **kwargs):
        """CRITICAL レベルでログ出力"""
        if error:
            kwargs['error_type'] = type(error).__name__
            kwargs['error_message'] = str(error)
        self.logger.critical(message, extra=kwargs, exc_info=error is not None)


def log_function_call(logger: logging.Logger = None):
    """
    関数呼び出しをログに記録するデコレータ
    
    Args:
        logger: 使用するロガー（Noneの場合はデフォルト）
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            if logger is None:
                log = get_logger()
            else:
                log = logger
            
            # 関数開始ログ
            log.debug(f"Function {func.__name__} started with args={args}, kwargs={kwargs}")
            
            try:
                result = func(*args, **kwargs)
                log.debug(f"Function {func.__name__} completed successfully")
                return result
            except Exception as e:
                log.error(f"Function {func.__name__} failed with error: {e}", exc_info=True)
                raise
        
        return wrapper
    return decorator


def log_api_call(api_name: str, logger: logging.Logger = None):
    """
    API呼び出しをログに記録するデコレータ
    
    Args:
        api_name: API名
        logger: 使用するロガー
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            if logger is None:
                log = setup_api_logger()
            else:
                log = logger
            
            log.info(f"API call started: {api_name}")
            
            try:
                result = func(*args, **kwargs)
                log.info(f"API call completed: {api_name}")
                return result
            except Exception as e:
                log.error(f"API call failed: {api_name} - {e}", exc_info=True)
                raise
        
        return wrapper
    return decorator


# デフォルトロガーの初期化
def initialize_logging():
    """アプリケーション起動時のログ初期化"""
    # メインロガー
    main_logger = setup_logging()
    main_logger.info("Logging system initialized")
    
    # 各種専用ロガー
    setup_api_logger()
    setup_article_logger()
    setup_scheduler_logger()
    
    return main_logger