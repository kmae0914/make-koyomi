class EtoCalculator:
    def __init__(self):
        # 十干(じっかん)
        self.jikkan = [
            "甲(きのえ)", "乙(きのと)", "丙(ひのえ)", "丁(ひのと)", "戊(つちのえ)",
            "己(つちのと)", "庚(かのえ)", "辛(かのと)", "壬(みずのえ)", "癸(みずのと)"
        ]
        
        # 十二支(じゅうにし)
        self.junishi = [
            "子(ね)", "丑(うし)", "寅(とら)", "卯(う)", "辰(たつ)", "巳(み)",
            "午(うま)", "未(ひつじ)", "申(さる)", "酉(とり)", "戌(いぬ)", "亥(い)"
        ]
    
    def get_eto(self, year):
        """
        年の干支を計算する
        
        Parameters:
            year (int): 西暦年
            
        Returns:
            tuple: (干支の文字列, 十干, 十二支)
        """
        # 十干と十二支のインデックスを計算
        jikkan_idx = (year + 6) % 10
        junishi_idx = (year + 8) % 12
        
        # 十干と十二支を取得
        jikkan = self.jikkan[jikkan_idx]
        junishi = self.junishi[junishi_idx]
        
        # 干支の組み合わせを作成（かっこ内の読み方は省略）
        eto = f"{jikkan.split('(')[0]}{junishi.split('(')[0]}"
        
        return (eto, jikkan, junishi)

def print_eto_range(start_year, end_year):
    """指定された年の範囲の干支を表示する"""
    calc = EtoCalculator()
    
    print(f"{start_year}年から{end_year}年までの干支:")
    print("-" * 50)
    print("西暦    和暦     干支    十干        十二支")
    print("-" * 50)
    
    for year in range(start_year, end_year + 1):
        # 令和年を計算
        reiwa_year = year - 2018  # 令和元年は2019年
        reiwa_str = f"令和{reiwa_year}年" if reiwa_year > 0 else "平成31年"
        
        # 干支を計算
        eto, jikkan, junishi = calc.get_eto(year)
        
        print(f"{year}  {reiwa_str:6}  {eto:4}  {jikkan:10}  {junishi}")

# 使用例
if __name__ == "__main__":
    # 2024年から2030年までの干支を表示
    print_eto_range(2024, 2030)
    
    # 特定の年の干支を確認
    calc = EtoCalculator()
    year = 2025
    eto, jikkan, junishi = calc.get_eto(year)
    print(f"\n{year}年（令和{year-2018}年）の干支:")
    print(f"干支: {eto}")
    print(f"十干: {jikkan}")
    print(f"十二支: {junishi}")