from datetime import datetime, timedelta
from typing import Dict, List, Union, Optional
from .astronomical import AstronomicalCalculator
from skyfield.api import utc  # 追加: UTCタイムゾーンのインポート

class CalendarBase:
    """暦計算の基本機能を提供する基底クラス"""
    
    def __init__(self, delta_t: Optional[float] = None):
        """
        Parameters:
            delta_t (float, optional): ΔT値（秒）
        """
        self.astronomical = AstronomicalCalculator(delta_t)
    
    def _create_result(
        self,
        identifier: str,
        dt: datetime,
        event_name: Optional[str] = None
    ) -> Dict:
        """
        計算結果を統一された形式で返す
        
        Parameters:
            identifier (str): イベントの識別子
            dt (datetime): イベントの日時
            event_name (str, optional): イベントの名称
            
        Returns:
            Dict: 以下の形式の辞書
            {
                '識別子': str,
                '年月日時刻': str,
                'datetime_jst': datetime,
                'イベント名': str  # event_nameが指定された場合のみ
            }
        """
        result = {
            '識別子': identifier,
            '年月日時刻': dt.strftime('%Y/%m/%d %H:%M:%S'),
            'datetime_jst': dt
        }
        if event_name:
            result['イベント名'] = event_name
        return result
    
    def _get_year_range(
        self,
        year: int,
        months_before: int = 0,
        months_after: int = 0
    ) -> tuple:
        """
        計算用の期間を取得
        
        Parameters:
            year (int): 対象年
            months_before (int): 前年からの月数
            months_after (int): 翌年への月数
            
        Returns:
            tuple: (開始時刻のTime object, 終了時刻のTime object)
        """
        # 開始時刻（UTCでの1月1日）
        start_date = datetime(year, 1, 1, tzinfo=utc)  # 修正: ts.utc → utc
        if months_before > 0:
            # monthsだけ前の月の1日に移動
            year_diff, month = divmod(months_before, 12)
            if month == 0:
                year_diff -= 1
                month = 12
            year_start = year - year_diff - 1
            month_start = 12 - month + 1
            start_date = datetime(year_start, month_start, 1, tzinfo=utc)  # 修正: ts.utc → utc
        
        # 終了時刻（翌年以降の1月1日）
        end_date = datetime(year + 1, 1, 1, tzinfo=utc)  # 修正: ts.utc → utc
        if months_after > 0:
            # monthsだけ後の月の1日に移動
            year_diff, month = divmod(months_after, 12)
            end_date = datetime(year + year_diff + 1, month + 1, 1, tzinfo=utc)  # 修正: ts.utc → utc
        
        return (
            self.astronomical.ts.from_datetime(start_date),
            self.astronomical.ts.from_datetime(end_date)
        )

    def calculate(self, year: int) -> Union[Dict, List[Dict]]:
        """
        暦イベントを計算する抽象メソッド
        
        Parameters:
            year (int): 対象年
            
        Returns:
            Union[Dict, List[Dict]]: 計算結果
        """
        raise NotImplementedError("Subclasses must implement calculate()")