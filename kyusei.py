def calculate_kusei(year):
    """
    年の九星を計算する関数
    
    Parameters:
    year (int): 西暦年数
    
    Returns:
    tuple: (九星の数字, 九星の名前)
    """
    # 九星の名前を定義
    kusei_names = {
        1: "一白水星",
        2: "二黒土星",
        3: "三碧木星",
        4: "四緑木星",
        5: "五黄土星",
        6: "六白金星",
        7: "七赤金星",
        8: "八白土星",
        9: "九紫火星"
    }
    
    def method2(year):
        """方法2: 各位の数字を足していく方法"""
        # 各位の数字を足す
        def sum_digits(n):
            return sum(int(digit) for digit in str(n))
        
        # 1桁になるまで繰り返し計算
        current_sum = year
        while current_sum > 9:
            current_sum = sum_digits(current_sum)
            
        # 1の場合は10として扱う
        if current_sum == 1:
            current_sum = 10
            
        return 11 - current_sum
    
    # 両方の方法で計算（結果は同じになるはず）
    result = method2(year)  # より簡単な方法2を優先使用
    
    return (result, kusei_names[result])

# 使用例
def test_kusei():
    test_years = [2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025]
    for year in test_years:
        number, name = calculate_kusei(year)
        print(f"{year}年: {name}（{number}番）")

if __name__ == "__main__":
    test_kusei()