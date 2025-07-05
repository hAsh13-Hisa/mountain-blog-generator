#!/usr/bin/env python3
"""
低山ハイキング用SVGイラスト生成スクリプト
美しいベクター画像でテーマに合ったビジュアルを作成
"""

import os
from pathlib import Path

class SVGImageCreator:
    def __init__(self):
        self.images_dir = Path(__file__).parent
        self.images_dir.mkdir(exist_ok=True)
    
    def create_hero_image(self):
        """ヒーローエリア用の山とハイキング道のイラスト"""
        svg_content = '''
<svg width="1200" height="800" viewBox="0 0 1200 800" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="skyGradient" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#87CEEB;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#E0F6FF;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="mountainGradient" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#2d5016;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#4a7c59;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="trailGradient" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#8B4513;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#A0522D;stop-opacity:1" />
    </linearGradient>
  </defs>
  
  <!-- 空 -->
  <rect width="1200" height="800" fill="url(#skyGradient)"/>
  
  <!-- 雲 -->
  <ellipse cx="200" cy="150" rx="60" ry="30" fill="white" opacity="0.8"/>
  <ellipse cx="230" cy="140" rx="40" ry="25" fill="white" opacity="0.8"/>
  <ellipse cx="180" cy="160" rx="45" ry="20" fill="white" opacity="0.8"/>
  
  <ellipse cx="800" cy="100" rx="50" ry="25" fill="white" opacity="0.7"/>
  <ellipse cx="820" cy="95" rx="35" ry="20" fill="white" opacity="0.7"/>
  
  <!-- 遠景の山々 -->
  <polygon points="0,500 200,300 400,400 600,250 800,350 1000,280 1200,400 1200,800 0,800" 
           fill="#6B8E6B" opacity="0.6"/>
  
  <!-- 中景の山 -->
  <polygon points="100,600 300,400 500,450 700,350 900,380 1100,320 1200,400 1200,800 0,800" 
           fill="#4a7c59" opacity="0.8"/>
  
  <!-- 前景の山 -->
  <polygon points="0,700 250,500 450,550 650,480 850,520 1050,460 1200,500 1200,800 0,800" 
           fill="url(#mountainGradient)"/>
  
  <!-- ハイキング道 -->
  <path d="M 50 750 Q 200 650 350 680 T 650 620 Q 800 610 950 650 T 1200 680" 
        stroke="url(#trailGradient)" stroke-width="15" fill="none" opacity="0.7"/>
  
  <!-- 木々 -->
  <circle cx="150" cy="620" r="25" fill="#2d5016"/>
  <rect x="145" y="620" width="10" height="40" fill="#8B4513"/>
  
  <circle cx="320" cy="580" r="30" fill="#2d5016"/>
  <rect x="315" y="580" width="10" height="45" fill="#8B4513"/>
  
  <circle cx="750" cy="540" r="35" fill="#2d5016"/>
  <rect x="745" y="540" width="10" height="50" fill="#8B4513"/>
  
  <!-- ハイカーシルエット -->
  <g transform="translate(400, 650)">
    <circle cx="0" cy="-30" r="8" fill="#2c3e50"/>
    <rect x="-5" y="-22" width="10" height="25" fill="#3498db"/>
    <rect x="-3" y="3" width="6" height="20" fill="#2c3e50"/>
    <rect x="-8" y="-15" width="16" height="8" fill="#e74c3c"/>
    <circle cx="6" cy="-18" r="4" fill="#8B4513"/>
  </g>
  
  <!-- 太陽 -->
  <circle cx="1000" cy="150" r="40" fill="#FFD700" opacity="0.8"/>
  
  <!-- 鳥 -->
  <path d="M 600 200 Q 605 195 610 200 Q 605 205 600 200" stroke="#2c3e50" stroke-width="2" fill="none"/>
  <path d="M 650 180 Q 655 175 660 180 Q 655 185 650 180" stroke="#2c3e50" stroke-width="2" fill="none"/>
</svg>'''
        
        with open(self.images_dir / "hero_mountain_hiking.svg", 'w', encoding='utf-8') as f:
            f.write(svg_content)
        print("✅ ヒーロー画像作成完了: hero_mountain_hiking.svg")
    
    def create_mountain_card(self, mountain_name, filename):
        """山カード用のイラスト"""
        svg_content = f'''
<svg width="400" height="300" viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="skyGrad_{filename}" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#87CEEB;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#E0F6FF;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="mountGrad_{filename}" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#2d5016;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#4a7c59;stop-opacity:1" />
    </linearGradient>
  </defs>
  
  <!-- 空 -->
  <rect width="400" height="300" fill="url(#skyGrad_{filename})"/>
  
  <!-- 山の形状（山によって変える） -->
  <polygon points="0,250 80,120 160,140 240,100 320,130 400,110 400,300 0,300" 
           fill="url(#mountGrad_{filename})"/>
  
  <!-- 緑の装飾 -->
  <circle cx="60" cy="220" r="15" fill="#2d5016"/>
  <circle cx="300" cy="200" r="18" fill="#2d5016"/>
  <circle cx="350" cy="190" r="12" fill="#2d5016"/>
  
  <!-- 雲 -->
  <ellipse cx="100" cy="60" rx="25" ry="15" fill="white" opacity="0.7"/>
  <ellipse cx="300" cy="50" rx="30" ry="18" fill="white" opacity="0.7"/>
  
  <!-- 山名テキスト -->
  <text x="200" y="280" text-anchor="middle" fill="#2c3e50" font-family="Arial, sans-serif" 
        font-size="16" font-weight="bold">{mountain_name}</text>
</svg>'''
        
        with open(self.images_dir / f"{filename}.svg", 'w', encoding='utf-8') as f:
            f.write(svg_content)
        print(f"✅ 山画像作成完了: {filename}.svg")
    
    def create_equipment_card(self, equipment_type, icon, filename):
        """装備カード用のイラスト"""
        icons = {
            "backpack": "🎒",
            "shoes": "👟", 
            "rain": "🧥"
        }
        
        svg_content = f'''
<svg width="400" height="300" viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bgGrad_{filename}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#e8f5e8;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#f4f9f4;stop-opacity:1" />
    </linearGradient>
    <radialGradient id="centerGlow_{filename}" cx="50%" cy="50%" r="50%">
      <stop offset="0%" style="stop-color:#ffffff;stop-opacity:0.8" />
      <stop offset="100%" style="stop-color:#e8f5e8;stop-opacity:0.2" />
    </radialGradient>
  </defs>
  
  <!-- 背景 -->
  <rect width="400" height="300" fill="url(#bgGrad_{filename})"/>
  <circle cx="200" cy="150" r="120" fill="url(#centerGlow_{filename})"/>
  
  <!-- アイコンエリア -->
  <circle cx="200" cy="150" r="60" fill="#4a7c59" opacity="0.1"/>
  <text x="200" y="170" text-anchor="middle" font-size="48" fill="#2d5016">{icon}</text>
  
  <!-- 装飾的な要素 -->
  <circle cx="80" cy="80" r="3" fill="#4a7c59" opacity="0.5"/>
  <circle cx="320" cy="70" r="4" fill="#4a7c59" opacity="0.5"/>
  <circle cx="350" cy="220" r="3" fill="#4a7c59" opacity="0.5"/>
  <circle cx="50" cy="250" r="2" fill="#4a7c59" opacity="0.5"/>
  
  <!-- 装備名 -->
  <text x="200" y="250" text-anchor="middle" fill="#2d5016" font-family="Arial, sans-serif" 
        font-size="18" font-weight="bold">{equipment_type}</text>
</svg>'''
        
        with open(self.images_dir / f"{filename}.svg", 'w', encoding='utf-8') as f:
            f.write(svg_content)
        print(f"✅ 装備画像作成完了: {filename}.svg")
    
    def create_support_card(self, support_type, icon, filename):
        """サポートカード用のイラスト"""
        svg_content = f'''
<svg width="400" height="300" viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="supportBg_{filename}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#3498db;stop-opacity:0.1" />
      <stop offset="100%" style="stop-color:#e8f5e8;stop-opacity:0.1" />
    </linearGradient>
  </defs>
  
  <!-- 背景 -->
  <rect width="400" height="300" fill="url(#supportBg_{filename})"/>
  
  <!-- メインアイコン -->
  <circle cx="200" cy="120" r="50" fill="#3498db" opacity="0.1"/>
  <text x="200" y="140" text-anchor="middle" font-size="40" fill="#3498db">{icon}</text>
  
  <!-- サポートタイプ -->
  <text x="200" y="220" text-anchor="middle" fill="#2c3e50" font-family="Arial, sans-serif" 
        font-size="16" font-weight="bold">{support_type}</text>
  
  <!-- 装飾線 -->
  <line x1="100" y1="250" x2="300" y2="250" stroke="#3498db" stroke-width="2" opacity="0.3"/>
</svg>'''
        
        with open(self.images_dir / f"{filename}.svg", 'w', encoding='utf-8') as f:
            f.write(svg_content)
        print(f"✅ サポート画像作成完了: {filename}.svg")

    def create_region_card(self, region_name, landmark_icon, filename):
        """地域カード用のイラスト"""
        svg_content = f'''
<svg width="400" height="300" viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="regionBg_{filename}" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#87CEEB;stop-opacity:0.3" />
      <stop offset="100%" style="stop-color:#e8f5e8;stop-opacity:0.3" />
    </linearGradient>
  </defs>
  
  <!-- 背景 -->
  <rect width="400" height="300" fill="url(#regionBg_{filename})"/>
  
  <!-- 地域の山々（シルエット） -->
  <polygon points="0,200 80,150 160,180 240,140 320,170 400,160 400,300 0,300" 
           fill="#4a7c59" opacity="0.3"/>
  
  <!-- ランドマークアイコン -->
  <circle cx="200" cy="120" r="45" fill="white" opacity="0.8"/>
  <text x="200" y="135" text-anchor="middle" font-size="36" fill="#2d5016">{landmark_icon}</text>
  
  <!-- 地域名 -->
  <text x="200" y="250" text-anchor="middle" fill="#2c3e50" font-family="Arial, sans-serif" 
        font-size="18" font-weight="bold">{region_name}</text>
</svg>'''
        
        with open(self.images_dir / f"{filename}.svg", 'w', encoding='utf-8') as f:
            f.write(svg_content)
        print(f"✅ 地域画像作成完了: {filename}.svg")

    def create_all_images(self):
        """すべてのSVG画像を生成"""
        print("🎨 低山ハイキング用SVG画像生成開始")
        print("=" * 50)
        
        # ヒーロー画像
        self.create_hero_image()
        
        # 山の画像
        self.create_mountain_card("高尾山", "mountain_takao")
        self.create_mountain_card("筑波山", "mountain_tsukuba") 
        self.create_mountain_card("讃岐富士", "mountain_sanuki")
        
        # 装備画像
        self.create_equipment_card("ザック選び", "🎒", "equipment_backpack")
        self.create_equipment_card("登山靴選び", "👟", "equipment_shoes")
        self.create_equipment_card("レインウェア", "🧥", "equipment_rain")
        
        # サポート画像
        self.create_support_card("基礎知識", "📚", "support_guide")
        self.create_support_card("安全対策", "🛡️", "support_safety")
        self.create_support_card("ファミリー向け", "👨‍👩‍👧‍👦", "support_family")
        
        # 地域画像
        self.create_region_card("関東地方", "🗼", "region_kanto")
        self.create_region_card("関西地方", "🏯", "region_kansai")
        self.create_region_card("九州地方", "♨️", "region_kyushu")
        
        print("=" * 50)
        print("🎉 すべてのSVG画像生成完了！")
        print("\n📁 生成されたファイル:")
        
        svg_files = list(self.images_dir.glob("*.svg"))
        for file in sorted(svg_files):
            print(f"  - {file.name}")
        
        print(f"\n📊 合計: {len(svg_files)}個のSVG画像")

def main():
    creator = SVGImageCreator()
    creator.create_all_images()
    
    print("\n🚀 次のステップ:")
    print("1. index.html の画像パスを .svg に更新")
    print("2. alt属性にアクセシブルな説明を追加")
    print("3. CSSでSVGの表示スタイルを最適化")

if __name__ == "__main__":
    main()