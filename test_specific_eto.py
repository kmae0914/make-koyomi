from koyomi.cycles.specific_eto import SpecificEto

def main():
    calculator = SpecificEto()
    
    # 2024年と2025年の特定干支の日を表示
    for year in [2024, 2025]:
        print(calculator.format_year(year))

if __name__ == "__main__":
    main()