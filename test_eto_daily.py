from koyomi.cycles.eto_daily import DailyEto
from datetime import date

def test_monthly_first_days_eto():
    """各月1日の干支を確認するテスト"""
    calculator = DailyEto()
    
    test_years = [2024, 2025]  # テストする年
    
    for year in test_years:
        print(f"\n=== {year}年 各月1日の干支 ===")
        print("月日       干支    読み          通日")
        print("-" * 50)
        
        # 1月から12月まで
        for month in range(1, 13):
            result = calculator.calculate_single_day(date(year, month, 1))
            date_str = result['日付'].strftime('%Y/%m/%d')
            print(f"{date_str}  {result['干支']}    {result['読み']}    {result['通日']:2d}/60")

if __name__ == "__main__":
    # test_monthly_first_days_eto()
    eto_data = DailyEto().calculate_year(2024)
    for eto in eto_data:
        print(f"{eto['日付']} {eto['干支']} {eto['読み']} {eto['通日']}")
