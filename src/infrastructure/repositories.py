"""
データリポジトリ実装
"""
import json
import random
from typing import Dict, List, Optional, Any
from pathlib import Path

from config.settings import get_settings
from config.logging_config import LoggerMixin
from src.domain.entities import Mountain, MountainFactory, DifficultyLevel


class RepositoryError(Exception):
    """リポジトリエラー"""
    pass


class MountainRepository(LoggerMixin):
    """山データリポジトリ"""
    
    def __init__(self):
        self.settings = get_settings()
        self._mountains_cache: Optional[Dict[str, Mountain]] = None
        self._mountains_data: Optional[Dict[str, Any]] = None
    
    def _load_mountains_data(self) -> Dict[str, Any]:
        """山データを読み込み"""
        if self._mountains_data is None:
            try:
                mountains_file = Path(self.settings.mountains_file_path)
                
                # 拡張版全国データファイルを最優先
                expanded_file = Path(self.settings.DATA_DIR) / "mountains_japan_expanded.json"
                japan_file = Path(self.settings.DATA_DIR) / "mountains_japan.json"
                
                if expanded_file.exists():
                    data_file = expanded_file
                elif japan_file.exists():
                    data_file = japan_file
                elif mountains_file.exists():
                    data_file = mountains_file
                else:
                    raise RepositoryError("山データファイルが見つかりません")
                
                with open(data_file, 'r', encoding='utf-8') as f:
                    self._mountains_data = json.load(f)
                
                self.log_info(f"Loaded mountain data from: {data_file}")
                
            except (FileNotFoundError, json.JSONDecodeError) as e:
                self.log_error("Failed to load mountain data", e)
                raise RepositoryError(f"山データの読み込みに失敗: {str(e)}")
        
        return self._mountains_data
    
    def _load_mountains_cache(self) -> Dict[str, Mountain]:
        """山エンティティのキャッシュを読み込み"""
        if self._mountains_cache is None:
            data = self._load_mountains_data()
            self._mountains_cache = {}
            
            for mountain_data in data['mountains']:
                mountain = MountainFactory.from_dict(mountain_data)
                self._mountains_cache[mountain.id] = mountain
            
            self.log_info(f"Cached {len(self._mountains_cache)} mountains")
        
        return self._mountains_cache
    
    def get_by_id(self, mountain_id: str) -> Optional[Mountain]:
        """IDで山を取得"""
        mountains = self._load_mountains_cache()
        return mountains.get(mountain_id)
    
    def get_all(self) -> List[Mountain]:
        """全ての山を取得"""
        mountains = self._load_mountains_cache()
        return list(mountains.values())
    
    def get_by_region(self, region: str) -> List[Mountain]:
        """地域で山を検索"""
        mountains = self.get_all()
        return [m for m in mountains if m.region == region]
    
    def get_by_prefecture(self, prefecture: str) -> List[Mountain]:
        """都道府県で山を検索"""
        mountains = self.get_all()
        return [m for m in mountains if prefecture in m.prefecture]
    
    def get_by_difficulty(self, difficulty: DifficultyLevel) -> List[Mountain]:
        """難易度で山を検索"""
        mountains = self.get_all()
        return [m for m in mountains if m.difficulty.level == difficulty]
    
    def get_beginner_friendly(self) -> List[Mountain]:
        """初心者向けの山を取得"""
        mountains = self.get_all()
        return [m for m in mountains if m.is_beginner_friendly()]
    
    def get_with_cable_car(self) -> List[Mountain]:
        """ケーブルカーがある山を取得"""
        mountains = self.get_all()
        return [m for m in mountains if m.has_cable_car()]
    
    def search_by_keyword(self, keyword: str) -> List[Mountain]:
        """キーワードで山を検索"""
        mountains = self.get_all()
        keyword_lower = keyword.lower()
        
        results = []
        for mountain in mountains:
            # 名前、県名、特徴、キーワードで検索
            search_text = " ".join([
                mountain.name,
                mountain.prefecture,
                mountain.region,
                " ".join(mountain.features),
                " ".join(mountain.keywords)
            ]).lower()
            
            if keyword_lower in search_text:
                results.append(mountain)
        
        return results
    
    def search_by_tags(self, tags: List[str]) -> List[Mountain]:
        """タグで山を検索"""
        data = self._load_mountains_data()
        search_tags = data.get('search_tags', {})
        
        matching_mountain_ids = set()
        for tag in tags:
            if tag in search_tags:
                matching_mountain_ids.update(search_tags[tag])
        
        mountains = self._load_mountains_cache()
        return [mountains[mid] for mid in matching_mountain_ids if mid in mountains]
    
    def get_random_mountain(self, difficulty: Optional[DifficultyLevel] = None) -> Optional[Mountain]:
        """ランダムな山を取得"""
        if difficulty:
            candidates = self.get_by_difficulty(difficulty)
        else:
            candidates = self.get_all()
        
        if not candidates:
            return None
        
        return random.choice(candidates)
    
    def get_recommendations(
        self,
        exclude_ids: List[str] = None,
        difficulty: Optional[DifficultyLevel] = None,
        region: Optional[str] = None,
        limit: int = 5
    ) -> List[Mountain]:
        """おすすめの山を取得"""
        mountains = self.get_all()
        
        # 除外IDを適用
        if exclude_ids:
            mountains = [m for m in mountains if m.id not in exclude_ids]
        
        # フィルタを適用
        if difficulty:
            mountains = [m for m in mountains if m.difficulty.level == difficulty]
        
        if region:
            mountains = [m for m in mountains if m.region == region]
        
        # ランダムにシャッフルして制限数まで返す
        random.shuffle(mountains)
        return mountains[:limit]
    
    def get_statistics(self) -> Dict[str, Any]:
        """山データの統計情報を取得"""
        mountains = self.get_all()
        
        if not mountains:
            return {}
        
        # 地域別統計
        region_counts = {}
        for mountain in mountains:
            region = mountain.region
            region_counts[region] = region_counts.get(region, 0) + 1
        
        # 難易度別統計
        difficulty_counts = {}
        for mountain in mountains:
            level = mountain.difficulty.level.value
            difficulty_counts[level] = difficulty_counts.get(level, 0) + 1
        
        # 標高統計
        elevations = [m.elevation for m in mountains]
        
        return {
            "total_mountains": len(mountains),
            "regions": region_counts,
            "difficulties": difficulty_counts,
            "elevation_stats": {
                "min": min(elevations),
                "max": max(elevations),
                "average": sum(elevations) // len(elevations)
            },
            "beginner_friendly_count": len(self.get_beginner_friendly()),
            "cable_car_count": len(self.get_with_cable_car())
        }
    
    def reload_data(self):
        """データを再読み込み"""
        self._mountains_cache = None
        self._mountains_data = None
        self.log_info("Mountain data cache cleared")


