from koyomi.seasonal.tsuyu import Tsuyuiri
from datetime import datetime
import pytest

def test_tsuyuiri_calculation():
    calculator = Tsuyuiri()
    result = calculator.calculate(2024)
    
    # 基本的な結果の形式を確認
    assert '識別子' in result
    assert '年月日時刻' in result
    assert 'datetime_jst' in result
    assert 'イベント名' in result
    
    # イベント名の確認
    assert result['イベント名'] == "入梅"
    assert result['識別子'] == "2024入梅"
    
    # 日時がJSTであることを確認
    assert str(result['datetime_jst'].tzinfo) == 'Asia/Tokyo'
    
    # 2024年のデータであることを確認
    assert result['datetime_jst'].year == 2024
    
    # 入梅は6月頃であることを確認
    assert result['datetime_jst'].month == 6

def test_multi_year_calculation():
    calculator = Tsuyuiri()
    
    # 複数年の計算結果を確認
    result_2024 = calculator.calculate(2024)
    result_2025 = calculator.calculate(2025)
    
    # 異なる年で正しく計算されていることを確認
    assert result_2024['datetime_jst'].year == 2024
    assert result_2025['datetime_jst'].year == 2025
    
    # どちらも6月頃であることを確認
    assert result_2024['datetime_jst'].month == 6
    assert result_2025['datetime_jst'].month == 6

def test_date_consistency():
    calculator = Tsuyuiri()
    
    # 同じ年の計算結果が一貫していることを確認
    result1 = calculator.calculate(2024)
    result2 = calculator.calculate(2024)
    
    assert result1['datetime_jst'] == result2['datetime_jst']