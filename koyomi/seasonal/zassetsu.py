from typing import Dict, List
from datetime import datetime, timedelta
from ..core.calendar_base import CalendarBase
from .sekki import SolarTerms
from skyfield.api import utc
from . import sekki
from . import shanichi
from ..cycles.eto_daily import DailyEto

class Zassetsu(CalendarBase):
    """雑節を計算するクラス"""
    
    def __init__(self, delta_t: float = 69.0):
        """初期化"""
        super().__init__(delta_t)
        self.sekki_calculator = sekki.SolarTerms(delta_t)
        self.shanichi_calculator = shanichi.Shanichi(delta_t)
        self.eto_calculator = DailyEto()

    
    def _find_sekki_date(self, year: int, sekki_name: str) -> datetime:
        """二十四節気から特定の節気の日付を取得"""
        terms = self.sekki_calculator.calculate(year)
        for term in terms:
            if term['イベント名'] == sekki_name:
                return term['datetime_jst']
        return None
    
    def calculate_setsubun(self, year: int) -> Dict:
        """節分（立春の前日）を計算"""
        solar_terms = self.sekki_calculator.calculate(year)
        for term in solar_terms:
            if term['イベント名'] == '立春':
                risshun_date = term['datetime_jst']
                setsubun_date = risshun_date - timedelta(days=1)
                return self._create_result(
                    f"{year}節分",
                    setsubun_date,
                    "節分"
                )
        return None
    
    def calculate_higan(self, year: int) -> List[Dict]:
        """お彼岸（春分・秋分の前後3日間）を計算"""
        results = []
        
        # 春分と秋分それぞれについて計算
        for sekki_name, season in [('春分', '春'), ('秋分', '秋')]:
            # 二十四節気から春分・秋分を見つける
            solar_terms = self.sekki_calculator.calculate(year)
            for term in solar_terms:
                if term['イベント名'] == sekki_name:
                    center_date = term['datetime_jst']
                    
                    # 前後3日間を追加
                    for days in range(-3, 4):
                        higan_date = center_date + timedelta(days=days)
                        results.append(self._create_result(
                            f"{year}{season}彼岸{days+4}日目",
                            higan_date,
                            f"{season}彼岸"
                        ))
        
        return results
    
    def calculate_hachijuhachiya(self, year: int) -> Dict:
        """八十八夜（立春から88日目）を計算"""
        solar_terms = self.sekki_calculator.calculate(year)
        for term in solar_terms:
            if term['イベント名'] == '立春':
                base_date = term['datetime_jst']
                hachijuhachiya = base_date + timedelta(days=87)  # 88日目なので87日後
                return self._create_result(
                    f"{year}八十八夜",
                    hachijuhachiya,
                    "八十八夜"
                )
        return None
    
    def calculate_nihyakutoka(self, year: int) -> Dict:
        """二百十日（立春から210日目）を計算"""
        solar_terms = self.sekki_calculator.calculate(year)
        for term in solar_terms:
            if term['イベント名'] == '立春':
                nihyaku_toka = term['datetime_jst'] + timedelta(days=209)  # 210日目
                return self._create_result(
                    f"{year}二百十日",
                    nihyaku_toka,
                    "二百十日"
                )
        return None
    
    def calculate(self, year: int) -> List[Dict]:
        """その年の全ての雑節を計算"""
        seasonal_days = []
        
        # 節分の計算
        setsubun = self.calculate_setsubun(year)
        if setsubun:
            seasonal_days.append(setsubun)
        
        # 彼岸の計算
        seasonal_days.extend(self.calculate_higan(year))
        
        # 社日の計算
        seasonal_days.extend(self.shanichi_calculator.calculate(year))
        
        # 八十八夜の計算
        hachijuhachiya = self.calculate_hachijuhachiya(year)
        if hachijuhachiya:
            seasonal_days.append(hachijuhachiya)
        
        # 二百十日の計算
        nihyakutoka = self.calculate_nihyakutoka(year)
        if nihyakutoka:
            seasonal_days.append(nihyakutoka)
        
        # None を除外し、日付でソート
        seasonal_days = [day for day in seasonal_days if day is not None]
        seasonal_days.sort(key=lambda x: x['datetime_jst'])
        
        return seasonal_days
