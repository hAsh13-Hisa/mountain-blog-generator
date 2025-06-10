#!/usr/bin/env python3
"""
記事生成テスト（WordPress投稿なし）
"""
import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from src.application.services import MountainArticleService
from src.infrastructure.repositories import RepositoryFactory

def test_article_generation():
    """記事生成テスト"""
    try:
        print("📝 記事生成テストを開始...")
        
        # 山データ読み込み
        mountain_repo = RepositoryFactory.get_mountain_repository()
        mountains = mountain_repo.get_all()
        
        if not mountains:
            print("❌ 山データが見つかりません")
            return
        
        # 最初の山を選択
        test_mountain = mountains[0]
        print(f"🏔️ テスト対象: {test_mountain.name} ({test_mountain.elevation}m)")
        
        # 記事生成サービス
        service = MountainArticleService()
        
        # 記事生成（WordPress投稿なし）
        print("🚀 記事生成中...")
        print("📊 デバッグモード: Claude APIレスポンスを詳細表示します")
        print("-" * 60)
        
        result = service.create_and_publish_article(
            mountain_id=test_mountain.id,
            theme="初心者向け登山ガイド",
            publish=False  # WordPress投稿しない
        )
        
        print("-" * 60)
        
        if result.success and result.article:
            article = result.article
            print("✅ 記事生成成功!")
            print(f"📌 タイトル: {article.content.title}")
            print(f"📊 文字数: {article.content.get_word_count():,}文字")
            print(f"⏱️ 生成時間: {result.generation_time:.2f}秒")
            print(f"🏷️ タグ: {', '.join(article.content.tags[:3])}...")
            print(f"📝 内容（最初の200文字）:")
            print(f"   {article.content.content[:200]}...")
            
        else:
            print(f"❌ 記事生成失敗: {result.error_message}")
        
    except Exception as e:
        print(f"❌ テスト失敗: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_article_generation()