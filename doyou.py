from skyfield.api import load
from skyfield.framelib import ecliptic_frame
import pandas as pd
from datetime import timezone, timedelta
import pytz

class DoyoCalculator:
    def __init__(self):
        self.ts = load.timescale()
        self.eph = load('de421.bsp')
        self.sun = self.eph['sun']
        self.earth = self.eph['earth']
        self.tz_tokyo = pytz.timezone('Asia/Tokyo')
        
        # 各季節の土用の黄経（度）
        self.DOYO_LONGITUDES = {
            '冬土用': 297,
            '春土用': 27,
            '夏土用': 117,
            '秋土用': 207
        }
    
    def get_solar_longitude(self, time):
        """指定された時刻の太陽黄経を計算"""
        earth_at_t = self.earth.at(time)
        sun_at_t = earth_at_t.observe(self.sun)
        _, lon, _ = sun_at_t.apparent().frame_latlon(ecliptic_frame)
        return lon.degrees
    
    def find_doyo_date(self, target_longitude, start_time, end_time, tolerance=0.001):
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
    
    def calculate_doyo_dates(self, year):
        """指定された年の各季節の土用入りの日付を計算"""
        results = []
        
        # 探索範囲を2年以上に拡大（前年の1月から次年の12月まで）
        t0 = self.ts.utc(year-1, 1, 1)
        t1 = self.ts.utc(year+1, 12, 31)
        
        for season, longitude in self.DOYO_LONGITUDES.items():
            # 1年の中で黄経が2回到達する可能性があるため、複数の期間で探索
            periods = [
                (self.ts.utc(year-1, 7, 1), self.ts.utc(year+1, 6, 30))
            ]
            
            for start_time, end_time in periods:
                try:
                    # 土用入りの日時を見つける
                    doyo_time = self.find_doyo_date(longitude, start_time, end_time)
                    
                    # UTC から日本時間に変換
                    dt_utc = doyo_time.utc_datetime()
                    dt_jst = dt_utc.replace(tzinfo=timezone.utc).astimezone(self.tz_tokyo)
                    
                    # 指定された年のデータのみを結果に含める
                    if dt_jst.year == year:
                        results.append({
                            '季節': season,
                            '年月日時刻': dt_jst.strftime('%Y/%m/%d %H:%M:%S'),
                            'datetime_jst': dt_jst,  # ソート用に保持
                        })
                except Exception as e:
                    print(f"Warning: {season}の計算中にエラーが発生しました: {str(e)}")
        
        # 日付でソート
        results.sort(key=lambda x: x['datetime_jst'])
        return results
    
    def export_to_excel(self, start_year, end_year, filename='doyo_dates.xlsx'):
        """指定された年範囲の土用入りデータをExcelファイルとして出力"""
        all_dates = []
        for year in range(start_year, end_year + 1):
            dates = self.calculate_doyo_dates(year)
            all_dates.extend(dates)
        
        # DataFrameの作成
        df = pd.DataFrame([{
            '季節': date['季節'],
            '年月日時刻': date['年月日時刻']
        } for date in all_dates])
        
        # Excelファイルとして保存
        df.to_excel(filename, index=False)
        print(f"土用入りデータを {filename} に出力しました。")

# 使用例
if __name__ == "__main__":
    calculator = DoyoCalculator()
    
    # 2024年のデータを表示
    results_2024 = calculator.calculate_doyo_dates(2024)
    for result in results_2024:
        print(f"{result['季節']}: {result['年月日時刻']}")
    
    # 2024年から2033年のデータをExcelファイルとして出力
    calculator.export_to_excel(2024, 2033, 'doyo_dates_2024_2033.xlsx')