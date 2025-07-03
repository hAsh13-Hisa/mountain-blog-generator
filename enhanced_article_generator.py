#!/usr/bin/env python3
"""
BE-PAL記事参考情報を活用した強化版記事生成器
"""
import json
from datetime import datetime
from pathlib import Path

class EnhancedArticleGenerator:
    def __init__(self):
        self.load_mountain_data()
    
    def load_mountain_data(self):
        """山データ（BE-PAL参考情報付き）を読み込み"""
        with open('data/mountains_japan_expanded.json', 'r', encoding='utf-8') as f:
            self.mountains_data = json.load(f)
    
    def get_mountain_by_id(self, mountain_id):
        """IDで山データを検索"""
        for mountain in self.mountains_data['mountains']:
            if mountain['id'] == mountain_id:
                return mountain
        return None
    
    def generate_enhanced_article_prompt(self, mountain_id):
        """BE-PAL参考情報を活用した強化版記事生成プロンプト"""
        mountain = self.get_mountain_by_id(mountain_id)
        if not mountain:
            return None
        
        # BE-PAL参考情報の確認
        bepal_info = mountain.get('bepal_reference')
        has_bepal_info = bepal_info is not None
        
        # プロンプト構築
        prompt = f"""
以下の山について、初心者・家族向けの魅力的な登山記事を作成してください。

## 基本情報
- 山名: {mountain['name']} ({mountain['elevation']}m)
- 所在地: {mountain['prefecture']} ({mountain['region']}地方)
- 難易度: {mountain['difficulty']['level']}
- アクセス: {mountain['location']['access_time']}

## 主な特徴
{', '.join(mountain['features'])}

## 推奨記事テーマ
{', '.join(mountain['article_themes'])}
"""
        
        # BE-PAL参考情報がある場合は追加
        if has_bepal_info:
            prompt += f"""
## 参考情報（BE-PAL記事より）
{bepal_info['description']}
"""
            
            if bepal_info.get('expert_comment'):
                prompt += f"""
### 専門家コメント
{bepal_info['expert_name']}: 「{bepal_info['expert_comment']}」
"""
        
        prompt += """
## 記事作成要件
1. **ターゲット**: 登山初心者・家族連れ
2. **文字数**: 2000-3000文字
3. **構成**: 
   - 魅力的な導入
   - アクセス・基本情報
   - 登山コース・見どころ
   - 季節の楽しみ方
   - 初心者向けアドバイス
   - 周辺の楽しみ方

4. **記述スタイル**:
   - 親しみやすく読みやすい文体
   - 具体的で実用的な情報
   - 安全面への配慮
   - 家族で楽しめる要素を強調

5. **SEO配慮**:
   - 地域名＋山名を自然に含める
   - 関連キーワードを適切に配置
   - 見出し構造を明確に
"""
        
        # 出典情報（BE-PAL参考情報がある場合）
        if has_bepal_info:
            prompt += f"""
## 重要: 出典明記
記事末尾に以下の参考文献情報を必ず記載してください：

【参考文献】
BE-PAL「全国のおすすめ低山58選！登山初心者も楽しめる人気の山を紹介」
{bepal_info['source_url']}
- {bepal_info['reference_article']}
"""
        
        return prompt
    
    def generate_article_metadata(self, mountain_id):
        """記事メタデータ生成"""
        mountain = self.get_mountain_by_id(mountain_id)
        if not mountain:
            return None
        
        bepal_info = mountain.get('bepal_reference')
        
        metadata = {
            "id": f"article_{mountain_id}_{datetime.now().strftime('%Y%m%d')}",
            "mountain_id": mountain_id,
            "title": f"{mountain['name']}（{mountain['elevation']}m）- {mountain['prefecture']}の初心者向け低山",
            "meta_description": f"{mountain['prefecture']}の{mountain['name']}（{mountain['elevation']}m）は{mountain['difficulty']['level']}レベルの低山。{', '.join(mountain['features'][:3])}が魅力。家族や初心者におすすめの登山コースを詳しく紹介。",
            "keywords": mountain['keywords'],
            "featured_image_alt": f"{mountain['name']}の登山風景",
            "category": "低山登山",
            "tags": ["初心者向け", "家族登山", mountain['prefecture'], mountain['region']],
            "difficulty_level": mountain['difficulty']['level'],
            "elevation": mountain['elevation'],
            "hiking_time": mountain['difficulty']['hiking_time'],
            "bepal_reference": bepal_info is not None,
            "created_at": datetime.now().isoformat()
        }
        
        return metadata
    
    def list_mountains_with_bepal_info(self):
        """BE-PAL参考情報付きの山をリスト表示"""
        bepal_mountains = []
        for mountain in self.mountains_data['mountains']:
            if 'bepal_reference' in mountain:
                bepal_mountains.append({
                    "id": mountain['id'],
                    "name": mountain['name'],
                    "prefecture": mountain['prefecture'],
                    "elevation": mountain['elevation'],
                    "has_expert_comment": bool(mountain['bepal_reference'].get('expert_comment'))
                })
        
        return bepal_mountains

# 実行例
if __name__ == "__main__":
    generator = EnhancedArticleGenerator()
    
    print("🏔️ BE-PAL参考情報付きの山一覧:")
    bepal_mountains = generator.list_mountains_with_bepal_info()
    
    for mountain in bepal_mountains:
        expert_mark = "👨‍🏫" if mountain['has_expert_comment'] else "📄"
        print(f"{expert_mark} {mountain['name']} ({mountain['prefecture']}, {mountain['elevation']}m)")
    
    print(f"\n📈 合計: {len(bepal_mountains)}山にBE-PAL参考情報を統合")
    
    # サンプル記事プロンプト生成
    sample_mountain = "mt_kinuhariyama_kanagawa"  # 衣張山
    prompt = generator.generate_enhanced_article_prompt(sample_mountain)
    
    print(f"\n📝 サンプル記事プロンプト（{sample_mountain}）:")
    print("=" * 50)
    print(prompt[:500] + "..." if len(prompt) > 500 else prompt)