from koyomi.seasonal.sekki import SolarTerms
from datetime import datetime
import pytest

def test_solar_terms_calculation():
    calculator = SolarTerms()
    results = calculator.calculate(2024)
    
    # 24節気全てが取得できていることを確認
    assert len(results) == 24
    
    # 各結果の形式を確認
    for result in results:
        assert '識別子' in result
        assert '年月日時刻' in result
        assert 'datetime_jst' in result
        assert 'イベント名' in result
        
        # 日時がJSTであることを確認
        assert str(result['datetime_jst'].tzinfo) == 'Asia/Tokyo'
        
        # 2024年のデータであることを確認
        assert result['datetime_jst'].year == 2024

def test_specific_terms():
    calculator = SolarTerms()
    results = calculator.calculate(2024)
    
    # 主要な節気の日付を確認
    term_dates = {term['イベント名']: term['datetime_jst'].date() for term in results}
    
    # 2024年の特定の節気の日付を確認
    # 実際の日付はSkyfieldの計算結果に基づき、天文学的に正確な値となる
    assert term_dates['春分'].month == 3
    assert term_dates['夏至'].month == 6
    assert term_dates['秋分'].month == 9
    assert term_dates['冬至'].month == 12

def test_sorted_order():
    calculator = SolarTerms()
    results = calculator.calculate(2024)
    
    # 日付順にソートされていることを確認
    dates = [result['datetime_jst'] for result in results]
    assert dates == sorted(dates)

def test_year_boundary():
    calculator = SolarTerms()
    
    # 2024年末と2025年初めの節気が正しく分離されていることを確認
    results_2024 = calculator.calculate(2024)
    results_2025 = calculator.calculate(2025)
    
    last_2024 = max(result['datetime_jst'] for result in results_2024)
    first_2025 = min(result['datetime_jst'] for result in results_2025)
    
    assert last_2024.year == 2024
    assert first_2025.year == 2025