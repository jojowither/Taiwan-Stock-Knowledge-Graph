import pandas as pd
import twstock


def main():
    all_twstock = twstock.codes
    all_twstock_code = list(all_twstock.keys())
    all_twstock_type = []
    all_twstock_name = []
    all_twstock_group = []
    all_twstock_market = []

    for twstock_code in all_twstock_code:
        all_twstock_type.append(all_twstock[twstock_code].type)
        all_twstock_name.append(all_twstock[twstock_code].name)
        all_twstock_group.append(all_twstock[twstock_code].group)
        all_twstock_market.append(all_twstock[twstock_code].market)

    stock_df = pd.DataFrame({'code': all_twstock_code,
                            'type': all_twstock_type,
                            'name': all_twstock_name,
                            'group': all_twstock_group,
                            'market': all_twstock_market,})

    stock_df.to_csv('../data/tw_stock_info_prep.csv', encoding='utf-8', index=False)


if __name__ == "__main__":
    main()
