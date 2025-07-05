#!/usr/bin/env python3
"""
サイト品質チェックスクリプト
リンク切れ、HTML構文、アクセシビリティ等を総合的に検証
"""

import os
import re
from pathlib import Path
from urllib.parse import urljoin, urlparse
import json

class SiteQualityChecker:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.issues = []
        self.warnings = []
        self.successes = []
        
    def log_issue(self, level, category, message, file_path=None):
        """問題をログに記録"""
        entry = {
            "level": level,
            "category": category, 
            "message": message,
            "file": str(file_path) if file_path else None
        }
        
        if level == "error":
            self.issues.append(entry)
        elif level == "warning":
            self.warnings.append(entry)
        else:
            self.successes.append(entry)
    
    def find_all_html_files(self):
        """すべてのHTMLファイルを見つける"""
        html_files = []
        for html_file in self.base_dir.rglob("*.html"):
            if "templates" not in str(html_file):  # テンプレートは除外
                html_files.append(html_file)
        return html_files
    
    def extract_links_from_html(self, file_path):
        """HTMLファイルからリンクを抽出"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # hrefリンクを抽出
            href_pattern = r'href=["\']([^"\']+)["\']'
            links = re.findall(href_pattern, content)
            
            # srcリンクも抽出（画像、JS、CSS）
            src_pattern = r'src=["\']([^"\']+)["\']'
            src_links = re.findall(src_pattern, content)
            
            return links, src_links
            
        except Exception as e:
            self.log_issue("error", "file_access", f"ファイル読み込みエラー: {e}", file_path)
            return [], []
    
    def check_link_exists(self, link, base_file_path):
        """リンク先ファイルが存在するかチェック"""
        # 外部リンクはスキップ
        if link.startswith(('http://', 'https://', 'mailto:', 'tel:')):
            return True
        
        # アンカーリンクはスキップ
        if link.startswith('#'):
            return True
        
        # 相対パスを絶対パスに変換
        if link.startswith('/'):
            # ルート相対パス
            target_path = self.base_dir / link.lstrip('/')
        else:
            # 現在のファイルからの相対パス
            target_path = base_file_path.parent / link
        
        # ディレクトリの場合はindex.htmlを確認
        if target_path.is_dir():
            target_path = target_path / "index.html"
        
        # 拡張子がない場合もindex.htmlを確認
        if not target_path.suffix and not target_path.exists():
            target_path = target_path / "index.html"
        
        return target_path.exists()
    
    def check_broken_links(self):
        """リンク切れをチェック"""
        print("🔗 リンク切れチェック中...")
        
        html_files = self.find_all_html_files()
        total_links = 0
        broken_links = 0
        
        for html_file in html_files:
            links, src_links = self.extract_links_from_html(html_file)
            all_links = links + src_links
            
            for link in all_links:
                total_links += 1
                
                if not self.check_link_exists(link, html_file):
                    broken_links += 1
                    self.log_issue("error", "broken_link", 
                                 f"リンク切れ: {link}", html_file)
        
        if broken_links == 0:
            self.log_issue("success", "links", f"✅ すべてのリンクが正常 ({total_links}個)")
        else:
            self.log_issue("error", "links", f"❌ {broken_links}/{total_links}個のリンクが切れています")
    
    def check_html_structure(self):
        """HTML構造をチェック"""
        print("📄 HTML構造チェック中...")
        
        html_files = self.find_all_html_files()
        
        for html_file in html_files:
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 基本的なHTML構造チェック
                checks = [
                    (r'<!DOCTYPE html>', "DOCTYPE宣言"),
                    (r'<html[^>]*lang=["\']ja["\']', "lang属性"),
                    (r'<meta[^>]*charset=["\']UTF-8["\']', "文字エンコーディング"),
                    (r'<meta[^>]*viewport[^>]*>', "viewport設定"),
                    (r'<title>', "titleタグ"),
                    (r'<meta[^>]*description[^>]*>', "description meta"),
                ]
                
                for pattern, description in checks:
                    if not re.search(pattern, content, re.IGNORECASE):
                        self.log_issue("warning", "html_structure", 
                                     f"{description}が見つかりません", html_file)
                
                # 見出しの階層チェック
                headings = re.findall(r'<(h[1-6])', content, re.IGNORECASE)
                if headings:
                    # h1があるかチェック
                    if 'h1' not in [h.lower() for h in headings]:
                        self.log_issue("warning", "accessibility", 
                                     "h1タグが見つかりません", html_file)
                
            except Exception as e:
                self.log_issue("error", "file_access", 
                             f"HTMLファイル解析エラー: {e}", html_file)
    
    def check_accessibility(self):
        """アクセシビリティをチェック"""
        print("♿ アクセシビリティチェック中...")
        
        html_files = self.find_all_html_files()
        
        for html_file in html_files:
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 画像のalt属性チェック
                img_tags = re.findall(r'<img[^>]*>', content, re.IGNORECASE)
                for img_tag in img_tags:
                    if 'alt=' not in img_tag:
                        self.log_issue("warning", "accessibility",
                                     f"alt属性がない画像: {img_tag[:50]}...", html_file)
                
                # リンクのaria-labelチェック（アイコンのみの場合）
                icon_links = re.findall(r'<a[^>]*>[\s]*<span[^>]*>[🏔️🎒👟🧥📚🛡️👨‍👩‍👧‍👦🗼🏯♨️]</span>[\s]*</a>', content)
                for link in icon_links:
                    if 'aria-label=' not in link:
                        self.log_issue("warning", "accessibility",
                                     "アイコンリンクにaria-labelがありません", html_file)
                
                # スキップリンクの存在チェック
                if 'skip-link' not in content and 'main-content' in content:
                    self.log_issue("warning", "accessibility",
                                 "スキップリンクが見つかりません", html_file)
                
            except Exception as e:
                self.log_issue("error", "file_access", 
                             f"アクセシビリティチェックエラー: {e}", html_file)
    
    def check_css_references(self):
        """CSS参照をチェック"""
        print("🎨 CSS参照チェック中...")
        
        html_files = self.find_all_html_files()
        
        for html_file in html_files:
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # CSSファイルの参照をチェック
                css_links = re.findall(r'<link[^>]*href=["\']([^"\']*\.css)["\']', content)
                for css_link in css_links:
                    if not self.check_link_exists(css_link, html_file):
                        self.log_issue("error", "css", 
                                     f"CSSファイルが見つかりません: {css_link}", html_file)
                
            except Exception as e:
                self.log_issue("error", "file_access", 
                             f"CSS参照チェックエラー: {e}", html_file)
    
    def check_js_references(self):
        """JavaScript参照をチェック"""
        print("⚡ JavaScript参照チェック中...")
        
        html_files = self.find_all_html_files()
        
        for html_file in html_files:
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # JSファイルの参照をチェック
                js_links = re.findall(r'<script[^>]*src=["\']([^"\']*\.js)["\']', content)
                for js_link in js_links:
                    if not self.check_link_exists(js_link, html_file):
                        self.log_issue("error", "javascript", 
                                     f"JavaScriptファイルが見つかりません: {js_link}", html_file)
                
            except Exception as e:
                self.log_issue("error", "file_access", 
                             f"JavaScript参照チェックエラー: {e}", html_file)
    
    def check_image_references(self):
        """画像参照をチェック"""
        print("🖼️ 画像参照チェック中...")
        
        html_files = self.find_all_html_files()
        
        for html_file in html_files:
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 画像ファイルの参照をチェック
                img_srcs = re.findall(r'<img[^>]*src=["\']([^"\']*)["\']', content)
                for img_src in img_srcs:
                    if not self.check_link_exists(img_src, html_file):
                        self.log_issue("error", "images", 
                                     f"画像ファイルが見つかりません: {img_src}", html_file)
                
            except Exception as e:
                self.log_issue("error", "file_access", 
                             f"画像参照チェックエラー: {e}", html_file)
    
    def check_responsive_design(self):
        """レスポンシブデザインをチェック"""
        print("📱 レスポンシブデザインチェック中...")
        
        css_file = self.base_dir / "css" / "minimal_design.css"
        
        if css_file.exists():
            try:
                with open(css_file, 'r', encoding='utf-8') as f:
                    css_content = f.read()
                
                # メディアクエリの存在チェック
                media_queries = re.findall(r'@media[^{]+\{', css_content)
                if len(media_queries) < 3:
                    self.log_issue("warning", "responsive", 
                                 f"メディアクエリが少ない可能性があります ({len(media_queries)}個)")
                else:
                    self.log_issue("success", "responsive", 
                                 f"✅ 適切なメディアクエリが設定されています ({len(media_queries)}個)")
                
                # viewportの設定確認
                html_files = self.find_all_html_files()
                for html_file in html_files:
                    with open(html_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    if 'viewport' not in content:
                        self.log_issue("error", "responsive", 
                                     "viewport meta tagが設定されていません", html_file)
                        
            except Exception as e:
                self.log_issue("error", "file_access", 
                             f"レスポンシブデザインチェックエラー: {e}")
        else:
            self.log_issue("error", "css", "CSSファイルが見つかりません")
    
    def check_seo_basics(self):
        """基本的なSEOをチェック"""
        print("🔍 SEO基本チェック中...")
        
        html_files = self.find_all_html_files()
        
        for html_file in html_files:
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # titleタグの長さチェック
                title_match = re.search(r'<title>([^<]+)</title>', content, re.IGNORECASE)
                if title_match:
                    title_length = len(title_match.group(1))
                    if title_length > 60:
                        self.log_issue("warning", "seo", 
                                     f"titleが長すぎます ({title_length}文字)", html_file)
                    elif title_length < 10:
                        self.log_issue("warning", "seo", 
                                     f"titleが短すぎます ({title_length}文字)", html_file)
                
                # descriptionの長さチェック
                desc_match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']+)["\']', content, re.IGNORECASE)
                if desc_match:
                    desc_length = len(desc_match.group(1))
                    if desc_length > 160:
                        self.log_issue("warning", "seo", 
                                     f"descriptionが長すぎます ({desc_length}文字)", html_file)
                    elif desc_length < 50:
                        self.log_issue("warning", "seo", 
                                     f"descriptionが短すぎます ({desc_length}文字)", html_file)
                
                # 構造化データのチェック
                if 'application/ld+json' not in content:
                    self.log_issue("warning", "seo", 
                                 "構造化データが設定されていません", html_file)
                
            except Exception as e:
                self.log_issue("error", "file_access", 
                             f"SEOチェックエラー: {e}", html_file)
    
    def check_file_structure(self):
        """ファイル構造をチェック"""
        print("📂 ファイル構造チェック中...")
        
        # 必須ディレクトリの存在チェック
        required_dirs = ['css', 'js', 'images', 'mountains', 'equipment', 'beginner']
        for dir_name in required_dirs:
            dir_path = self.base_dir / dir_name
            if not dir_path.exists():
                self.log_issue("error", "structure", f"必須ディレクトリが見つかりません: {dir_name}")
            else:
                self.log_issue("success", "structure", f"✅ {dir_name}ディレクトリ確認")
        
        # 必須ファイルの存在チェック
        required_files = [
            'index.html',
            'css/minimal_design.css',
            'js/minimal.js'
        ]
        for file_path in required_files:
            full_path = self.base_dir / file_path
            if not full_path.exists():
                self.log_issue("error", "structure", f"必須ファイルが見つかりません: {file_path}")
            else:
                self.log_issue("success", "structure", f"✅ {file_path}確認")
    
    def generate_site_map(self):
        """サイトマップを生成"""
        print("🗺️ サイトマップ生成中...")
        
        html_files = self.find_all_html_files()
        site_map = {}
        
        for html_file in html_files:
            relative_path = html_file.relative_to(self.base_dir)
            
            # URLパスに変換
            if relative_path.name == 'index.html':
                if relative_path.parent == Path('.'):
                    url_path = '/'
                else:
                    url_path = f"/{relative_path.parent}/"
            else:
                url_path = f"/{relative_path}"
            
            # タイトルを抽出
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                title_match = re.search(r'<title>([^<]+)</title>', content, re.IGNORECASE)
                title = title_match.group(1) if title_match else str(relative_path)
                
                site_map[url_path] = {
                    "title": title,
                    "file": str(relative_path)
                }
                
            except Exception as e:
                site_map[url_path] = {
                    "title": "エラー",
                    "file": str(relative_path),
                    "error": str(e)
                }
        
        return site_map
    
    def run_all_checks(self):
        """すべてのチェックを実行"""
        print("🔍 サイト品質チェック開始")
        print("=" * 50)
        
        # 各種チェック実行
        self.check_file_structure()
        self.check_broken_links()
        self.check_html_structure()
        self.check_accessibility()
        self.check_css_references()
        self.check_js_references()
        self.check_image_references()
        self.check_responsive_design()
        self.check_seo_basics()
        
        # サイトマップ生成
        site_map = self.generate_site_map()
        
        # 結果レポート出力
        self.print_results(site_map)
        
        return len(self.issues) == 0
    
    def print_results(self, site_map):
        """結果を表示"""
        print("\n" + "=" * 50)
        print("📊 サイト品質チェック結果")
        print("=" * 50)
        
        # 成功項目
        if self.successes:
            print(f"\n✅ 成功項目 ({len(self.successes)}個):")
            for success in self.successes:
                print(f"  {success['message']}")
        
        # 警告項目
        if self.warnings:
            print(f"\n⚠️ 警告項目 ({len(self.warnings)}個):")
            for warning in self.warnings:
                file_info = f" ({warning['file']})" if warning['file'] else ""
                print(f"  [{warning['category']}] {warning['message']}{file_info}")
        
        # エラー項目
        if self.issues:
            print(f"\n❌ エラー項目 ({len(self.issues)}個):")
            for issue in self.issues:
                file_info = f" ({issue['file']})" if issue['file'] else ""
                print(f"  [{issue['category']}] {issue['message']}{file_info}")
        
        # サイトマップ
        print(f"\n🗺️ サイトマップ ({len(site_map)}ページ):")
        for url, info in sorted(site_map.items()):
            if 'error' in info:
                print(f"  {url} - ❌ {info['error']}")
            else:
                print(f"  {url} - {info['title']}")
        
        # 総合評価
        print("\n" + "=" * 50)
        if len(self.issues) == 0:
            if len(self.warnings) == 0:
                print("🎉 完璧！すべてのチェックに合格しました")
                grade = "A+"
            else:
                print("✅ 良好！重大な問題はありません")
                grade = "A"
        elif len(self.issues) <= 3:
            print("⚠️ 注意！軽微な問題があります")
            grade = "B"
        elif len(self.issues) <= 10:
            print("🔧 修正必要！複数の問題があります")
            grade = "C"
        else:
            print("🚨 要修正！多数の問題があります")
            grade = "D"
        
        print(f"総合評価: {grade}")
        print(f"エラー: {len(self.issues)}個 | 警告: {len(self.warnings)}個 | 成功: {len(self.successes)}個")

def main():
    checker = SiteQualityChecker()
    is_perfect = checker.run_all_checks()
    
    if is_perfect:
        print("\n🚀 サイトは公開準備完了です！")
    else:
        print("\n🔧 問題を修正してから公開してください")
    
    return 0 if is_perfect else 1

if __name__ == "__main__":
    exit(main())