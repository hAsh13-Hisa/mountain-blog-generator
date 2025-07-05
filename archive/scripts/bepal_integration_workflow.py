#!/usr/bin/env python3
"""
BE-PAL記事統合ワークフロー - 再利用可能なシステム
新しいBE-PAL記事や外部記事を山データベースに統合するための標準化されたツール
"""
import json
import re
from datetime import datetime
from pathlib import Path

class BePalIntegrationWorkflow:
    def __init__(self):
        self.mountains_db_path = Path("data/mountains_japan_expanded.json")
        self.elevation_limit = 400  # 標高制限
        self.workflow_log = []
    
    def log_step(self, step, message):
        """ワークフロー進行ログ"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {step}: {message}"
        self.workflow_log.append(log_entry)
        print(f"🔄 {log_entry}")
    
    def extract_mountain_data_from_text(self, text_content, source_info):
        """
        テキストから山の情報を抽出
        
        Parameters:
        text_content (str): 記事のテキスト内容
        source_info (dict): ソース情報（タイトル、URL、出版社など）
        
        Returns:
        list: 抽出された山データのリスト
        """
        self.log_step("EXTRACT", "記事テキストから山データを抽出開始")
        
        extracted_mountains = []
        
        # 標高パターンのマッチング（標高XXXm）
        elevation_pattern = r'標高(\d+(?:\.\d+)?)m'
        # 山名パターンのマッチング
        mountain_pattern = r'([都道府県]{2,3}）｜([^｜\n]+)'
        
        lines = text_content.split('\n')
        current_mountain = None
        
        for i, line in enumerate(lines):
            # 都道府県｜山名 のパターンを検索
            if '｜' in line and any(pref in line for pref in ['県', '府', '道', '都']):
                parts = line.split('｜')
                if len(parts) >= 2:
                    prefecture = parts[0].strip()
                    mountain_name = parts[1].strip()
                    
                    # 次の行で標高を探す
                    next_lines = lines[i+1:i+5]  # 次の4行を確認
                    elevation = None
                    description = ""
                    
                    for next_line in next_lines:
                        elevation_match = re.search(elevation_pattern, next_line)
                        if elevation_match:
                            elevation = float(elevation_match.group(1))
                            break
                    
                    # 標高制限チェック
                    if elevation and elevation <= self.elevation_limit:
                        # 説明文を抽出（標高行から数行先まで）
                        desc_start = i + 2
                        desc_lines = []
                        for j in range(desc_start, min(desc_start + 10, len(lines))):
                            if j < len(lines):
                                desc_line = lines[j].strip()
                                if desc_line and not desc_line.startswith('▼') and not desc_line.startswith('image'):
                                    desc_lines.append(desc_line)
                                elif desc_line.startswith('▼'):
                                    break
                        
                        description = ' '.join(desc_lines)
                        
                        mountain_data = {
                            "name": mountain_name,
                            "prefecture": prefecture,
                            "elevation": elevation,
                            "description": description,
                            "source": source_info
                        }
                        
                        extracted_mountains.append(mountain_data)
                        self.log_step("FOUND", f"{mountain_name} ({prefecture}, {elevation}m)")
        
        self.log_step("EXTRACT", f"抽出完了: {len(extracted_mountains)}山を発見")
        return extracted_mountains
    
    def create_mountain_id(self, mountain_name, prefecture):
        """山IDを生成"""
        # 山名から不要な文字を除去し、ローマ字風のIDを生成
        clean_name = re.sub(r'[山岳峰嶽]', '', mountain_name)
        prefecture_short = {
            '北海道': 'hokkaido', '青森県': 'aomori', '岩手県': 'iwate', '宮城県': 'miyagi',
            '秋田県': 'akita', '山形県': 'yamagata', '福島県': 'fukushima', '茨城県': 'ibaraki',
            '栃木県': 'tochigi', '群馬県': 'gunma', '埼玉県': 'saitama', '千葉県': 'chiba',
            '東京都': 'tokyo', '神奈川県': 'kanagawa', '新潟県': 'niigata', '富山県': 'toyama',
            '石川県': 'ishikawa', '福井県': 'fukui', '山梨県': 'yamanashi', '長野県': 'nagano',
            '岐阜県': 'gifu', '静岡県': 'shizuoka', '愛知県': 'aichi', '三重県': 'mie',
            '滋賀県': 'shiga', '京都府': 'kyoto', '大阪府': 'osaka', '兵庫県': 'hyogo',
            '奈良県': 'nara', '和歌山県': 'wakayama', '鳥取県': 'tottori', '島根県': 'shimane',
            '岡山県': 'okayama', '広島県': 'hiroshima', '山口県': 'yamaguchi', '徳島県': 'tokushima',
            '香川県': 'kagawa', '愛媛県': 'ehime', '高知県': 'kochi', '福岡県': 'fukuoka',
            '佐賀県': 'saga', '長崎県': 'nagasaki', '熊本県': 'kumamoto', '大分県': 'oita',
            '宮崎県': 'miyazaki', '鹿児島県': 'kagoshima', '沖縄県': 'okinawa'
        }.get(prefecture, 'unknown')
        
        # 簡単なローマ字変換（基本的なもののみ）
        name_romaji = clean_name.lower().replace('ヶ', 'ga').replace('ー', '').replace('・', '')
        
        return f"mt_{name_romaji}_{prefecture_short}"
    
    def convert_to_full_mountain_data(self, extracted_mountain, existing_mountains):
        """
        抽出された山データを完全な山データ形式に変換
        """
        mountain_id = self.create_mountain_id(extracted_mountain['name'], extracted_mountain['prefecture'])
        
        # 重複チェック
        if any(m['id'] == mountain_id for m in existing_mountains):
            self.log_step("SKIP", f"{extracted_mountain['name']} - 既存データに存在")
            return None
        
        # 地域判定
        region_map = {
            '北海道': '北海道',
            '青森県': '東北', '岩手県': '東北', '宮城県': '東北', '秋田県': '東北', '山形県': '東北', '福島県': '東北',
            '茨城県': '関東', '栃木県': '関東', '群馬県': '関東', '埼玉県': '関東', '千葉県': '関東', '東京都': '関東', '神奈川県': '関東',
            '新潟県': '中部', '富山県': '中部', '石川県': '中部', '福井県': '中部', '山梨県': '中部', '長野県': '中部', '岐阜県': '中部', '静岡県': '中部', '愛知県': '中部',
            '三重県': '関西', '滋賀県': '関西', '京都府': '関西', '大阪府': '関西', '兵庫県': '関西', '奈良県': '関西', '和歌山県': '関西',
            '鳥取県': '中国', '島根県': '中国', '岡山県': '中国', '広島県': '中国', '山口県': '中国',
            '徳島県': '四国', '香川県': '四国', '愛媛県': '四国', '高知県': '四国',
            '福岡県': '九州', '佐賀県': '九州', '長崎県': '九州', '熊本県': '九州', '大分県': '九州', '宮崎県': '九州', '鹿児島県': '九州', '沖縄県': '九州'
        }
        
        region = region_map.get(extracted_mountain['prefecture'], '不明')
        
        # 完全な山データ構造を作成
        full_mountain_data = {
            "id": mountain_id,
            "name": extracted_mountain['name'],
            "name_en": f"Mount {extracted_mountain['name']}",
            "prefecture": extracted_mountain['prefecture'],
            "region": region,
            "elevation": extracted_mountain['elevation'],
            "location": {
                "latitude": 0.0,  # 要手動入力
                "longitude": 0.0,  # 要手動入力
                "nearest_station": "要調査",
                "access_time": "要調査"
            },
            "difficulty": {
                "level": "初級",  # デフォルト
                "hiking_time": "要調査",
                "distance": "要調査",
                "elevation_gain": f"約{int(extracted_mountain['elevation'] * 0.8)}m"
            },
            "features": ["要調査"],
            "seasons": {
                "best": ["春", "秋"],
                "cherry_blossom": "要調査",
                "autumn_leaves": "要調査"
            },
            "keywords": [extracted_mountain['prefecture'].replace('県', '').replace('府', '').replace('道', '').replace('都', ''), "低山", "初心者向け"],
            "article_themes": [
                f"{extracted_mountain['name']}の魅力",
                f"{extracted_mountain['prefecture']}の低山ハイキング"
            ],
            "source_reference": {
                "description": extracted_mountain['description'],
                "source": extracted_mountain['source']['title'],
                "source_url": extracted_mountain['source']['url'],
                "extraction_date": datetime.now().strftime("%Y-%m-%d")
            }
        }
        
        self.log_step("CONVERT", f"{extracted_mountain['name']} データ変換完了")
        return full_mountain_data
    
    def integrate_new_mountains(self, extracted_mountains):
        """
        新しい山データを既存データベースに統合
        """
        self.log_step("INTEGRATE", "既存データベースを読み込み")
        
        with open(self.mountains_db_path, 'r', encoding='utf-8') as f:
            mountains_db = json.load(f)
        
        existing_mountains = mountains_db['mountains']
        new_mountains = []
        
        for extracted_mountain in extracted_mountains:
            full_data = self.convert_to_full_mountain_data(extracted_mountain, existing_mountains)
            if full_data:
                new_mountains.append(full_data)
                existing_mountains.append(full_data)
        
        if new_mountains:
            # メタデータ更新
            version_parts = mountains_db['metadata']['version'].split('.')
            new_version = f"{version_parts[0]}.{int(version_parts[1]) + 1}"
            
            mountains_db['metadata']['version'] = new_version
            mountains_db['metadata']['last_updated'] = datetime.now().strftime("%Y-%m-%d")
            mountains_db['metadata']['total_mountains'] = len(existing_mountains)
            
            # データベース保存
            with open(self.mountains_db_path, 'w', encoding='utf-8') as f:
                json.dump(mountains_db, f, ensure_ascii=False, indent=2)
            
            self.log_step("SAVE", f"データベース更新完了 (v{new_version})")
            self.log_step("SUCCESS", f"{len(new_mountains)}山を新規追加")
        else:
            self.log_step("INFO", "追加できる新しい山データはありませんでした")
        
        return new_mountains
    
    def run_full_workflow(self, article_file_path, source_info):
        """
        完全なワークフローを実行
        
        Parameters:
        article_file_path (str): 記事テキストファイルのパス
        source_info (dict): ソース情報
            - title: 記事タイトル
            - url: 記事URL
            - publication: 出版社
            - date: 公開日
        
        Returns:
        dict: 実行結果
        """
        self.log_step("START", f"BE-PAL統合ワークフロー開始: {article_file_path}")
        
        try:
            # 1. テキストファイル読み込み
            with open(article_file_path, 'r', encoding='utf-8') as f:
                text_content = f.read()
            
            # 2. 山データ抽出
            extracted_mountains = self.extract_mountain_data_from_text(text_content, source_info)
            
            # 3. データベース統合
            new_mountains = self.integrate_new_mountains(extracted_mountains)
            
            # 4. 結果サマリー作成
            summary_file = f"integration_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            summary = {
                "workflow_date": datetime.now().isoformat(),
                "source_info": source_info,
                "extracted_count": len(extracted_mountains),
                "integrated_count": len(new_mountains),
                "new_mountains": new_mountains,
                "workflow_log": self.workflow_log
            }
            
            with open(f"logs/{summary_file}", 'w', encoding='utf-8') as f:
                json.dump(summary, f, ensure_ascii=False, indent=2)
            
            self.log_step("COMPLETE", f"ワークフロー完了 - サマリー: logs/{summary_file}")
            
            return {
                "status": "success",
                "extracted_count": len(extracted_mountains),
                "integrated_count": len(new_mountains),
                "summary_file": summary_file
            }
            
        except Exception as e:
            self.log_step("ERROR", f"ワークフロー実行エラー: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "workflow_log": self.workflow_log
            }

# 使用例とヘルパー関数
def create_bepal_source_info(article_title, article_url):
    """BE-PAL記事用のソース情報を作成"""
    return {
        "title": article_title,
        "url": article_url,
        "publication": "BE-PAL",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "copyright_notice": "記事内容の引用時は出典を明記すること"
    }

# CLI実行用メイン関数
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python bepal_integration_workflow.py <記事ファイル.txt> [記事タイトル] [記事URL]")
        print()
        print("例:")
        print("  python bepal_integration_workflow.py BE-PAL記事.txt")
        print("  python bepal_integration_workflow.py 新記事.txt '記事タイトル' 'https://example.com'")
        sys.exit(1)
    
    article_file = sys.argv[1]
    article_title = sys.argv[2] if len(sys.argv) > 2 else "記事タイトル未設定"
    article_url = sys.argv[3] if len(sys.argv) > 3 else "URL未設定"
    
    # ログディレクトリ作成
    Path("logs").mkdir(exist_ok=True)
    
    # ワークフロー実行
    workflow = BePalIntegrationWorkflow()
    source_info = create_bepal_source_info(article_title, article_url)
    
    result = workflow.run_full_workflow(article_file, source_info)
    
    print("\n" + "="*50)
    print("🏔️ BE-PAL統合ワークフロー結果")
    print("="*50)
    if result["status"] == "success":
        print(f"✅ 成功")
        print(f"📊 抽出された山: {result['extracted_count']}山")
        print(f"🆕 新規追加: {result['integrated_count']}山")
        print(f"📄 詳細レポート: {result['summary_file']}")
    else:
        print(f"❌ エラー: {result['error']}")
    print("="*50)