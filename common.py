#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Sekki:
    """節気の基本クラス"""
    def __init__(self, name, longitude):
        self.name = name
        self.longitude = longitude

class SekkiResult:
    """節気の計算結果を格納するクラス"""
    def __init__(self, name, date, longitude, method):
        self.name = name
        self.date = date
        self.longitude = longitude
        self.method = method  # 計算方法の説明

    def __str__(self):
        return f"{self.name}: {self.date.strftime('%Y年%m月%d日 %H:%M:%S')} (黄経: {self.longitude}°) [{self.method}]"

SEKKI_DEFINITIONS = [
    Sekki("立春", 315), Sekki("雨水", 330), Sekki("啓蟄", 345),
    Sekki("春分", 0), Sekki("清明", 15), Sekki("穀雨", 30),
    Sekki("立夏", 45), Sekki("小満", 60), Sekki("芒種", 75),
    Sekki("夏至", 90), Sekki("小暑", 105), Sekki("大暑", 120),
    Sekki("立秋", 135), Sekki("処暑", 150), Sekki("白露", 165),
    Sekki("秋分", 180), Sekki("寒露", 195), Sekki("霜降", 210),
    Sekki("立冬", 225), Sekki("小雪", 240), Sekki("大雪", 255),
    Sekki("冬至", 270), Sekki("小寒", 285), Sekki("大寒", 300)
]
