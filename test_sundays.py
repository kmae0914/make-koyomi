from koyomi.cycles.sundays import Sundays
from datetime import date

def test_sundays():
    calculator = Sundays()
    
    print("\n=== 2025年の日曜日（ISO週番号付き） ===")
    print(calculator.format_year(2025, include_week_number=True))
    
    print("\n=== 2025年1月の日曜日 ===")
    print(calculator.format_month(2025, 1))
    
    # 特定の月の第n日曜日の検証
    results = calculator.calculate(2025)
    january_sundays = [r for r in results if r['月'] == 1]
    
    print("\n2025年1月の日曜日:")
    for result in january_sundays:
        print(f"{result['日付'].strftime('%Y/%m/%d')}: 第{result['第n日曜']}日曜日")

if __name__ == "__main__":
    test_sundays()