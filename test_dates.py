from koyomi.seasonal.sekki import SolarTerms
from koyomi.seasonal.tsuyu import Tsuyuiri
from koyomi.seasonal.hange import Hangesho
from koyomi.seasonal.doyo import Doyo
from koyomi.seasonal.zassetsu import Zassetsu
from koyomi.seasonal.tanabata import Tanabata
from datetime import datetime

def print_dates(year):
    print(f"\n=== {year}年の暦の確認 ===")
    
    # 二十四節気
    sekki = SolarTerms()
    terms = sekki.calculate(year)
    
    print("\n二十四節気:")
    print(f"{'節気名':<10} {'年月日時刻'}")
    print("-" * 50)
    for term in terms:
        print(f"{term['イベント名']:<10} {term['年月日時刻']}")
    
    # 雑節
    print("\n雑節:")
    print(f"{'イベント名':<10} {'年月日時刻'}")
    print("-" * 50)
    
    # 土用
    doyo = Doyo()
    doyo_results = doyo.calculate(year)
    for result in doyo_results:
        print(f"{result['イベント名']:<10} {result['年月日時刻']}")
    
    # 雑節（節分、彼岸、八十八夜、二百十日）
    zassetsu = Zassetsu()
    zassetsu_results = zassetsu.calculate(year)
    for result in zassetsu_results:
        print(f"{result['イベント名']:<10} {result['年月日時刻']}")
    
    # 七夕
    tanabata = Tanabata()
    tanabata_results = tanabata.calculate(year)
    for result in tanabata_results:
        print(f"{result['イベント名']:<10} {result['年月日時刻']}")
    
    # 入梅
    tsuyu = Tsuyuiri()
    tsuyu_result = tsuyu.calculate(year)
    print(f"{tsuyu_result['イベント名']:<10} {tsuyu_result['年月日時刻']}")
    
    # 半夏生
    hange = Hangesho()
    hange_result = hange.calculate(year)
    print(f"{hange_result['イベント名']:<10} {hange_result['年月日時刻']}")

if __name__ == "__main__":
    # 2024年と2025年の日付を確認
    for year in [2024, 2025]:
        print_dates(year)