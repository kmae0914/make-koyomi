from koyomi.facade import KoyomiFacade

def main():
    koyomi = KoyomiFacade()

    # 基本情報の表示（統計情報付き）
    print(koyomi.format_year_summary(2024))

    # 統計情報なしで表示
    print(koyomi.format_year_summary(2024, include_stats=False))

    # 月別イベントの表示
    print(koyomi.format_month_events(2024, 1))

if __name__ == "__main__":
    main()