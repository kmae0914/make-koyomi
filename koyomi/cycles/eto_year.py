from typing import Dict, List
from ..core.calendar_base import CalendarBase

class YearEto(CalendarBase):
    """年の干支を計算するクラス"""
    
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
    
    def calculate(self, year: int) -> Dict:
        """
        指定された年の干支を計算
        
        Parameters:
            year (int): 対象年
            
        Returns:
            Dict: 計算結果
            {
                '年': int,
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
                }
                '六十干支番号': int（1-60）
            }
        """
        # 十干と十二支のインデックスを計算
        jikkan_idx = (year + 6) % 10  # 甲（きのえ）を基準に計算
        junishi_idx = (year + 8) % 12  # 子（ね）を基準に計算
        
        # 六十干支の通し番号を計算（1〜60）
        cycle_number = (jikkan_idx * 12 + junishi_idx) % 60 + 1
        
        return {
            '年': year,
            '干支': f"{self.JIKKAN[jikkan_idx]}{self.JUNISHI[junishi_idx]}",
            '読み': f"{self.JIKKAN_YOMI[jikkan_idx]}{self.JUNISHI_YOMI[junishi_idx]}",
            '十干': {
                '漢字': self.JIKKAN[jikkan_idx],
                '読み': self.JIKKAN_YOMI[jikkan_idx],
                '番号': jikkan_idx + 1  # 1から始まる番号
            },
            '十二支': {
                '漢字': self.JUNISHI[junishi_idx],
                '読み': self.JUNISHI_YOMI[junishi_idx],
                '番号': junishi_idx + 1  # 1から始まる番号
            },
            '六十干支番号': cycle_number
        }
    
    def calculate_range(self, start_year: int, end_year: int) -> List[Dict]:
        """
        指定された範囲の年の干支を計算
        
        Parameters:
            start_year (int): 開始年
            end_year (int): 終了年（含む）
            
        Returns:
            List[Dict]: 各年の干支情報
        """
        results = []
        for year in range(start_year, end_year + 1):
            results.append(self.calculate(year))
        return results
    
    def format_range(self, start_year: int, end_year: int, include_wareki: bool = True) -> str:
        """
        指定された範囲の年の干支を整形して文字列で返す
        
        Parameters:
            start_year (int): 開始年
            end_year (int): 終了年（含む）
            include_wareki (bool): 和暦（令和）を含めるかどうか
            
        Returns:
            str: 整形された干支情報
        """
        results = self.calculate_range(start_year, end_year)
        
        output = [
            f"\n{start_year}年から{end_year}年までの干支",
            "-" * 60
        ]
        
        if include_wareki:
            output.append("西暦    和暦     干支    読み           十干        十二支")
            output.append("-" * 60)
            for result in results:
                year = result['年']
                # 令和年を計算（2019年5月1日が令和元年）
                reiwa_year = year - 2018
                reiwa_str = f"令和{reiwa_year}年" if reiwa_year > 0 else "平成31年"
                
                output.append(
                    f"{year:<8}{reiwa_str:<8}{result['干支']:<8}"
                    f"{result['読み']:<14}{result['十干']['読み']:<10}"
                    f"{result['十二支']['読み']}"
                )
        else:
            output.append("西暦    干支    読み           十干        十二支")
            output.append("-" * 60)
            for result in results:
                output.append(
                    f"{result['年']:<8}{result['干支']:<8}{result['読み']:<14}"
                    f"{result['十干']['読み']:<10}{result['十二支']['読み']}"
                )
        
        return "\n".join(output)