import pandas as pd
import twstock
from selenium import webdriver
from tqdm import tqdm
import re


def main():
    # initialize driver
    chromedriver = '/usr/local/bin/chromedriver'
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument("--disable-notifications")
    driver = webdriver.Chrome(chromedriver, chrome_options=options)

    # create empty df
    concept_df = pd.DataFrame(columns=['concept', 'stock'])

    # pchome股市概念股
    concept_stock_url = 'https://pchome.megatime.com.tw/group/sto3'
    driver.get(concept_stock_url)
    all_concept_xpath = '//*[@id="bttb"]/table/tbody/tr/td/div[2]'
    concepts = driver.find_element_by_xpath(all_concept_xpath)
    concepts = concepts.text.split('\n')

    for idx, concept in enumerate(concepts, start=1):
        buttom_xpath = f'{all_concept_xpath}/span[{idx}]/a'
        driver.find_element_by_xpath(buttom_xpath).click()
        indiv_concept_xpath = '//*[@id="bttb"]/table[3]'
        indiv_concept_table = driver.find_element_by_xpath(indiv_concept_xpath).get_attribute('outerHTML')
        indiv_concept_table = pd.read_html(indiv_concept_table)[0]
        stocks = indiv_concept_table['股票▲'].tolist()

        pattern = r"\(\d+\)"
        for stock in stocks:
            stock_code = re.search(pattern, stock).group()
            stock_code = re.sub(r'[\(\)]', "", stock_code)
            concept_dict = {'concept': concept,
                            'stock': stock_code}
            concept_df = concept_df.append(concept_dict, ignore_index=True)
        
        # 還要處理有下一頁的問題
        # 檢查哪裡吃太多記憶體，修正
        breakpoint()

        driver.execute_script("window.history.go(-1)")


        breakpoint()

if __name__ == "__main__":
    main()