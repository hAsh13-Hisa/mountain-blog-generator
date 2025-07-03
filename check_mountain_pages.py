#!/usr/bin/env python3
"""
全山ページのヘッダー問題をチェック
"""
from pathlib import Path
import re

def check_mountain_pages():
    """山ページのヘッダー関連問題をチェック"""
    
    mountains_dir = Path('static_site/mountains')
    issues = []
    
    print("🔍 山ページのヘッダー問題チェック開始...\n")
    
    for mountain_dir in mountains_dir.iterdir():
        if mountain_dir.is_dir() and mountain_dir.name != 'index.html':
            index_file = mountain_dir / 'index.html'
            
            if index_file.exists():
                print(f"📄 チェック中: {mountain_dir.name}")
                
                content = index_file.read_text(encoding='utf-8')
                
                # CSSリンクの確認
                css_links = re.findall(r'<link[^>]*href="([^"]*\.css)"[^>]*>', content)
                print(f"  CSS: {css_links}")
                
                # bodyタグに padding-top があるかチェック
                if 'style=' in content and 'padding-top' in content:
                    print(f"  ⚠️  個別のpadding-top設定あり")
                    issues.append((mountain_dir.name, "individual_padding"))
                
                # ヘッダーの構造確認
                if '<header role="banner">' in content:
                    print(f"  ✅ ヘッダー構造OK")
                else:
                    print(f"  ❌ ヘッダー構造異常")
                    issues.append((mountain_dir.name, "header_structure"))
                
                # main要素の開始位置確認
                main_match = re.search(r'<main[^>]*>.*?<', content, re.DOTALL)
                if main_match:
                    main_content = main_match.group(0)
                    if 'style=' in main_content and 'margin-top' in main_content:
                        print(f"  ⚠️  mainに個別margin-top設定あり")
                        issues.append((mountain_dir.name, "main_margin"))
                
                print()
    
    # 問題の要約
    print("📊 問題の要約:")
    if not issues:
        print("✅ 問題は見つかりませんでした")
    else:
        for mountain, issue_type in issues:
            print(f"  ❌ {mountain}: {issue_type}")
    
    return issues

if __name__ == "__main__":
    issues = check_mountain_pages()
    
    if issues:
        print(f"\n🔧 {len(issues)}件の問題が見つかりました。修正が必要です。")
    else:
        print("\n✅ 全ての山ページは正常です。")