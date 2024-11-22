from koyomi.cycles.holiday import Holiday
from datetime import date

def main():
    calculator = Holiday()
    
    # 2024年の祝日・休日を表示
    print("【祝日・休日（振替休日含む）】")
    print(calculator.format_year(2024))
    
    print("\n【祝日のみ】")
    print(calculator.format_year(2024, include_substitute=False))
    
    print("\n【振替休日・国民の休日の詳細】")
    calculator.print_substitute_details(2024)
    
    # 2025年も同様に表示
    print("\n" + "=" * 70)
    print("【2025年】")
    print(calculator.format_year(2025))
    calculator.print_substitute_details(2025)

if __name__ == "__main__":
    main()