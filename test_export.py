from koyomi.facade import KoyomiFacade
from koyomi.utils.export import CalendarExporter
from koyomi.seasonal.doyo import Doyo

def test_export():
    koyomi = KoyomiFacade()
    
    print("Excelファイルに出力中...")
    koyomi.export_year_data(2025, format='excel')
    
    print("出力完了！")
    print("ファイルは output ディレクトリに保存されました。")

if __name__ == "__main__":
    test_export()