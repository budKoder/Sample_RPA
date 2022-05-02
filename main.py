import time

from web_bot import connect_to_url, move_tab_to_target, select_data_and_search, download_excel
from file_control import is_download_finished, move_file
from chrome_driver import generate_chrome, close_chrome


if __name__ == "__main__":
    driver = generate_chrome()
    # download excel file from web
    connect_to_url(driver)
    move_tab_to_target(driver)
    select_data_and_search(driver)
    download_excel(driver)
    if is_download_finished():
        time.sleep(3)
        close_chrome(driver)

    # move downloaded file in local environment
    move_name = move_file()

