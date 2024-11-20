from skyfield import almanac_east_asia as almanac_ea
from skyfield import almanac
from skyfield.api import load
from datetime import datetime, timedelta, timezone
import pytz
from nizyushiekki import SolarTermsCalculator

class TraditionalTanabataCalculator:
    def __init__(self):
        self.ts = load.timescale()
        self.eph = load('de421.bsp')
        self.tz_jst = pytz.timezone('Asia/Tokyo')
        self.solar_terms_calc = SolarTermsCalculator()
    
    def _find_syosyo(self, year):
        """指定された年の処暑の日時を求める"""
        terms = self.solar_terms_calc.calculate_solar_terms(year)
        
        for term in terms:
            if term['term_name'] == '処暑':
                dt_utc = term['datetime_jst'].astimezone(timezone.utc)
                return self.ts.from_datetime(dt_utc)
        
        return None
    
    def _find_all_new_moons_around_syosyo(self, syosyo_time):
        """処暑を含む日までの2ヶ月前からの新月をすべて取得"""
        syosyo_dt = syosyo_time.utc_datetime()
        # 処暑の2ヶ月前から処暑の日の終わりまでを探索範囲とする
        t0 = self.ts.utc(syosyo_dt.year, syosyo_dt.month - 2, 1)
        next_day = syosyo_dt + timedelta(days=1)
        t1 = self.ts.from_datetime(next_day)
        
        t, y = almanac.find_discrete(t0, t1, almanac.moon_phases(self.eph))
        
        # 新月のみをフィルタリング
        new_moons = [(ti, yi) for ti, yi in zip(t, y) if yi == 0]
        return [nm[0] for nm in new_moons]  # Time オブジェクトのリストを返す
    
    def _find_nearest_new_moon(self, syosyo_time, new_moons):
        """処暑に最も近い新月を見つける（処暑の日までで）"""
        syosyo_dt = syosyo_time.astimezone(self.tz_jst).date()
        nearest_new_moon = None
        min_diff = float('inf')
        
        # デバッグ情報を収集
        debug_info = []
        for new_moon in new_moons:
            new_moon_dt = new_moon.astimezone(self.tz_jst).date()
            # 日付の差を計算
            time_diff = (syosyo_dt - new_moon_dt).days
            
            # 時間差のデバッグ情報も保持（より詳細な情報として）
            detailed_diff = syosyo_time.tt - new_moon.tt
            
            debug_info.append({
                'new_moon': new_moon,
                'time_diff_days': detailed_diff,
                'date_diff_days': time_diff
            })
            
            # 新月が処暑と同じ日か前の日の場合のみ対象とする
            if time_diff >= 0 and time_diff < min_diff:
                min_diff = time_diff
                nearest_new_moon = new_moon
        
        return nearest_new_moon, debug_info
    
    def calculate_tanabata(self, year):
        """伝統的七夕の日付を計算"""
        # 処暑の日時を求める
        syosyo = self._find_syosyo(year)
        if syosyo is None:
            raise ValueError(f"Could not find Syosyo for year {year}")
        
        # 処暑までの新月を全て取得
        new_moons = self._find_all_new_moons_around_syosyo(syosyo)
        if not new_moons:
            raise ValueError(f"Could not find new moons for year {year}")
        
        # 処暑に最も近い（前までの）新月を見つける
        nearest_new_moon, debug_info = self._find_nearest_new_moon(syosyo, new_moons)
        if nearest_new_moon is None:
            raise ValueError(f"Could not find appropriate New Moon for year {year}")
        
        # 新月の日を1日目として数え、7日目を計算
        new_moon_date = nearest_new_moon.astimezone(self.tz_jst)
        tanabata_date = (new_moon_date + timedelta(days=6)).date()
        
        return tanabata_date, syosyo, nearest_new_moon, debug_info
    
    def get_tanabata_info(self, year):
        """七夕の詳細情報を取得"""
        tanabata_date, syosyo, new_moon, debug_info = self.calculate_tanabata(year)
        
        # デバッグ情報を整形
        debug_details = []
        for info in debug_info:
            nm = info['new_moon'].astimezone(self.tz_jst)
            time_diff = info['time_diff_days']
            date_diff = info['date_diff_days']
            debug_details.append(
                f"新月: {nm.strftime('%Y-%m-%d %H:%M:%S')} "
                f"(処暑まで: {time_diff:+.2f}日, 日付差: {date_diff}日)"
            )
        
        return {
            '年': year,
            '処暑': syosyo.astimezone(self.tz_jst).strftime('%Y-%m-%d %H:%M:%S %Z'),
            '選択された新月': new_moon.astimezone(self.tz_jst).strftime('%Y-%m-%d %H:%M:%S %Z'),
            '七夕': tanabata_date.strftime('%Y-%m-%d'),
            '新月からの日数': 7,
            'デバッグ情報': debug_details
        }

def main():
    calculator = TraditionalTanabataCalculator()
    
    # 複数年の計算例
    print("2024-2026年の伝統的七夕:\n")
    for year in range(2024, 2027):
        info = calculator.get_tanabata_info(year)
        print(f"=== {year}年 ===")
        print(f"処暑: {info['処暑']}")
        print(f"選択された新月: {info['選択された新月']}")
        print(f"七夕（新月から{info['新月からの日数']}日目）: {info['七夕']}")
        print("\nデバッグ情報（処暑との時間差）:")
        for debug_line in info['デバッグ情報']:
            print(debug_line)
        print()

if __name__ == "__main__":
    main()