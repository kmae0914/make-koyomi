from typing import Dict, List, Optional
from datetime import date, datetime, timedelta
import calendar
from ..core.calendar_base import CalendarBase
from ..seasonal.sekki import SolarTerms

class Holiday(CalendarBase):
    """日本の祝日を計算するクラス"""
    
    # 固定日の祝日定義
    FIXED_HOLIDAYS = {
        1: {
            1: "元日"
        },
        2: {
            11: "建国記念の日",
            23: "天皇誕生日"
        },
        4: {
            29: "昭和の日"
        },
        5: {
            3: "憲法記念日",
            4: "みどりの日",
            5: "こどもの日"
        },
        8: {
            11: "山の日"
        },
        11: {
            3: "文化の日",
            23: "勤労感謝の日"
        }
    }
    
    # ハッピーマンデー制度による祝日
    HAPPY_MONDAY = {
        1: (2, "成人の日"),      # 1月第2月曜日
        7: (3, "海の日"),       # 7月第3月曜日
        9: (3, "敬老の日"),     # 9月第3月曜日
        10: (2, "スポーツの日")  # 10月第2月曜日
    }

    def __init__(self):
        """初期化"""
        super().__init__()
        self.sekki_calculator = SolarTerms()
    
    def _find_monday_date(self, year: int, month: int, week: int) -> date:
        """指定された月の第n月曜日を求める"""
        c = calendar.monthcalendar(year, month)
        for week_days in c:
            monday = week_days[0]  # 月曜日
            if monday != 0:
                week -= 1
                if week == 0:
                    return date(year, month, monday)
    
    def _get_equinox_holiday(self, year: int, sekki_name: str, holiday_name: str) -> Dict:
        """春分の日・秋分の日を計算"""
        terms = self.sekki_calculator.calculate(year)
        for term in terms:
            if term['イベント名'] == sekki_name:
                dt = term['datetime_jst']
                return {
                    '日付': dt.date(),
                    '名称': holiday_name,
                    '種類': '祝日'
                }
        return None
    
    def calculate(self, year: int, include_substitute: bool = True) -> List[Dict]:
        """
        指定された年の祝日と休日を計算
        
        Parameters:
            year (int): 年
            include_substitute (bool): 振替休日を含めるかどうか。デフォルトはTrue
            
        Returns:
            List[Dict]: 祝日・休日情報のリスト
            各要素は {'日付': date, '名称': str, '種類': str, 'オリジナル祝日': Optional[str]}
        """
        results = {}
        
        # 1. 固定日の祝日
        for month, days in self.FIXED_HOLIDAYS.items():
            for day, name in days.items():
                holiday_date = date(year, month, day)
                results[holiday_date] = {
                    '日付': holiday_date,
                    '名称': name,
                    '種類': '祝日',
                    'オリジナル祝日': None
                }
        
        # 2. ハッピーマンデー
        for month, (week, name) in self.HAPPY_MONDAY.items():
            holiday_date = self._find_monday_date(year, month, week)
            results[holiday_date] = {
                '日付': holiday_date,
                '名称': name,
                '種類': '祝日',
                'オリジナル祝日': None
            }
        
        # 3. 春分・秋分
        spring = self._get_equinox_holiday(year, '春分', '春分の日')
        if spring:
            spring['オリジナル祝日'] = None
            results[spring['日付']] = spring
        
        autumn = self._get_equinox_holiday(year, '秋分', '秋分の日')
        if autumn:
            autumn['オリジナル祝日'] = None
            results[autumn['日付']] = autumn
        
        if include_substitute:
            # 4. 振替休日と国民の休日を追加
            holiday_dates = sorted(results.keys())
            additional_holidays = {}
            
            for holiday_date in holiday_dates:
                # 祝日が日曜の場合
                if holiday_date.weekday() == 6:
                    original_name = results[holiday_date]['名称']
                    next_day = holiday_date + timedelta(days=1)
                    while next_day in results or next_day in additional_holidays:
                        next_day += timedelta(days=1)
                    additional_holidays[next_day] = {
                        '日付': next_day,
                        '名称': '休日',
                        '種類': f'{original_name}の振替休日',
                        'オリジナル祝日': original_name
                    }
                
                # 祝日に挟まれた平日を探す
                if holiday_date + timedelta(days=2) in results:
                    between_date = holiday_date + timedelta(days=1)
                    if between_date not in results and between_date.weekday() < 6:
                        additional_holidays[between_date] = {
                            '日付': between_date,
                            '名称': '休日',
                            '種類': '国民の休日',
                            'オリジナル祝日': None
                        }
            
            results.update(additional_holidays)
        
        # 日付順にソート
        sorted_results = [results[k] for k in sorted(results.keys())]
        
        return sorted_results
    
    def format_year(self, year: int, include_substitute: bool = True) -> str:
        """
        指定された年の祝日・休日を整形して文字列で返す
        
        Parameters:
            year (int): 年
            include_substitute (bool): 振替休日を含めるかどうか。デフォルトはTrue
        
        Returns:
            str: 整形された祝日情報
        """
        results = self.calculate(year, include_substitute)
        
        output = [
            f"\n{year}年の{'祝日・休日' if include_substitute else '祝日'}",
            "-" * 60,
            "日付         名称           種類",
            "-" * 60
        ]
        
        for result in results:
            date_str = result['日付'].strftime('%Y/%m/%d')
            name = result['名称']
            type_str = result['種類']
            output.append(f"{date_str}  {name:<12} {type_str}")
        
        return "\n".join(output)