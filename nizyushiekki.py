#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ephem
from datetime import datetime, timedelta
import math
import pytz

class Sekki:
    def __init__(self, name, longitude):
        self.name = name
        self.longitude = longitude

class NijushiSekki:
    def __init__(self):
        self.sekkis = [
            Sekki("立春", 315), Sekki("雨水", 330), Sekki("啓蟄", 345),
            Sekki("春分", 0), Sekki("清明", 15), Sekki("穀雨", 30),
            Sekki("立夏", 45), Sekki("小満", 60), Sekki("芒種", 75),
            Sekki("夏至", 90), Sekki("小暑", 105), Sekki("大暑", 120),
            Sekki("立秋", 135), Sekki("処暑", 150), Sekki("白露", 165),
            Sekki("秋分", 180), Sekki("寒露", 195), Sekki("霜降", 210),
            Sekki("立冬", 225), Sekki("小雪", 240), Sekki("大雪", 255),
            Sekki("冬至", 270), Sekki("小寒", 285), Sekki("大寒", 300)
        ]
        self.jst = pytz.timezone('Asia/Tokyo')

    def _get_solar_longitude(self, date):
        """太陽黄経を計算（補正済み）"""
        sun = ephem.Sun()
        observer = ephem.Observer()
        observer.date = date
        observer.pressure = 0
        sun.compute(observer)
        return (math.degrees(sun.hlong) + 180) % 360

    def _to_jst(self, date):
        """UTC日時を日本時間に変換"""
        dt = ephem.Date(date).datetime()
        utc = pytz.utc.localize(dt)
        return utc.astimezone(self.jst)

    def _is_near_midnight(self, dt):
        """日付変更線付近かどうかを判定"""
        return (dt.hour == 23 and dt.minute >= 50) or \
               (dt.hour == 0 and dt.minute <= 10)

    def _find_sekki_date_high_precision(self, base_date, target_longitude):
        """高精度な節気の日時計算（1秒単位）"""
        start = ephem.Date(base_date - 1.0/24/6)  # 10分前から
        end = ephem.Date(base_date + 1.0/24/6)    # 10分後まで
        
        best_date = None
        min_diff = 360
        
        # 1秒単位での探索
        current = start
        while current <= end:
            longitude = self._get_solar_longitude(current)
            diff = abs((longitude - target_longitude + 180) % 360 - 180)
            
            if diff < min_diff:
                min_diff = diff
                best_date = current
                
                if diff < 0.00001:  # より厳密な判定
                    break
            
            current = ephem.Date(current + 1.0/24/60/60)  # 1秒進める
        
        return best_date

    def _find_sekki_date(self, year, target_longitude):
        """二分探索で指定された黄経の日時を見つける"""
        # 探索範囲を1年間に設定（前年12月から）
        start = ephem.Date(f'{year-1}/12/1')
        end = ephem.Date(f'{year}/12/31')
        
        # まず1分単位での探索
        while (end - start) > ephem.minute:
            mid = ephem.Date((start + end) / 2)
            longitude = self._get_solar_longitude(mid)
            
            if abs(longitude - target_longitude) < 0.0001:
                # 日付変更線付近かチェック
                jst_dt = self._to_jst(mid)
                if self._is_near_midnight(jst_dt):
                    # 高精度計算
                    return self._find_sekki_date_high_precision(mid, target_longitude)
                return mid
            elif ((longitude - target_longitude + 180) % 360 - 180) < 0:
                start = mid
            else:
                end = mid
        
        # 日付変更線付近かチェック
        jst_dt = self._to_jst(start)
        if self._is_near_midnight(jst_dt):
            # 高精度計算
            return self._find_sekki_date_high_precision(start, target_longitude)
        return start

    def get_sekki_dates(self, year):
        """指定された年の二十四節気を計算"""
        result = []
        
        # 二分二至の日付を取得
        major_dates = {
            0: ephem.next_vernal_equinox(str(year)),      # 春分
            90: ephem.next_summer_solstice(str(year)),    # 夏至
            180: ephem.next_autumn_equinox(str(year)),    # 秋分
            270: ephem.next_winter_solstice(str(year))    # 冬至
        }
        
        for sekki in self.sekkis:
            try:
                # 二分二至の場合は既知の日付を使用
                if sekki.longitude in major_dates:
                    date = major_dates[sekki.longitude]
                else:
                    date = self._find_sekki_date(year, sekki.longitude)
                
                jst_dt = self._to_jst(date)
                
                # 計算された日付が指定された年のものかチェック
                if jst_dt.year == year:
                    result.append({
                        "名前": sekki.name,
                        "日付": jst_dt.strftime("%Y年%m月%d日 %H:%M:%S"),  # 秒まで表示
                        "黄経": f"{sekki.longitude}°",
                        "精度": "高精度" if self._is_near_midnight(jst_dt) else "通常"
                    })
                
            except Exception as e:
                print(f"Error calculating {sekki.name}: {str(e)}")
        
        return sorted(result, key=lambda x: datetime.strptime(x["日付"], "%Y年%m月%d日 %H:%M:%S"))

def main():
    try:
        year = datetime.now().year
        print(f"{year}年の二十四節気")
        print("-" * 50)
        
        calculator = NijushiSekki()
        results = calculator.get_sekki_dates(year)
        
        if results:
            print("\n計算結果:")
            for sekki in results:
                print(f"{sekki['名前']}: {sekki['日付']} (黄経: {sekki['黄経']}) [{sekki['精度']}]")
        else:
            print("\n節気の計算に失敗しました。")
            
    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    main()