class AreaCodeRepository(LoggerMixin):
    """楽天トラベル地域コードリポジトリ"""
    
    def __init__(self):
        self.area_codes = {
            "北海道": "01",
            "青森県": "02", "岩手県": "03", "宮城県": "04", "秋田県": "05",
            "山形県": "06", "福島県": "07",
            "茨城県": "08", "栃木県": "09", "群馬県": "10", "埼玉県": "11",
            "千葉県": "12", "東京都": "13", "神奈川県": "14",
            "新潟県": "15", "富山県": "16", "石川県": "17", "福井県": "18",
            "山梨県": "19", "長野県": "20", "岐阜県": "21", "静岡県": "22",
            "愛知県": "23", "三重県": "24",
            "滋賀県": "25", "京都府": "26", "大阪府": "27", "兵庫県": "28",
            "奈良県": "29", "和歌山県": "30",
            "鳥取県": "31", "島根県": "32", "岡山県": "33", "広島県": "34",
            "山口県": "35",
            "徳島県": "36", "香川県": "37", "愛媛県": "38", "高知県": "39",
            "福岡県": "40", "佐賀県": "41", "長崎県": "42", "熊本県": "43",
            "大分県": "44", "宮崎県": "45", "鹿児島県": "46", "沖縄県": "47"
        }
    
    def get_area_code(self, prefecture: str) -> str:
        """都道府県名から地域コードを取得"""
        # 複数県をまたぐ場合は最初の県を使用
        first_prefecture = prefecture.split("・")[0]
        return self.area_codes.get(first_prefecture, "01")  # デフォルトは北海道
    
    def get_prefecture_name(self, area_code: str) -> Optional[str]:
        """地域コードから都道府県名を取得"""
        for prefecture, code in self.area_codes.items():
            if code == area_code:
                return prefecture
        return None


# リポジトリファクトリー
class RepositoryFactory:
    """リポジトリファクトリー"""
    
    _mountain_repository: Optional[MountainRepository] = None
    _area_code_repository: Optional[AreaCodeRepository] = None
    
    @classmethod
    def get_mountain_repository(cls) -> MountainRepository:
        """山リポジトリを取得（シングルトン）"""
        if cls._mountain_repository is None:
            cls._mountain_repository = MountainRepository()
        return cls._mountain_repository
    
    @classmethod
    def get_area_code_repository(cls) -> AreaCodeRepository:
        """地域コードリポジトリを取得（シングルトン）"""
        if cls._area_code_repository is None:
            cls._area_code_repository = AreaCodeRepository()
        return cls._area_code_repository
    
    @classmethod
    def reset(cls):
        """すべてのリポジトリをリセット"""
        cls._mountain_repository = None
        cls._area_code_repository = None