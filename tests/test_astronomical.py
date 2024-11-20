from koyomi.core.astronomical import AstronomicalCalculator
from datetime import datetime
from skyfield.api import utc
import pytest

def test_solar_longitude():
    calc = AstronomicalCalculator()
    
    # 2024年夏至前後の時刻で太陽黄経をテスト
    time = calc.ts.from_datetime(datetime(2024, 6, 21, 12, 0, tzinfo=utc))
    longitude = calc.get_solar_longitude(time)
    
    # 夏至は黄経90度付近
    assert 89 < longitude < 91

def test_find_solar_term_date():
    calc = AstronomicalCalculator()
    
    # 2024年夏至（黄経90度）の日時を計算
    start = calc.ts.from_datetime(datetime(2024, 6, 1, tzinfo=utc))
    end = calc.ts.from_datetime(datetime(2024, 7, 1, tzinfo=utc))
    
    result_time = calc.find_solar_term_date(90, start, end)
    result_dt = calc.to_jst_datetime(result_time)
    
    # 2024年の夏至は6月21日
    assert result_dt.year == 2024
    assert result_dt.month == 6
    assert result_dt.day == 21

def test_to_jst_datetime():
    calc = AstronomicalCalculator()
    
    # UTCの2024-01-01 00:00:00がJSTでは2024-01-01 09:00:00になることを確認
    time = calc.ts.from_datetime(datetime(2024, 1, 1, tzinfo=utc))
    jst_dt = calc.to_jst_datetime(time)
    
    assert jst_dt.hour == 9
    assert jst_dt.minute == 0
    assert str(jst_dt.tzinfo) == 'Asia/Tokyo'