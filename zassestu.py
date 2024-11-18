from datetime import datetime, date, timedelta
from typing import Dict, List, Tuple
from skyfield.api import load
from nizyushiekki import SolarTermsCalculator

class SeasonalEventsCalculator:
    def __init__(self):
        # SolarTermsCalculatorのインスタンス化
        self.solar_terms_calc = SolarTermsCalculator()
        
        # 固定雑節の日付
        self.FIXED_EVENTS = {
            'setsubun': (2, 3),        # 節分
            'nyubai': (6, 11),         # 入梅
            'hange': (7, 2),           # 半夏生
            'nihyaku_toka': (9, 1),    # 二百十日
            'daishi': (12, 21),        # 大師
            'toshikoshi': (12, 31)     # 年越
        }

    def get_solar_terms(self, year: int) -> List[dict]:
        """二十四節気を取得"""
        return self.solar_terms_calc.calculate_solar_terms(year)

    def calculate_higan(self, year: int, solar_terms: List[dict]) -> Dict[str, List[date]]:
        """彼岸の期間を計算"""
        higan_periods = {}
        
        # 春分と秋分の日を見つける
        for term in solar_terms:
            dt = datetime.strptime(term['年月日時刻'], '%Y/%m/%d %H:%M:%S')
            if term['term_name'] in ['春分', '秋分']:
                season = '春' if term['term_name'] == '春分' else '秋'
                center_date = dt.date()
                dates = []
                for i in range(-3, 4):  # 前後3日間
                    dates.append(center_date + timedelta(days=i))
                higan_periods[f'{season}彼岸'] = dates
        
        return higan_periods

    def calculate_doyo(self, year: int, solar_terms: List[dict]) -> Dict[str, Tuple[date, date]]:
        """土用期間を計算"""
        doyo_periods = {}
        doyo_start_terms = ['立夏', '立秋', '立冬', '立春']
        
        for term in solar_terms:
            if term['term_name'] in doyo_start_terms:
                dt = datetime.strptime(term['年月日時刻'], '%Y/%m/%d %H:%M:%S')
                term_date = dt.date()
                season = {
                    '立夏': '春',
                    '立秋': '夏',
                    '立冬': '秋',
                    '立春': '冬'
                }[term['term_name']]
                
                # 土用は節気の前18日間
                start_date = term_date - timedelta(days=18)
                end_date = term_date - timedelta(days=1)
                doyo_periods[f'{season}土用'] = (start_date, end_date)
        
        return doyo_periods

    def get_all_events(self, year: int) -> Dict[str, Dict]:
        """年間の全雑節を計算"""
        # 二十四節気を取得
        solar_terms = self.get_solar_terms(year)
        
        # 各種雑節を計算
        events = {
            '二十四節気': solar_terms,
            '彼岸': self.calculate_higan(year, solar_terms),
            '土用': self.calculate_doyo(year, solar_terms),
            '固定雑節': {
                name: date(year, month, day)
                for name, (month, day) in self.FIXED_EVENTS.items()
            }
        }
        
        return events

    def print_year_events(self, year: int):
        """年間の雑節一覧を表示"""
        events = self.get_all_events(year)
        
        print(f"{year}年の雑節一覧")
        print("=" * 50)
        
        # 二十四節気
        print("\n二十四節気:")
        for term in events['二十四節気']:
            print(f"{term['term_name']}: {term['年月日時刻']}")
        
        # 彼岸
        print("\n彼岸:")
        for name, dates in events['彼岸'].items():
            print(f"{name}: {dates[0].strftime('%m-%d')} ～ {dates[-1].strftime('%m-%d')}")
        
        # 土用
        print("\n土用:")
        for name, (start, end) in events['土用'].items():
            print(f"{name}: {start.strftime('%m-%d')} ～ {end.strftime('%m-%d')}")
        
        # 固定雑節
        print("\nその他の雑節:")
        for name, dt in events['固定雑節'].items():
            print(f"{name}: {dt.strftime('%m-%d')}")

# 使用例
if __name__ == "__main__":
    calc = SeasonalEventsCalculator()
    
    # 2025年の雑節を計算して表示
    calc.print_year_events(2025)
    
    # 特定の期間の二十四節気を表示
    print("\n2024年から2025年の二十四節気:")
    for year in range(2024, 2026):
        terms = calc.get_solar_terms(year)
        for term in terms:
            print(f"{term['term_name']}: {term['年月日時刻']}")