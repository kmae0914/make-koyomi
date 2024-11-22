from typing import Dict, List, Union
import pandas as pd
from datetime import datetime, date
import os

class CalendarExporter:
    """暦データのエクスポート機能を提供するクラス"""
    
    @staticmethod
    def _remove_timezone(dt):
        """タイムゾーン情報を除去"""
        if isinstance(dt, datetime) and dt.tzinfo is not None:
            return dt.replace(tzinfo=None)
        return dt
    
    @staticmethod
    def _flatten_date(data: Dict, prefix: str = '') -> Dict:
        """ネストされた辞書を平坦化"""
        flattened = {}
        for key, value in data.items():
            if isinstance(value, dict):
                nested = CalendarExporter._flatten_date(value, f"{prefix}{key}_")
                flattened.update(nested)
            else:
                # datetime型の場合はタイムゾーン情報を除去
                if isinstance(value, (datetime, date)):
                    value = CalendarExporter._remove_timezone(value)
                flattened[f"{prefix}{key}"] = value
        return flattened

    @staticmethod
    def create_year_summary_df(year_info: Dict) -> pd.DataFrame:
        """年間サマリーをDataFrameに変換"""
        flattened = CalendarExporter._flatten_date(year_info)
        return pd.DataFrame([flattened])

    @staticmethod
    def create_daily_events_df(daily_events: Dict) -> Dict[str, pd.DataFrame]:
        """日単位イベントをDataFrameに変換"""
        dfs = {}
        
        # 日付を日付のみの形式に変換する関数
        def format_date(d):
            if isinstance(d, datetime):
                return d.date()
            return d

        # 特定干支
        if '特定干支' in daily_events:
            eto_data = []
            for eto_type, dates in daily_events['特定干支'].items():
                for d in dates:
                    eto_data.append({
                        '日付': format_date(d),  # 時間情報を削除
                        '干支': eto_type
                    })
            if eto_data:
                dfs['特定干支'] = pd.DataFrame(sorted(eto_data, key=lambda x: x['日付']))
        
        # 祝日
        if '祝日' in daily_events:
            holiday_data = [
                {
                    '日付': format_date(event['日付']),  # 時間情報を削除
                    '名称': event['名称'],
                    '種類': event['種類']
                }
                for event in daily_events['祝日']
            ]
            dfs['祝日'] = pd.DataFrame(sorted(holiday_data, key=lambda x: x['日付']))
        
        # 土用入り
        if '土用' in daily_events:
            # 土用の期間（４期）の日付データを整形
            doyo_data = []
            # 順序を維持するために固定のリストを使用
            seasons = ['春土用', '夏土用', '秋土用', '冬土用']
            
            # 既存の土用データを季節ごとにマッピング
            doyo_dates = {}
            for event in daily_events['土用']:
                doyo_dates[event['季節']] = event['日付']
            
            # 定義された順序で土用データを生成
            for season in seasons:
                if season in doyo_dates:
                    doyo_data.append({
                        '季節': season,
                        '日付': doyo_dates[season]
                    })
            
            dfs['土用'] = pd.DataFrame(doyo_data)

        # 八専
        if '八専' in daily_events:
            hassen_periods = []
            current_period = None
            sorted_events = sorted(daily_events['八専'], key=lambda x: x['日付'])
            
            for event in sorted_events:
                if (current_period is None or 
                    (event['日付'] - current_period['最終日']).days > 1):
                    if current_period is not None:
                        hassen_periods.append(current_period['開始日'])
                    current_period = {
                        '開始日': event['日付'],
                        '最終日': event['日付']
                    }
                else:
                    current_period['最終日'] = event['日付']
            
            if current_period is not None:
                hassen_periods.append(current_period['開始日'])
            
            dfs['八専'] = pd.DataFrame({"八専開始日": hassen_periods})
        
        # 日曜日
        if '日曜日' in daily_events:
            # 月ごとにグループ化して日付のリストを作成
            sunday_data = []
            current_data = {}
            
            for event in sorted(daily_events['日曜日'], key=lambda x: x['日付']):
                month = event['月']
                day = event['日']
                
                if month not in current_data:
                    current_data[month] = []
                current_data[month].append(str(day))
            
            # 1月から12月までのデータを作成（日曜日がない月も含む）
            for month in range(1, 13):
                days_list = current_data.get(month, [])
                sunday_data.append({
                    '月': f"{month}月",
                    '日にち': ', '.join(days_list) if days_list else '-'
                })
            
            dfs['日曜日'] = pd.DataFrame(sunday_data)
        
        return dfs
    
    @staticmethod
    def create_monthly_events_df(monthly_info: List[Dict]) -> Dict[str, pd.DataFrame]:
        """月別イベントをDataFrameに変換"""
        all_sekki = []
        all_zassetsu = []
        processed_events = set()  # 期間イベントの重複を防ぐ
        
        # 月情報のDataFrame作成
        monthly_data = []
        for month, month_data in enumerate(monthly_info, 1):
            monthly_data.append({
                '月': f"{month}月",
                '月初干支': month_data['月情報']['月初干支'],
                '大小': month_data['月情報']['大小']
            })
        
        dfs = {}
        # 月情報のDataFrameを追加
        dfs['月情報'] = pd.DataFrame(monthly_data)
        
        # 既存の節気・雑節の処理
        for month_data in monthly_info:
            # 節気
            for sekki in month_data.get('節気', []):
                dt = CalendarExporter._remove_timezone(sekki['datetime_jst'])
                all_sekki.append({
                    '日付': dt,
                    '節気名': sekki['イベント名'],
                })
            
            # 雑節
            for zassetsu in month_data.get('雑節', []):
                dt = CalendarExporter._remove_timezone(zassetsu['datetime_jst'])
                event_id = f"{zassetsu['識別子']}"
                
                # 期間イベントの処理（彼岸など）
                if '彼岸' in event_id:
                    base_id = event_id.replace('1日目', '').replace('2日目', '').\
                                     replace('3日目', '').replace('4日目', '').\
                                     replace('5日目', '').replace('6日目', '').\
                                     replace('7日目', '')
                    if base_id not in processed_events:
                        processed_events.add(base_id)
                        all_zassetsu.append({
                            '日付': dt,
                            '雑節名': zassetsu['イベント名'].replace('1日目', '').strip(),
                        })
                # 社日の処理
                elif '社日' in event_id:
                    all_zassetsu.append({
                        '日付': dt,
                        '雑節名': zassetsu['イベント名'],
                    })
                # その他の雑節
                else:
                    all_zassetsu.append({
                        '日付': dt,
                        '雑節名': zassetsu['イベント名'],
                    })
        
        if all_sekki:
            dfs['節気'] = pd.DataFrame(all_sekki)
        if all_zassetsu:
            # 日付でソート
            all_zassetsu.sort(key=lambda x: x['日付'])
            dfs['雑節'] = pd.DataFrame(all_zassetsu)
        
        return dfs

