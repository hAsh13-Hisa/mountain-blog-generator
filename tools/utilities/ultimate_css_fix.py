#!/usr/bin/env python3
"""
CSSバージョン最終更新
"""
import re
from pathlib import Path

def update_css_version_in_file(file_path, new_version):
    """HTMLファイルのCSSバージョンを更新"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # CSSリンクのバージョンを更新
    pattern = r'/css/style\.css(\?v=\d+)?'
    replacement = f'/css/style.css?v={new_version}'
    
    updated_content = re.sub(pattern, replacement, content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    return content != updated_content

def main():
    """全HTMLファイルのCSSバージョンを更新"""
    new_version = "202507032250"
    static_dir = Path('static_site')
    html_files = list(static_dir.rglob('*.html'))
    
    updated_count = 0
    for html_file in html_files:
        try:
            if update_css_version_in_file(html_file, new_version):
                updated_count += 1
                print(f"✅ {html_file}")
        except Exception as e:
            print(f"❌ {html_file}: {e}")
    
    print(f"\n🎯 CSSバージョン更新完了: {updated_count}/{len(html_files)}ファイル")
    print(f"📌 新バージョン: v={new_version}")

if __name__ == "__main__":
    main()