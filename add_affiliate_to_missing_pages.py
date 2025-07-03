#!/usr/bin/env python3
"""
アフィリエイトセクションが不足している山ページに追加
"""
from pathlib import Path
import re

def get_affiliate_template():
    """アフィリエイトセクションのテンプレートを取得"""
    return '''
            <div class="affiliate-section">
                <h3>🎒 おすすめの登山グッズ</h3>
                <p class="affiliate-disclaimer">※以下の商品リンクは楽天アフィリエイトです。価格・在庫は変動する場合があります。</p>
                <div class="affiliate-products">
                    <div class="affiliate-product">
                    <a href="https://hb.afl.rakuten.co.jp/ichiba/2c4ba3a3.7a6dd580.2c4ba3a4.bbdf25a3/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fsports%2Fnew-balance-hiking-shoes%2F&link_type=hybrid_url&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJoeWJyaWRfdXJsIiwic2l6ZSI6IjI0MHgyNDAiLCJuYW0iOjEsIm5hbXAiOiJyaWdodCIsImNvbSI6MSwiY29tcCI6ImRvd24iLCJwcmljZSI6MSwiYm9yIjoxLCJjb2wiOjEsImJidG4iOjEsInByb2QiOjAsImFtcCI6ZmFsc2V9" target="_blank" rel="noopener nofollow" onclick="gtag(\'event\', \'click\', {\'event_category\': \'affiliate\', \'event_label\': \'トレッキングシューズ\'});">
                        トレッキングシューズ
                    </a>
                    <span class="price">¥8,900</span>
                </div>
<div class="affiliate-product">
                    <a href="https://hb.afl.rakuten.co.jp/ichiba/2c4ba3a3.7a6dd580.2c4ba3a4.bbdf25a3/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Foutdoor%2Fmontbell-daypack%2F&link_type=hybrid_url&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJoeWJyaWRfdXJsIiwic2l6ZSI6IjI0MHgyNDAiLCJuYW0iOjEsIm5hbXAiOiJyaWdodCIsImNvbSI6MSwiY29tcCI6ImRvd24iLCJwcmljZSI6MSwiYm9yIjoxLCJjb2wiOjEsImJidG4iOjEsInByb2QiOjAsImFtcCI6ZmFsc2V9" target="_blank" rel="noopener nofollow" onclick="gtag(\'event\', \'click\', {\'event_category\': \'affiliate\', \'event_label\': \'軽量デイパック\'});">
                        軽量デイパック 20L
                    </a>
                    <span class="price">¥5,500</span>
                </div>
<div class="affiliate-product">
                    <a href="https://hb.afl.rakuten.co.jp/ichiba/2c4ba3a3.7a6dd580.2c4ba3a4.bbdf25a3/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fsports%2Fhydration-bottle%2F&link_type=hybrid_url&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJoeWJyaWRfdXJsIiwic2l6ZSI6IjI0MHgyNDAiLCJuYW0iOjEsIm5hbXAiOiJyaWdodCIsImNvbSI6MSwiY29tcCI6ImRvd24iLCJwcmljZSI6MSwiYm9yIjoxLCJjb2wiOjEsImJidG4iOjEsInByb2QiOjAsImFtcCI6ZmFsc2V9" target="_blank" rel="noopener nofollow" onclick="gtag(\'event\', \'click\', {\'event_category\': \'affiliate\', \'event_label\': \'保温・保冷水筒\'});">
                        保温・保冷水筒 500ml
                    </a>
                    <span class="price">¥2,980</span>
                </div>
<div class="affiliate-product">
                    <a href="https://hb.afl.rakuten.co.jp/ichiba/2c4ba3a3.7a6dd580.2c4ba3a4.bbdf25a3/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Foutdoor%2Frain-jacket%2F&link_type=hybrid_url&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJoeWJyaWRfdXJsIiwic2l6ZSI6IjI0MHgyNDAiLCJuYW0iOjEsIm5hbXAiOiJyaWdodCIsImNvbSI6MSwiY29tcCI6ImRvd24iLCJwcmljZSI6MSwiYm9yIjoxLCJjb2wiOjEsImJidG4iOjEsInByb2QiOjAsImFtcCI6ZmFsc2V9" target="_blank" rel="noopener nofollow" onclick="gtag(\'event\', \'click\', {\'event_category\': \'affiliate\', \'event_label\': \'軽量レインジャケット\'});">
                        軽量レインジャケット
                    </a>
                    <span class="price">¥3,200</span>
                </div>
<div class="affiliate-product">
                    <a href="https://hb.afl.rakuten.co.jp/ichiba/2c4ba3a3.7a6dd580.2c4ba3a4.bbdf25a3/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fsafety%2Fbear-bell%2F&link_type=hybrid_url&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJoeWJyaWRfdXJsIiwic2l6ZSI6IjI0MHgyNDAiLCJuYW0iOjEsIm5hbXAiOiJyaWdodCIsImNvbSI6MSwiY29tcCI6ImRvd24iLCJwcmljZSI6MSwiYm9yIjoxLCJjb2wiOjEsImJidG4iOjEsInByb2QiOjAsImFtcCI6ZmFsc2V9" target="_blank" rel="noopener nofollow" onclick="gtag(\'event\', \'click\', {\'event_category\': \'affiliate\', \'event_label\': \'登山用熊鈴\'});">
                        登山用熊鈴
                    </a>
                    <span class="price">¥890</span>
                </div>
                </div>
                <p class="affiliate-note">💡 <strong>登山装備選びのポイント:</strong> 軽量性、耐久性、機能性のバランスを考慮して選びましょう。</p>
            </div>'''

def add_affiliate_sections():
    """アフィリエイトセクションを不足ページに追加"""
    
    mountains_dir = Path('static_site/mountains')
    affiliate_template = get_affiliate_template()
    updated_files = []
    
    print("🛒 アフィリエイトセクション追加開始...\n")
    
    for mountain_dir in mountains_dir.iterdir():
        if mountain_dir.is_dir() and mountain_dir.name != 'index.html':
            index_file = mountain_dir / 'index.html'
            
            if index_file.exists():
                content = index_file.read_text(encoding='utf-8')
                
                # アフィリエイトセクションがない場合は追加
                if 'affiliate-section' not in content:
                    # 関連記事の前に挿入
                    pattern = r'(\s*<div class="related-articles">)'
                    replacement = affiliate_template + r'\n                \1'
                    
                    new_content = re.sub(pattern, replacement, content)
                    
                    if new_content != content:
                        index_file.write_text(new_content, encoding='utf-8')
                        updated_files.append(mountain_dir.name)
                        print(f"  ✅ 追加: {mountain_dir.name}")
                    else:
                        print(f"  ⚠️  挿入位置が見つからない: {mountain_dir.name}")
                else:
                    print(f"  ✓ 既存: {mountain_dir.name}")
    
    print(f"\n📊 結果:")
    print(f"  更新ファイル数: {len(updated_files)}")
    if updated_files:
        print(f"  更新した山: {', '.join(updated_files)}")
    
    return updated_files

if __name__ == "__main__":
    files = add_affiliate_sections()
    
    if files:
        print(f"\n🚀 {len(files)}個のファイルにアフィリエイトセクションを追加しました。")
    else:
        print(f"\n✅ 追加が必要なファイルはありませんでした。")