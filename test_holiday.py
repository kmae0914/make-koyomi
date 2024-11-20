from koyomi.cycles.holiday import Holiday
from datetime import date

if __name__ == "__main__":
    calculator = Holiday()

    # 振替休日を含めて表示（デフォルト）
    print(calculator.format_year(2024))

    # 祝日のみ表示
    print(calculator.format_year(2024, include_substitute=False))

    # 計算結果の詳細な情報を取得
    results = calculator.calculate(2024)
    for result in results:
        if result['オリジナル祝日']:
            print(f"{result['日付']}: {result['種類']} (元の祝日: {result['オリジナル祝日']})")