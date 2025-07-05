#!/usr/bin/env python3
"""
山一覧・地域別ページの中身生成修正スクリプト
"""
import json
from pathlib import Path
from collections import defaultdict

class PageContentGenerator:
    def __init__(self):
        self.load_data()
        self.output_dir = Path("static_site")
        
    def load_data(self):
        """データベース読み込み"""
        with open('data/mountains_japan_expanded.json', 'r', encoding='utf-8') as f:
            self.mountains_data = json.load(f)
        self.mountains = self.mountains_data['mountains']
        
    def generate_mountain_list_content(self):
        """山一覧ページのメインコンテンツ生成"""
        content = '''
        <div class="container">
            <div class="hero-section">
                <h1>🏔️ 山一覧</h1>
                <p class="hero-description">全47山の低山データベース</p>
                <div class="stats">
                    <span>標高20m〜400m</span> | <span>初心者・家族向け</span> | <span>登山道整備済み</span>
                </div>
            </div>
            
            <div class="mountains-section">
                <h2>標高順山一覧</h2>
                <div class="mountains-grid">
'''
        
        # 標高順にソート
        sorted_mountains = sorted(self.mountains, key=lambda x: x['elevation'])
        
        for mountain in sorted_mountains:
            try:
                features = mountain.get('features', [])
                feature_tags = ''.join([f'<span class="tag">#{feature}</span> ' for feature in features[:3]])
                
                name = mountain.get('name', '名前なし')
                prefecture = mountain.get('prefecture', '都道府県なし')
                elevation = mountain.get('elevation', 0)
                mountain_id = mountain.get('id', 'unknown')
                difficulty = mountain.get('difficulty', {}).get('level', '初級')
                
                content += f'''
                <div class="mountain-card">
                    <h3><a href="/mountains/{mountain_id}/">{name} ({elevation}m)</a></h3>
                    <p class="mountain-location">{prefecture} | {difficulty}</p>
                    <p class="mountain-description">{name}は{prefecture}にある標高{elevation}mの低山です。</p>
                    <div class="mountain-tags">
                        {feature_tags}
                    </div>
                </div>
'''
            except Exception as e:
                print(f"❌ 山データエラー: {mountain.get('name', 'unknown')} - {e}")
                continue
        
        content += '''
                </div>
            </div>
        </div>
'''
        return content
        
    def generate_regions_list_content(self):
        """地域別ページのメインコンテンツ生成"""
        # 都道府県別にグループ化
        prefectures = defaultdict(list)
        for mountain in self.mountains:
            pref = mountain.get('prefecture', '未分類')
            if pref and pref != '未分類':
                prefectures[pref].append(mountain)
        
        content = '''
        <div class="container">
            <div class="hero-section">
                <h1>🗾 地域別山一覧</h1>
                <p class="hero-description">日本全国の低山を都道府県別にご紹介</p>
                <div class="stats">
                    <span>25都道府県</span> | <span>47山</span> | <span>アクセス良好</span>
                </div>
            </div>
            
            <div class="regions-section">
                <h2>都道府県別一覧</h2>
                <div class="regions-grid">
'''
        
        # 都道府県を山数の多い順にソート
        sorted_prefs = sorted(prefectures.items(), key=lambda x: len(x[1]), reverse=True)
        
        for pref, mountains in sorted_prefs:
            mountain_names = ', '.join([m['name'] for m in mountains[:3]])
            if len(mountains) > 3:
                mountain_names += f' 他{len(mountains)-3}山'
                
            content += f'''
                <div class="region-card">
                    <a href="/regions/{pref}/">
                        <div class="region-card-content">
                            <h3>{pref} ({len(mountains)}山)</h3>
                            <p class="region-description">{mountain_names}</p>
                            <div class="region-mountains">{len(mountains)}山を詳しく見る</div>
                        </div>
                    </a>
                </div>
'''
        
        content += '''
                </div>
            </div>
        </div>
'''
        return content
        
    def update_html_page(self, file_path, new_main_content):
        """HTMLページのmain部分を更新"""
        if not file_path.exists():
            print(f"❌ ファイルが見つかりません: {file_path}")
            return False
            
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # main要素内のコンテンツを置き換え
        import re
        pattern = r'(<main[^>]*>).*?(</main>)'
        replacement = f'\\1{new_main_content}\\2'
        
        updated_html = re.sub(pattern, replacement, html_content, flags=re.DOTALL)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_html)
            
        print(f"✅ 更新完了: {file_path}")
        return True
        
    def fix_all_pages(self):
        """全ページを修正"""
        print("🔧 山一覧・地域別ページ修正開始...")
        
        # 1. 山一覧ページ修正
        mountains_content = self.generate_mountain_list_content()
        mountains_main = f'\n    <main id="main-content" role="main">{mountains_content}\n    </main>\n    '
        
        mountains_page = self.output_dir / 'mountains' / 'index.html'
        self.update_html_page(mountains_page, mountains_main)
        
        # 2. 地域別一覧ページ修正
        regions_content = self.generate_regions_list_content()
        regions_main = f'\n    <main id="main-content" role="main">{regions_content}\n    </main>\n    '
        
        regions_page = self.output_dir / 'regions' / 'index.html'
        self.update_html_page(regions_page, regions_main)
        
        print("✅ 山一覧・地域別ページ修正完了!")

if __name__ == "__main__":
    generator = PageContentGenerator()
    generator.fix_all_pages()