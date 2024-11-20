from typing import Dict, List
from datetime import datetime, timedelta
from ..core.calendar_base import CalendarBase
from .sekki import SolarTerms
from ..cycles.eto_daily import DailyEto

class Shanichi(CalendarBase):
    """社日を計算するクラス"""
    
    def __init__(self, delta_t: float = 69.0):
        """
        Parameters:
            delta_t (float): ΔT値（秒）。デフォルトは2024年の概算値
        """
        super().__init__(delta_t)
        self.sekki_calculator = SolarTerms(delta_t)
        self.eto_calculator = DailyEto()
    
    def _find_sekki_date(self, year: int, sekki_name: str) -> datetime:
        """二十四節気から春分・秋分の日付を取得"""
        terms = self.sekki_calculator.calculate(year)
        for term in terms:
            if term['イベント名'] == sekki_name:
                return term['datetime_jst']
        return None
    
    def _find_nearest_tsuchinoe(self, base_date: datetime, range_days: int = 15) -> datetime:
        """
        指定された日付の前後range_days日以内で最も近い戊の日を見つける
        
        Parameters:
            base_date (datetime): 基準となる日付
            range_days (int): 前後の探索日数
            
        Returns:
            datetime: 最も近い戊の日
        """
        # 探索範囲の日付リスト作成
        dates_to_check = [
            base_date.date() + timedelta(days=i)
            for i in range(-range_days, range_days + 1)
        ]
        
        # 各日の干支を計算し、戊の日を抽出
        tsuchinoe_dates = []
        for check_date in dates_to_check:
            eto = self.eto_calculator.calculate_single_day(check_date)
            # 戊（つちのえ）は十干の5番目（インデックスは4）
            if eto['十干']['番号'] == 4:
                tsuchinoe_dates.append(check_date)
        
        if not tsuchinoe_dates:
            return None
        
        # 基準日に最も近い戊の日を選択
        base_date_only = base_date.date()
        nearest_date = min(
            tsuchinoe_dates,
            key=lambda d: abs((d - base_date_only).days)
        )
        
        # 時刻情報を保持したdatetimeを返す
        return datetime.combine(
            nearest_date,
            datetime.min.time(),
            tzinfo=self.astronomical.tz_jst
        )
    
    def calculate(self, year: int) -> List[Dict]:
        """
        指定された年の春季・秋季の社日を計算
        
        Parameters:
            year (int): 対象年
            
        Returns:
            List[Dict]: 社日の日付リスト
        """
        results = []
        
        # 春分と秋分それぞれについて計算
        for sekki_name, season in [('春分', '春'), ('秋分', '秋')]:
            # 節気の日時を取得
            sekki_date = self._find_sekki_date(year, sekki_name)
            if sekki_date:
                # 最も近い戊の日を探す
                shanichi_date = self._find_nearest_tsuchinoe(sekki_date)
                if shanichi_date:
                    results.append(self._create_result(
                        f"{year}{season}社日",
                        shanichi_date,
                        f"{season}社日"
                    ))
        
        # 日付順にソート
        results.sort(key=lambda x: x['datetime_jst'])
        
        return results

    def print_details(self, year: int) -> None:
        """
        社日の詳細情報を表示（デバッグ用）
        """
        for sekki_name, season in [('春分', '春'), ('秋分', '秋')]:
            print(f"\n=== {year}年 {season}社日 ===")
            
            # 節気の日時を取得
            sekki_date = self._find_sekki_date(year, sekki_name)
            if not sekki_date:
                print(f"{sekki_name}の日時が取得できませんでした。")
                continue
                
            print(f"{sekki_name}: {sekki_date.strftime('%Y/%m/%d %H:%M:%S')}")
            
            # 最も近い戊の日を探す
            shanichi_date = self._find_nearest_tsuchinoe(sekki_date)
            if not shanichi_date:
                print("戊の日が見つかりませんでした。")
                continue
            
            print(f"{season}社日: {shanichi_date.strftime('%Y/%m/%d %H:%M:%S')}")
            
            # 干支の確認
            eto = self.eto_calculator.calculate_single_day(shanichi_date.date())
            print(f"干支: {eto['干支']} ({eto['読み']})")
            print(f"通日: {eto['通日']}/60")