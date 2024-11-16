#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ephem
import math
import pytz
from datetime import datetime, timedelta
from common import SEKKI_DEFINITIONS, SekkiResult
import pandas as pd
import os

class HighPrecisionCalculator:
    """高精度な二十四節気計算クラス"""
    
    def __init__(self):
        self.jst = pytz.timezone('Asia/Tokyo')

    def _calculate_delta_t(self, year, month):
        """より正確なΔT（TT-UTC）の計算"""
        y = year + (month - 0.5) / 12

        if 2005 <= year <= 2050:
            t = y - 2000
            return 62.92 + 0.32217 * t + 0.005589 * t * t
        elif 1986 <= year <= 2005:
            t = y - 2000
            return 63.86 + 0.3345 * t - 0.060374 * t * t + 0.0017275 * t * t * t + 0.000651814 * t * t * t * t + 0.00002373599 * t * t * t * t * t
        else:
            return 69.184  # デフォルト値

    def _calculate_vsop87_correction(self, jd):
        """VSOP87理論による補正値の計算"""
        T = (jd - 2451545.0) / 36525.0
        
        # 主要な周期項による補正
        correction = (
            + 0.00134 * math.cos(math.radians(1.7535 + 6283.0758 * T))
            + 0.00154 * math.cos(math.radians(2.1934 - 6283.0758 * T))
            + 0.00200 * math.cos(math.radians(3.7375 + 12566.1517 * T))
            + 0.00179 * math.cos(math.radians(1.7959 + 6283.0758 * T))
        )
        
        return correction

    def _calculate_nutation(self, jd):
        """章動の計算（IAU 2000B model）"""
        T = (jd - 2451545.0) / 36525.0
        
        # 平均黄道傾斜角（度）
        epsilon = 23.43929111 - 0.013004167 * T - 0.000000164 * T * T + 0.000000503 * T * T * T
        
        # 月の平均軌道要素（度）
        Omega = 125.04452 - 1934.136261 * T + 0.0020708 * T * T + T * T * T / 450000
        L = 280.4665 + 36000.7698 * T
        Lp = 218.3165 + 481267.8813 * T
        
        # 黄経における章動（度）
        delta_psi = (-17.20 * math.sin(math.radians(Omega))
                    - 1.32 * math.sin(math.radians(2 * L))
                    - 0.23 * math.sin(math.radians(2 * Lp))
                    + 0.21 * math.sin(math.radians(2 * Omega))) / 3600.0
        
        return delta_psi

    def _calculate_aberration(self, jd):
        """光行差の計算"""
        T = (jd - 2451545.0) / 36525.0
        
        # 地球軌道の離心率
        e = 0.016708634 - 0.000042037 * T - 0.0000001267 * T * T
        
        # 近日点黄経（度）
        pi = 102.93735 + 1.71946 * T + 0.00046 * T * T
        
        # 光行差定数（度）
        kappa = 20.49552 / 3600.0
        
        # 平均黄経（度）
        L = 280.46646 + 36000.76983 * T + 0.0003032 * T * T
        
        # 光行差の計算
        aberration = -kappa * math.cos(math.radians(L - pi))
        
        return aberration

    def _get_precise_solar_longitude(self, date):
        """高精度な太陽黄経の計算"""
        try:
            # 基本の太陽黄経計算（PyEphem）
            sun = ephem.Sun()
            observer = ephem.Observer()
            observer.date = date
            observer.pressure = 0
            sun.compute(observer)
            base_longitude = math.degrees(sun.hlong)
            
            # ユリウス日の計算
            jd = ephem.Date(date) + 2415020
            
            # VSOP87による補正
            vsop87_correction = self._calculate_vsop87_correction(jd)
            
            # 章動の補正
            nutation = self._calculate_nutation(jd)
            
            # 光行差の補正
            aberration = self._calculate_aberration(jd)
            
            # 補正の適用
            longitude = (base_longitude + vsop87_correction + nutation + aberration) % 360
            
            return (longitude + 180) % 360
            
        except Exception as e:
            print(f"太陽黄経計算でエラー: {str(e)}")
            raise

    def _find_precise_date(self, year, target_longitude, debug=False):
        """高精度な日時の探索"""
        # 探索範囲を設定（前年12月から当年12月まで）
        start = ephem.Date(f'{year-1}/12/1')
        end = ephem.Date(f'{year}/12/31')
        
        if debug:
            print(f"\n探索開始 - 節気: {target_longitude}°")
        
        # 1日間隔で粗い探索を行い、候補を見つける
        candidates = []
        current = start
        while current <= end:
            try:
                longitude = self._get_precise_solar_longitude(current)
                diff = abs((longitude - target_longitude + 180) % 360 - 180)
                
                if diff < 1:  # 1度以内の候補を全て記録
                    candidates.append((current, diff))
                    if debug:
                        print(f"候補発見: {ephem.Date(current).datetime()} 黄経: {longitude:.4f}° 差: {diff:.4f}°")
                
                current = ephem.Date(current + 1)  # 1日進める
            except Exception as e:
                print(f"探索中にエラー: {str(e)}")
                current = ephem.Date(current + 1)  # エラーが発生しても次に進む
        
        if not candidates:
            return None
        
        # 各候補について詳細探索を行う
        best_dates = []
        for candidate_date, _ in candidates:
            try:
                # 詳細探索（1分単位）
                start = ephem.Date(candidate_date - 1)
                end = ephem.Date(candidate_date + 1)
                best_date = None
                min_diff = 360
                
                step = ephem.minute  # 1分単位で探索
                current = start
                while current <= end:
                    longitude = self._get_precise_solar_longitude(current)
                    diff = abs((longitude - target_longitude + 180) % 360 - 180)
                    
                    if diff < min_diff:
                        min_diff = diff
                        best_date = current
                    
                    current = ephem.Date(current + step)
                
                if best_date and min_diff < 0.00001:
                    best_dates.append(best_date)
                    
            except Exception as e:
                print(f"詳細探索中にエラー: {str(e)}")
                continue
        
        return best_dates

    def _to_jst(self, date):
        """UTC日時を日本時間に変換"""
        dt = ephem.Date(date).datetime()
        utc = pytz.utc.localize(dt)
        return utc.astimezone(self.jst)

    def _is_target_year(self, dt, year):
        """指定された年に属する日付かどうかを判定"""
        if dt.month == 1 and hasattr(self, '_current_longitude') and self._current_longitude in [285, 300]:
            return dt.year == year
        elif dt.month == 1:
            return dt.year == year + 1
        elif dt.month == 12:
            return dt.year == year
        else:
            return dt.year == year

    def calculate_sekki(self, year):
        """二十四節気を計算"""
        results = []
        print(f"\n{year}年の二十四節気を計算中...")
        
        for sekki in SEKKI_DEFINITIONS:
            try:
                self._current_longitude = sekki.longitude
                dates = self._find_precise_date(year, sekki.longitude, False)
                
                if dates:
                    target_year_found = False
                    for date in dates:
                        jst_dt = self._to_jst(date)
                        
                        if self._is_target_year(jst_dt, year):
                            results.append(SekkiResult(
                                sekki.name,
                                jst_dt,
                                sekki.longitude,
                                "VSOP87補正計算"
                            ))
                            print(f"計算完了: {sekki.name} ({sekki.longitude}°)")
                            target_year_found = True
                            break
                
                    if not target_year_found:
                        print(f"\n警告: {sekki.name} の対象年の日時が見つかりませんでした")
                else:
                    print(f"\n警告: {sekki.name} の日時が見つかりませんでした")
                
            except Exception as e:
                print(f"\nエラー: {sekki.name} の計算中に問題が発生")
                print(f"詳細: {str(e)}")
            
            finally:
                if hasattr(self, '_current_longitude'):
                    delattr(self, '_current_longitude')
        
        return sorted(results, key=lambda x: x.date)

def main():
    try:
        current_year = datetime.now().year
        all_results = []

        print(f"{current_year}年の二十四節気（VSOP87補正計算）")
        print("-" * 50)
        
        calculator = HighPrecisionCalculator()
        results = calculator.calculate_sekki(current_year)
        
        if results:
            for result in results:
                date_str = result.date.strftime('%Y/%m/%d %H:%M:%S')
                identifier = f"{current_year}{result.name}"
                
                all_results.append({
                    '年月日時刻': date_str,
                    '識別子': identifier
                })
                print(result)
            
            # Excelファイルが開かれていないか確認
            try:
                output_file = 'sekki_results.xlsx'
                if os.path.exists(output_file):
                    os.remove(output_file)
                
                df = pd.DataFrame(all_results)
                df.to_excel(output_file, index=False)
                print(f"\n計算結果が '{output_file}' に保存されました。")
            except PermissionError:
                print("\n警告: Excelファイルが他のプログラムで開かれているため、保存できませんでした。")
                print("ファイルを閉じてから再度実行してください。")
        else:
            print(f"\n{current_year}年の計算に失敗しました。")
            
    except Exception as e:
        print(f"\nエラーが発生しました: {e}")
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    main()
