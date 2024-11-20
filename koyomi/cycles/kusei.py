from typing import Dict, List
from ..core.calendar_base import CalendarBase

class Kusei(CalendarBase):
    """九星を計算するクラス"""
    
    # 九星の定義
    KUSEI_DEFINITIONS = {
        1: {
            "漢字": "一白水星",
            "読み": "いっぱくすいせい",
            "属性": "水",
            "方位": "北",
            "色": "白"
        },
        2: {
            "漢字": "二黒土星",
            "読み": "じこくどせい",
            "属性": "土",
            "方位": "南西",
            "色": "黒"
        },
        3: {
            "漢字": "三碧木星",
            "読み": "さんぺきもくせい",
            "属性": "木",
            "方位": "東",
            "色": "碧"
        },
        4: {
            "漢字": "四緑木星",
            "読み": "しろくもくせい",
            "属性": "木",
            "方位": "東南",
            "色": "緑"
        },
        5: {
            "漢字": "五黄土星",
            "読み": "ごおうどせい",
            "属性": "土",
            "方位": "中央",
            "色": "黄"
        },
        6: {
            "漢字": "六白金星",
            "読み": "ろっぱくきんせい",
            "属性": "金",
            "方位": "西北",
            "色": "白"
        },
        7: {
            "漢字": "七赤金星",
            "読み": "しちせききんせい",
            "属性": "金",
            "方位": "西",
            "色": "赤"
        },
        8: {
            "漢字": "八白土星",
            "読み": "はっぱくどせい",
            "属性": "土",
            "方位": "南",
            "色": "白"
        },
        9: {
            "漢字": "九紫火星",
            "読み": "きゅうしかせい",
            "属性": "火",
            "方位": "南",
            "色": "紫"
        }
    }
    
    def _calculate_number(self, year: int) -> int:
        """
        九星の番号を計算
        
        Parameters:
            year (int): 対象年
            
        Returns:
            int: 九星の番号（1-9）
        """
        # 各位の数字を足す
        def sum_digits(n: int) -> int:
            return sum(int(digit) for digit in str(n))
        
        # 1桁になるまで繰り返し計算
        current_sum = year
        while current_sum > 9:
            current_sum = sum_digits(current_sum)
        
        # 1の場合は10として扱い、11から引く
        if current_sum == 1:
            current_sum = 10
            
        # 11から引いて九星の番号を得る
        return 11 - current_sum
    
    def calculate(self, year: int) -> Dict:
        """
        指定された年の九星を計算
        
        Parameters:
            year (int): 対象年
            
        Returns:
            Dict: 計算結果
            {
                '年': int,
                '九星番号': int（1-9）,
                '漢字': str,
                '読み': str,
                '属性': str,
                '方位': str,
                '色': str
            }
        """
        number = self._calculate_number(year)
        kusei_info = self.KUSEI_DEFINITIONS[number]
        
        return {
            '年': year,
            '九星番号': number,
            **kusei_info  # 九星の情報を展開
        }
    
    def calculate_range(self, start_year: int, end_year: int) -> List[Dict]:
        """
        指定された範囲の年の九星を計算
        
        Parameters:
            start_year (int): 開始年
            end_year (int): 終了年（含む）
            
        Returns:
            List[Dict]: 各年の九星情報
        """
        return [self.calculate(year) for year in range(start_year, end_year + 1)]
    
    def format_range(self, start_year: int, end_year: int, include_details: bool = True) -> str:
        """
        指定された範囲の年の九星を整形して文字列で返す
        
        Parameters:
            start_year (int): 開始年
            end_year (int): 終了年（含む）
            include_details (bool): 属性、方位、色の情報も含めるか
            
        Returns:
            str: 整形された九星情報
        """
        results = self.calculate_range(start_year, end_year)
        
        output = [
            f"\n{start_year}年から{end_year}年までの九星",
            "-" * 80 if include_details else "-" * 50
        ]
        
        if include_details:
            output.append("西暦    九星        読み                属性    方位    色")
            output.append("-" * 80)
            for result in results:
                output.append(
                    f"{result['年']:<8}{result['漢字']:<12}"
                    f"{result['読み']:<20}{result['属性']:<8}"
                    f"{result['方位']:<8}{result['色']}"
                )
        else:
            output.append("西暦    九星        読み")
            output.append("-" * 50)
            for result in results:
                output.append(
                    f"{result['年']:<8}{result['漢字']:<12}{result['読み']}"
                )
        
        return "\n".join(output)