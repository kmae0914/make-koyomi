from skyfield import almanac_east_asia as almanac_ea
from skyfield import almanac
from skyfield.api import load
from datetime import timezone, timedelta
import pytz
import pandas as pd

class SolarTermsCalculator:
    def __init__(self):
        self.ts = load.timescale()
        self.eph = load('de421.bsp')
        self.tz_tokyo = pytz.timezone('Asia/Tokyo')
    
    def calculate_solar_terms(self, year):
        t0 = self.ts.utc(year, 1, 1)
        t1 = self.ts.utc(year + 1, 1, 1)
        
        t, y = almanac.find_discrete(t0, t1, almanac_ea.solar_terms(self.eph))
        
        results = []
        for ti, yi in zip(t, y):
            dt_utc = ti.utc_datetime()
            dt_jst = dt_utc.replace(tzinfo=timezone.utc).astimezone(self.tz_tokyo)
            
            # 識別子の作成
            name_jp = almanac_ea.SOLAR_TERMS_JP[yi]
            term_id = f"{dt_jst.year}{name_jp}"
            
            results.append({
                '識別子': term_id,
                '年月日時刻': dt_jst.strftime('%Y/%m/%d %H:%M:%S'),
                'datetime_jst': dt_jst,  # ソート用に保持
                'term_name': name_jp
            })
        
        return results
    
    def get_terms_for_years(self, start_year, end_year):
        """指定された年範囲の節気を取得"""
        all_terms = []
        for year in range(start_year, end_year+1):
            terms = self.calculate_solar_terms(year)
            all_terms.extend(terms)
            
        # 日時でソート
        all_terms.sort(key=lambda x: x['datetime_jst'])
        return all_terms
    
    def export_to_excel(self, start_year, end_year, filename='solar_terms.xlsx'):
        """節気データをExcelファイルとして出力"""
        terms = self.get_terms_for_years(start_year, end_year)
        
        # DataFrameの作成
        df = pd.DataFrame([{
            '識別子': term['識別子'],
            '年月日時刻': term['年月日時刻']
        } for term in terms])
        
        # Excelファイルとして保存
        df.to_excel(filename, index=False)
        print(f"節気データを {filename} に出力しました。")

# 使用例
# if __name__ == "__main__":
#     calculator = SolarTermsCalculator()
    
#     # 2024年から2033年の節気をExcelファイルとして出力
#     calculator.export_to_excel(2024, 2033, 'solar_terms_2024_2033.xlsx')