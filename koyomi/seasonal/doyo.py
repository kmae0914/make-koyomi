from typing import Dict, List
from .longitude_base import SolarLongitudeEvent
from datetime import datetime
from skyfield.api import utc

class Doyo(SolarLongitudeEvent):
    """土用の日付を計算するクラス"""
    
    # 土用の定義
    DOYO_DEFINITIONS = {
        '冬土用': 297.0,
        '春土用': 27.0,
        '夏土用': 117.0,
        '秋土用': 207.0
    }
    
    def __init__(self, delta_t: float = 69.0):
        """
        Parameters:
            delta_t (float): ΔT値（秒）。デフォルトは2024年の概算値
        """
        super().__init__(0.0, delta_t)
    
    def calculate(self, year: int) -> List[Dict]:
        """
        指定された年の全ての土用の日付を計算
        
        Parameters:
            year (int): 対象年
            
        Returns:
            List[Dict]: 土用の日付リスト
        """
        results = []
        
        # 探索期間を1年の前後に設定
        t0 = self.astronomical.ts.from_datetime(
            datetime(year - 1, 7, 1, tzinfo=utc)
        )
        t1 = self.astronomical.ts.from_datetime(
            datetime(year + 1, 6, 30, tzinfo=utc)
        )
        
        for season, longitude in self.DOYO_DEFINITIONS.items():
            self.target_longitude = longitude
            
            # 目標の黄経となる時刻を探索
            time = self.astronomical.find_solar_term_date(
                longitude, t0, t1
            )
            
            dt = self.astronomical.to_jst_datetime(time)
            
            # 指定された年のデータのみを使用
            if dt.year == year:
                results.append(self._create_result(
                    f"{year}{season}",
                    dt,
                    season
                ))
        
        # 日付順にソート
        results.sort(key=lambda x: x['datetime_jst'])
        
        return results