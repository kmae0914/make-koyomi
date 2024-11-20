from typing import Dict, List
from datetime import date, datetime, timedelta
from ..core.calendar_base import CalendarBase

class DailyEto(CalendarBase):
    """日ごとの干支（えと）を計算するクラス"""
    
    # 十干(じっかん)
    JIKKAN = [
        "甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"
    ]
    JIKKAN_YOMI = [
        "きのえ", "きのと", "ひのえ", "ひのと", "つちのえ",
        "つちのと", "かのえ", "かのと", "みずのえ", "みずのと"
    ]
    
    # 十二支(じゅうにし)
    JUNISHI = [
        "子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"
    ]
    JUNISHI_YOMI = [
        "ね", "うし", "とら", "う", "たつ", "み",
        "うま", "ひつじ", "さる", "とり", "いぬ", "い"
    ]
    
    def __init__(self, base_date: date = date(2024, 1, 1)):
        """
        Parameters:
            base_date (date): 干支計算の基準日。デフォルトは2024年1月1日
        """
        super().__init__()
        self.base_date = base_date
    
    def calculate_single_day(self, target_date: date) -> Dict:
        """
        指定された日の干支を計算
        
        Parameters:
            target_date (date): 干支を計算したい日付
            
        Returns:
            Dict: 計算結果
            {
                '日付': date,
                '干支': str（例: "甲子"）,
                '読み': str（例: "きのえね"）,
                '十干': {
                    '漢字': str,
                    '読み': str,
                    '番号': int（0-9）
                },
                '十二支': {
                    '漢字': str,
                    '読み': str,
                    '番号': int（0-11）
                },
                '通日': int（1-60）
            }
        """
        # 基準日からの経過日数を計算
        days_diff = (target_date - self.base_date).days
        
        # 60日周期での日数を計算
        cycle_days = days_diff % 60
        
        # 十干と十二支のインデックスを計算
        jikkan_index = cycle_days % 10
        junishi_index = cycle_days % 12
        
        return {
            '日付': target_date,
            '干支': f"{self.JIKKAN[jikkan_index]}{self.JUNISHI[junishi_index]}",
            '読み': f"{self.JIKKAN_YOMI[jikkan_index]}{self.JUNISHI_YOMI[junishi_index]}",
            '十干': {
                '漢字': self.JIKKAN[jikkan_index],
                '読み': self.JIKKAN_YOMI[jikkan_index],
                '番号': jikkan_index
            },
            '十二支': {
                '漢字': self.JUNISHI[junishi_index],
                '読み': self.JUNISHI_YOMI[junishi_index],
                '番号': junishi_index
            },
            '通日': cycle_days + 1  # 1から60までの日番号
        }
    
    def calculate_month(self, year: int, month: int) -> List[Dict]:
        """
        指定された年月の全日の干支を計算
        
        Parameters:
            year (int): 年
            month (int): 月
            
        Returns:
            List[Dict]: その月の全日の干支情報
        """
        results = []
        target_date = date(year, month, 1)
        
        # 月末まで繰り返し
        while target_date.month == month:
            results.append(self.calculate_single_day(target_date))
            target_date += timedelta(days=1)
            
        return results
    
    def calculate_year(self, year: int) -> List[Dict]:
        """
        指定された年の全日の干支を計算
        
        Parameters:
            year (int): 年
            
        Returns:
            List[Dict]: その年の全日の干支情報
        """
        results = []
        target_date = date(year, 1, 1)
        
        # 年末まで繰り返し
        while target_date.year == year:
            results.append(self.calculate_single_day(target_date))
            target_date += timedelta(days=1)
            
        return results
    
    def format_month_calendar(self, year: int, month: int) -> str:
        """
        指定された年月の干支カレンダーを文字列形式で返す
        
        Parameters:
            year (int): 年
            month (int): 月
            
        Returns:
            str: 整形されたカレンダー文字列
        """
        results = self.calculate_month(year, month)
        
        output = [
            f"\n{year}年{month}月の干支暦",
            "=" * 50,
            "日付    干支    読み          通日",
            "-" * 50
        ]
        
        for r in results:
            date_str = r['日付'].strftime('%m/%d')
            output.append(
                f"{date_str}  {r['干支']}    {r['読み']}    {r['通日']:2d}/60"
            )
        
        return "\n".join(output)