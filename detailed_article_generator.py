#!/usr/bin/env python3
"""
APIを使わずに詳細記事を生成するジェネレーター
"""
import json
import os
from datetime import datetime
from pathlib import Path

class DetailedArticleGenerator:
    def __init__(self):
        self.load_data()
    
    def load_data(self):
        """データファイルを読み込み"""
        with open('data/mountains_japan_expanded.json', 'r', encoding='utf-8') as f:
            self.mountains_data = json.load(f)
    
    def generate_detailed_article_content(self, mountain):
        """データベースから詳細記事コンテンツを生成（APIなし）"""
        name = mountain['name']
        elevation = mountain['elevation']
        prefecture = mountain.get('prefecture', self.get_prefecture_from_id(mountain['id']))
        features = mountain.get('features', [])
        difficulty = mountain.get('difficulty', {})
        location = mountain.get('location', {})
        
        # 見出し用セクションID生成
        sections = [
            f"{name}の魅力と基本情報",
            "アクセス情報", 
            "登山コースと見どころ",
            f"{name}で出会える自然",
            "季節ごとの楽しみ方",
            "初心者・家族連れへのアドバイス",
            "おすすめの登山装備",
            "周辺の見どころ・グルメ",
            f"まとめ：{name}の魅力"
        ]
        
        # 目次HTML生成
        toc_html = ""
        for i, section in enumerate(sections, 1):
            toc_html += f'<li><a href="#section-{i}">{section}</a></li>'
        
        # 特徴リスト
        features_list = ""
        if features:
            for feature in features[:5]:
                features_list += f"<li><strong>{feature}</strong></li>"
        
        # 基本データ
        basic_data = f"""
<h3>基本データ</h3>
<ul>
<li><strong>標高</strong>：{elevation}m</li>
<li><strong>登山時間</strong>：{difficulty.get('hiking_time', '片道1-2時間（初心者でも安心）')}</li>
<li><strong>登山距離</strong>：{difficulty.get('distance', '約3-5km（往復）')}</li>
<li><strong>難易度</strong>：{difficulty.get('level', '初級')}（登山道は整備済み）</li>
<li><strong>最寄り駅</strong>：{location.get('nearest_station', '要確認')}</li>
</ul>
"""
        
        # アクセス情報
        access_info = f"""
<h3>公共交通機関でのアクセス</h3>
<ul>
<li><strong>最寄り駅</strong>：{location.get('nearest_station', '要確認')}</li>
<li><strong>アクセス時間</strong>：{location.get('access_time', '要確認')}</li>
</ul>

<h3>車でのアクセス</h3>
<ul>
<li>主要都市から約30分-1時間程度</li>
<li><strong>駐車場</strong>：登山口付近に有料駐車場あり（要確認）</li>
<li>休日は混雑するため、早めの到着がおすすめ</li>
</ul>
"""
        
        # 季節情報
        seasons_info = """
<h3>春（3月〜5月）</h3>
<p>新緑の季節。山野草が美しく、気候も登山に適しています。</p>

<h3>夏（6月〜8月）</h3>
<p>緑豊かな季節。早朝登山がおすすめで、涼しい山頂で休憩を楽しめます。</p>

<h3>秋（9月〜11月）</h3>
<p>紅葉シーズン。山全体が美しく色づき、一年で最も人気の季節です。</p>

<h3>冬（12月〜2月）</h3>
<p>積雪期は装備を整えて。晴れた日の雪景色は格別の美しさです。</p>
"""
        
        # 詳細記事コンテンツ
        content = f"""<h2 id="section-1">{name}の魅力と基本情報</h2>
<p>{name}（{name.replace('山', 'やま').replace('岳', 'だけ')}）は、{prefecture}に位置する標高{elevation}mの低山です。初心者や家族連れでも安心して楽しめる山として人気があり、登山道も整備されているため、日帰り登山の定番スポットとして多くの人に愛されています。</p>

{basic_data}

<h2 id="section-2">アクセス情報</h2>
<p>{name}へのアクセスは比較的良好です。</p>

{access_info}

<h2 id="section-3">登山コースと見どころ</h2>
<p>{name}には初心者向けのコースが整備されており、安全に登山を楽しめます。</p>

<h3>主要登山コース</h3>
<ul>
<li><strong>所要時間</strong>：{difficulty.get('hiking_time', '登り1-2時間、下り30分-1時間')}</li>
<li><strong>特徴</strong>：整備された登山道で初心者でも安心</li>
<li><strong>見どころ</strong>：山頂からの展望と豊かな自然</li>
</ul>

<h2 id="section-4">{name}で出会える自然</h2>
<p>{name}の魅力は、豊かな自然環境にあります。</p>

<h3>植物・自然</h3>
<ul>
{features_list if features_list else '<li>四季折々の美しい自然</li><li>様々な山野草</li><li>野鳥観察スポット</li>'}
</ul>

<h2 id="section-5">季節ごとの楽しみ方</h2>

{seasons_info}

<h2 id="section-6">初心者・家族連れへのアドバイス</h2>

<h3>服装と持ち物</h3>
<ul>
<li><strong>服装</strong>：動きやすい服装、履き慣れた運動靴でOK</li>
<li><strong>持ち物</strong>：水分、軽食、タオル、虫除けスプレー（夏季）</li>
<li><strong>雨具</strong>：天候急変に備えて携帯を推奨</li>
</ul>

<h3>注意点</h3>
<ul>
<li>登山道以外への立ち入りは避ける</li>
<li>ゴミは必ず持ち帰る</li>
<li>野生動物に遭遇した場合は静かに距離を取る</li>
</ul>

<h2 id="section-7">おすすめの登山装備</h2>
<p>{name}登山を快適に楽しむための装備をご紹介します。初心者の方にも使いやすいアイテムを厳選しました。</p>

<h2 id="section-8">周辺の見どころ・グルメ</h2>

<h3>周辺の観光スポット</h3>
<p>登山の前後に立ち寄れる周辺の見どころや、地元のグルメスポットをご紹介。温泉や道の駅なども充実しており、一日中楽しめます。</p>

<h2 id="section-9">まとめ：{name}の魅力</h2>
<p>{name}は、{prefecture}を代表する魅力的な低山です。標高{elevation}mと手頃な高さながら、豊かな自然、美しい景観、そして山頂からの展望など、低山登山の醍醐味がすべて詰まっています。</p>

<p>初心者や家族連れでも安心して楽しめる整備された登山道、下山後には周辺の観光地やグルメスポットなど、一日中楽しめる要素が揃っています。週末の日帰り登山に、ぜひ{name}を訪れてみてはいかがでしょうか。豊かな自然と素晴らしい眺望が、きっと心に残る登山体験を提供してくれるでしょう。</p>"""
        
        return content, sections
    
    def get_prefecture_from_id(self, mountain_id):
        """IDから都道府県を推測"""
        if '_' in mountain_id:
            id_parts = mountain_id.split('_')
            if len(id_parts) >= 3:
                pref_code = id_parts[-1]
                pref_map = {
                    '秋田': '秋田県', '栃木': '栃木県', '埼玉': '埼玉県', 
                    '千葉': '千葉県', '神奈川': '神奈川県', '静岡': '静岡県',
                    '兵庫': '兵庫県', '愛媛': '愛媛県', '福岡': '福岡県', 
                    '大分': '大分県', '北海道': '北海道', '青森': '青森県',
                    '宮城': '宮城県', '群馬': '群馬県', '東京': '東京都',
                    '京都': '京都府', '大阪': '大阪府', '兵庫': '兵庫県',
                    '奈良': '奈良県', '和歌山': '和歌山県', '岡山': '岡山県',
                    '徳島': '徳島県', '香川': '香川県', '熊本': '熊本県',
                    '長崎': '長崎県', '鹿児島': '鹿児島県'
                }
                return pref_map.get(pref_code, pref_code)
        return '要確認'
    
    def generate_article_json(self, mountain):
        """詳細記事のJSONデータを生成"""
        prefecture = mountain.get('prefecture', self.get_prefecture_from_id(mountain['id']))
        content, sections = self.generate_detailed_article_content(mountain)
        
        # 目次HTML
        toc_html = ""
        for i, section in enumerate(sections, 1):
            toc_html += f'<li><a href="#section-{i}">{section}</a></li>'
        
        article_data = {
            "mountain_name": mountain['name'],
            "mountain_id": mountain['id'], 
            "elevation": mountain['elevation'],
            "prefecture": prefecture,
            "title": f"【{mountain['name']}完全ガイド】{prefecture}の魅力的な低山を徹底解説",
            "excerpt": f"{mountain['name']}は{prefecture}にある標高{mountain['elevation']}mの低山です。初心者でも楽しめる登山情報と魅力をご紹介します。",
            "content": content,
            "tags": [
                mountain['name'],
                prefecture,
                "低山",
                "初心者登山",
                "日帰り登山"
            ],
            "featured_image_url": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4",
            "featured_image_alt": f"{mountain['name']} 登山風景",
            "products_count": 8,
            "created_at": datetime.now().isoformat(),
            "table_of_contents": toc_html
        }
        
        return article_data
    
    def generate_all_detailed_articles(self):
        """全山の詳細記事を生成"""
        mountains = self.mountains_data['mountains']
        generated_count = 0
        
        for mountain in mountains:
            try:
                article_data = self.generate_article_json(mountain)
                
                # 記事ファイル保存
                filename = f"article_{mountain['name']}_{datetime.now().strftime('%Y%m%d')}.json"
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(article_data, f, ensure_ascii=False, indent=2)
                
                print(f"✅ 生成完了: {mountain['name']} ({mountain['elevation']}m)")
                generated_count += 1
                
            except Exception as e:
                print(f"❌ エラー: {mountain['name']} - {e}")
        
        print(f"\n🎉 詳細記事生成完了: {generated_count}山")
        return generated_count

if __name__ == "__main__":
    generator = DetailedArticleGenerator()
    generator.generate_all_detailed_articles()