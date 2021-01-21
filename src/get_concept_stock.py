import re
import time

import pandas as pd
import twstock
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from tqdm import tqdm

CHROMEDRIVER_PATH = '/usr/local/bin/chromedriver'
CONCEPT_STCOK_URL = 'https://pchome.megatime.com.tw/group/sto3'  # pchome股市概念股

ALL_CONCEPT_XPATH = '//*[@id="bttb"]/table/tbody/tr/td/div[2]'
SELECT_XPATH = '//*[@id="bttb"]/div[5]/select'
INDIV_CONCEPT_XPATH = '//*[@id="bttb"]/table[3]'


def init_driver():
    # initialize driver
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument("--disable-notifications")
    driver = webdriver.Chrome(CHROMEDRIVER_PATH, chrome_options=options)
    driver.get(CONCEPT_STCOK_URL)
    return driver


def get_all_concept(driver):
    concepts = driver.find_element_by_xpath(ALL_CONCEPT_XPATH)
    concepts = concepts.text.split('\n')
    return concepts


def click_concept_button(concept_idx, driver):
    concepts_xpath = f'{ALL_CONCEPT_XPATH}/span[{concept_idx}]/a'
    cur_url = driver.current_url
    # wait the driver to click button
    while True:
        driver.find_element_by_xpath(concepts_xpath).click()
        if driver.current_url != cur_url:
            break
    return concepts_xpath


def get_all_subpages(driver, concepts_xpath):
    select = Select(driver.find_element_by_xpath(SELECT_XPATH))
    subpages = [opt.text for opt in select.options]
    return select, subpages


def get_stock_table(driver):
    indiv_concept_table = driver.find_element_by_xpath(
        INDIV_CONCEPT_XPATH).get_attribute('outerHTML')
    indiv_concept_table = pd.read_html(indiv_concept_table)[0]
    stocks = indiv_concept_table['股票▲'].tolist()
    return stocks


def construct_concept_df(stocks, concept, concept_df):
    for stock in stocks:
        stock_code = filter_code(stock)
        concept_dict = {'concept': concept,
                        'stock': stock_code}
        concept_df = concept_df.append(concept_dict, ignore_index=True)
    return concept_df


def filter_code(stock):
    pattern = r"\(\d+\w*\)"
    stock_code = re.search(pattern, stock).group()
    stock_code = re.sub(r'[\(\)]', "", stock_code)
    return stock_code


def main():
    driver = init_driver()
    concepts = get_all_concept(driver)
    concept_df = pd.DataFrame(columns=['concept', 'stock'])

    for concept_idx, concept in enumerate(tqdm(concepts, desc='Process',
                                               colour='#00af91'), start=1):

        concepts_xpath = click_concept_button(concept_idx, driver)
        select, subpages = get_all_subpages(driver, concepts_xpath)
        for page_idx, opt in enumerate(subpages):
            if page_idx != 0:
                select.select_by_value(opt)
                select = Select(driver.find_element_by_xpath(SELECT_XPATH))
                # time.sleep(5)

            stocks = get_stock_table(driver)
            concept_df = construct_concept_df(stocks, concept, concept_df)

        # driver.execute_script("window.history.go(-1)")
        driver.get(CONCEPT_STCOK_URL)

    concept_df.to_csv('../data/concept_prep.csv', encoding='utf-8', index=False)
    print('\nDone')


if __name__ == "__main__":
    main()
