from koyomi.cycles.hassen import Hassen
from datetime import date

def test_hassen():
    calculator = Hassen()
    
    # 2024年の八専を表示
    print(calculator.format_year(2024))
    
    # 2025年の八専も表示
    print("\n" + "=" * 70)
    print(calculator.format_year(2025))
    
    # 特定の日の八専情報を確認
    test_date = date(2024, 1, 1)
    result = calculator.calculate_single_day(test_date)
    
    print(f"\n{test_date}の八専情報:")
    print(f"干支: {result['干支']}")
    if result['八専期間']:
        print(f"種類: {result['種類']}")
        print(f"五行: {result['五行']}")
    else:
        print("八専期間ではありません")

if __name__ == "__main__":
    test_hassen()