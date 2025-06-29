#!/usr/bin/env python3
"""
シンプル記事生成ツール（改良版）
複数キーワード対応版
"""
import sys
import os
import json
from datetime import datetime

# プロジェクトルートをパスに追加
sys.path.insert(0, os.path.abspath('.'))

from simple_article_generator import SimpleArticleGenerator

def parse_keywords(keywords_str):
    """キーワード文字列をパース"""
    if not keywords_str:
        return None
    
    # カンマ区切りまたはスペース区切りに対応
    if ',' in keywords_str:
        keywords = [k.strip() for k in keywords_str.split(',')]
    else:
        # スペース区切りの場合、複数単語のキーワードも考慮
        keywords = keywords_str.split()
    
    # 結合してテーマ文字列を作成
    return ' '.join(keywords)

def main():
    """メイン処理"""
    print("🔧 シンプル記事生成ツール（複数キーワード対応版）")
    print("=" * 60)
    
    generator = SimpleArticleGenerator()
    
    # 引数チェック
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python simple_article_generator_v2.py <mountain_id> [キーワード1] [キーワード2] ...")
        print("  python simple_article_generator_v2.py <mountain_id> \"キーワード1,キーワード2\"")
        print("  python simple_article_generator_v2.py --list  # 山一覧を表示")
        print("\n例:")
        print("  python simple_article_generator_v2.py mt_takao 初心者 グルメ カフェ")
        print("  python simple_article_generator_v2.py mt_takao \"初心者,グルメ,カフェ\"")
        print("  python simple_article_generator_v2.py mt_fuji_shizuoka 家族 ご来光 夏")
        return
    
    # 山一覧表示
    if sys.argv[1] == '--list':
        generator.list_available_mountains()
        return
    
    # 記事生成
    mountain_id = sys.argv[1]
    
    # 複数のキーワードを処理
    if len(sys.argv) > 2:
        # 複数引数の場合
        keywords = sys.argv[2:]
        theme = ' '.join(keywords)
    else:
        theme = None
    
    print(f"🎯 対象: {mountain_id}")
    print(f"📝 テーマ: {theme or '自動選択'}")
    if theme and len(theme.split()) > 1:
        print(f"   キーワード: {', '.join(theme.split())}")
    print()
    
    # 記事生成実行
    article_data = generator.generate_single_article(mountain_id, theme)
    
    if article_data:
        print(f"\n🎉 記事生成成功！")
        
        # JSONファイルに保存
        json_filename = generator.save_article_as_json(article_data)
        
        # HTMLプレビューを作成
        html_filename = generator.create_simple_html_preview(article_data)
        
        # XMLファイルも作成
        xml_filename = generator.create_wordpress_xml(article_data)
        
        print(f"\n📄 生成ファイル:")
        if json_filename:
            print(f"  📋 JSON: {json_filename}")
        if html_filename:
            print(f"  🌐 HTML: {html_filename}")
        if xml_filename:
            print(f"  📤 XML: {xml_filename}")
        
        print(f"\n💡 HTMLプレビューをブラウザで開いて確認してください")
        print(f"💡 XMLファイルはWordPressのインポート機能で使用できます")
        
    else:
        print(f"\n❌ 記事生成に失敗しました")

if __name__ == '__main__':
    main()