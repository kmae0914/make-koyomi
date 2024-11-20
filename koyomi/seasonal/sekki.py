import pytz
from ..core.calendar_base import CalendarBase
from skyfield import almanac_east_asia as almanac_ea
from skyfield import almanac
from typing import List, Dict

class SolarTerms(CalendarBase):
    """二十四節気を計算するクラス"""
    
    def __init__(self, delta_t: float = 69.0):
        """
        Parameters:
            delta_t (float): ΔT値（秒）。デフォルトは2024年の概算値
        """
        super().__init__(delta_t)
    
    def calculate(self, year: int) -> List[Dict]:
        """
        指定された年の二十四節気を計算
        
        Parameters:
            year (int): 対象年
            
        Returns:
            List[Dict]: 二十四節気の日時リスト。各要素は以下の形式:
            {
                '識別子': f"{year}{節気名}",
                '年月日時刻': "YYYY/MM/DD HH:MM:SS",
                'datetime_jst': datetime object (JST),
                'イベント名': 節気名
            }
        """
        # 計算期間の設定（年の前後1ヶ月を含む）
        t0, t1 = self._get_year_range(year, 1, 1)
        
        # 二十四節気の計算
        t, y = almanac.find_discrete(t0, t1, almanac_ea.solar_terms(self.astronomical.eph))
        
        results = []
        for time, idx in zip(t, y):
            # 日本時間に変換
            dt_jst = self.astronomical.to_jst_datetime(time)
            
            # 指定された年のデータのみを抽出
            if dt_jst.year == year:
                name_ja = almanac_ea.SOLAR_TERMS_JP[idx]
                
                results.append(self._create_result(
                    f"{year}{name_ja}",
                    dt_jst,
                    name_ja
                ))
        
        # 日付でソート
        results.sort(key=lambda x: x['datetime_jst'])
        
        return results
    
    def print_terms(self, year: int) -> None:
        """
        指定された年の二十四節気を見やすく表示
        
        Parameters:
            year (int): 対象年
        """
        terms = self.calculate(year)
        
        print(f"\n=== {year}年の二十四節気 ===")
        print(f"{'節気名':<10} {'年月日時刻':<30}")
        print("-" * 50)
        
        for term in terms:
            print(f"{term['イベント名']:<10} {term['年月日時刻']:<30}")
        
        print("-" * 50)
        print(f"総計: {len(terms)}件の節気\n")