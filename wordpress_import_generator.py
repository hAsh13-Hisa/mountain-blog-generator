#!/usr/bin/env python3
"""
WordPress インポート用記事生成ツール
WXR形式のXMLファイルを生成して、WordPress管理画面からインポート可能
"""
import sys
import os
import json
from datetime import datetime, timedelta

# プロジェクトルートをパスに追加
sys.path.insert(0, os.path.abspath('.'))

from simple_article_generator import SimpleArticleGenerator
from utils.wordpress_wxr_fixed import generate_valid_wxr

class WordPressImportGenerator:
    """WordPressインポート用ジェネレーター"""
    
    def __init__(self):
        self.generator = SimpleArticleGenerator()
    
    def generate_import_file(self, mountain_ids: list, output_filename: str = None):
        """複数の山の記事を生成してWXR形式で出力"""
        
        if not output_filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_filename = f"wordpress_import_{timestamp}.xml"
        
        print(f"🔧 WordPress インポートファイル生成開始")
        print(f"📋 対象の山: {len(mountain_ids)}件")
        print("=" * 60)
        
        articles_data = []
        
        for i, mountain_id in enumerate(mountain_ids, 1):
            print(f"\n[{i}/{len(mountain_ids)}] {mountain_id}")
            try:
                # 記事を生成
                article = self.generator.generate_single_article(mountain_id)
                if article:
                    articles_data.append(article)
                    print(f"✅ 生成成功")
                else:
                    print(f"❌ 生成失敗")
            except Exception as e:
                print(f"❌ エラー: {e}")
        
        if not articles_data:
            print("\n❌ 記事が生成されませんでした")
            return None
        
        # WXR形式のXMLを生成
        print(f"\n📝 WXR形式XMLファイル作成中...")
        xml_content = generate_valid_wxr(articles_data)
        
        # ファイルに保存
        try:
            with open(output_filename, 'w', encoding='utf-8') as f:
                f.write(xml_content)
            
            print(f"✅ インポートファイル作成完了: {output_filename}")
            print(f"\n📌 WordPressへのインポート方法:")
            print("1. WordPress管理画面にログイン")
            print("2. ツール → インポート → WordPress を選択")
            print("3. 生成されたXMLファイルをアップロード")
            print("4. 記事の投稿者を選択してインポート実行")
            
            return output_filename
            
        except Exception as e:
            print(f"❌ ファイル保存エラー: {e}")
            return None
    
    def generate_scheduled_import(self, mountain_ids: list, start_date: str = None, interval_hours: int = 24):
        """予約投稿用のインポートファイルを生成"""
        
        output_filename = f"wordpress_scheduled_import_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xml"
        
        print(f"🔧 WordPress 予約投稿インポートファイル生成開始")
        print(f"📋 対象の山: {len(mountain_ids)}件")
        print(f"📅 投稿間隔: {interval_hours}時間")
        print("=" * 60)
        
        # 開始時刻の設定
        if start_date:
            start_time = datetime.fromisoformat(start_date)
        else:
            start_time = datetime.now() + timedelta(days=1)  # 明日から開始
        
        articles_data = []
        
        for i, mountain_id in enumerate(mountain_ids, 1):
            print(f"\n[{i}/{len(mountain_ids)}] {mountain_id}")
            try:
                article = self.generator.generate_single_article(mountain_id)
                if article:
                    articles_data.append(article)
                    print(f"✅ 生成成功")
                else:
                    print(f"❌ 生成失敗")
            except Exception as e:
                print(f"❌ エラー: {e}")
        
        if not articles_data:
            print("\n❌ 記事が生成されませんでした")
            return None
        
        # 予約投稿用のWXR XMLを生成
        print(f"\n📝 予約投稿用WXRファイル作成中...")
        xml_content = generate_valid_wxr(articles_data, start_time, interval_hours)
        
        # ファイルに保存
        try:
            with open(output_filename, 'w', encoding='utf-8') as f:
                f.write(xml_content)
            
            print(f"✅ 予約投稿インポートファイル作成完了: {output_filename}")
            print(f"\n📌 インポート時の注意事項:")
            print("- 予約投稿として取り込まれます")
            print(f"- 最初の記事: {start_time.strftime('%Y-%m-%d %H:%M')}")
            print(f"- 投稿間隔: {interval_hours}時間ごと")
            
            return output_filename
            
        except Exception as e:
            print(f"❌ ファイル保存エラー: {e}")
            return None

def main():
    """メイン処理"""
    print("🔧 WordPress インポートファイル生成ツール")
    print("=" * 60)
    
    generator = WordPressImportGenerator()
    
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  即時公開用:")
        print("    python wordpress_import_generator.py <mountain_id1> <mountain_id2> ...")
        print("  予約投稿用:")
        print("    python wordpress_import_generator.py --scheduled <mountain_id1> <mountain_id2> ...")
        print("\n例:")
        print("  python wordpress_import_generator.py mt_takao mt_tsukuba mt_fuji_shizuoka")
        print("  python wordpress_import_generator.py --scheduled mt_takao mt_tsukuba")
        return
    
    # 予約投稿モードかチェック
    if sys.argv[1] == '--scheduled':
        mountain_ids = sys.argv[2:]
        if not mountain_ids:
            print("❌ 山IDを指定してください")
            return
        generator.generate_scheduled_import(mountain_ids)
    else:
        mountain_ids = sys.argv[1:]
        generator.generate_import_file(mountain_ids)

if __name__ == '__main__':
    main()