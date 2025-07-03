#!/usr/bin/env python3
"""
HTMLファイルのCSSリンクにバージョンパラメータを追加
"""
from pathlib import Path
import re
from datetime import datetime

def add_css_version():
    """全HTMLファイルのCSSリンクにバージョンを追加"""
    
    # バージョンタイムスタンプ
    version = datetime.now().strftime("%Y%m%d%H%M")
    
    # 対象ディレクトリ
    static_dir = Path('static_site')
    
    # 置換パターン
    old_pattern = r'<link rel="stylesheet" href="/css/style\.css">'
    new_pattern = f'<link rel="stylesheet" href="/css/style.css?v={version}">'
    
    updated_files = []
    
    print(f"🔄 CSSリンクにバージョン v={version} を追加中...")
    
    # 全HTMLファイルを処理
    for html_file in static_dir.rglob('*.html'):
        content = html_file.read_text(encoding='utf-8')
        
        if '/css/style.css' in content:
            # バージョンパラメータを追加
            new_content = re.sub(old_pattern, new_pattern, content)
            
            if new_content != content:
                html_file.write_text(new_content, encoding='utf-8')
                updated_files.append(str(html_file))
                print(f"  ✅ 更新: {html_file}")
    
    print(f"\n📊 更新結果:")
    print(f"  更新ファイル数: {len(updated_files)}")
    print(f"  バージョン: v={version}")
    
    return updated_files

if __name__ == "__main__":
    files = add_css_version()
    
    if files:
        print(f"\n🚀 {len(files)}個のファイルを更新しました。デプロイが必要です。")
    else:
        print("\n✅ 更新が必要なファイルはありませんでした。")