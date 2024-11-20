from typing import Dict, List
import calendar
from ..core.calendar_base import CalendarBase

class MonthLength(CalendarBase):
    """月の大小を計算するクラス"""
    
    # 月の日数による分類
    MONTH_TYPES = {
        28: "小",  # 閏年でない2月
        29: "小",  # 閏年の2月
        30: "小",
        31: "大"
    }
    
    def calculate(self, year: int, month: int) -> Dict:
        """
        指定された年月の大小を計算
        
        Parameters:
            year (int): 年
            month (int): 月
            
        Returns:
            Dict: 計算結果
            {
                '年': int,
                '月': int,
                '日数': int,
                '大小': str,  # "大" or "小"
                '閏月': bool  # 2月の場合のみTrue/False
            }
        """
        # monthrangeは(曜日, 日数)のタプルを返す
        _, days = calendar.monthrange(year, month)
        
        is_leap = False
        if month == 2:
            is_leap = calendar.isleap(year)
        
        return {
            '年': year,
            '月': month,
            '日数': days,
            '大小': self.MONTH_TYPES[days],
            '閏月': is_leap and month == 2
        }
    
    def calculate_year(self, year: int) -> List[Dict]:
        """
        指定された年の全月の大小を計算
        
        Parameters:
            year (int): 年
            
        Returns:
            List[Dict]: その年の全月の大小情報
        """
        return [self.calculate(year, month) for month in range(1, 13)]
    
    def format_year(self, year: int) -> str:
        """
        指定された年の月の大小を整形して文字列で返す
        
        Parameters:
            year (int): 年
            
        Returns:
            str: 整形された月の大小情報
        """
        results = self.calculate_year(year)
        
        output = [
            f"\n{year}年の月の大小",
            "-" * 50,
            "月    日数    大小    備考",
            "-" * 50
        ]
        
        for result in results:
            note = "閏月" if result['閏月'] else ""
            output.append(
                f"{result['月']:2d}月   {result['日数']:2d}日    {result['大小']}     {note}"
            )
        
        return "\n".join(output)
    
    def format_years(self, start_year: int, end_year: int) -> str:
        """
        指定された範囲の年の月の大小を整形して文字列で返す
        
        Parameters:
            start_year (int): 開始年
            end_year (int): 終了年
            
        Returns:
            str: 整形された月の大小情報
        """
        output = []
        for year in range(start_year, end_year + 1):
            output.append(self.format_year(year))
        return "\n".join(output)