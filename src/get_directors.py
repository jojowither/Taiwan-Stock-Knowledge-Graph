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
    executive_df = pd.DataFrame(columns=['name', 'code', 'job', 'stock_num'])

    # 永豐金證券網頁
    # 董監事經理人及大股東
    stock_web_url = 'https://www.sinotrade.com.tw/Stock/Stock_3_1/Stock_3_1_6_2?ticker='

    for twstock_code in tqdm(all_twstock_code, desc='Process', colour='#00af91'):
        if all_twstock[twstock_code].type == '股票':
            url = f'{stock_web_url}{twstock_code}'
            driver.get(url)
            driver.switch_to.frame('SysJustIFRAME')
            xpath = '//*[@id="SysJustIFRAMEDIV"]/table/tbody/tr[2]/td[2]/center/table/tbody/tr[1]/td/table'
            tbl = driver.find_element_by_xpath(
                xpath).get_attribute('outerHTML')
            df = pd.read_html(tbl)[0]
            size = df.shape

            for idx in range(2, size[0]-1):
                row = df.iloc[idx]
                job = row[0]
                name = row[1]
                stock_num = row[2]

                executive_dict = {'name': name,
                                  'code': twstock_code,
                                  'job': job,
                                  'stock_num': stock_num}
                executive_df = executive_df.append(
                    executive_dict, ignore_index=True)

    executive_df.to_csv('../data/executive_prep.csv', encoding='utf-8', index=False)
    print('\nDone')


if __name__ == "__main__":
    main()
