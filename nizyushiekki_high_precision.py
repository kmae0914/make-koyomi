#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ephem
import math
import pytz
from datetime import datetime, timedelta
from common import SEKKI_DEFINITIONS, SekkiResult

class HighPrecisionCalculator:
    """高精度な二十四節気計算クラス"""
    
    def __init__(self):
        self.jst = pytz.timezone('Asia/Tokyo')
        
    def _calculate_orbital_elements(self, jd):
        """軌道要素の計算"""
        T = (jd - 2451545.0) / 36525.0
        
        e = 0.016708634 - 0.000042037 * T - 0.0000001267 * T * T
        pi = 102.93735 + 1.71946 * T + 0.00046 * T * T
        i = 23.43929111 - 0.013004167 * T - 0.000000164 * T * T
        omega = 174.873174 - 0.241347 * T + 0.00004 * T * T
        
        return e, pi, i, omega

    def _calculate_nutation(self, jd):
        """章動の計算"""
        T = (jd - 2451545.0) / 36525.0
        
        M = 357.52910 + 35999.05030 * T - 0.0001559 * T * T
        eps = 23.43929111 - 0.013004167 * T
        
        delta_psi = -17.20 * math.sin(math.radians(M)) / 3600.0
        delta_eps = 9.20 * math.cos(math.radians(M)) / 3600.0
        
        return delta_psi, delta_eps

    def _calculate_aberration(self, jd):
        """光行差の計算"""
        T = (jd - 2451545.0) / 36525.0
        v = 0.01720209895
        c = 173.14463098
        kappa = v / c * 180.0 / math.pi
        
        return kappa

    def _get_precise_solar_longitude(self, date):
        """高精度な太陽黄経の計算"""
        jd = date + 2415020
        
        sun = ephem.Sun()
        observer = ephem.Observer()
        observer.date = date
        observer.pressure = 0
        sun.compute(observer)
        longitude = math.degrees(sun.hlong)
        
        e, pi, i, omega = self._calculate_orbital_elements(jd)
        delta_psi, delta_eps = self._calculate_nutation(jd)
        longitude += delta_psi
        
        aberration = self._calculate_aberration(jd)
        longitude -= aberration * math.cos(math.radians(longitude - pi))
        
        return (longitude + 180) % 360

    def _find_precise_date(self, year, target_longitude, debug=False):
        """高精度な日時の探索"""
        # 探索範囲を設定（前年8月から翌年4月まで）
        start = ephem.Date(f'{year-1}/08/1')
        end = ephem.Date(f'{year+1}/04/30')
        
        if debug:
            print(f"\n探索開始 - 節気: {target_longitude}°")
            print(f"探索期間: {ephem.Date(start).datetime()} - {ephem.Date(end).datetime()}")
        
        # 3日間隔で粗い探索を行い、候補を見つける
        candidates = []
        current = start
        while current <= end:
            longitude = self._get_precise_solar_longitude(current)
            diff = abs((longitude - target_longitude + 180) % 360 - 180)
            
            if diff < 2:  # 2度以内の候補を全て記録
                candidates.append((current, diff))
                if debug:
                    print(f"候補発見: {ephem.Date(current).datetime()} 黄経: {longitude:.4f}° 差: {diff:.4f}°")
            
            current = ephem.Date(current + 3)  # 3日進める
        
        if not candidates:
            if debug:
                print("候補が見つかりませんでした")
            return None
        
        # 各候補について詳細探索を行う
        best_dates = []
        for candidate_date, _ in candidates:
            # 詳細探索（1秒単位）
            start = ephem.Date(candidate_date - 3)  # 前後3日
            end = ephem.Date(candidate_date + 3)
            best_date = None
            min_diff = 360
            
            while (end - start) > ephem.second:
                mid = ephem.Date((start + end) / 2)
                longitude = self._get_precise_solar_longitude(mid)
                diff = abs((longitude - target_longitude + 180) % 360 - 180)
                
                if diff < min_diff:
                    min_diff = diff
                    best_date = mid
                    
                    if debug and diff < 0.01:
                        print(f"精密解発見: {ephem.Date(mid).datetime()} 黄経: {longitude:.6f}° 差: {diff:.6f}°")
                
                if ((longitude - target_longitude + 180) % 360 - 180) < 0:
                    start = mid
                else:
                    end = mid
            
            if best_date:
                best_dates.append(best_date)
        
        return best_dates

    def _to_jst(self, date):
        """UTC日時を日本時間に変換"""
        dt = ephem.Date(date).datetime()
        utc = pytz.utc.localize(dt)
        return utc.astimezone(self.jst)

    def _is_target_year(self, dt, year):
        """指定された年に属する日付かどうかを判定"""
        # 1月の場合は前年の結果として扱う
        if dt.month == 1:
            return dt.year == year + 1
        # 12月の場合は当年の結果として扱う
        elif dt.month == 12:
            return dt.year == year
        # その他の月は年が一致する必要がある
        else:
            return dt.year == year

    def calculate_sekki(self, year):
        """二十四節気を計算"""
        results = []
        
        # 二分二至の日付を取得
        major_dates = {
            0: ephem.next_vernal_equinox(str(year)),      # 春分
            90: ephem.next_summer_solstice(str(year)),    # 夏至
            180: ephem.next_autumn_equinox(str(year)),    # 秋分
            270: ephem.next_winter_solstice(str(year))    # 冬至
        }
        
        print(f"\n{year}年の二十四節気を計算中...")
        
        for sekki in SEKKI_DEFINITIONS:
            try:
                # 二分二至の場合は既知の日付を使用
                if sekki.longitude in major_dates:
                    dates = [major_dates[sekki.longitude]]
                    method = "二分二至専用関数"
                else:
                    # すべての節気でデバッグ出力を無効化
                    dates = self._find_precise_date(year, sekki.longitude, False)
                    method = "高精度計算"
                
                if dates:
                    target_year_found = False
                    for date in dates:
                        jst_dt = self._to_jst(date)
                        
                        # 年の判定
                        if self._is_target_year(jst_dt, year):
                            results.append(SekkiResult(
                                sekki.name,
                                jst_dt,
                                sekki.longitude,
                                method
                            ))
                            print(f"計算完了: {sekki.name} ({sekki.longitude}°)")
                            target_year_found = True
                            break  # 対象年の節気が見つかったら次の節気へ
                        else:
                            print(f"対象年外の候補: {sekki.name} - {jst_dt.strftime('%Y年%m月%d日')}")
                    
                    if not target_year_found:
                        print(f"\n警告: {sekki.name} ({sekki.longitude}°) の対象年の日時が見つかりませんでした")
                else:
                    print(f"\n警告: {sekki.name} ({sekki.longitude}°) の日時が見つかりませんでした")
                
            except Exception as e:
                print(f"\nエラー: {sekki.name} ({sekki.longitude}°) の計算中に問題が発生")
                print(f"詳細: {str(e)}")
        
        # 結果を日付順にソート
        sorted_results = sorted(results, key=lambda x: x.date)
        
        # 結果の検証
        print(f"\n計算された節気の数: {len(sorted_results)}/24")
        if len(sorted_results) < 24:
            print("\n欠落している節気:")
            found_longitudes = {result.longitude for result in sorted_results}
            for sekki in SEKKI_DEFINITIONS:
                if sekki.longitude not in found_longitudes:
                    print(f"- {sekki.name} ({sekki.longitude}°)")
        
        return sorted_results

def main():
    try:
        year = datetime.now().year
        print(f"{year}年の二十四節気（高精度計算）")
        print("-" * 50)
        
        calculator = HighPrecisionCalculator()
        results = calculator.calculate_sekki(year)
        
        if results:
            print("\n計算結果:")
            for result in results:
                print(f"{result.name}: {result.date.strftime('%Y年%m月%d日 %H:%M:%S')} "
                      f"(黄経: {result.longitude}°) [{result.method}]")
        else:
            print("\n計算に失敗しました。")
            
    except Exception as e:
        print(f"\nエラーが発生しました: {e}")
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    main()
