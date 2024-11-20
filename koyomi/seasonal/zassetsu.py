from typing import Dict, List
from datetime import datetime, timedelta
from ..core.calendar_base import CalendarBase
from .sekki import SolarTerms
from skyfield.api import utc

class Zassetsu(CalendarBase):
    """雑節（節分、彼岸、八十八夜、二百十日）を計算するクラス"""
    
    def __init__(self, delta_t: float = 69.0):
        """
        Parameters:
            delta_t (float): ΔT値（秒）。デフォルトは2024年の概算値
        """
        super().__init__(delta_t)
        self.sekki_calculator = SolarTerms(delta_t)
    
    def _find_sekki_date(self, year: int, sekki_name: str) -> datetime:
        """二十四節気から特定の節気の日付を取得"""
        terms = self.sekki_calculator.calculate(year)
        for term in terms:
            if term['イベント名'] == sekki_name:
                return term['datetime_jst']
        return None
    
    def calculate_setsubun(self, year: int) -> Dict:
        """節分（立春の前日）を計算"""
        risshun = self._find_sekki_date(year, '立春')
        if risshun:
            setsubun = risshun - timedelta(days=1)
            return self._create_result(
                f"{year}節分",
                setsubun,
                "節分"
            )
        return None
    
    def calculate_higan(self, year: int) -> List[Dict]:
        """お彼岸（春分・秋分の前後3日間）を計算"""
        results = []
        
        for sekki_name in ['春分', '秋分']:
            center_date = self._find_sekki_date(year, sekki_name)
            if center_date:
                season = '春' if sekki_name == '春分' else '秋'
                
                # 前後3日間（計7日間）を追加
                for days in range(-3, 4):
                    higan_date = center_date + timedelta(days=days)
                    day_num = days + 4  # 1日目から7日目に変換
                    results.append(self._create_result(
                        f"{year}{season}彼岸{day_num}日目",
                        higan_date,
                        f"{season}彼岸"
                    ))
        
        return results
    
    def calculate_hachijuhachiya(self, year: int) -> Dict:
        """八十八夜（立春から88日目）を計算"""
        risshun = self._find_sekki_date(year, '立春')
        if risshun:
            hachijuhachiya = risshun + timedelta(days=87)  # 88日目なので87日後
            return self._create_result(
                f"{year}八十八夜",
                hachijuhachiya,
                "八十八夜"
            )
        return None
    
    def calculate_nihyaku_toka(self, year: int) -> Dict:
        """二百十日（立春から210日目）を計算"""
        risshun = self._find_sekki_date(year, '立春')
        if risshun:
            nihyaku_toka = risshun + timedelta(days=209)  # 210日目なので209日後
            return self._create_result(
                f"{year}二百十日",
                nihyaku_toka,
                "二百十日"
            )
        return None
    
    def calculate(self, year: int) -> List[Dict]:
        """
        指定された年の全ての雑節を計算
        
        Parameters:
            year (int): 対象年
            
        Returns:
            List[Dict]: 雑節の日付リスト
        """
        results = []
        
        # 節分
        setsubun = self.calculate_setsubun(year)
        if setsubun:
            results.append(setsubun)
        
        # お彼岸
        results.extend(self.calculate_higan(year))
        
        # 八十八夜
        hachijuhachiya = self.calculate_hachijuhachiya(year)
        if hachijuhachiya:
            results.append(hachijuhachiya)
        
        # 二百十日
        nihyaku_toka = self.calculate_nihyaku_toka(year)
        if nihyaku_toka:
            results.append(nihyaku_toka)
        
        # 日付でソート
        results.sort(key=lambda x: x['datetime_jst'])
        
        return results