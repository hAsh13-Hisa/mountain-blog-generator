#!/usr/bin/env python3
"""
シンプル記事生成ツール（予約投稿機能なし）
基本的な単発記事生成機能に戻す
"""
import sys
import os
import json
from datetime import datetime

# プロジェクトルートをパスに追加
sys.path.insert(0, os.path.abspath('.'))

from config.settings import get_settings
from config.logging_config import get_logger
from src.application.services import ArticleGenerationService, ImageService, AffiliateService
from src.infrastructure.repositories import RepositoryFactory
from src.domain.entities import GenerationRequest

logger = get_logger("simple_generator")

class SimpleArticleGenerator:
    """シンプルな記事生成クラス"""
    
    def __init__(self):
        self.settings = get_settings()
        self.article_service = ArticleGenerationService()
        self.image_service = ImageService()
        self.affiliate_service = AffiliateService()
        self.mountain_repo = RepositoryFactory.get_mountain_repository()
    
    def generate_single_article(self, mountain_id: str, theme: str = None) -> dict:
        """単一記事を生成"""
        print(f"🔧 記事生成開始: {mountain_id}")
        
        try:
            # 山データを取得
            mountain = self.mountain_repo.get_by_id(mountain_id)
            if not mountain:
                raise Exception(f"山が見つかりません: {mountain_id}")
            
            print(f"🏔️ 山: {mountain.name} ({mountain.elevation}m)")
            
            # 記事生成リクエストを作成
            request = GenerationRequest(
                mountain_id=mountain_id,
                theme=theme or "初心者向け登山ガイド",
                target_length=2000,
                publish=False
            )
            
            # 記事を生成
            print("📝 記事生成中...")
            result = self.article_service.generate_article(request)
            
            if not result.success:
                raise Exception(f"記事生成エラー: {result.error_message}")
            
            article = result.article
            print(f"✅ 記事生成完了 ({result.generation_time:.2f}秒)")
            print(f"   タイトル: {article.content.title}")
            print(f"   文字数: {len(article.content.content)}文字")
            
            # アイキャッチ画像を取得
            print("🖼️ アイキャッチ画像取得中...")
            featured_image = self.image_service.get_featured_image(mountain)
            
            # アフィリエイト商品を取得
            print("🛒 アフィリエイト商品取得中...")
            products = self.affiliate_service.get_hiking_products(mountain)
            
            # アフィリエイトリンクを記事に埋め込み
            content_with_affiliates = self._embed_affiliates_in_content(
                article.content.content, 
                products
            )
            
            # 結果をまとめる
            article_data = {
                "mountain_name": mountain.name,
                "mountain_id": mountain.id,
                "elevation": mountain.elevation,
                "prefecture": mountain.prefecture,
                "title": article.content.title,
                "content": content_with_affiliates,
                "excerpt": article.content.excerpt,
                "tags": article.content.tags,
                "featured_image_url": featured_image.url if featured_image else None,
                "featured_image_alt": featured_image.alt_text if featured_image else None,
                "products_count": len(products),
                "generation_time": result.generation_time,
                "created_at": datetime.now().isoformat()
            }
            
            print(f"🖼️ アイキャッチ画像: {'✅' if featured_image else '❌'}")
            print(f"🛒 アフィリエイト商品: {len(products)}件")
            
            return article_data
            
        except Exception as e:
            logger.error(f"記事生成エラー: {e}")
            print(f"❌ エラー: {e}")
            return None
    
    def _embed_affiliates_in_content(self, content: str, products: list) -> str:
        """アフィリエイトリンクを記事に埋め込み"""
        if not products:
            return content
        
        # 記事の最後にアフィリエイトセクションを追加
        affiliate_section = "\n\n<h3>おすすめの登山用品・宿泊施設</h3>\n\n<h4>登山用品</h4>\n<ul>\n"
        
        for product in products:
            affiliate_section += f'<li><a href="{product.url}" target="_blank" rel="noopener">{product.name}</a> - ¥{product.price:,}</li>\n'
        
        affiliate_section += "</ul>\n"
        
        return content + affiliate_section
    
    def list_available_mountains(self):
        """利用可能な山一覧を表示"""
        mountains = self.mountain_repo.get_all()
        
        print(f"\n📋 利用可能な山: {len(mountains)}件")
        print("=" * 60)
        
        # 地域別にグループ化
        regions = {}
        for mountain in mountains:
            region = mountain.region
            if region not in regions:
                regions[region] = []
            regions[region].append(mountain)
        
        for region, region_mountains in regions.items():
            print(f"\n🌍 {region} ({len(region_mountains)}件)")
            print("-" * 30)
            
            for mountain in region_mountains[:5]:  # 各地域最大5件表示
                difficulty = mountain.difficulty.level.value
                print(f"  🏔️ {mountain.name} ({mountain.elevation}m) - {difficulty}")
                print(f"     ID: {mountain.id}")
            
            if len(region_mountains) > 5:
                print(f"     ... 他{len(region_mountains) - 5}件")
    
    def save_article_as_json(self, article_data: dict, filename: str = None):
        """記事をJSONファイルに保存"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            mountain_name = article_data.get('mountain_name', 'unknown')
            filename = f"article_{mountain_name}_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(article_data, f, ensure_ascii=False, indent=2)
            
            print(f"💾 記事保存: {filename}")
            return filename
            
        except Exception as e:
            print(f"❌ 保存エラー: {e}")
            return None
    
    def create_simple_html_preview(self, article_data: dict, filename: str = None):
        """シンプルなHTMLプレビューを作成"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            mountain_name = article_data.get('mountain_name', 'unknown')
            filename = f"preview_{mountain_name}_{timestamp}.html"
        
        html_content = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{article_data['title']}</title>
    <style>
        body {{ font-family: 'Helvetica Neue', Arial, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px; }}
        h1, h2, h3 {{ color: #333; }}
        .meta {{ background: #f5f5f5; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
        .meta span {{ display: inline-block; margin-right: 15px; }}
        .featured-image {{ text-align: center; margin: 20px 0; }}
        .featured-image img {{ max-width: 100%; height: auto; border-radius: 8px; }}
        .content {{ margin: 20px 0; }}
        .tags {{ margin-top: 20px; }}
        .tag {{ background: #007cba; color: white; padding: 3px 8px; border-radius: 3px; margin-right: 5px; font-size: 0.9em; }}
    </style>
</head>
<body>
    <h1>{article_data['title']}</h1>
    
    <div class="meta">
        <span>🏔️ <strong>{article_data['mountain_name']}</strong></span>
        <span>📏 <strong>{article_data['elevation']}m</strong></span>
        <span>📍 <strong>{article_data['prefecture']}</strong></span>
        <span>📝 <strong>{len(article_data['content'])}文字</strong></span>
        <span>🛒 <strong>{article_data['products_count']}商品</strong></span>
    </div>
    
    {f'<div class="featured-image"><img src="{article_data["featured_image_url"]}" alt="{article_data["featured_image_alt"]}" /></div>' if article_data.get('featured_image_url') else ''}
    
    <div class="content">
        {article_data['content']}
    </div>
    
    <div class="tags">
        {''.join([f'<span class="tag">{tag}</span>' for tag in article_data['tags']])}
    </div>
    
    <hr style="margin: 30px 0;">
    <p><strong>概要:</strong> {article_data['excerpt']}</p>
    <p><small>生成時間: {article_data['generation_time']:.2f}秒 | 作成日時: {article_data['created_at']}</small></p>
</body>
</html>"""
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"🌐 HTMLプレビュー作成: {filename}")
            return filename
            
        except Exception as e:
            print(f"❌ HTMLプレビュー作成エラー: {e}")
            return None

def main():
    """メイン処理"""
    print("🔧 シンプル記事生成ツール")
    print("=" * 60)
    
    generator = SimpleArticleGenerator()
    
    # 引数チェック
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python simple_article_generator.py <mountain_id> [theme]")
        print("  python simple_article_generator.py --list  # 山一覧を表示")
        print("\n例:")
        print("  python simple_article_generator.py mt_takao")
        print("  python simple_article_generator.py mt_takao '初心者向け登山ガイド'")
        return
    
    # 山一覧表示
    if sys.argv[1] == '--list':
        generator.list_available_mountains()
        return
    
    # 記事生成
    mountain_id = sys.argv[1]
    theme = sys.argv[2] if len(sys.argv) > 2 else None
    
    print(f"🎯 対象: {mountain_id}")
    print(f"📝 テーマ: {theme or '自動選択'}")
    print()
    
    # 記事生成実行
    article_data = generator.generate_single_article(mountain_id, theme)
    
    if article_data:
        print(f"\n🎉 記事生成成功！")
        
        # JSONファイルに保存
        json_filename = generator.save_article_as_json(article_data)
        
        # HTMLプレビューを作成
        html_filename = generator.create_simple_html_preview(article_data)
        
        print(f"\n📄 生成ファイル:")
        if json_filename:
            print(f"  📋 JSON: {json_filename}")
        if html_filename:
            print(f"  🌐 HTML: {html_filename}")
        
        print(f"\n💡 HTMLプレビューをブラウザで開いて確認してください")
        
    else:
        print(f"\n❌ 記事生成に失敗しました")

if __name__ == '__main__':
    main()