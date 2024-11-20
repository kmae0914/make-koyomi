from koyomi.cycles.month_length import MonthLength
import calendar

def test_month_length():
    calculator = MonthLength()
    
    # 2024年（閏年）と2025年の月の大小を表示
    print(calculator.format_years(2024, 2025))
    
    # 特定の月の詳細情報を表示
    result = calculator.calculate(2024, 2)
    print("\n2024年2月の詳細:")
    print(f"日数: {result['日数']}日")
    print(f"大小: {result['大小']}")
    print(f"閏月: {'はい' if result['閏月'] else 'いいえ'}")

def test_accuracy():
    """月の大小が正しいか検証"""
    calculator = MonthLength()
    year = 2024
    
    # 大の月（31日）
    big_months = [1, 3, 5, 7, 8, 10, 12]
    for month in big_months:
        result = calculator.calculate(year, month)
        assert result['大小'] == "大"
        assert result['日数'] == 31
    
    # 小の月（30日）
    small_months = [4, 6, 9, 11]
    for month in small_months:
        result = calculator.calculate(year, month)
        assert result['大小'] == "小"
        assert result['日数'] == 30
    
    # 2月の特別処理
    feb_2024 = calculator.calculate(2024, 2)  # 閏年
    assert feb_2024['日数'] == 29
    assert feb_2024['大小'] == "小"
    assert feb_2024['閏月'] == True
    
    feb_2025 = calculator.calculate(2025, 2)  # 平年
    assert feb_2025['日数'] == 28
    assert feb_2025['大小'] == "小"
    assert feb_2025['閏月'] == False

if __name__ == "__main__":
    print("月の大小の表示テスト:")
    test_month_length()
    print("\n精度検証テスト:")
    test_accuracy()
    print("全てのテストが正常に完了しました。")