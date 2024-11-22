from typing import Dict, List
from datetime import date, timedelta
import calendar
from ..core.calendar_base import CalendarBase

class Sundays(CalendarBase):
    """日曜日を計算するクラス"""
    
    # 曜日の日本語表記
    WEEKDAY_JA = ["月", "火", "水", "木", "金", "土", "日"]
    
    def __init__(self):
        """初期化"""
        super().__init__()
        # 日本のカレンダー設定（月曜始まり）
        self.calendar = calendar.Calendar(firstweekday=calendar.MONDAY)
    
    def _get_month_sundays(self, year: int, month: int) -> List[date]:
        """指定された年月の日曜日を取得"""
        return [
            date(year, month, day)
            for day in self.calendar.itermonthdays(year, month)
            if day != 0 and date(year, month, day).weekday() == 6
        ]
    
    def calculate(self, year: int) -> List[Dict]:
        """
        指定された年の日曜日を計算
        
        Parameters:
            year (int): 年
            
        Returns:
            List[Dict]: その年の全ての日曜日
            各要素は {
                '日付': date,
                '月': int,
                '日': int,
                '第n日曜': int,  # その月の第何日曜日か
                'ISO週番号': int  # ISO 8601の週番号
            }
        """
        results = []
        
        # 1月から12月まで処理
        for month in range(1, 13):
            sundays = self._get_month_sundays(year, month)
            
            # その月の日曜日を順番に処理
            for i, sunday in enumerate(sundays, start=1):
                year, week, _ = sunday.isocalendar()
                results.append({
                    '日付': sunday,
                    '月': month,
                    '日': sunday.day,
                    '第n日曜': i,
                    'ISO週番号': week
                })
        
        return results
    
    def format_year(self, year: int, include_week_number: bool = False) -> str:
        """
        指定された年の日曜日一覧を整形して文字列で返す
        
        Parameters:
            year (int): 年
            include_week_number (bool): ISO週番号を含めるかどうか
        """
        results = self.calculate(year)
        
        current_month = 0
        output = [f"\n{year}年の日曜日一覧"]
        
        for result in results:
            # 月が変わったら月見出しを追加
            if result['月'] != current_month:
                current_month = result['月']
                output.append(f"\n{current_month}月:")
                if include_week_number:
                    output.append("日付         第n日曜    ISO週番号")
                else:
                    output.append("日付         第n日曜")
                output.append("─" * (40 if include_week_number else 25))
            
            # 日付情報の整形
            date_str = result['日付'].strftime('%Y/%m/%d')
            nth_sunday = f"第{result['第n日曜']}日曜日"
            
            if include_week_number:
                week_str = f"第{result['ISO週番号']:2d}週"
                output.append(f"{date_str}  {nth_sunday:<10}  {week_str}")
            else:
                output.append(f"{date_str}  {nth_sunday}")
        
        return "\n".join(output)
    
    def format_month(self, year: int, month: int, include_week_number: bool = False) -> str:
        """指定された年月の日曜日一覧を整形して文字列で返す"""
        results = [r for r in self.calculate(year) if r['月'] == month]
        
        output = [f"\n{year}年{month}月の日曜日一覧"]
        
        if include_week_number:
            output.append("日付         第n日曜    ISO週番号")
        else:
            output.append("日付         第n日曜")
        output.append("─" * (40 if include_week_number else 25))
        
        for result in results:
            date_str = result['日付'].strftime('%Y/%m/%d')
            nth_sunday = f"第{result['第n日曜']}日曜日"
            
            if include_week_number:
                week_str = f"第{result['ISO週番号']:2d}週"
                output.append(f"{date_str}  {nth_sunday:<10}  {week_str}")
            else:
                output.append(f"{date_str}  {nth_sunday}")
        
        return "\n".join(output)
    
    def calculate_year(self, year: int) -> List[Dict]:
        """
        指定された年の日曜日を計算（calculate メソッドを継承）
        """
        return self.calculate(year)
