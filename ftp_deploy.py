#!/usr/bin/env python3
"""
ロリポップサーバーへのFTPデプロイスクリプト
"""
import ftplib
import os
from pathlib import Path
from datetime import datetime
import json
from dotenv import load_dotenv

load_dotenv()

class LolipopFTPDeployer:
    def __init__(self):
        # FTP設定（.envファイルから読み込み）
        self.ftp_host = os.getenv('LOLIPOP_FTP_HOST', 'ftp.lolipop.jp')
        self.ftp_user = os.getenv('LOLIPOP_FTP_USER')
        self.ftp_pass = os.getenv('LOLIPOP_FTP_PASS')
        self.remote_dir = os.getenv('LOLIPOP_REMOTE_DIR', '/mountain-blog')
        
        # ローカルディレクトリ
        self.local_dir = Path('dist')
        self.articles_dir = Path('generated_articles')
        
    def connect(self):
        """FTP接続"""
        self.ftp = ftplib.FTP(self.ftp_host)
        self.ftp.login(self.ftp_user, self.ftp_pass)
        print(f"Connected to {self.ftp_host}")
        
    def disconnect(self):
        """FTP切断"""
        self.ftp.quit()
        print("Disconnected from FTP server")
    
    def create_remote_dir(self, path):
        """リモートディレクトリ作成"""
        try:
            self.ftp.mkd(path)
            print(f"Created directory: {path}")
        except ftplib.error_perm:
            # ディレクトリが既に存在する場合
            pass
    
    def upload_file(self, local_file, remote_path):
        """ファイルアップロード"""
        with open(local_file, 'rb') as f:
            self.ftp.storbinary(f'STOR {remote_path}', f)
        print(f"Uploaded: {local_file} -> {remote_path}")
    
    def upload_directory(self, local_dir, remote_dir):
        """ディレクトリ全体をアップロード"""
        local_path = Path(local_dir)
        
        for item in local_path.rglob('*'):
            if item.is_file():
                # リモートパス計算
                relative_path = item.relative_to(local_path)
                remote_path = f"{remote_dir}/{relative_path}".replace('\\', '/')
                
                # ディレクトリ作成
                remote_file_dir = '/'.join(remote_path.split('/')[:-1])
                if remote_file_dir:
                    self.create_remote_dir(remote_file_dir)
                
                # ファイルアップロード
                self.upload_file(item, remote_path)
    
    def generate_html_from_article(self, article_json):
        """記事JSONからHTML生成"""
        with open(article_json, 'r', encoding='utf-8') as f:
            article = json.load(f)
        
        html_template = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{article['title']}</title>
    <meta name="description" content="{article['meta_description']}">
    <meta name="keywords" content="{', '.join(article['keywords'])}">
    <link rel="stylesheet" href="/css/style.css">
</head>
<body>
    <header>
        <h1>日本の低山ガイド</h1>
        <nav>
            <a href="/">ホーム</a>
            <a href="/mountains">山一覧</a>
            <a href="/about">このサイトについて</a>
        </nav>
    </header>
    
    <main>
        <article>
            <h1>{article['title']}</h1>
            <img src="{article['featured_image_url']}" alt="{article['title']}" class="featured-image">
            
            <div class="article-meta">
                <span>山名: {article['mountain_name']}</span>
                <span>標高: {article['elevation']}m</span>
                <span>更新日: {article['date']}</span>
            </div>
            
            <div class="article-content">
                {article['content']}
            </div>
            
            <div class="affiliate-section">
                <h2>おすすめ商品</h2>
                <div class="products">
                    {''.join([self._generate_product_html(p) for p in article['affiliate_products']])}
                </div>
            </div>
        </article>
    </main>
    
    <footer>
        <p>&copy; 2025 日本の低山ガイド</p>
    </footer>
</body>
</html>"""
        
        return html_template
    
    def _generate_product_html(self, product):
        """商品HTML生成"""
        return f"""
        <div class="product-card">
            <a href="{product['affiliateUrl']}" target="_blank" rel="noopener">
                <img src="{product['mediumImageUrl']}" alt="{product['itemName']}">
                <h3>{product['itemName']}</h3>
            </a>
        </div>
        """
    
    def deploy_site(self):
        """サイト全体をデプロイ"""
        try:
            self.connect()
            
            # 基本ディレクトリ作成
            self.create_remote_dir(self.remote_dir)
            self.ftp.cwd(self.remote_dir)
            
            # CSSアップロード
            self.create_remote_dir('css')
            self.upload_file('static/style.css', 'css/style.css')
            
            # 記事HTMLを生成してアップロード
            self.create_remote_dir('articles')
            for json_file in self.articles_dir.glob('*.json'):
                if 'with_image' not in str(json_file):
                    html_content = self.generate_html_from_article(json_file)
                    html_filename = json_file.stem + '.html'
                    
                    # 一時HTMLファイル作成
                    temp_html = Path(f'temp_{html_filename}')
                    with open(temp_html, 'w', encoding='utf-8') as f:
                        f.write(html_content)
                    
                    # アップロード
                    self.upload_file(temp_html, f'articles/{html_filename}')
                    
                    # 一時ファイル削除
                    temp_html.unlink()
            
            # インデックスページ生成・アップロード
            self.generate_and_upload_index()
            
            print("Deployment completed successfully!")
            
        finally:
            self.disconnect()
    
    def generate_and_upload_index(self):
        """インデックスページ生成・アップロード"""
        # 記事一覧取得
        articles = []
        for json_file in self.articles_dir.glob('*.json'):
            if 'with_image' not in str(json_file):
                with open(json_file, 'r', encoding='utf-8') as f:
                    article = json.load(f)
                    articles.append({
                        'title': article['title'],
                        'url': f'/articles/{json_file.stem}.html',
                        'mountain': article['mountain_name'],
                        'elevation': article['elevation']
                    })
        
        # インデックスHTML生成
        index_html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>日本の低山ガイド - 標高400m以下の初心者向け登山情報</title>
    <link rel="stylesheet" href="/css/style.css">
</head>
<body>
    <header>
        <h1>日本の低山ガイド</h1>
        <p>標高400m以下、登山道整備済みの安全な低山情報</p>
    </header>
    
    <main>
        <h2>山の記事一覧</h2>
        <div class="article-list">
            {''.join([f'''
            <div class="article-card">
                <h3><a href="{a['url']}">{a['title']}</a></h3>
                <p>{a['mountain']} (標高{a['elevation']}m)</p>
            </div>
            ''' for a in articles])}
        </div>
    </main>
    
    <footer>
        <p>&copy; 2025 日本の低山ガイド</p>
    </footer>
</body>
</html>"""
        
        # 一時ファイル作成・アップロード
        temp_index = Path('temp_index.html')
        with open(temp_index, 'w', encoding='utf-8') as f:
            f.write(index_html)
        
        self.upload_file(temp_index, 'index.html')
        temp_index.unlink()

if __name__ == "__main__":
    deployer = LolipopFTPDeployer()
    deployer.deploy_site()