from datetime import datetime, date, timedelta

class DailyKanshiCalculator:
    def __init__(self):
        # 十干(じっかん)
        self.JIKKAN = [
            "甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"
        ]
        self.JIKKAN_YOMI = [
            "きのえ", "きのと", "ひのえ", "ひのと", "つちのえ",
            "つちのと", "かのえ", "かのと", "みずのえ", "みずのと"
        ]
        
        # 十二支(じゅうにし)
        self.JUNISHI = [
            "子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"
        ]
        self.JUNISHI_YOMI = [
            "ね", "うし", "とら", "う", "たつ", "み",
            "うま", "ひつじ", "さる", "とり", "いぬ", "い"
        ]
    
        self.BASE_DATE = date(2024, 1, 1)

    def get_kanshi(self, target_date: date) -> dict:
        """
        指定された日付の干支を計算する
        """
        # 基準日からの経過日数を計算
        days_diff = (target_date - self.BASE_DATE).days
        
        # 60日周期での日数を計算
        cycle_days = days_diff % 60
        
        # 十干と十二支のインデックスを計算
        jikkan_index = cycle_days % 10
        junishi_index = cycle_days % 12
        
        return {
            'kanshi': f"{self.JIKKAN[jikkan_index]}{self.JUNISHI[junishi_index]}",
            'yomi': f"{self.JIKKAN_YOMI[jikkan_index]}{self.JUNISHI_YOMI[junishi_index]}",
            'jikkan': {
                'kanshi': self.JIKKAN[jikkan_index],
                'yomi': self.JIKKAN_YOMI[jikkan_index],
                'index': jikkan_index
            },
            'junishi': {
                'kanshi': self.JUNISHI[junishi_index],
                'yomi': self.JUNISHI_YOMI[junishi_index],
                'index': junishi_index
            },
            'cycle_day': cycle_days + 1  # 1から60までの日番号
        }

    def get_month_kanshi(self, year: int, month: int) -> list:
        """
        指定された年月の全日の干支を計算する
        """
        results = []
        target_date = date(year, month, 1)
        
        # 月末まで繰り返し
        while target_date.month == month:
            kanshi = self.get_kanshi(target_date)
            results.append({
                'date': target_date,
                'kanshi': kanshi
            })
            target_date += timedelta(days=1)
            
        return results

    def print_month_kanshi(self, year: int, month: int):
        """
        指定された年月の干支カレンダーを表示
        """
        results = self.get_month_kanshi(year, month)
        
        print(f"{year}年{month}月の干支暦")
        print("=" * 50)
        print("日付    干支    読み          日番号")
        print("-" * 50)
        
        for r in results:
            date_str = r['date'].strftime('%m/%d')
            kanshi = r['kanshi']
            print(f"{date_str}  {kanshi['kanshi']}    {kanshi['yomi']}    {kanshi['cycle_day']:2d}/60")

# 使用例
if __name__ == "__main__":
    calc = DailyKanshiCalculator()
    
    # テスト用の日付で確認
    test_dates = [
        date(1893, 1, 1),
        date(1893, 2, 1),
        date(1893, 3, 1),
        date(1893, 4, 1),
        date(1893, 5, 1),
        date(1893, 6, 1),
        date(1893, 7, 1),
        date(1893, 8, 1),
        date(1893, 9, 1),
        date(1893, 10, 1),
        date(1893, 11, 1),
        date(1893, 12, 1),
    ]
    
    print("干支の確認:")
    for test_date in test_dates:
        result = calc.get_kanshi(test_date)
        print(f"{test_date.strftime('%Y-%m-%d')}: {result['kanshi']} ({result['yomi']})")