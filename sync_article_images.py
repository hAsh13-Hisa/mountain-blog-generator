#!/usr/bin/env python3
"""
記事メタデータJSONを基に、記事ページと一覧ページの画像を同期
"""
import json
from pathlib import Path
import re

class ArticleImageSynchronizer:
    def __init__(self):
        self.metadata_file = Path('data/article_metadata.json')
        self.static_dir = Path('static_site')
        
    def load_metadata(self):
        """記事メタデータを読み込み"""
        with open(self.metadata_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save_metadata(self, metadata):
        """記事メタデータを保存"""
        with open(self.metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    def extract_article_images(self):
        """各記事ページから現在の画像URLを抽出"""
        metadata = self.load_metadata()
        updated = False
        
        print("📸 記事ページから画像URLを抽出中...")
        
        for article_id, article_data in metadata['articles'].items():
            article_path = self.static_dir / article_data['url'].strip('/') / 'index.html'
            
            if article_path.exists():
                content = article_path.read_text(encoding='utf-8')
                
                # featured-image クラスの画像を探す
                match = re.search(r'<img[^>]*src="([^"]*)"[^>]*class="featured-image"', content)
                if match:
                    current_image = match.group(1)
                    if current_image != article_data.get('featured_image'):
                        print(f"  📷 {article_data['title']}: 画像URL更新")
                        print(f"     旧: {article_data.get('featured_image', 'なし')}")
                        print(f"     新: {current_image}")
                        article_data['featured_image'] = current_image
                        updated = True
        
        if updated:
            self.save_metadata(metadata)
            print("✅ メタデータを更新しました")
        else:
            print("✅ 全ての画像URLは最新です")
        
        return metadata
    
    def sync_list_page(self, metadata=None):
        """一覧ページの画像をメタデータと同期"""
        if metadata is None:
            metadata = self.load_metadata()
        
        list_page = self.static_dir / 'mountains' / 'index.html'
        content = list_page.read_text(encoding='utf-8')
        updated_content = content
        
        print("\n🔄 山一覧ページの画像を同期中...")
        
        for article_id, article_data in metadata['articles'].items():
            # 現在の画像URLを探して置換
            pattern = rf'(<a href="{article_data["url"]}"[^>]*>)\s*<img[^>]*src="[^"]*"([^>]*alt="{re.escape(article_data["title"])}")'
            replacement = rf'\1\n                    <img src="{article_data["featured_image"]}"\2'
            
            new_content = re.sub(pattern, replacement, updated_content, flags=re.DOTALL)
            
            if new_content != updated_content:
                print(f"  ✅ {article_data['title']}: 同期完了")
                updated_content = new_content
            else:
                # alt属性に（）が含まれる場合の対応
                alt_variations = [
                    article_data["title"],
                    article_data["title"].split("（")[0],  # （）を除去
                    article_data.get("subtitle", "").split("】")[-1].strip()  # サブタイトルから取得
                ]
                
                for alt_text in alt_variations:
                    pattern = rf'(<a href="{article_data["url"]}"[^>]*>)\s*<img[^>]*src="[^"]*"([^>]*alt="{re.escape(alt_text)}")'
                    new_content = re.sub(pattern, replacement, updated_content, flags=re.DOTALL)
                    
                    if new_content != updated_content:
                        print(f"  ✅ {article_data['title']}: 同期完了 (alt: {alt_text})")
                        updated_content = new_content
                        break
                else:
                    print(f"  ⚠️  {article_data['title']}: パターンが見つかりません")
        
        if updated_content != content:
            list_page.write_text(updated_content, encoding='utf-8')
            print("\n✅ 山一覧ページを更新しました")
        else:
            print("\n✅ 山一覧ページは既に最新です")
    
    def verify_sync(self):
        """同期状態を確認"""
        metadata = self.load_metadata()
        list_page = self.static_dir / 'mountains' / 'index.html'
        list_content = list_page.read_text(encoding='utf-8')
        
        print("\n🔍 画像同期状態の確認:")
        all_synced = True
        
        for article_id, article_data in metadata['articles'].items():
            # 記事ページの画像
            article_path = self.static_dir / article_data['url'].strip('/') / 'index.html'
            article_image = "不明"
            
            if article_path.exists():
                article_content = article_path.read_text(encoding='utf-8')
                match = re.search(r'<img[^>]*src="([^"]*)"[^>]*class="featured-image"', article_content)
                if match:
                    article_image = match.group(1)
            
            # 一覧ページの画像
            list_pattern = rf'href="{article_data["url"]}"[^>]*>.*?<img[^>]*src="([^"]*)"'
            list_match = re.search(list_pattern, list_content, re.DOTALL)
            list_image = list_match.group(1) if list_match else "不明"
            
            # メタデータの画像
            metadata_image = article_data.get('featured_image', '未設定')
            
            if article_image == list_image == metadata_image:
                print(f"  ✅ {article_data['title']}: 完全同期")
            else:
                print(f"  ❌ {article_data['title']}:")
                print(f"     記事ページ: {article_image}")
                print(f"     一覧ページ: {list_image}")
                print(f"     メタデータ: {metadata_image}")
                all_synced = False
        
        return all_synced

def main():
    """メイン処理"""
    syncer = ArticleImageSynchronizer()
    
    # 1. 記事ページから画像URLを抽出してメタデータ更新
    metadata = syncer.extract_article_images()
    
    # 2. 一覧ページを同期
    syncer.sync_list_page(metadata)
    
    # 3. 同期状態を確認
    if syncer.verify_sync():
        print("\n✅ 全ての画像が完全に同期されています！")
    else:
        print("\n⚠️  同期に問題があります。確認してください。")

if __name__ == "__main__":
    main()