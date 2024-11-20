from skyfield import almanac_east_asia as almanac_ea
from skyfield import almanac
from skyfield.api import load
from datetime import datetime, timezone, timedelta
import pytz
import pandas as pd
from typing import List, Dict
from nizyushiekki import SolarTermsCalculator
from daily_rokuzikkanshi import DailyKanshiCalculator

class JapaneseSeasonalDaysCalculator:
    def __init__(self):
        # 2024年のΔT = 69秒を設定
        self.ts = load.timescale(delta_t=69.0)
        self.eph = load('de421.bsp')
        self.tz_tokyo = pytz.timezone('Asia/Tokyo')
        self.solar_terms_calculator = SolarTermsCalculator()
    
    def calculate_setsubun(self, year: int) -> Dict:
        """節分 (立春の前日) を計算"""
        solar_terms = self.solar_terms_calculator.calculate_solar_terms(year)
        for term in solar_terms:
            if term['term_name'] == '立春':
                risshun_date = term['datetime_jst']
                setsubun_date = risshun_date - timedelta(days=1)
                return {
                    '識別子': f"{year}節分",
                    '年月日時刻': setsubun_date.strftime('%Y/%m/%d %H:%M:%S'),
                    'datetime_jst': setsubun_date
                }
    
    def calculate_higan(self, year: int) -> List[Dict]:
        """お彼岸 (春分・秋分の前後3日間) を計算"""
        solar_terms = self.solar_terms_calculator.calculate_solar_terms(year)
        higan_dates = []
        
        for term in solar_terms:
            if term['term_name'] in ['春分', '秋分']:
                center_date = term['datetime_jst']
                season = '春' if term['term_name'] == '春分' else '秋'
                
                # 前後3日間を追加
                for days in range(-3, 4):
                    higan_date = center_date + timedelta(days=days)
                    higan_dates.append({
                        '識別子': f"{year}{season}彼岸{days+3+1}日目",
                        '年月日時刻': higan_date.strftime('%Y/%m/%d %H:%M:%S'),
                        'datetime_jst': higan_date
                    })
        
        return higan_dates
    
    def get_solar_longitude(self, time):
        """指定された時刻での太陽黄経を計算"""
        from skyfield.api import wgs84
        
        # 東京の座標を使用
        TOKYO_LAT = 35.6762
        TOKYO_LON = 139.6503
        tokyo = wgs84.latlon(TOKYO_LAT, TOKYO_LON)
        
        earth = self.eph['earth']
        sun = self.eph['sun']
        
        # 東京からの観測位置を使用
        tokyo_observer = earth + tokyo
        s = tokyo_observer.at(time).observe(sun).apparent()
        lat, lon, dist = s.ecliptic_latlon()
        return lon.degrees

    def find_solar_longitude_time(self, target_longitude, t0, t1, tolerance=0.0001):
        """
        二分探索で指定された黄経になる時刻を見つける（世界時ベース）
        """
        earth = self.eph['earth']
        sun = self.eph['sun']
        
        while True:
            tmid = self.ts.tt_jd((t0.tt + t1.tt) / 2)
            
            # 黄経の計算
            s = earth.at(tmid).observe(sun).apparent()
            lat, lon, dist = s.ecliptic_latlon()
            current_longitude = lon.degrees
            
            if abs(current_longitude - target_longitude) < tolerance:
                return tmid
            
            if current_longitude < target_longitude:
                t0 = tmid
            else:
                t1 = tmid
    
    def calculate_shanichi(self, year: int) -> List[Dict]:
        """社日 (春分・秋分の最も近い戊の日) を計算"""
        solar_terms = self.solar_terms_calculator.calculate_solar_terms(year)
        shanichi_dates = []
        
        # DailyKanshiCalculatorのインスタンスを作成
        kanshi_calc = DailyKanshiCalculator()
        
        def find_nearest_tsuchinoe(base_date):
            # 前後15日を探索
            search_range = range(-15, 16)
            tsuchinoe_dates = []
            
            for days in search_range:
                target_date = base_date.date() + timedelta(days=days)
                kanshi = kanshi_calc.get_kanshi(target_date)
                
                # 戊（つちのえ）の日を見つける（十干インデックスが4の日）
                if kanshi['jikkan']['index'] == 4:
                    tsuchinoe_dates.append(target_date)
            
            # 基準日に最も近い戊の日を選択
            if tsuchinoe_dates:
                return min(tsuchinoe_dates, 
                          key=lambda d: abs((d - base_date.date()).days))
            return None
        
        for term in solar_terms:
            if term['term_name'] in ['春分', '秋分']:
                season = '春' if term['term_name'] == '春分' else '秋'
                shanichi_date = find_nearest_tsuchinoe(term['datetime_jst'])
                
                if shanichi_date:
                    # datetime型に変換（タイムゾーン付き）
                    shanichi_datetime = datetime.combine(
                        shanichi_date, 
                        datetime.min.time()
                    ).replace(tzinfo=self.tz_tokyo)
                    
                    shanichi_dates.append({
                        '識別子': f"{year}{season}社日",
                        '年月日時刻': shanichi_datetime.strftime('%Y/%m/%d %H:%M:%S'),
                        'datetime_jst': shanichi_datetime
                    })
        
        return shanichi_dates
    
    def calculate_hachijuhachi_ya(self, year: int) -> Dict:
        """八十八夜 (立春から88日目) を計算"""
        solar_terms = self.solar_terms_calculator.calculate_solar_terms(year)
        
        for term in solar_terms:
            if term['term_name'] == '立春':
                base_date = term['datetime_jst']
                hachijuhachi_ya = base_date + timedelta(days=87)
                return {
                    '識別子': f"{year}八十八夜",
                    '年月日時刻': hachijuhachi_ya.strftime('%Y/%m/%d %H:%M:%S'),
                    'datetime_jst': hachijuhachi_ya
                }
    
    def calculate_nihyaku_toka(self, year: int) -> Dict:
        """二百十日 (立春から210日目) を計算"""
        solar_terms = self.solar_terms_calculator.calculate_solar_terms(year)
        
        for term in solar_terms:
            if term['term_name'] == '立春':
                nihyaku_toka = term['datetime_jst'] + timedelta(days=209)
                return {
                    '識別子': f"{year}二百十日",
                    '年月日時刻': nihyaku_toka.strftime('%Y/%m/%d %H:%M:%S'),
                    'datetime_jst': nihyaku_toka
                }

    def get_all_seasonal_days(self, year: int) -> List[Dict]:
        """その年の全ての雑節を取得"""
        seasonal_days = []
        
        # 各雑節の計算を実行
        seasonal_days.append(self.calculate_setsubun(year))
        seasonal_days.extend(self.calculate_higan(year))
        seasonal_days.extend(self.calculate_shanichi(year))
        seasonal_days.append(self.calculate_hachijuhachi_ya(year))
        seasonal_days.append(self.calculate_nihyaku_toka(year))
        
        # None を除外し、日付でソート
        seasonal_days = [day for day in seasonal_days if day is not None]
        seasonal_days.sort(key=lambda x: x['datetime_jst'])
        
        return seasonal_days
    
    def export_to_excel(self, start_year: int, end_year: int, filename: str = 'seasonal_days.xlsx'):
        """雑節データをExcelファイルとして出力"""
        all_days = []
        for year in range(start_year, end_year + 1):
            all_days.extend(self.get_all_seasonal_days(year))
        
        df = pd.DataFrame([{
            '識別子': day['識別子'],
            '年月日時刻': day['年月日時刻']
        } for day in all_days])
        
        df.to_excel(filename, index=False)
        print(f"雑節データを {filename} に出力しました。")
