from koyomi.core.calendar_base import CalendarBase
from datetime import datetime
from skyfield.api import utc
import pytest

class TestCalendarEvent(CalendarBase):
    """テスト用の具象クラス"""
    def __init__(self):
        # 警告を避けるためにsuper().__init__()を明示的に呼び出す
        super().__init__()
        
    def calculate(self, year):
        start, end = self._get_year_range(year, 1, 1)
        test_time = self.astronomical.ts.from_datetime(
            datetime(year, 6, 1, tzinfo=utc)
        )
        return self._create_result(
            f"{year}テストイベント",
            self.astronomical.to_jst_datetime(test_time),
            "テストイベント"
        )

def test_create_result():
    calculator = TestCalendarEvent()
    test_dt = datetime(2024, 6, 1, 9, 0, tzinfo=calculator.astronomical.tz_jst)
    
    # イベント名なしのケース
    result = calculator._create_result("test123", test_dt)
    assert result['識別子'] == "test123"
    assert result['年月日時刻'] == "2024/06/01 09:00:00"
    assert result['datetime_jst'] == test_dt
    assert 'イベント名' not in result
    
    # イベント名ありのケース
    result = calculator._create_result("test123", test_dt, "テスト")
    assert result['イベント名'] == "テスト"

def test_get_year_range():
    calculator = TestCalendarEvent()
    
    # 基本的な年範囲
    start, end = calculator._get_year_range(2024)
    assert calculator.astronomical.to_jst_datetime(start).year == 2024
    assert calculator.astronomical.to_jst_datetime(end).year == 2025
    
    # 前後の月を含む範囲
    start, end = calculator._get_year_range(2024, 2, 2)
    start_dt = calculator.astronomical.to_jst_datetime(start)
    end_dt = calculator.astronomical.to_jst_datetime(end)
    
    assert start_dt.year == 2023
    assert start_dt.month == 11
    assert end_dt.year == 2025
    assert end_dt.month == 3

def test_calculate():
    calculator = TestCalendarEvent()
    result = calculator.calculate(2024)
    
    assert result['識別子'] == "2024テストイベント"
    assert result['イベント名'] == "テストイベント"
    assert result['datetime_jst'].year == 2024
    assert result['datetime_jst'].month == 6