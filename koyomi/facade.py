from typing import Dict, List, Optional
from datetime import date, datetime
from .cycles.eto_year import YearEto
from .cycles.eto_daily import DailyEto
from .cycles.eto_month import MonthEto
from .cycles.kusei import Kusei
from .cycles.specific_eto import SpecificEto
from .cycles.nattoin import Nattoin
from .cycles.hassen import Hassen
from .cycles.sundays import Sundays
from .cycles.holiday import Holiday
from .seasonal.sekki import SolarTerms
from .seasonal.zassetsu import Zassetsu
from .seasonal.tanabata import Tanabata
from .seasonal.doyo import Doyo
from .utils.export import CalendarFileExporter
from .seasonal.tsuyu import Tsuyuiri
from .seasonal.hange import Hangesho
from .seasonal.tanabata import Tanabata

class KoyomiFacade:
    """暦計算機能のファサードクラス"""
    
    def __init__(self):
        """各計算機能のインスタンスを初期化"""
        # 干支関連
        self.year_eto = YearEto()
        self.daily_eto = DailyEto()
        self.month_eto = MonthEto()
        self.specific_eto = SpecificEto()
        
        # 暦注関連
        self.kusei = Kusei()
        self.nattoin = Nattoin()
        self.hassen = Hassen()
        
        # 季節関連
        self.sekki = SolarTerms()
        self.zassetsu = Zassetsu()
        self.tanabata = Tanabata()
        
        # その他
        self.holiday = Holiday()
        self.sundays = Sundays()
        
        # 土用計算機の初期化を追加
        self.doyo_calculator = Doyo()
    
    def get_year_info(self, year: int) -> Dict:
        """年の基本情報を取得"""
        return {
            '干支': self.year_eto.calculate(year),
            '九星': self.kusei.calculate(year),
            '納音': self.nattoin.calculate(year)
        }
    
    def get_month_info(self, year: int, month: int) -> Dict:
        """月の情報を取得"""
        import calendar
        from datetime import date
        
        # 月の日数を取得
        _, days_in_month = calendar.monthrange(year, month)
        # 月初めの日の干支を取得
        first_day = date(year, month, 1)
        first_day_eto = self.daily_eto.calculate_single_day(first_day)
        
        return {
            '干支': self.month_eto.calculate(year, month),
            '節気': [term for term in self.sekki.calculate(year) 
                    if term['datetime_jst'].month == month],
            '雑節': [event for event in self.zassetsu.calculate(year)
                    if event['datetime_jst'].month == month],
            '月情報': {
                '大小': '大' if days_in_month == 31 else '小',
                '月初干支': first_day_eto['干支']
            }
        }
    
    def get_daily_events(self, year: int) -> Dict:
        """日単位のイベントを取得"""
        events = {}
        
        # 土用の計算と追加
        doyo_events = self.doyo_calculator.calculate(year)
        if doyo_events:
            events['土用'] = []
            for event in doyo_events:
                events['土用'].append({
                    '季節': event['イベント名'],
                    '日付': event['datetime_jst'].date()
                })
        
        # 八専の計算
        hassen_events = self.hassen.calculate_year(year)
        if hassen_events:
            events['八専'] = hassen_events
            # 八専と間日の日数を計算
            hassen_count = len([e for e in hassen_events if e['種類'] == '八専'])
            mabi_count = len([e for e in hassen_events if e['種類'] == '間日'])
            
            # 統計情報を追加
            events['統計'] = {
                '八専日数': hassen_count,
                '間日数': mabi_count,
                # ... 他の統計情報 ...
            }
        
        holidays = self.holiday.calculate(year)
        specific_eto = self.specific_eto.calculate_year(year)
        sundays = self.sundays.calculate_year(year)
        
        # eventsディクショナリに全てのイベントを追加
        events.update({
            '特定干支': specific_eto,
            '祝日': holidays,
            '日曜日': sundays,
        })
        
        # 入梅
        tsuyuiri = Tsuyuiri()
        events['入梅'] = [tsuyuiri.calculate(year)]
        
        # 半夏生
        hangesho = Hangesho()
        events['半夏生'] = [hangesho.calculate(year)]
        
        # 七夕（新暦・伝統的）
        tanabata = Tanabata()
        events['七夕'] = tanabata.calculate(year)
        
        return events  # 土用を含む全てのイベントを返す
    
    def format_year_summary(self, year: int, include_stats: bool = True) -> str:
        """
        年間情報のサマリーを整形して出力
        
        Parameters:
            year (int): 対象年
            include_stats (bool): 統計情報を含めるかどうか
        """
        year_info = self.get_year_info(year)
        daily_events = self.get_daily_events(year) if include_stats else None

        output = [
            f"\n{year}年の暦情報",
            "=" * 50,
            f"干支: {year_info['干支']['干支']}（{year_info['干支']['読み']}）",
            f"九星: {year_info['九星']['漢字']}（{year_info['九星']['読み']}）",
            f"納音: {year_info['納音']['納音']['漢字']}（{year_info['納音']['納音']['読み']}）"
        ]
        
        if include_stats:
            stats = daily_events['統計']
            output.extend([
                "",
                "統計情報:",
                f"・八専: {stats['八専日数']}日（うち間日: {stats['間日数']}日）",
                f"・特定干支: {stats['特定干支日数']}日",
                f"・祝日: {stats['祝日数']}日"
            ])
        
        output.extend([
            "",
            "利用可能な情報:",
            "- 月別情報（get_month_info）",
            "  ・月の干支",
            "  ・二十四節気",
            "  ・雑節",
            "",
            "- 日別情報（get_daily_events）",
            "  ・八専と間日",
            "  ・特定干支の日（甲子、庚申、己巳）",
            "  ・祝日",
            "",
            "- その他",
            "  ・七夕（新暦・伝統的）",
            "  ・日曜日"
        ])
        
        return "\n".join(output)
    
    def format_month_events(self, year: int, month: int) -> str:
        """月のイベントを整形して出力"""
        info = self.get_month_info(year, month)
        
        output = [
            f"\n{year}年{month}月の暦情報",
            "=" * 50,
            "\n【節気】"
        ]
        
        for term in info['節気']:
            output.append(f"- {term['イベント名']}: {term['年月日時刻']}")
        
        if info['雑節']:
            output.append("\n【雑節】")
            for event in info['雑節']:
                output.append(f"- {event['イベント名']}: {event['年月日時刻']}")
        
        return "\n".join(output)
    
    def export_year_data(self, year: int, format: str = 'excel', output_dir: str = 'output'):
        """
        指定された年の暦データをファイルに出力
        
        Parameters:
            year (int): 対象年
            format (str): 出力形式 ('excel' or 'csv')
            output_dir (str): 出力ディレクトリ
        """
        # 全データの取得
        year_info = self.get_year_info(year)
        daily_events = self.get_daily_events(year)
        monthly_info = [self.get_month_info(year, month) for month in range(1, 13)]
        
        # エクスポート実行
        exporter = CalendarFileExporter(output_dir)
        exporter.export_year_data(
            year_info,
            daily_events,
            monthly_info,
            year,
            format
        )
