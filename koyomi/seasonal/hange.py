from typing import Dict
from .longitude_base import SolarLongitudeEvent

class Hangesho(SolarLongitudeEvent):
    """半夏生の日付を計算するクラス"""
    
    def __init__(self, delta_t: float = 69.0):
        """
        Parameters:
            delta_t (float): ΔT値（秒）。デフォルトは2024年の概算値
        """
        # 半夏生の黄経は100度
        super().__init__(100.0, delta_t)
    
    def calculate(self, year: int) -> Dict:
        """
        指定された年の半夏生の日付を計算
        
        Parameters:
            year (int): 対象年
            
        Returns:
            Dict: 計算結果
            {
                '識別子': f"{year}半夏生",
                '年月日時刻': "YYYY/MM/DD HH:MM:SS",
                'datetime_jst': datetime object (JST),
                'イベント名': "半夏生"
            }
        """
        # 半夏生は7月頃
        dt = self._find_longitude_date(year, 7, 1)
        
        return self._create_result(
            f"{year}半夏生",
            dt,
            "半夏生"
        )