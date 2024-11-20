from koyomi.cycles.kusei import Kusei

def test_kusei():
    calculator = Kusei()
    
    # 2024年の九星を詳しく表示
    result_2024 = calculator.calculate(2024)
    print("\n2024年の九星詳細:")
    print(f"九星: {result_2024['漢字']} ({result_2024['読み']})")
    print(f"九星番号: {result_2024['九星番号']}")
    print(f"属性: {result_2024['属性']}")
    print(f"方位: {result_2024['方位']}")
    print(f"色: {result_2024['色']}")
    
    # 2024年から2030年までの九星を表示（詳細情報あり）
    print(calculator.format_range(2024, 2030))
    
    # 詳細情報なしでの表示も確認
    print(calculator.format_range(2024, 2030, include_details=False))

if __name__ == "__main__":
    test_kusei()