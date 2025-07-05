#!/usr/bin/env python3
"""
記事メタデータJSONを使用して山一覧ページの画像を更新
"""
import json
from pathlib import Path
import re

def update_mountains_list():
    """山一覧ページの画像を記事ページと統一"""
    
    # メタデータ読み込み
    with open('data/article_metadata.json', 'r', encoding='utf-8') as f:
        metadata = json.load(f)
    
    # 山一覧ページの読み込み
    list_page = Path('static_site/mountains/index.html')
    content = list_page.read_text(encoding='utf-8')
    
    print("🔄 山一覧ページの画像を更新中...")
    
    # 各山の画像を更新
    for article_id, article_data in metadata['articles'].items():
        # 現在の画像URLパターンを探す
        pattern = rf'(<a href="{article_data["url"]}"[^>]*>)\s*<img src="[^"]*" alt="{article_data["title"]}"'
        
        # 新しい画像URLに置換
        replacement = rf'\1\n                    <img src="{article_data["featured_image"]}" alt="{article_data["title"]}"'
        
        # 置換実行
        new_content = re.sub(pattern, replacement, content)
        
        if new_content != content:
            print(f"  ✅ {article_data['title']}: {article_data['featured_image']}")
            content = new_content
        else:
            print(f"  ⚠️  {article_data['title']}: パターンが見つかりません")
    
    # ファイル保存
    list_page.write_text(content, encoding='utf-8')
    print("\n✅ 山一覧ページの更新が完了しました！")
    
    return True

def verify_images():
    """画像URLの統一性を確認"""
    
    with open('data/article_metadata.json', 'r', encoding='utf-8') as f:
        metadata = json.load(f)
    
    print("\n🔍 画像URL統一性チェック:")
    
    # 山一覧ページの確認
    list_page = Path('static_site/mountains/index.html')
    list_content = list_page.read_text(encoding='utf-8')
    
    all_match = True
    
    for article_id, article_data in metadata['articles'].items():
        # 記事ページの画像確認
        article_page = Path(f'static_site{article_data["url"]}index.html')
        if article_page.exists():
            article_content = article_page.read_text(encoding='utf-8')
            
            # 記事ページの featured-image を探す
            article_match = re.search(r'class="featured-image"[^>]*src="([^"]*)"', article_content)
            article_image = article_match.group(1) if article_match else "Not found"
            
            # 一覧ページの画像を探す
            list_pattern = rf'href="{article_data["url"]}"[^>]*>.*?<img[^>]*src="([^"]*)"'
            list_match = re.search(list_pattern, list_content, re.DOTALL)
            list_image = list_match.group(1) if list_match else "Not found"
            
            # メタデータと比較
            metadata_image = article_data['featured_image']
            
            if article_image == list_image == metadata_image:
                print(f"  ✅ {article_data['title']}: 統一されています")
            else:
                print(f"  ❌ {article_data['title']}:")
                print(f"     記事ページ: {article_image}")
                print(f"     一覧ページ: {list_image}")
                print(f"     メタデータ: {metadata_image}")
                all_match = False
    
    return all_match

if __name__ == "__main__":
    # 画像を更新
    update_mountains_list()
    
    # 統一性を確認
    if verify_images():
        print("\n✅ 全ての画像が統一されています！")
    else:
        print("\n⚠️  画像の不一致があります。確認してください。")