# [前のコードと同じなので省略...]

    def print_seasonal_days(self, start_year: int, end_year: int):
        """雑節データを見やすく出力"""
        all_days = []
        for year in range(start_year, end_year + 1):
            all_days.extend(self.get_all_seasonal_days(year))
        
        # 日付でソート
        all_days.sort(key=lambda x: x['datetime_jst'])
        
        # ヘッダー出力
        print("\n=== 日本の伝統的な暦の節日 ===")
        print(f"期間: {start_year}年 ～ {end_year}年")
        print("=" * 50)
        print(f"{'識別子':<20} {'年月日時刻':<30}")
        print("-" * 50)
        
        # データ出力
        for day in all_days:
            print(f"{day['識別子']:<20} {day['年月日時刻']:<30}")
        
        print("-" * 50)
        print(f"総計: {len(all_days)}件の節日\n")

    def find_solar_longitude_time(self, target_longitude, t0, t1, tolerance=0.0001):
        """
        二分探索で指定された黄経になる時刻を見つける
        
        Args:
            target_longitude (float): 目標の黄経（度）
            t0 (Time): 探索開始時刻
            t1 (Time): 探索終了時刻
            tolerance (float): 許容誤差（度）
        
        Returns:
            Time: 指定された黄経になる時刻
        """
        earth = self.eph['earth']
        sun = self.eph['sun']
        
        while True:
            # TTでの中間時刻を計算
            tmid = self.ts.tt_jd((t0.tt + t1.tt) / 2)
            
            # 中間時刻での黄経を計算
            s = earth.at(tmid).observe(sun).apparent()
            lat, lon, dist = s.ecliptic_latlon()
            current_longitude = lon.degrees
            
            # 目標との差が許容誤差以内なら終了
            if abs(current_longitude - target_longitude) < tolerance:
                # 最後の補正計算を行う
                final_time = tmid
                return final_time
            
            # 探索範囲を半分に絞る
            if current_longitude < target_longitude:
                t0 = tmid
            else:
                t1 = tmid

# デバッグ出力用
if __name__ == "__main__":
    calculator = JapaneseSeasonalDaysCalculator()

    # 二十四節気の表示を追加
    for year in range(2024, 2026):
        solar_terms = calculator.solar_terms_calculator.calculate_solar_terms(year)
        print(f"\n=== {year}年の二十四節気 ===")
        print(f"{'節気名':<10} {'年月日時刻':<30}")
        print("-" * 50)
        for term in solar_terms:
            print(f"{term['term_name']:<10} {term['datetime_jst'].strftime('%Y/%m/%d %H:%M:%S'):<30}")
        print("-" * 50)
        print(f"総計: {len(solar_terms)}件の節気\n")

    calculator.print_seasonal_days(2024, 2025)