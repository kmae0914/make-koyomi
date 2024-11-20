from skyfield.api import load
from skyfield.framelib import ecliptic_frame
import pandas as pd
from datetime import timezone, timedelta
import pytz

class TsuyuiriCalculator:
    def __init__(self):
        self.ts = load.timescale()
        self.eph = load('de421.bsp')
        self.sun = self.eph['sun']
        self.earth = self.eph['earth']
        self.tz_tokyo = pytz.timezone('Asia/Tokyo')
        
        # 入梅の黄経（度）
        self.Tsuyuiri_LONGITUDE = 80
    
    def get_solar_longitude(self, time):
        """指定された時刻の太陽黄経を計算"""
        earth_at_t = self.earth.at(time)
        sun_at_t = earth_at_t.observe(self.sun)
        _, lon, _ = sun_at_t.apparent().frame_latlon(ecliptic_frame)
        return lon.degrees
    
    def find_Tsuyuiri_date(self, target_longitude, start_time, end_time, tolerance=0.001):
        """二分探索で特定の黄経になる日時を見つける"""
        while (end_time.tt - start_time.tt) > tolerance:
            mid_time = self.ts.tt_jd((start_time.tt + end_time.tt) / 2)
            mid_lon = self.get_solar_longitude(mid_time)
            
            # 黄経が360度を超える場合の処理
            if mid_lon > target_longitude + 180:
                mid_lon -= 360
            elif mid_lon < target_longitude - 180:
                mid_lon += 360
                
            if abs(mid_lon - target_longitude) < tolerance:
                return mid_time
            elif mid_lon < target_longitude:
                start_time = mid_time
            else:
                end_time = mid_time
        
        return start_time
    
    def calculate_Tsuyuiri_date(self, year):
        """指定された年の入梅の日付を計算"""
        # 5月1日から7月末までを探索範囲とする（十分な余裕を持って）
        t0 = self.ts.utc(year, 5, 1)
        t1 = self.ts.utc(year, 7, 31)
        
        try:
            # 入梅の日時を見つける
            Tsuyuiri_time = self.find_Tsuyuiri_date(self.Tsuyuiri_LONGITUDE, t0, t1)
            
            # UTC から日本時間に変換
            dt_utc = Tsuyuiri_time.utc_datetime()
            dt_jst = dt_utc.replace(tzinfo=timezone.utc).astimezone(self.tz_tokyo)
            
            return {
                '年月日時刻': dt_jst.strftime('%Y/%m/%d %H:%M:%S'),
                'datetime_jst': dt_jst
            }
            
        except Exception as e:
            print(f"Warning: 入梅の計算中にエラーが発生しました: {str(e)}")
            return None
    
    def export_to_excel(self, start_year, end_year, filename='Tsuyuiri_dates.xlsx'):
        """指定された年範囲の入梅データをExcelファイルとして出力"""
        all_dates = []
        for year in range(start_year, end_year + 1):
            date = self.calculate_Tsuyuiri_date(year)
            if date:
                all_dates.append({
                    '年': year,
                    '年月日時刻': date['年月日時刻']
                })
        
        # DataFrameの作成
        df = pd.DataFrame(all_dates)
        
        # Excelファイルとして保存
        df.to_excel(filename, index=False)
        print(f"入梅データを {filename} に出力しました。")

# 使用例
if __name__ == "__main__":
    calculator = TsuyuiriCalculator()
    
    # 2024年の入梅を計算
    result_2024 = calculator.calculate_Tsuyuiri_date(2024)
    if result_2024:
        print(f"2024年の入梅: {result_2024['年月日時刻']}")

    # 2025年の入梅を計算
    result_2025 = calculator.calculate_Tsuyuiri_date(2025)
    if result_2025:
        print(f"2025年の入梅: {result_2025['年月日時刻']}")
    
    # 2024年から2033年のデータをExcelファイルとして出力
    calculator.export_to_excel(2024, 2033, 'Tsuyuiri_dates_2024_2033.xlsx')