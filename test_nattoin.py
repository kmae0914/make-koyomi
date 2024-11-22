from koyomi.cycles.nattoin import Nattoin
from datetime import date

def test_nattoin():
    calculator = Nattoin()
    
    # 2024年（甲辰年）の納音を表示
    result_2024 = calculator.calculate(2024)
    print("\n2024年の納音詳細:")
    print(calculator.format_single(result_2024))
    
    # 対応する干支の表示
    nattoin = result_2024['納音']
    print(f"対応する干支: {', '.join(nattoin['対応干支'])}")
    
    # 2024年から2030年までの納音を表示
    print(calculator.format_range(2024, 2030))

if __name__ == "__main__":
    test_nattoin()