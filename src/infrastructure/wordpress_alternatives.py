#!/usr/bin/env python3
"""
WordPress投稿の代替実装方法
"""
import requests
import json
import base64
from typing import Dict, Any, List, Optional
from datetime import datetime
import hashlib
import time

from config.settings import get_settings
from config.logging_config import LoggerMixin


class WordPressAlternativeClient(LoggerMixin):
    """WordPress投稿の代替クライアント"""
    
    def __init__(self):
        self.settings = get_settings()
        self.base_url = self.settings.WP_URL
    
    def method_1_cookie_auth(self, username: str, password: str) -> Optional[requests.Session]:
        """
        方法1: Cookie認証を使用
        通常のWordPressパスワードが必要
        """
        session = requests.Session()
        
        try:
            # ログインページを取得
            login_url = f"{self.base_url}/wp-login.php"
            login_page = session.get(login_url)
            
            # ログインリクエスト
            login_data = {
                'log': username,
                'pwd': password,
                'wp-submit': 'Log In',
                'redirect_to': f'{self.base_url}/wp-admin/',
                'testcookie': '1'
            }
            
            response = session.post(login_url, data=login_data, allow_redirects=False)
            
            # 認証成功確認
            if response.status_code == 302 and 'wordpress_logged_in' in session.cookies:
                self.log_info("Cookie認証成功")
                
                # Nonceを取得
                admin_page = session.get(f"{self.base_url}/wp-admin/")
                if 'wp_nonce' in admin_page.text:
                    # Nonceを抽出
                    import re
                    nonce_match = re.search(r'var wpApiSettings = {"root":".*?","nonce":"(.*?)"', admin_page.text)
                    if nonce_match:
                        session.headers['X-WP-Nonce'] = nonce_match.group(1)
                
                return session
            else:
                self.log_error("Cookie認証失敗")
                return None
                
        except Exception as e:
            self.log_error(f"Cookie認証エラー: {e}")
            return None
    
    def method_2_custom_auth_header(self) -> Dict[str, str]:
        """
        方法2: カスタム認証ヘッダー
        .htaccessやサーバー設定に依存しない方法
        """
        # カスタムヘッダーを使用
        app_password = self.settings.WP_APP_PASSWORD.replace(' ', '')
        auth_string = f"{self.settings.WP_USERNAME}:{app_password}"
        
        # 複数の認証ヘッダーを試す
        headers = {
            'Authorization': f'Basic {base64.b64encode(auth_string.encode()).decode()}',
            'X-WP-Username': self.settings.WP_USERNAME,
            'X-WP-Password': app_password,
            'X-Authorization': f'Basic {base64.b64encode(auth_string.encode()).decode()}',
            'Content-Type': 'application/json'
        }
        
        return headers
    
    def method_3_direct_db_insert(self) -> str:
        """
        方法3: 直接データベース挿入用のSQLを生成
        （管理者がphpMyAdminなどで実行）
        """
        sql_template = """
-- WordPress記事直接挿入SQL
-- 使用前に必ずバックアップを取ってください

INSERT INTO wp_posts (
    post_author, 
    post_date, 
    post_date_gmt, 
    post_content, 
    post_title, 
    post_excerpt, 
    post_status, 
    comment_status, 
    ping_status, 
    post_name, 
    post_modified, 
    post_modified_gmt, 
    post_type
) VALUES (
    1, -- 管理者のユーザーID
    NOW(), 
    UTC_TIMESTAMP(), 
    '{content}', 
    '{title}', 
    '{excerpt}', 
    'draft', 
    'open', 
    'open', 
    '{slug}', 
    NOW(), 
    UTC_TIMESTAMP(), 
    'post'
);

-- タグの設定（別途実行が必要）
-- SET @post_id = LAST_INSERT_ID();
-- INSERT INTO wp_term_relationships (object_id, term_taxonomy_id) VALUES (@post_id, term_id);
"""
        return sql_template
    
    def method_4_wp_cli_commands(self) -> List[str]:
        """
        方法4: WP-CLIコマンドを生成
        SSHアクセスが必要
        """
        commands = []
        
        # JSONファイルから記事データを読み込む想定
        command_template = """
wp post create \\
  --post_title='{title}' \\
  --post_content='{content}' \\
  --post_excerpt='{excerpt}' \\
  --post_status=draft \\
  --post_author=1 \\
  --tags_input='{tags}'
"""
        
        commands.append("#!/bin/bash")
        commands.append("# WP-CLI記事投稿スクリプト")
        commands.append("# 実行前にWordPressディレクトリに移動してください")
        commands.append("")
        
        return commands
    
    def method_5_xml_import(self, articles: List[Dict[str, Any]]) -> str:
        """
        方法5: WordPress XML形式でエクスポート
        WordPress Importerで読み込み可能
        """
        xml_content = """<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0"
    xmlns:excerpt="http://wordpress.org/export/1.2/excerpt/"
    xmlns:content="http://purl.org/rss/1.0/modules/content/"
    xmlns:wfw="http://wellformedweb.org/CommentAPI/"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:wp="http://wordpress.org/export/1.2/">
<channel>
    <title>Mountain Blog Articles</title>
    <link>{site_url}</link>
    <description>Mountain Blog Generator Export</description>
    <language>ja</language>
    <wp:wxr_version>1.2</wp:wxr_version>
    <generator>Mountain Blog Generator</generator>
"""
        
        for article in articles:
            # HTMLエンティティをエスケープ
            title = self._escape_xml(article.get('title', ''))
            content = self._escape_xml(article.get('content', ''))
            excerpt = self._escape_xml(article.get('excerpt', ''))
            
            xml_content += f"""
    <item>
        <title>{title}</title>
        <link>{self.base_url}/?p=1</link>
        <pubDate>{datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>
        <dc:creator><![CDATA[admin]]></dc:creator>
        <description></description>
        <content:encoded><![CDATA[{content}]]></content:encoded>
        <excerpt:encoded><![CDATA[{excerpt}]]></excerpt:encoded>
        <wp:post_date>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</wp:post_date>
        <wp:post_type>post</wp:post_type>
        <wp:status>draft</wp:status>
"""
            
            # タグを追加
            for tag in article.get('tags', []):
                xml_content += f"""
        <category domain="post_tag" nicename="{self._slugify(tag)}"><![CDATA[{tag}]]></category>
"""
            
            xml_content += """
    </item>
"""
        
        xml_content += """
</channel>
</rss>"""
        
        return xml_content
    
    def _escape_xml(self, text: str) -> str:
        """XMLエスケープ"""
        return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&apos;')
    
    def _slugify(self, text: str) -> str:
        """スラッグ生成"""
        # 簡易的なスラッグ生成
        return text.lower().replace(' ', '-').replace('　', '-')
    
    def generate_all_methods_report(self) -> str:
        """
        すべての代替方法のレポートを生成
        """
        report = """
# WordPress投稿 代替方法レポート

## 現在の問題
- Application Passwords認証が401エラー
- REST APIへの認証が通らない

## 解決策

### 1. Cookie認証（要: 実パスワード）
- 通常のWordPressパスワードでログイン
- セッションCookieを使用してAPI呼び出し
- 最も確実だが、実パスワードが必要

### 2. WordPress XML Import（推奨）
- 記事をXML形式でエクスポート
- WordPress管理画面からインポート
- 最も安全で確実

### 3. WP-CLI（サーバーアクセス必要）
- コマンドラインから直接投稿
- 大量投稿に最適
- SSHアクセスが必要

### 4. 直接SQL（上級者向け）
- データベースに直接挿入
- 最速だがリスクあり
- バックアップ必須

### 5. カスタムプラグイン
- 認証を回避する専用エンドポイント
- 最も柔軟な方法
- 開発知識が必要

## 推奨フロー
1. 記事生成 → XML形式で出力
2. WordPress管理画面でインポート
3. 一括で下書き保存 → 確認後公開
"""
        return report


def test_alternative_methods():
    """代替方法のテスト"""
    client = WordPressAlternativeClient()
    
    print("🔍 WordPress投稿 代替方法分析")
    print("="*60)
    
    # レポート出力
    report = client.generate_all_methods_report()
    print(report)
    
    # XML形式での出力例
    print("\n📝 XML形式での出力例:")
    
    # サンプル記事データ
    sample_articles = [{
        'title': 'テスト記事',
        'content': 'これはテスト記事です。',
        'excerpt': 'テスト',
        'tags': ['テスト', 'サンプル']
    }]
    
    xml_content = client.method_5_xml_import(sample_articles)
    
    # XMLファイルとして保存
    with open('wordpress_import_sample.xml', 'w', encoding='utf-8') as f:
        f.write(xml_content)
    
    print("✅ wordpress_import_sample.xml を作成しました")
    print("   WordPress管理画面 → ツール → インポート → WordPress で読み込み可能")
    

if __name__ == '__main__':
    test_alternative_methods()