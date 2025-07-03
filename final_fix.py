#!/usr/bin/env python3
"""
最終完全修正
"""
import re
from pathlib import Path

def final_fix_html(file_path):
    """HTMLファイルの最終修正"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. 重複main要素を完全削除
    # </main>\s*</main> パターンを </main> に置換
    content = re.sub(r'</main>\s*</main>', '</main>', content)
    
    # 2. 余計なheaderタグ削除
    content = re.sub(r'\s*<header role="banner">\s*', '\n    <header role="banner">\n        ', content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    """メイン処理"""
    problem_files = [
        'static_site/mountains/index.html',
        'static_site/regions/index.html'
    ]
    
    for file_path in problem_files:
        path = Path(file_path)
        if path.exists():
            final_fix_html(path)
            print(f"✅ 修正完了: {file_path}")

if __name__ == "__main__":
    main()