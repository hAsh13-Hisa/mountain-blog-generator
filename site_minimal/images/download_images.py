#!/usr/bin/env python3
"""
低山ハイキング用フリー画像ダウンロードスクリプト
Unsplash API を使用して高品質な山・ハイキング画像を取得
"""

import requests
import os
from pathlib import Path
import json
import time

# Unsplash API (無料・アクセスキー不要のパブリックAPI)
UNSPLASH_BASE_URL = "https://source.unsplash.com"

class ImageDownloader:
    def __init__(self):
        self.images_dir = Path(__file__).parent
        self.images_dir.mkdir(exist_ok=True)
        
    def download_image(self, query, width, height, filename):
        """Unsplash から画像をダウンロード"""
        url = f"{UNSPLASH_BASE_URL}/{width}x{height}/?{query}"
        
        try:
            print(f"📥 ダウンロード中: {filename}")
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            file_path = self.images_dir / filename
            with open(file_path, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ 保存完了: {file_path}")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"❌ エラー: {filename} - {e}")
            return False
    
    def download_all_images(self):
        """必要な画像をすべてダウンロード"""
        
        images_config = [
            # ヒーロー画像
            {
                "query": "mountain,hiking,japan,forest,trail",
                "width": 1200,
                "height": 800,
                "filename": "hero_mountain_hiking.jpg"
            },
            
            # 山の画像
            {
                "query": "mount,takao,tokyo,hiking,trail",
                "width": 400,
                "height": 300,
                "filename": "mountain_takao.jpg"
            },
            {
                "query": "mount,tsukuba,hiking,view",
                "width": 400,
                "height": 300,
                "filename": "mountain_tsukuba.jpg"
            },
            {
                "query": "mountain,cone,setouchi,kagawa",
                "width": 400,
                "height": 300,
                "filename": "mountain_sanuki.jpg"
            },
            
            # 装備画像
            {
                "query": "hiking,backpack,outdoor,gear",
                "width": 400,
                "height": 300,
                "filename": "equipment_backpack.jpg"
            },
            {
                "query": "hiking,boots,shoes,trail",
                "width": 400,
                "height": 300,
                "filename": "equipment_shoes.jpg"
            },
            {
                "query": "rain,jacket,outdoor,gear",
                "width": 400,
                "height": 300,
                "filename": "equipment_rain.jpg"
            },
            
            # サポート画像
            {
                "query": "hiking,guide,book,map",
                "width": 400,
                "height": 300,
                "filename": "support_guide.jpg"
            },
            {
                "query": "hiking,safety,equipment,first-aid",
                "width": 400,
                "height": 300,
                "filename": "support_safety.jpg"
            },
            {
                "query": "family,hiking,children,nature",
                "width": 400,
                "height": 300,
                "filename": "support_family.jpg"
            },
            
            # 地域画像
            {
                "query": "tokyo,tower,urban,hiking",
                "width": 400,
                "height": 300,
                "filename": "region_kanto.jpg"
            },
            {
                "query": "kyoto,temple,mountain,hiking",
                "width": 400,
                "height": 300,
                "filename": "region_kansai.jpg"
            },
            {
                "query": "kyushu,hot,spring,mountain",
                "width": 400,
                "height": 300,
                "filename": "region_kyushu.jpg"
            }
        ]
        
        print("🏔️ 低山ハイキング画像ダウンロード開始")
        print("=" * 50)
        
        success_count = 0
        total_count = len(images_config)
        
        for i, config in enumerate(images_config, 1):
            print(f"\n[{i}/{total_count}] {config['filename']}")
            
            if self.download_image(
                config['query'],
                config['width'], 
                config['height'],
                config['filename']
            ):
                success_count += 1
            
            # API制限を避けるため少し待機
            time.sleep(1)
        
        print("\n" + "=" * 50)
        print(f"📊 ダウンロード完了: {success_count}/{total_count}")
        
        if success_count == total_count:
            print("🎉 すべての画像のダウンロードが完了しました！")
        else:
            print(f"⚠️  {total_count - success_count}個の画像でエラーが発生しました")
        
        return success_count == total_count

def main():
    downloader = ImageDownloader()
    
    print("📁 保存先ディレクトリ:", downloader.images_dir)
    
    # 既存の画像をチェック
    existing_images = list(downloader.images_dir.glob("*.jpg"))
    if existing_images:
        print(f"🔍 既存の画像: {len(existing_images)}個")
        
        response = input("既存の画像を上書きしますか？ (y/N): ").strip().lower()
        if response not in ['y', 'yes']:
            print("❌ ダウンロードをキャンセルしました")
            return
    
    # ダウンロード実行
    success = downloader.download_all_images()
    
    if success:
        print("\n🚀 次のステップ:")
        print("1. site_minimal/index.html の画像パスを更新")
        print("2. レスポンシブ画像設定を追加")
        print("3. 遅延読み込み実装")
        print("4. alt属性の適切な設定")

if __name__ == "__main__":
    main()