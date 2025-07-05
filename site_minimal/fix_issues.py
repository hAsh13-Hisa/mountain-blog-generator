#!/usr/bin/env python3
"""
サイト品質問題の修正スクリプト
検出された問題を自動修正
"""

import re
from pathlib import Path

class SiteFixer:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        
    def fix_missing_mountain_images(self):
        """不足している山画像を既存画像で代替"""
        print("🖼️ 不足している山画像を修正中...")
        
        # 既存の山画像
        existing_images = {
            "takao": "mountain_takao.svg",
            "tsukuba": "mountain_tsukuba.svg", 
            "sanuki": "mountain_sanuki.svg"
        }
        
        # 代替マッピング
        fallback_mapping = {
            "円": "takao",
            "函館": "takao",
            "岩木": "tsukuba",
            "金華": "tsukuba",
            "塩見": "sanuki",
            "鋸": "sanuki",
            "大平": "takao",
            "浅間": "tsukuba",
            "渋沢丘陵": "takao"
        }
        
        # HTMLファイルを更新
        html_files = list(self.base_dir.rglob("*.html"))
        for html_file in html_files:
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 画像パスを修正
                for mountain_key, fallback_key in fallback_mapping.items():
                    fallback_image = existing_images[fallback_key]
                    
                    # パターンを修正
                    patterns = [
                        f'src="([^"]*)/mountain_{mountain_key}[^"]*\\.svg"',
                        f"src='([^']*)/mountain_{mountain_key}[^']*\\.svg'"
                    ]
                    
                    for pattern in patterns:
                        content = re.sub(
                            pattern,
                            lambda m: f'src="{m.group(1)}/{fallback_image}"',
                            content
                        )
                
                # 更新をファイルに保存
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
            except Exception as e:
                print(f"❌ エラー: {html_file} - {e}")
        
        print("✅ 山画像の修正完了")
    
    def fix_skip_links(self):
        """スキップリンクを追加"""
        print("♿ スキップリンクを追加中...")
        
        html_files = list(self.base_dir.rglob("*.html"))
        for html_file in html_files:
            # index.html以外を処理（index.htmlには既にある）
            if html_file.name == "index.html" and html_file.parent == self.base_dir:
                continue
                
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # スキップリンクが既にある場合はスキップ
                if 'skip-link' in content:
                    continue
                
                # <body>タグの直後にスキップリンクを挿入
                skip_link = '''    <!-- Skip Link -->
    <a href="#main-content" class="sr-only">メインコンテンツへスキップ</a>

'''
                
                content = re.sub(
                    r'(<body[^>]*>)',
                    r'\1\n' + skip_link,
                    content
                )
                
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
            except Exception as e:
                print(f"❌ エラー: {html_file} - {e}")
        
        print("✅ スキップリンクの追加完了")
    
    def fix_seo_descriptions(self):
        """SEO用のdescriptionを改善"""
        print("🔍 SEO descriptionを改善中...")
        
        # より良いdescription
        improved_descriptions = {
            "このサイトについて": "低山旅行は初心者・ファミリー向けの低山ハイキング情報サイトです。安全で楽しい山歩きをサポートします。",
            "お問い合わせ": "低山旅行サイトへのお問い合わせページ。山の情報や装備に関するご質問をお気軽にお寄せください。",
            "地域別ガイド": "全国47都道府県の低山を地域別にご紹介。お住まいの地域からアクセス良好な山を見つけましょう。",
            "利用規約": "低山旅行サイトの利用規約。サイトご利用時のルールや注意事項について詳しく説明しています。",
            "プライバシーポリシー": "低山旅行サイトのプライバシーポリシー。個人情報の取り扱いやCookieの使用について詳しく説明。"
        }
        
        html_files = list(self.base_dir.rglob("*.html"))
        for html_file in html_files:
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # titleからページ種別を判定
                title_match = re.search(r'<title>([^<-]+)', content)
                if title_match:
                    page_title = title_match.group(1).strip()
                    
                    for key, description in improved_descriptions.items():
                        if key in page_title:
                            # 既存のdescriptionを置換
                            content = re.sub(
                                r'<meta name="description" content="[^"]*"',
                                f'<meta name="description" content="{description}"',
                                content,
                                flags=re.IGNORECASE
                            )
                            break
                
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
            except Exception as e:
                print(f"❌ エラー: {html_file} - {e}")
        
        print("✅ SEO descriptionの改善完了")
    
    def add_image_fallbacks(self):
        """画像のフォールバック対応を追加"""
        print("🖼️ 画像フォールバック対応を追加中...")
        
        html_files = list(self.base_dir.rglob("*.html"))
        for html_file in html_files:
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # onerrorハンドラを追加（既にない場合）
                content = re.sub(
                    r'(<img[^>]*src="[^"]*mountain_[^"]*\.svg"[^>]*)(>)',
                    lambda m: m.group(1) + ' onerror="this.src=\'{}/images/hero_mountain_hiking.svg\'".format(window.location.origin)' + m.group(2) if 'onerror' not in m.group(1) else m.group(0),
                    content
                )
                
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
            except Exception as e:
                print(f"❌ エラー: {html_file} - {e}")
        
        print("✅ 画像フォールバック対応完了")
    
    def fix_all_issues(self):
        """すべての問題を修正"""
        print("🔧 サイト品質問題修正開始")
        print("=" * 50)
        
        self.fix_missing_mountain_images()
        self.fix_skip_links()
        self.fix_seo_descriptions()
        self.add_image_fallbacks()
        
        print("=" * 50)
        print("🎉 すべての修正完了！")

def main():
    fixer = SiteFixer()
    fixer.fix_all_issues()
    
    print("\n🚀 修正後の確認方法:")
    print("python3 check_site.py で再チェックを実行してください")

if __name__ == "__main__":
    main()