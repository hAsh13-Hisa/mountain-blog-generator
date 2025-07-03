#!/usr/bin/env python3
"""
HTMLファイルの構造問題を一括修正
"""
import re
from pathlib import Path

def fix_html_file(file_path):
    """HTMLファイルの重複main要素とヘッダー問題を修正"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. 重複main要素を修正（複数の<main>を1つに）
    content = re.sub(r'<main[^>]*>\s*<main[^>]*>', '<main id="main-content" role="main">', content)
    content = re.sub(r'</main>\s*</main>', '</main>', content)
    
    # 2. ヘッダーをheader[role="banner"]に統一
    content = re.sub(r'<header>', '<header role="banner">', content)
    content = re.sub(r'<header role="banner" role="banner">', '<header role="banner">', content)
    
    # 3. CSSバージョンを最新に統一
    content = re.sub(r'/css/style\.css\?v=\d+', '/css/style.css?v=202507032237', content)
    content = re.sub(r'/css/style\.css"', '/css/style.css?v=202507032237"', content)
    
    # 4. 不要な改行文字削除
    content = re.sub(r'No newline at end of file\n', '', content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def fix_all_html_files():
    """全HTMLファイルを修正"""
    static_dir = Path('static_site')
    html_files = list(static_dir.rglob('*.html'))
    
    print(f"🔧 {len(html_files)}個のHTMLファイルを修正中...")
    
    fixed_count = 0
    for html_file in html_files:
        try:
            fix_html_file(html_file)
            fixed_count += 1
            print(f"✅ {html_file}")
        except Exception as e:
            print(f"❌ {html_file}: {e}")
    
    print(f"🎯 修正完了: {fixed_count}/{len(html_files)}ファイル")

if __name__ == "__main__":
    fix_all_html_files()