from koyomi.seasonal.shanichi import Shanichi
from datetime import datetime

def test_shanichi():
    calculator = Shanichi()
    
    # 2024年と2025年の社日を詳細表示
    for year in [2024, 2025]:
        calculator.print_details(year)
        
        # 計算結果の確認
        print(f"\n{year}年の社日一覧:")
        print(f"{'イベント名':<10} {'年月日時刻'}")
        print("-" * 50)
        
        results = calculator.calculate(year)
        for result in results:
            print(f"{result['イベント名']:<10} {result['年月日時刻']}")
        print()

if __name__ == "__main__":
    test_shanichi()