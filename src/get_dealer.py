import pandas as pd
import twstock
from selenium import webdriver
from tqdm import tqdm


def main():
    # get stock code
    all_twstock = twstock.codes
    all_twstock_code = list(all_twstock.keys())

    # initialize driver
    chromedriver = '/usr/local/bin/chromedriver'
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome(chromedriver, chrome_options=options)

    # create empty df
    dealer_df = pd.DataFrame(columns=['dealer', 'code', 'BuySell'])

    # 永豐金證券網頁
    # 主力進出
    stock_web_url = 'https://www.sinotrade.com.tw/Stock/Stock_3_1/Stock_3_1_6_7?ticker='

    for twstock_code in tqdm(all_twstock_code, desc='Process', colour='#00af91'):
        if all_twstock[twstock_code].type == '股票':
            url = f'{stock_web_url}{twstock_code}'
            driver.get(url)
            driver.switch_to.frame('SysJustIFRAME')

            xpath = '//*[@id="oMainTable"]'
            try:
                tbl = driver.find_element_by_xpath(
                    xpath).get_attribute('outerHTML')
            except:
                continue
            df = pd.read_html(tbl)[0]

            start_tr_idx = 8
            end_tr_idx = 22
            buy_dealer_idx, buy_idx = 0, 3
            sell_dealer_idx, sell_idx = 5, 8
            for idx in range(start_tr_idx, end_tr_idx+1):
                series = df.iloc[idx]
                if pd.notnull(series[0]) and '合計買超' in series[0]:
                    break

                if pd.notnull(series[buy_dealer_idx]):
                    buy_dealer = series[buy_dealer_idx]
                    buy_amount = int(series[buy_idx])
                    buy_dict = {'dealer': buy_dealer,
                            'code': twstock_code,
                            'BuySell': buy_amount}
                    dealer_df = dealer_df.append(buy_dict, ignore_index=True)
                if pd.notnull(series[sell_dealer_idx]):
                    sell_dealer = series[sell_dealer_idx]
                    sell_amount = int(series[sell_idx])
                    sell_dict = {'dealer': sell_dealer,
                            'code': twstock_code,
                            'BuySell': -sell_amount}
                    dealer_df = dealer_df.append(sell_dict, ignore_index=True)

    dealer_df.to_csv('../data/dealer_prep.csv', encoding='utf-8', index=False)
    print('\nDone')

if __name__=='__main__':
    main()
