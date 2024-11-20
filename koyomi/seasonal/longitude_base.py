from typing import Dict, Optional
from datetime import datetime
from ..core.calendar_base import CalendarBase
from skyfield.api import utc

class SolarLongitudeEvent(CalendarBase):
    """太陽黄経に基づく暦要素の基底クラス"""
    
    def __init__(self, longitude: float, delta_t: Optional[float] = None):
        super().__init__(delta_t)
        self.target_longitude = longitude
    
    def _find_longitude_date(self, year: int, search_month: int, months_range: int = 1) -> datetime:
        """
        指定された月の前後で目標の太陽黄経となる日時を探索
        
        Parameters:
            year (int): 対象年
            search_month (int): 探索の中心となる月
            months_range (int): 探索範囲（前後の月数）
            
        Returns:
            datetime: 目標の黄経となる日時（JST）
        """
        # 探索期間の設定
        start_year = year
        start_month = search_month - months_range
        if start_month < 1:
            start_month += 12
            start_year -= 1
            
        end_year = year
        end_month = search_month + months_range
        if end_month > 12:
            end_month -= 12
            end_year += 1
        
        t0 = self.astronomical.ts.from_datetime(
            datetime(start_year, start_month, 1, tzinfo=utc)
        )
        t1 = self.astronomical.ts.from_datetime(
            datetime(end_year, end_month, 1, tzinfo=utc)
        )
        
        # 目標の黄経となる時刻を探索
        time = self.astronomical.find_solar_term_date(
            self.target_longitude, t0, t1
        )
        
        return self.astronomical.to_jst_datetime(time)
    
    def calculate(self, year: int) -> Dict:
        """
        暦要素を計算する抽象メソッド
        """
        raise NotImplementedError("Subclasses must implement calculate()")