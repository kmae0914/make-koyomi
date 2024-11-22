from typing import Dict, List, Optional
from .eto_year import YearEto
from ..core.calendar_base import CalendarBase

class Nattoin(CalendarBase):
    """納音を計算するクラス"""
    
    # 納音の定義（60干支との対応）
    NATTOIN_DEFINITIONS = [
        # 1-6
        ('海中金', 'かいちゅうきん', ['甲子', '乙丑']),
        ('爐中火', 'ろちゅうか', ['丙寅', '丁卯']),
        ('大林木', 'たいりんぼく', ['戊辰', '己巳']),
        ('路傍土', 'ろぼうど', ['庚午', '辛未']),
        ('釼鋒金', 'じんぼうきん', ['壬申', '癸酉']),
        ('山頭火', 'さんとうか', ['甲戌', '乙亥']),
        # 7-12
        ('澗下水', 'かんかすい', ['丙子', '丁丑']),
        ('城頭土', 'じょうとうど', ['戊寅', '己卯']),
        ('白鑞金', 'はくろうきん', ['庚辰', '辛巳']),
        ('楊柳木', 'ようりゅうぼく', ['壬午', '癸未']),
        ('井泉水', 'せいせんすい', ['甲申', '乙酉']),
        ('屋上土', 'おくじょうど', ['丙戌', '丁亥']),
        # 13-18
        ('霹靂火', 'へきれきか', ['戊子', '己丑']),
        ('松柏木', 'しょうはくぼく', ['庚寅', '辛卯']),
        ('長流水', 'ちょうりゅうすい', ['壬辰', '癸巳']),
        ('沙中金', 'さちゅうきん', ['甲午', '乙未']),
        ('山下火', 'さんげか', ['丙申', '丁酉']),
        ('平地木', 'へいちぼく', ['戊戌', '己亥']),
        # 19-24
        ('壁上土', 'へきじょうど', ['庚子', '辛丑']),
        ('金箔金', 'きんぱくきん', ['壬寅', '癸卯']),
        ('覆燈火', 'ふくとうか', ['甲辰', '乙巳']),
        ('天河水', 'てんがすい', ['丙午', '丁未']),
        ('大駅土', 'たいえきど', ['戊申', '己酉']),
        ('釵釧金', 'さいせんきん', ['庚戌', '辛亥']),
        # 25-30
        ('桑柘木', 'そうしゃくもく', ['壬子', '癸丑']),
        ('大溪水', 'だいけいすい', ['甲寅', '乙卯']),
        ('沙中土', 'さちゅうど', ['丙辰', '丁巳']),
        ('天上火', 'てんじょうか', ['戊午', '己未']),
        ('柘榴木', 'ざくろぼく', ['庚申', '辛酉']),
        ('大海水', 'たいかいすい', ['壬戌', '癸亥'])
    ]

    def __init__(self):
        """初期化"""
        super().__init__()
        self.eto_calculator = YearEto()
        
        # 干支から納音へのマッピングを作成
        self.eto_to_nattoin = {}
        for kanji, yomi, eto_list in self.NATTOIN_DEFINITIONS:
            for eto in eto_list:
                self.eto_to_nattoin[eto] = {
                    '漢字': kanji,
                    '読み': yomi,
                    '対応干支': eto_list
                }

    def calculate(self, year: int) -> Dict:
        """
        指定された年の納音を計算
        
        Parameters:
            year (int): 対象年
            
        Returns:
            Dict: 計算結果
            {
                '年': int,
                '干支': str,
                '納音': {
                    '漢字': str,
                    '読み': str,
                    '対応干支': List[str]
                }
            }
        """
        # まず干支を計算
        eto_result = self.eto_calculator.calculate(year)
        kanshi = eto_result['干支']
        
        # 干支から納音を取得
        nattoin_info = self.eto_to_nattoin.get(kanshi)
        
        return {
            '年': year,
            '干支': kanshi,
            '納音': nattoin_info
        }
    
    def calculate_range(self, start_year: int, end_year: int) -> List[Dict]:
        """指定された範囲の年の納音を計算"""
        return [self.calculate(year) for year in range(start_year, end_year + 1)]
    
    def format_single(self, result: Dict) -> str:
        """単年の納音情報を整形"""
        nattoin = result['納音']
        return (
            f"{result['年']}年（{result['干支']}）の納音: "
            f"{nattoin['漢字']}（{nattoin['読み']}）"
        )
    
    def format_range(self, start_year: int, end_year: int) -> str:
        """指定された範囲の年の納音を整形して文字列で返す"""
        results = self.calculate_range(start_year, end_year)
        
        output = [
            f"\n{start_year}年から{end_year}年までの納音",
            "─" * 70,
            "年        干支      納音",
            "─" * 70
        ]
        
        for result in results:
            nattoin = result['納音']
            output.append(
                f"{result['年']:<8}  "
                f"{result['干支']:<8}  "
                f"{nattoin['漢字']}（{nattoin['読み']}）"
            )
        
        return "\n".join(output)