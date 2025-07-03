#!/usr/bin/env python3
"""
山ページのアフィリエイトセクション有無をチェック
"""
from pathlib import Path
import re

def check_affiliate_sections():
    """山ページのアフィリエイトセクションをチェック"""
    
    mountains_dir = Path('static_site/mountains')
    results = {}
    
    print("🔍 山ページのアフィリエイトセクションチェック...\n")
    
    for mountain_dir in mountains_dir.iterdir():
        if mountain_dir.is_dir() and mountain_dir.name != 'index.html':
            index_file = mountain_dir / 'index.html'
            
            if index_file.exists():
                content = index_file.read_text(encoding='utf-8')
                
                # アフィリエイトセクションの有無
                has_affiliate_section = 'affiliate-section' in content
                has_affiliate_products = 'affiliate-products' in content
                
                # アフィリエイトリンク数
                affiliate_links = re.findall(r'hb\.afl\.rakuten\.co\.jp', content)
                link_count = len(affiliate_links)
                
                results[mountain_dir.name] = {
                    'has_section': has_affiliate_section,
                    'has_products': has_affiliate_products,
                    'link_count': link_count
                }
                
                status = "✅" if has_affiliate_section and link_count > 0 else "❌"
                print(f"{status} {mountain_dir.name}: アフィリエイトセクション={has_affiliate_section}, リンク数={link_count}")
    
    print(f"\n📊 結果:")
    missing = [name for name, data in results.items() if not data['has_section'] or data['link_count'] == 0]
    if missing:
        print(f"  アフィリエイト不足: {len(missing)}件")
        for name in missing:
            print(f"    - {name}")
    else:
        print("  ✅ 全ページにアフィリエイトあり")
    
    return results

if __name__ == "__main__":
    check_affiliate_sections()