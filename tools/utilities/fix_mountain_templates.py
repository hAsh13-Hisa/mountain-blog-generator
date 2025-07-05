#!/usr/bin/env python3
"""
山ページのテンプレート崩れを修正
"""
from pathlib import Path
import re

def fix_mountain_templates():
    """山ページのHTMLテンプレートを修正"""
    
    mountains_dir = Path('static_site/mountains')
    fixed_files = []
    
    print("🔧 山ページテンプレート修正開始...\n")
    
    for mountain_dir in mountains_dir.iterdir():
        if mountain_dir.is_dir() and mountain_dir.name != 'index.html':
            index_file = mountain_dir / 'index.html'
            
            if index_file.exists():
                content = index_file.read_text(encoding='utf-8')
                original_content = content
                
                # mainタグ内の不要な改行を修正
                pattern = r'<main id="main-content" role="main">\s*\n\s*\n\s*<nav class="breadcrumb"'
                replacement = r'<main id="main-content" role="main">\n        <nav class="breadcrumb"'
                content = re.sub(pattern, replacement, content)
                
                # その他のテンプレート問題を修正
                # ファイル末尾の不要な改行も修正
                if content.endswith(' No newline at end of file'):
                    content = content.replace(' No newline at end of file', '')
                
                if content != original_content:
                    index_file.write_text(content, encoding='utf-8')
                    fixed_files.append(mountain_dir.name)
                    print(f"  ✅ 修正: {mountain_dir.name}")
                else:
                    print(f"  ✓ 正常: {mountain_dir.name}")
    
    print(f"\n📊 修正結果:")
    print(f"  修正ファイル数: {len(fixed_files)}")
    if fixed_files:
        print(f"  修正した山: {', '.join(fixed_files)}")
    
    return fixed_files

if __name__ == "__main__":
    files = fix_mountain_templates()
    
    if files:
        print(f"\n🚀 {len(files)}個のファイルを修正しました。デプロイが必要です。")
    else:
        print("\n✅ 修正が必要なファイルはありませんでした。")