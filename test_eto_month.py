from koyomi.cycles.eto_month import MonthEto

def test_month_eto():
    calculator = MonthEto()
    
    # 2024年と2025年の月干支を表示
    for year in [2024, 2025]:
        print(calculator.format_year(year))
        print()
    
    # 特定の月の詳細情報を表示
    result = calculator.calculate(2024, 1)
    print("\n2024年1月の詳細:")
    print(f"年干支: {result['年干支']}")
    print(f"月干支: {result['月干支']}")

if __name__ == "__main__":
    test_month_eto()