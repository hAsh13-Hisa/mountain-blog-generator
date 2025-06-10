#!/usr/bin/env python3
"""
Mountain Blog Generator - Web Application
Flask ベースの Web UI
"""
import sys
import os
import json
import traceback
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.exceptions import HTTPException

# プロジェクトルートをパスに追加
sys.path.insert(0, os.path.abspath('../../..'))

from config.settings import get_settings
from config.logging_config import get_logger
from src.application.services import MountainArticleService
from src.infrastructure.repositories import RepositoryFactory
from src.domain.entities import GenerationRequest

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mountain-blog-generator-secret-key'  # 実際の運用では環境変数から取得

# ロガー設定
logger = get_logger("web_app")

# サービス初期化
mountain_service = MountainArticleService()
mountain_repo = RepositoryFactory.get_mountain_repository()

@app.route('/')
def index():
    """メインページ"""
    try:
        mountains = mountain_repo.get_all()
        settings = get_settings()
        
        # 地域でグループ化
        regions = {}
        for mountain in mountains:
            region = mountain.region
            if region not in regions:
                regions[region] = []
            regions[region].append(mountain)
        
        return render_template('index.html', 
                             mountains=mountains,
                             regions=regions,
                             wp_url=settings.WP_URL)
    except Exception as e:
        logger.error(f"Index page error: {e}")
        return render_template('error.html', error=str(e)), 500

@app.route('/api/mountains')
def get_mountains():
    """山データAPI"""
    try:
        mountains = mountain_repo.get_all()
        mountains_data = []
        
        for mountain in mountains:
            mountains_data.append({
                'id': mountain.id,
                'name': mountain.name,
                'name_en': mountain.name_en,
                'prefecture': mountain.prefecture,
                'region': mountain.region,
                'elevation': mountain.elevation,
                'difficulty': {
                    'level': mountain.difficulty.level.value,
                    'hiking_time': mountain.difficulty.hiking_time,
                    'distance': mountain.difficulty.distance
                },
                'features': mountain.features[:3],  # 最初の3つの特徴
                'article_themes': mountain.article_themes[:3]  # 最初の3つのテーマ
            })
        
        return jsonify({
            'success': True,
            'mountains': mountains_data,
            'total': len(mountains_data)
        })
    except Exception as e:
        logger.error(f"Mountains API error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/mountain/<mountain_id>')
def get_mountain_detail(mountain_id):
    """山詳細情報API"""
    try:
        mountain = mountain_repo.get_by_id(mountain_id)
        if not mountain:
            return jsonify({'success': False, 'error': '山が見つかりません'}), 404
        
        mountain_data = {
            'id': mountain.id,
            'name': mountain.name,
            'name_en': mountain.name_en,
            'prefecture': mountain.prefecture,
            'region': mountain.region,
            'elevation': mountain.elevation,
            'description': getattr(mountain, 'description', ''),
            'difficulty': {
                'level': mountain.difficulty.level.value,
                'hiking_time': mountain.difficulty.hiking_time,
                'distance': mountain.difficulty.distance,
                'elevation_gain': mountain.difficulty.elevation_gain
            },
            'location': {
                'nearest_station': getattr(mountain.location, 'nearest_station', ''),
                'access_time': getattr(mountain.location, 'access_time', ''),
                'driving_time': getattr(mountain.location, 'driving_time', ''),
                'parking_info': getattr(mountain.location, 'parking_info', '')
            },
            'features': getattr(mountain, 'features', []),
            'facilities': getattr(mountain, 'facilities', []),
            'article_themes': getattr(mountain, 'article_themes', []),
            'best_seasons': getattr(mountain, 'best_seasons', [])
        }
        
        return jsonify({
            'success': True,
            'mountain': mountain_data
        })
    except Exception as e:
        logger.error(f"Mountain detail API error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/generate', methods=['POST'])
def generate_article():
    """記事生成API"""
    try:
        data = request.json
        mountain_id = data.get('mountain_id')
        theme = data.get('theme')
        publish = data.get('publish', False)
        
        if not mountain_id:
            return jsonify({'success': False, 'error': '山IDが必要です'}), 400
        
        logger.info(f"Article generation request: {mountain_id}, theme: {theme}")
        
        # 記事生成実行
        result = mountain_service.create_and_publish_article(
            mountain_id=mountain_id,
            theme=theme if theme else None,
            publish=publish
        )
        
        if result.success and result.article:
            article_data = {
                'id': result.article.id,
                'mountain': {
                    'id': result.article.mountain.id,
                    'name': result.article.mountain.name,
                    'elevation': result.article.mountain.elevation
                },
                'content': {
                    'title': result.article.content.title,
                    'content': result.article.content.content,
                    'excerpt': result.article.content.excerpt,
                    'tags': result.article.content.tags,
                    'word_count': result.article.content.get_word_count()
                },
                'featured_image': {
                    'url': None,  # 一時的に無効化
                    'alt_text': None
                },
                'wordpress_id': result.article.wordpress_id,
                'created_at': result.article.created_at.isoformat() if result.article.created_at else None
            }
            
            return jsonify({
                'success': True,
                'article': article_data,
                'generation_time': round(result.generation_time, 2),
                'published': bool(result.article.wordpress_id)
            })
        else:
            error_msg = result.error_message or '記事生成に失敗しました'
            logger.error(f"Article generation failed: {error_msg}")
            return jsonify({'success': False, 'error': error_msg}), 500
            
    except Exception as e:
        logger.error(f"Generate article API error: {e}")
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/download/<article_id>')
def download_article(article_id):
    """記事ダウンロード"""
    try:
        # 簡易実装: セッションから記事データを取得
        # 実際の実装では記事IDからDBまたはキャッシュから取得
        return jsonify({'success': False, 'error': 'ダウンロード機能は開発中です'}), 501
    except Exception as e:
        logger.error(f"Download article error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/health')
def health_check():
    """ヘルスチェック"""
    try:
        mountains_count = len(mountain_repo.get_all())
        settings = get_settings()
        
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'mountains_loaded': mountains_count,
            'wordpress_configured': bool(settings.WP_URL and settings.WP_USERNAME),
            'claude_configured': bool(settings.ANTHROPIC_API_KEY),
            'rakuten_configured': bool(settings.RAKUTEN_APP_ID)
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500

@app.errorhandler(404)
def not_found_error(error):
    """404エラーハンドラー"""
    return render_template('error.html', 
                         error='ページが見つかりません',
                         error_code=404), 404

@app.errorhandler(500)
def internal_error(error):
    """500エラーハンドラー"""
    logger.error(f"Internal server error: {error}")
    return render_template('error.html', 
                         error='サーバー内部エラーが発生しました',
                         error_code=500), 500

@app.errorhandler(Exception)
def handle_exception(e):
    """一般例外ハンドラー"""
    if isinstance(e, HTTPException):
        return e
    
    logger.error(f"Unhandled exception: {e}")
    traceback.print_exc()
    return render_template('error.html', 
                         error='予期しないエラーが発生しました',
                         error_code=500), 500

if __name__ == '__main__':
    print("🌐 Mountain Blog Generator Web UI")
    print("📍 URL: http://localhost:5001")
    print("📋 Health Check: http://localhost:5001/health")
    print("🔧 Debug mode: ON")
    
    app.run(debug=True, host='0.0.0.0', port=5001)