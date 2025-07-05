#!/usr/bin/env python3
"""
完全ワークフロー: 山データ → 記事生成 → 静的サイト → FTPデプロイ
"""
import json
import os
from pathlib import Path
from datetime import datetime
from article_generator import ArticleGenerator
from unified_deploy import UnifiedDeploySystem

class MountainBlogWorkflow:
    def __init__(self):
        self.article_gen = ArticleGenerator()
        self.deployer = UnifiedDeploySystem()
        self.mountains_data = Path("data/mountains_japan_expanded.json")
        self.generated_dir = Path("data/articles")
        
        # 記事保存ディレクトリ作成
        self.generated_dir.mkdir(exist_ok=True)
    
    def generate_and_deploy_article(self, mountain_id):
        """指定した山の記事を生成してデプロイ"""
        print(f"=== 山記事の生成とデプロイ: {mountain_id} ===")
        
        # 1. 山データ読み込み
        with open(self.mountains_data, 'r', encoding='utf-8') as f:
            mountains = json.load(f)
        
        # 指定の山を検索
        target_mountain = None
        for mountain in mountains['mountains']:
            if mountain['id'] == mountain_id:
                target_mountain = mountain
                break
        
        if not target_mountain:
            print(f"山ID '{mountain_id}' が見つかりません")
            return False
        
        print(f"対象の山: {target_mountain['name']} ({target_mountain['elevation']}m)")
        
        # 2. 記事生成
        print("記事生成中...")
        article_data = self.article_gen.generate_article(target_mountain)
        
        # 3. 記事JSONファイル保存
        article_file = self.generated_dir / f"{mountain_id}.json"
        with open(article_file, 'w', encoding='utf-8') as f:
            json.dump(article_data, f, ensure_ascii=False, indent=2)
        
        print(f"記事保存: {article_file}")
        
        # 4. 静的サイト生成とFTPデプロイ
        self.deployer.deploy_article(article_file)
        
        return True
    
    def deploy_existing_articles(self):
        """既存の記事JSONファイルを全てデプロイ"""
        print("=== 既存記事の一括デプロイ ===")
        
        article_files = list(self.generated_dir.glob("*.json"))
        if not article_files:
            print("デプロイする記事がありません")
            return
        
        print(f"{len(article_files)}件の記事をデプロイします")
        
        for article_file in article_files:
            try:
                print(f"デプロイ中: {article_file.name}")
                self.deployer.deploy_article(article_file)
            except Exception as e:
                print(f"エラー: {article_file.name} - {e}")
                continue
        
        print("一括デプロイ完了")
    
    def list_available_mountains(self):
        """デプロイ可能な山のリストを表示"""
        with open(self.mountains_data, 'r', encoding='utf-8') as f:
            mountains = json.load(f)
        
        print("=== 利用可能な山 ===")
        for mountain in mountains['mountains']:
            status = "✓" if (self.generated_dir / f"{mountain['id']}.json").exists() else "○"
            print(f"{status} {mountain['id']}: {mountain['name']} ({mountain['elevation']}m) - {mountain['prefecture']}")
        
        print("\n✓ = 記事生成済み, ○ = 未生成")
    
    def batch_generate_region(self, region_name):
        """特定地域の山を一括生成・デプロイ"""
        print(f"=== {region_name}地域の一括生成・デプロイ ===")
        
        with open(self.mountains_data, 'r', encoding='utf-8') as f:
            mountains = json.load(f)
        
        target_mountains = [m for m in mountains['mountains'] if m['region'] == region_name]
        
        if not target_mountains:
            print(f"地域'{region_name}'の山が見つかりません")
            return
        
        print(f"{len(target_mountains)}件の山を処理します")
        
        for mountain in target_mountains:
            try:
                self.generate_and_deploy_article(mountain['id'])
                print(f"完了: {mountain['name']}")
            except Exception as e:
                print(f"エラー: {mountain['name']} - {e}")
                continue
        
        print(f"{region_name}地域の一括処理完了")

# メイン処理
if __name__ == "__main__":
    import sys
    from dotenv import load_dotenv
    
    load_dotenv()
    
    workflow = MountainBlogWorkflow()
    
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python deploy_workflow.py list                    # 利用可能な山をリスト")
        print("  python deploy_workflow.py generate <mountain_id>  # 特定の山の記事生成・デプロイ")
        print("  python deploy_workflow.py deploy                  # 既存記事の一括デプロイ")
        print("  python deploy_workflow.py region <region_name>    # 地域別一括処理")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "list":
        workflow.list_available_mountains()
    elif command == "generate" and len(sys.argv) > 2:
        workflow.generate_and_deploy_article(sys.argv[2])
    elif command == "deploy":
        workflow.deploy_existing_articles()
    elif command == "region" and len(sys.argv) > 2:
        workflow.batch_generate_region(sys.argv[2])
    else:
        print("コマンドが不正です")