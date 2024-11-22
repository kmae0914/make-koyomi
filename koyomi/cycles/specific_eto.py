from typing import Dict, List
from datetime import date, timedelta
from ..core.calendar_base import CalendarBase
from .eto_daily import DailyEto

class SpecificEto(CalendarBase):
    """特定の干支（甲子、庚申、己巳）の日を計算するクラス"""
    
    # 対象となる干支のリスト
    TARGET_ETO = ['甲子', '庚申', '己巳']
    
    def __init__(self):
        """初期化"""
        super().__init__()
        self.eto_calculator = DailyEto()
    
    def calculate_year(self, year: int) -> Dict[str, List[date]]:
        """
        指定された年の特定干支の日を計算
        
        Parameters:
            year (int): 対象年
            
        Returns:
            Dict[str, List[date]]: 干支ごとの日付リスト
        """
        results = {eto: [] for eto in self.TARGET_ETO}
        current_date = date(year, 1, 1)
        
        # 年末まで繰り返し
        while current_date.year == year:
            eto = self.eto_calculator.calculate_single_day(current_date)
            if eto['干支'] in self.TARGET_ETO:
                results[eto['干支']].append(current_date)
            current_date += timedelta(days=1)
        
        return results
    
    def format_year(self, year: int) -> str:
        """
        指定された年の特定干支の日を整形して文字列で返す
        """
        results = self.calculate_year(year)
        
        output = [f"\n{year}年"]
        
        # 各干支の日付を表示
        for eto in self.TARGET_ETO:
            dates = results[eto]
            output.extend([
                f"\n{eto}の日:",
                "─" * 25
            ])
            
            for target_date in dates:
                output.append(target_date.strftime('%Y/%m/%d'))
        
        return "\n".join(output)