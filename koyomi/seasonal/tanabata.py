from typing import Dict, List, Optional
from datetime import datetime, timedelta
from ..core.calendar_base import CalendarBase
from .sekki import SolarTerms
from skyfield import almanac
from skyfield.api import utc

class Tanabata(CalendarBase):
    """七夕の日付を計算するクラス（新暦七夕と伝統的七夕）"""
    
    def __init__(self, delta_t: float = 69.0):
        """
        Parameters:
            delta_t (float): ΔT値（秒）。デフォルトは2024年の概算値
        """
        super().__init__(delta_t)
        self.sekki_calculator = SolarTerms(delta_t)
    
    def _find_shosho(self, year: int) -> Optional[datetime]:
        """
        指定された年の処暑の日時を取得
        
        Parameters:
            year (int): 対象年
            
        Returns:
            Optional[datetime]: 処暑の日時。見つからない場合はNone
        """
        terms = self.sekki_calculator.calculate(year)
        for term in terms:
            if term['イベント名'] == '処暑':
                return term['datetime_jst']
        return None

    def _find_all_new_moons(self, shosho_time: datetime) -> List[datetime]:
        """
        処暑を含む日までの2ヶ月前からの新月をすべて取得
        
        Parameters:
            shosho_time (datetime): 処暑の日時
            
        Returns:
            List[datetime]: 新月の日時リスト
        """
        # 探索開始時刻（処暑の2ヶ月前）
        start_time = self.astronomical.ts.from_datetime(
            shosho_time - timedelta(days=60)
        )
        
        # 探索終了時刻（処暑の翌日）
        end_time = self.astronomical.ts.from_datetime(
            shosho_time + timedelta(days=1)
        )
        
        # 新月を取得
        t, y = almanac.find_discrete(
            start_time,
            end_time,
            almanac.moon_phases(self.astronomical.eph)
        )
        
        # 新月（月相が0）のみをフィルタリングし、JSTに変換
        new_moons = [
            self.astronomical.to_jst_datetime(t_i)
            for t_i, y_i in zip(t, y) if y_i == 0
        ]
        
        return new_moons

    def _find_nearest_new_moon(self, shosho_time: datetime, new_moons: List[datetime]) -> Optional[datetime]:
        """
        処暑に最も近い新月を見つける（処暑の日までで）
        
        Parameters:
            shosho_time (datetime): 処暑の日時
            new_moons (List[datetime]): 新月の日時リスト
            
        Returns:
            Optional[datetime]: 最も近い新月の日時。見つからない場合はNone
        """
        shosho_date = shosho_time.date()
        nearest_new_moon = None
        min_diff = float('inf')
        
        for new_moon in new_moons:
            new_moon_date = new_moon.date()
            time_diff = (shosho_date - new_moon_date).days
            
            # 新月が処暑と同じ日か前の日の場合のみ対象とする
            if time_diff >= 0 and time_diff < min_diff:
                min_diff = time_diff
                nearest_new_moon = new_moon
        
        return nearest_new_moon

    def calculate_modern(self, year: int) -> Dict:
        """
        新暦の七夕（7月7日）を計算
        
        Parameters:
            year (int): 対象年
            
        Returns:
            Dict: 計算結果
        """
        tanabata_date = datetime(year, 7, 7, 0, 0, tzinfo=self.astronomical.tz_jst)
        return self._create_result(
            f"{year}新暦七夕",
            tanabata_date,
            "新暦七夕"
        )

    def calculate_traditional(self, year: int) -> Optional[Dict]:
        """
        伝統的七夕（処暑前の最も近い新月から数えて7日目）を計算
        
        Parameters:
            year (int): 対象年
            
        Returns:
            Optional[Dict]: 計算結果。計算できない場合はNone
        """
        # 処暑の日時を取得
        shosho = self._find_shosho(year)
        if not shosho:
            return None
        
        # 新月を取得
        new_moons = self._find_all_new_moons(shosho)
        if not new_moons:
            return None
        
        # 処暑に最も近い新月を見つける
        nearest_new_moon = self._find_nearest_new_moon(shosho, new_moons)
        if not nearest_new_moon:
            return None
        
        # 新月の日を1日目として数え、7日目を計算
        tanabata_date = nearest_new_moon + timedelta(days=6)  # 7日目なので6日後
        
        return self._create_result(
            f"{year}伝統的七夕",
            tanabata_date,
            "伝統的七夕"
        )

    def calculate(self, year: int) -> List[Dict]:
        """
        指定された年の新暦と伝統的七夕を計算
        
        Parameters:
            year (int): 対象年
            
        Returns:
            List[Dict]: 七夕の日付リスト
        """
        results = []
        
        # 新暦の七夕
        modern = self.calculate_modern(year)
        if modern:
            results.append(modern)
        
        # 伝統的七夕
        traditional = self.calculate_traditional(year)
        if traditional:
            results.append(traditional)
        
        # 日付でソート
        results.sort(key=lambda x: x['datetime_jst'])
        
        return results