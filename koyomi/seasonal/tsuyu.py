from typing import Dict
from .longitude_base import SolarLongitudeEvent

class Tsuyuiri(SolarLongitudeEvent):
    """入梅の日付を計算するクラス"""
    
    def __init__(self, delta_t: float = 69.0):
        """
        Parameters:
            delta_t (float): ΔT値（秒）。デフォルトは2024年の概算値
        """
        # 入梅の黄経は80度
        super().__init__(80.0, delta_t)
    
    def calculate(self, year: int) -> Dict:
        """
        指定された年の入梅の日付を計算
        
        Parameters:
            year (int): 対象年
            
        Returns:
            Dict: 計算結果
            {
                '識別子': f"{year}入梅",
                '年月日時刻': "YYYY/MM/DD HH:MM:SS",
                'datetime_jst': datetime object (JST),
                'イベント名': "入梅"
            }
        """
        # 入梅は6月頃
        dt = self._find_longitude_date(year, 6, 1)
        
        return self._create_result(
            f"{year}入梅",
            dt,
            "入梅"
        )