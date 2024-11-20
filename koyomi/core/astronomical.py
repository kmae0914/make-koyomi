from skyfield.api import load
from skyfield.framelib import ecliptic_frame
import pytz
from datetime import datetime, timezone

class AstronomicalCalculator:
    """天文計算の基本機能を提供するクラス"""
    def __init__(self, delta_t=None):
        """
        Parameters:
            delta_t (float, optional): ΔT値（秒）。設定しない場合はskyfieldのデフォルト値を使用。
        """
        self.ts = load.timescale() if delta_t is None else load.timescale(delta_t=delta_t)
        self.eph = load('de421.bsp')
        self.sun = self.eph['sun']
        self.earth = self.eph['earth']
        self.tz_jst = pytz.timezone('Asia/Tokyo')

    def get_solar_longitude(self, time):
        """
        指定された時刻の太陽黄経を計算
        
        Parameters:
            time: Skyfield Time object
        
        Returns:
            float: 太陽黄経（度）
        """
        earth_at_t = self.earth.at(time)
        sun_at_t = earth_at_t.observe(self.sun)
        _, lon, _ = sun_at_t.apparent().frame_latlon(ecliptic_frame)
        return lon.degrees

    def find_solar_term_date(self, target_longitude, start_time, end_time, tolerance=0.001):
        """
        指定された黄経になる日時を二分探索で特定
        
        Parameters:
            target_longitude (float): 目標の黄経（度）
            start_time: Skyfield Time object（探索開始時刻）
            end_time: Skyfield Time object（探索終了時刻）
            tolerance (float): 許容誤差（度）
        
        Returns:
            Skyfield Time object: 指定された黄経になる時刻
        """
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

    def to_jst_datetime(self, time):
        """
        Skyfield Time objectを日本時間のdatetimeに変換
        
        Parameters:
            time: Skyfield Time object
        
        Returns:
            datetime: 日本時間のdatetime（タイムゾーン付き）
        """
        dt_utc = time.utc_datetime()
        return dt_utc.replace(tzinfo=timezone.utc).astimezone(self.tz_jst)