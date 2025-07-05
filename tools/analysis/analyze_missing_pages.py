#!/usr/bin/env python3
"""
サイト内リンクを分析して未作成ページを特定
"""
import os
import re
from pathlib import Path

def analyze_missing_pages():
    """未作成ページを分析"""
    
    # 内部リンクを抽出（外部リンクとアンカーリンクを除外）
    internal_links = set()
    
    # 既存HTMLファイルからリンクを抽出
    html_files = list(Path('static_site').rglob('*.html'))
    
    for html_file in html_files:
        content = html_file.read_text(encoding='utf-8')
        
        # href属性を抽出
        links = re.findall(r'href="([^"]*)"', content)
        
        for link in links:
            # 内部リンクのみを対象（外部URL、アンカー、CSSなどを除外）
            if (link.startswith('/') and 
                not link.startswith('//') and
                not link.startswith('/#') and
                not link.endswith('.css') and
                not link.endswith('.js') and
                not link.endswith('.xml') and
                not link.endswith('.ico') and
                not link.endswith('.png')):
                internal_links.add(link)
    
    print("🔍 内部リンク一覧:")
    for link in sorted(internal_links):
        print(f"  {link}")
    
    # 既存ページをチェック
    existing_pages = set()
    
    # トップページ
    if Path('static_site/index.html').exists():
        existing_pages.add('/')
    
    # 山ページ
    mountains_dir = Path('static_site/mountains')
    if mountains_dir.exists():
        for mountain_dir in mountains_dir.iterdir():
            if mountain_dir.is_dir() and (mountain_dir / 'index.html').exists():
                existing_pages.add(f'/mountains/{mountain_dir.name}/')
    
    print(f"\n📄 既存ページ:")
    for page in sorted(existing_pages):
        print(f"  ✓ {page}")
    
    # 未作成ページを特定
    missing_pages = internal_links - existing_pages
    
    print(f"\n❌ 未作成ページ ({len(missing_pages)}件):")
    for page in sorted(missing_pages):
        print(f"  📝 {page}")
    
    return missing_pages

if __name__ == "__main__":
    missing = analyze_missing_pages()
    
    # カテゴリ別に分類
    categories = {
        'pages': [],      # 一般ページ
        'regions': [],    # 地域ページ  
        'difficulty': [], # 難易度ページ
        'other': []       # その他
    }
    
    for page in missing:
        if page.startswith('/regions/'):
            categories['regions'].append(page)
        elif page.startswith('/difficulty/'):
            categories['difficulty'].append(page)
        elif page in ['/about/', '/beginner/', '/equipment/', '/contact/', '/privacy/', '/terms/']:
            categories['pages'].append(page)
        else:
            categories['other'].append(page)
    
    print(f"\n📊 カテゴリ別未作成ページ:")
    for category, pages in categories.items():
        if pages:
            print(f"  {category}: {len(pages)}件")
            for page in pages:
                print(f"    - {page}")