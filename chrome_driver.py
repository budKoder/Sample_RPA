from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import sys

from message_box import showMbox,MB_OK,ICON_STOP
from logging_pack import logger


def close_chrome(chrome:webdriver):
    """
    exit chromedriver
    :param chrome: chromedriver instance
    """
    chrome.quit()


def generate_chrome()->webdriver:
    """
    generate chrome driver instance
    :return: chrome driver instance
    """
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        options.add_experimental_option("detach", True)
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option('prefs', {
            'download.prompt_for_download': False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })
        # automatically download chrome driver from web
        chrome = webdriver.Chrome(options=options,service=Service(ChromeDriverManager().install()))

        return chrome
    except Exception as e:
        msg = f"Failed to create Chrome Instance."
        logger.critical(msg)
        showMbox(msg, "Critical", MB_OK | ICON_STOP)
        sys.exit()