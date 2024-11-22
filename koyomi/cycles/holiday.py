from typing import Dict, List, Optional
import unicodedata
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
                    '種類': '祝日',
                    'オリジナル祝日': None
                }
        return None

    def calculate(self, year: int, **kwargs) -> List[Dict]:
        """
        指定された年の祝日と休日を計算
        
        Parameters:
            year (int): 年
            **kwargs: 追加のオプション
                include_substitute (bool): 振替休日を含めるかどうか。デフォルトはTrue
        """
        include_substitute = kwargs.get('include_substitute', True)
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
            results[spring['日付']] = spring
        
        autumn = self._get_equinox_holiday(year, '秋分', '秋分の日')
        if autumn:
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

    def _get_text_width(self, text: str) -> int:
        """文字列の表示幅を計算（全角文字は2、半角文字は1として計算）"""
        width = 0
        for c in text:
            width += 2 if unicodedata.east_asian_width(c) in ('F', 'W', 'A') else 1
        return width
    
    def _format_column(self, text: str, width: int) -> str:
        """文字列を指定した表示幅で整形"""
        text_width = self._get_text_width(text)
        padding = width - text_width
        if padding > 0:
            return text + " " * padding
        return text

    def format_year(self, year: int, include_substitute: bool = True) -> str:
        """指定された年の祝日・休日を整形して文字列で返す"""
        results = self.calculate(year, include_substitute=include_substitute)
        
        output = [
            f"\n{year}年の{'祝日・休日' if include_substitute else '祝日'}",
            "─" * 70,
            f"{self._format_column('日付', 12)}  {self._format_column('名称', 14)}  種類",
            "─" * 70
        ]
        
        for result in results:
            date_str = result['日付'].strftime('%Y/%m/%d')
            name = result['名称']
            display_type = result['種類']
            
            output.append(
                f"{self._format_column(date_str, 12)}  "
                f"{self._format_column(name, 14)}  "
                f"{display_type}"
            )
        
        return "\n".join(output)

    def print_substitute_details(self, year: int) -> None:
        """振替休日の詳細情報を表示"""
        results = self.calculate(year, include_substitute=True)
        
        substitutes = [r for r in results if r['オリジナル祝日']]
        if not substitutes:
            print(f"\n{year}年の振替休日・国民の休日はありません。")
            return
        
        print(f"\n{year}年の振替休日・国民の休日:")
        print("─" * 70)
        for holiday in substitutes:
            date_str = holiday['日付'].strftime('%Y/%m/%d')
            print(f"{date_str}: {holiday['種類']}")