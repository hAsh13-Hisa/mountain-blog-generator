#!/usr/bin/env python3
"""
レイアウト問題の自動チェック
"""
from pathlib import Path
import re

def check_layout_issues():
    """HTMLファイルの一般的なレイアウト問題をチェック"""
    
    issues = []
    static_dir = Path('static_site')
    
    print("🔍 レイアウト問題チェック開始...\n")
    
    for html_file in static_dir.rglob('*.html'):
        content = html_file.read_text(encoding='utf-8')
        file_issues = []
        
        # 1. CSSリンクの確認
        css_links = re.findall(r'<link[^>]*rel="stylesheet"[^>]*>', content)
        if not css_links:
            file_issues.append("CSS未リンク")
        
        # 2. viewport設定の確認
        if 'name="viewport"' not in content:
            file_issues.append("viewport未設定")
        
        # 3. 空のmainタグチェック
        main_content = re.search(r'<main[^>]*>(.*?)</main>', content, re.DOTALL)
        if main_content and len(main_content.group(1).strip()) < 100:
            file_issues.append("main要素が空または短すぎる")
        
        # 4. 不要な空行・改行チェック
        if re.search(r'<main[^>]*>\s*\n\s*\n\s*<', content):
            file_issues.append("main内に不要な空行")
        
        # 5. CSSバージョンパラメータチェック
        if '/css/style.css"' in content and '?v=' not in content:
            file_issues.append("CSSバージョンパラメータなし")
        
        # 6. 基本的なHTML構造チェック
        required_elements = ['<header', '<main', '<footer']
        for element in required_elements:
            if element not in content:
                file_issues.append(f"{element.strip('<')}要素が見つからない")
        
        if file_issues:
            issues.append((str(html_file), file_issues))
            print(f"⚠️  {html_file.relative_to(static_dir)}: {', '.join(file_issues)}")
        else:
            print(f"✅ {html_file.relative_to(static_dir)}: 正常")
    
    print(f"\n📊 チェック結果:")
    if issues:
        print(f"  問題のあるファイル: {len(issues)}件")
        for file_path, file_issues in issues:
            print(f"    {Path(file_path).name}: {len(file_issues)}件の問題")
    else:
        print("  ✅ 全ファイル正常")
    
    return issues

def check_css_issues():
    """CSS関連の問題をチェック"""
    
    css_file = Path('static_site/css/style.css')
    if not css_file.exists():
        print("❌ CSSファイルが見つかりません")
        return
    
    content = css_file.read_text(encoding='utf-8')
    issues = []
    
    print("\n🎨 CSS問題チェック:")
    
    # z-index重複チェック
    z_indexes = re.findall(r'z-index:\s*(\d+)', content)
    z_index_counts = {}
    for z in z_indexes:
        z_index_counts[z] = z_index_counts.get(z, 0) + 1
    
    duplicates = [z for z, count in z_index_counts.items() if count > 1]
    if duplicates:
        issues.append(f"z-index重複: {', '.join(duplicates)}")
    
    # 必須プロパティチェック
    if 'padding-top' not in content:
        issues.append("bodyのpadding-top未設定")
    
    if 'position: fixed' not in content and 'position: sticky' not in content:
        issues.append("ヘッダーの固定position未設定")
    
    if issues:
        for issue in issues:
            print(f"  ⚠️  {issue}")
    else:
        print("  ✅ CSS正常")
    
    return issues

if __name__ == "__main__":
    html_issues = check_layout_issues()
    css_issues = check_css_issues()
    
    if html_issues or css_issues:
        print(f"\n🔧 修正が必要な問題が見つかりました。")
    else:
        print(f"\n✅ レイアウトに問題は見つかりませんでした。")