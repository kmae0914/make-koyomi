from typing import Dict, List
from datetime import date, datetime, timedelta
from ..core.calendar_base import CalendarBase
from .eto_daily import DailyEto

class Hassen(CalendarBase):
    """八専を計算するクラス"""
    
    # 八専の期間（甲子から数えて49-60番目の干支）の定義
    HASSEN_PERIOD = {
        '壬子': {'五行': '水水', '種類': '八専'},
        '癸丑': {'五行': '水土', '種類': '間日'},
        '甲寅': {'五行': '木木', '種類': '八専'},
        '乙卯': {'五行': '木木', '種類': '八専'},
        '丙辰': {'五行': '火土', '種類': '間日'},
        '丁巳': {'五行': '火火', '種類': '八専'},
        '戊午': {'五行': '土火', '種類': '間日'},
        '己未': {'五行': '土土', '種類': '八専'},
        '庚申': {'五行': '金金', '種類': '八専'},
        '辛酉': {'五行': '金金', '種類': '八専'},
        '壬戌': {'五行': '水土', '種類': '間日'},
        '癸亥': {'五行': '水水', '種類': '八専'}
    }
    
    def __init__(self):
        """初期化"""
        super().__init__()
        self.eto_calculator = DailyEto()
    
    def _is_hassen_period(self, kanshi: str) -> bool:
        """指定された干支が八専の期間に含まれるかどうかを判定"""
        return kanshi in self.HASSEN_PERIOD
    
    def calculate_single_day(self, target_date: date) -> Dict:
        """
        指定された日の八専情報を計算
        
        Parameters:
            target_date (date): 対象日
            
        Returns:
            Dict: 計算結果
            {
                '日付': date,
                '干支': str,
                '八専期間': bool,
                '五行': str,  # 八専期間の場合のみ
                '種類': str,  # 八専期間の場合のみ（'八専' or '間日'）
            }
        """
        # 日の干支を計算
        eto = self.eto_calculator.calculate_single_day(target_date)
        kanshi = eto['干支']
        
        result = {
            '日付': target_date,
            '干支': kanshi,
            '八専期間': self._is_hassen_period(kanshi)
        }
        
        # 八専期間の場合は追加情報を設定
        if result['八専期間']:
            hassen_info = self.HASSEN_PERIOD[kanshi]
            result.update({
                '五行': hassen_info['五行'],
                '種類': hassen_info['種類']
            })
        
        return result
    
    def calculate_year(self, year: int) -> List[Dict]:
        """指定された年の全日の八専情報を計算"""
        results = []
        current_date = date(year, 1, 1)
        
        # 年末まで繰り返し
        while current_date.year == year:
            result = self.calculate_single_day(current_date)
            if result['八専期間']:  # 八専期間の日のみを追加
                results.append(result)
            current_date += timedelta(days=1)
        
        return results
    
    def format_year(self, year: int) -> str:
        """
        指定された年の八専情報を整形して文字列で返す
        """
        results = self.calculate_year(year)
        
        output = [
            f"\n{year}年の八専",
            "─" * 70,
            "日付         干支      種類      五行",
            "─" * 70
        ]
        
        current_month = 0
        for result in results:
            # 月が変わったら区切り線を入れる
            if result['日付'].month != current_month:
                current_month = result['日付'].month
                if current_month > 1:  # 最初の月以外で区切り線を追加
                    output.append("─" * 70)
        
            date_str = result['日付'].strftime('%Y/%m/%d')
            output.append(
                f"{date_str}  {result['干支']:<8}  "
                f"{result['種類']:<8}  {result['五行']}"
            )
        
        # 統計情報を追加
        hassen_days = len([r for r in results if r['種類'] == '八専'])
        mabi_days = len([r for r in results if r['種類'] == '間日'])
        
        output.extend([
            "─" * 70,
            f"八専: {hassen_days}日",
            f"間日: {mabi_days}日",
            f"合計: {len(results)}日"
        ])
        
        return "\n".join(output)