class CalendarFileExporter:
    """暦データのファイル出力を管理するクラス"""
    
    def __init__(self, output_dir: str = 'output'):
        """
        Parameters:
            output_dir (str): 出力ディレクトリ
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.exporter = CalendarExporter()
    
    def _save_excel(self, dfs: Dict[str, pd.DataFrame], filename: str):
        """DataFrameをExcelファイルとして保存"""
        with pd.ExcelWriter(
            os.path.join(self.output_dir, filename),
            engine='openpyxl',
            datetime_format='yyyy/mm/dd'
        ) as writer:
            for sheet_name, df in dfs.items():
                if not df.empty:
                    df_formatted = df.copy()
                    
                    # 日付列の処理（日曜日と土用以外のシート）
                    if sheet_name not in ['日曜日'] and '日付' in df.columns:
                        df_formatted['日付'] = pd.to_datetime(df['日付']).dt.date
                    
                    # DataFrameをExcelに書き出し
                    df_formatted.to_excel(writer, sheet_name=sheet_name, index=False)
                    
                    # ワークシートの取得
                    worksheet = writer.sheets[sheet_name]
                    
                    # 列幅の自動調整
                    for column in worksheet.columns:
                        max_length = 0
                        column = list(column)
                        for cell in column:
                            try:
                                if len(str(cell.value)) > max_length:
                                    max_length = len(str(cell.value))
                            except:
                                pass
                        adjusted_width = (max_length + 2) * 1.2
                        worksheet.column_dimensions[column[0].column_letter].width = adjusted_width
                    
                    # 日付列のフォーマット（土用シートの場合）
                    if sheet_name == '土用':
                        for row in worksheet.iter_rows(min_row=2):  # ヘッダーを除く
                            date_cell = row[1]  # '日付'列は2列目
                            if date_cell.value:
                                date_cell.number_format = 'yyyy/mm/dd'

    
    def _save_csv(self, dfs: Dict[str, pd.DataFrame], base_filename: str):
        """DataFrameをCSVファイルとして保存"""
        for name, df in dfs.items():
            if not df.empty:
                df_formatted = df.copy()
                # 日付列を文字列形式で保存
                if '日付' in df.columns:
                    df_formatted['日付'] = pd.to_datetime(df['日付']).dt.strftime('%Y/%m/%d')
                if '開始日' in df.columns:
                    df_formatted['開始日'] = pd.to_datetime(df['開始日']).dt.strftime('%Y/%m/%d')
                if '終了日' in df.columns:
                    df_formatted['終了日'] = pd.to_datetime(df['終了日']).dt.strftime('%Y/%m/%d')
                
                filename = f"{base_filename}_{name}.csv"
                df_formatted.to_csv(os.path.join(self.output_dir, filename), index=False)


    def export_year_data(self, 
                        year_info: Dict,
                        daily_events: Dict,
                        monthly_info: List[Dict],
                        year: int,
                        format: str = 'excel'):
        """年間データをファイルに出力"""
        # DataFrameの作成
        dfs = {
            '年情報': self.exporter.create_year_summary_df(year_info)
        }
        
        # 日単位イベントの追加
        daily_dfs = self.exporter.create_daily_events_df(daily_events)
        dfs.update(daily_dfs)
        
        # 月別イベントの追加
        monthly_dfs = self.exporter.create_monthly_events_df(monthly_info)
        dfs.update(monthly_dfs)
        
        # ファイル出力
        if format.lower() == 'excel':
            self._save_excel(dfs, f"calendar_{year}.xlsx")
            print(f"Excel ファイルを保存しました: {os.path.join(self.output_dir, f'calendar_{year}.xlsx')}")
        else:
            self._save_csv(dfs, f"calendar_{year}")
            print(f"CSV ファイルを保存しました: {self.output_dir} ディレクトリ")