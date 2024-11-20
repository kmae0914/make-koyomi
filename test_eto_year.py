from koyomi.cycles.eto_year import YearEto

def test_year_eto():
    calculator = YearEto()
    
    # 2024年の干支を詳しく表示
    result_2024 = calculator.calculate(2024)
    print("\n2024年の干支詳細:")
    print(f"干支: {result_2024['干支']} ({result_2024['読み']})")
    print(f"十干: {result_2024['十干']['漢字']} ({result_2024['十干']['読み']})")
    print(f"十二支: {result_2024['十二支']['漢字']} ({result_2024['十二支']['読み']})")
    print(f"六十干支番号: {result_2024['六十干支番号']}/60")
    
    # 2024年から2030年までの干支を表示
    print(calculator.format_range(2024, 2030))
    
    # 和暦を含まない表示も確認
    print(calculator.format_range(2024, 2030, include_wareki=False))

if __name__ == "__main__":
    test_year_eto()