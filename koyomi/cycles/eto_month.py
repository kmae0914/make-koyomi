from typing import Dict, List
from ..core.calendar_base import CalendarBase
from .eto_year import YearEto

class MonthEto(CalendarBase):
    """月の干支を計算するクラス"""
    
    # 年の十干のグループ分け
    STEM_GROUPS = {
        "甲": 0, "己": 0,  # 甲/己グループ
        "乙": 1, "庚": 1,  # 乙/庚グループ
        "丙": 2, "辛": 2,  # 丙/辛グループ
        "丁": 3, "壬": 3,  # 丁/壬グループ
        "戊": 4, "癸": 4   # 戊/癸グループ
    }
    
    # 月ごとの干支を定義
    MONTH_ZODIAC = {
        1: ["丙寅", "戊寅", "庚寅", "壬寅", "甲寅"],    # 正月
        2: ["丁卯", "己卯", "辛卯", "癸卯", "乙卯"],    # 二月
        3: ["戊辰", "庚辰", "壬辰", "甲辰", "丙辰"],    # 三月
        4: ["己巳", "辛巳", "癸巳", "乙巳", "丁巳"],    # 四月
        5: ["庚午", "壬午", "甲午", "丙午", "戊午"],    # 五月
        6: ["辛未", "癸未", "乙未", "丁未", "己未"],    # 六月
        7: ["壬申", "甲申", "丙申", "戊申", "庚申"],    # 七月
        8: ["癸酉", "乙酉", "丁酉", "己酉", "辛酉"],    # 八月
        9: ["甲戌", "丙戌", "戊戌", "庚戌", "壬戌"],    # 九月
        10: ["乙亥", "丁亥", "己亥", "辛亥", "癸亥"],   # 十月
        11: ["丙子", "戊子", "庚子", "壬子", "甲子"],   # 十一月
        12: ["丁丑", "己丑", "辛丑", "癸丑", "乙丑"]    # 十二月
    }
    
    def __init__(self):
        super().__init__()
        self.year_eto_calculator = YearEto()
    
    def _get_month_zodiac(self, month: int, year_stem: str) -> str:
        """
        月と年の干から月の干支を求める
        
        Parameters:
            month (int): 月 (1-12)
            year_stem (str): 年の干
            
        Returns:
            str: 月の干支
        """
        if not 1 <= month <= 12:
            raise ValueError("月は1から12の間で指定してください")
        
        if year_stem not in self.STEM_GROUPS:
            raise ValueError("無効な年の干が指定されています")
        
        # 年の干から該当するグループのインデックスを取得
        group_index = self.STEM_GROUPS[year_stem]
        
        return self.MONTH_ZODIAC[month][group_index]
    
    def calculate(self, year: int, month: int) -> Dict:
        """
        指定された年月の干支を計算
        
        Parameters:
            year (int): 年
            month (int): 月
            
        Returns:
            Dict: 計算結果
            {
                '年': int,
                '月': int,
                '年干支': str,
                '月干支': str
            }
        """
        # 年の干支を取得
        year_result = self.year_eto_calculator.calculate(year)
        year_stem = year_result['十干']['漢字']
        
        # 月の干支を計算
        month_zodiac = self._get_month_zodiac(month, year_stem)
        
        return {
            '年': year,
            '月': month,
            '年干支': year_result['干支'],
            '月干支': month_zodiac
        }
    
    def calculate_year(self, year: int) -> List[Dict]:
        """
        指定された年の全月の干支を計算
        
        Parameters:
            year (int): 年
            
        Returns:
            List[Dict]: その年の全月の干支情報
        """
        return [self.calculate(year, month) for month in range(1, 13)]
    
    def format_year(self, year: int) -> str:
        """
        指定された年の月干支を整形して文字列で返す
        
        Parameters:
            year (int): 年
            
        Returns:
            str: 整形された月干支情報
        """
        results = self.calculate_year(year)
        year_eto = results[0]['年干支']  # 全ての結果で同じ
        
        output = [
            f"\n{year}年（{year_eto}）の月干支",
            "-" * 40,
            "月    月干支",
            "-" * 40
        ]
        
        for result in results:
            output.append(f"{result['月']:2d}月   {result['月干支']}")
        
        return "\n".join(output)