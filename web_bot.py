from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
import sys

from message_box import showMbox,MB_OK,ICON_STOP,ICON_EXLAIM
from chrome_driver import close_chrome
from library import read_single_tag
from logging_pack import logger


def frame_switch(driver,xpath=''):
    """
    switch web frame
    :param driver: chrome driver instance
    :param xpath: to switch frame's xpath. If xpath is not given, switch frame to default
    """
    try:
        if xpath == '':
            driver.switch_to.default_content()
        else:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            driver.switch_to.frame(driver.find_element(By.XPATH, xpath))
    except Exception as e:
        msg = f"Failed to switch the web frame. Details - {e}\n"
        logger.critical(msg)
        showMbox("Failed to switch the web frame","Critical",MB_OK|ICON_STOP)
        close_chrome(driver)
        sys.exit()


def connect_to_url(driver):
    """
    connect to user set url
    :param driver: chrome driver instance
    """
    try:
        url = read_single_tag("url")
        driver.get(url)
    except Exception as e:
        msg = f"Failed to connect to url. Details - {e}\n"
        logger.critical(msg)
        showMbox("Failed to connect to url", "Critical", MB_OK|ICON_STOP)
        close_chrome(driver)
        sys.exit()


def move_tab_to_target(driver):
    """
    move to target page
    :param driver: chrome driver instance
    """
    try:
        # select tab
        time.sleep(2)
        tab = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="gnbStart"]/ul/li[4]/a')))
        tab.click()
        # select menu
        time.sleep(2)
        menu = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="gnbStart"]/ul/li[4]/div/ul/li[2]/div/a')))
        menu.click()
    except Exception as e:
        msg = f"Failed to move page. Details - {e}\n"
        logger.critical(msg)
        showMbox("Failed to move page", "Critical", MB_OK|ICON_STOP)
        close_chrome(driver)
        sys.exit()


def select_data_and_search(driver):
    """
    set user set search option
    :param driver: chrome driver instance
    """
    frame_switch(driver,'//*[@id="bankIframe"]')

    try:
        time.sleep(2)
        # set search date
        search_date = read_single_tag("search_date")
        date_field = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="tmpInqStrDt"]')))
        date_field.clear()
        date_field.send_keys(search_date)

        # set search_type
        # search_type = 0 : 최초, 1 : 현재, 2 : 특정회차
        # search_type_dtl = 고시회차
        search_type = read_single_tag("search_type")
        search_type_dtl = read_single_tag("search_type_dtl")

        # when date type to select not matched, show alert and exit
        if not (isinstance(search_type,int) and isinstance(search_type_dtl,int)):
            msg = "Invalid search type. Search type(dtl) must be integer.\nCheck the settings and retry.\n"
            logger.debug(msg)
            showMbox(msg,"Warning",MB_OK|ICON_EXLAIM)
            close_chrome(driver)
            sys.exit()

        time.sleep(2)
        if search_type == 0:
            driver.find_element(By.XPATH,'//*[@id="inqFrm"]/table/tbody/tr[3]/td/div/label[1]/span').click()
        elif search_type == 1:
            driver.find_element(By.XPATH,'//*[@id="Area1"]/span').click()
        elif search_type == 2:
            driver.find_element(By.XPATH,'//*[@id="inqFrm"]/table/tbody/tr[3]/td/div/label[3]/span').click()

            search_type_dtl = read_single_tag("search_type_dtl")
            driver.find_element(By.XPATH,'//*[@id="pbldSqn"]').send_keys(search_type_dtl)

        # search
        driver.find_element(By.XPATH, '//*[@id="HANA_CONTENTS_DIV"]/div[2]/a').click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="searchContentDiv"]/div[1]/a[2]')))
    except Exception as e:
        msg = f"Failed to set search options. Details - {e}\n"
        logger.critical(msg)
        showMbox("Failed to set search options","Critical",MB_OK|ICON_STOP)
        close_chrome(driver)
        sys.exit()


def download_excel(driver):
    """
    download searched data's excel file'
    :param driver: chrome driver instance
    """
    try:
        # change frame to searched frame
        frame_switch(driver)
        time.sleep(1)
        frame_switch(driver, '//*[@id="bankIframe"]')

        download_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="searchContentDiv"]/div[1]/a[2]')))
        time.sleep(2)

        # scroll down to show download button
        # useless. just to show people that bot is working...
        driver.execute_script("arguments[0].scrollIntoView();", download_btn)
        download_btn.click()
    except Exception as e:
        msg = f"Failed to download the file. Details - {e}\n"
        logger.critical(msg)
        showMbox("Failed to download the file", "Critical", MB_OK|ICON_STOP)
        close_chrome(driver)
        sys.exit()