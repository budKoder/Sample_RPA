import datetime
import webbrowser
import winreg
import shutil
import time
import sys
import os

from message_box import showMbox,MB_OK,ICON_STOP
from library import read_single_tag
from logging_pack import logger


def get_download_path():
    """
    get chrome driver's default download path.
    :return: default download path for linux or windows
    """
    if os.name == 'nt':
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            location = winreg.QueryValueEx(key, downloads_guid)[0]
        return location
    else:
        return os.path.join(os.path.expanduser('~'), 'downloads')


def is_download_finished():
    """
    check if download finished in time
    :return: return True if download finished in time. else, return False
    """
    path = get_download_path()

    seconds = 0
    dl_wait = True
    while dl_wait and seconds < 30:
        time.sleep(1)
        dl_wait = False
        for fname in os.listdir(path):
            if fname.endswith('.crdownload'):
                dl_wait = True
            else:
                return True
        seconds += 1
    return False


def get_download_file_name():
    """
    get currently downloaded full file name(file path + file name) and file name(file name only)
    :return: downloaded file name. If there is no file downloaded, return none
    """
    download_path = get_download_path()
    if len(os.listdir(download_path)) > 0:
        full_filename = max([download_path+"\\"+f for f in os.listdir(download_path)], key= os.path.getctime)
        filename = os.path.basename(full_filename)
        ext = os.path.splitext(full_filename)[1]
    else:
        full_filename = None
        filename = None
        ext = None
    return full_filename, filename, ext


def popup_folders(path):
    """
    popup folder window
    :param path: to open folder path
    """
    webbrowser.open(path)


def move_file():
    """
    move file to user set folder
    while moving, show folders to confirm file movement to user.(useless...)
    """
    try:
        default_path = get_download_path()
        webbrowser.open(default_path)
        time.sleep(5)

        full_filename, file_name, ext = get_download_file_name()
        move_path = os.path.realpath(read_single_tag("move_path"))

        now = datetime.datetime.now().strftime("%Y%m%d")
        move_name = read_single_tag("move_name") + "_" + now + ext
        full_move_path = os.path.join(move_path,move_name)
        shutil.move(full_filename,full_move_path)

        webbrowser.open(move_path)
        time.sleep(5)

        return full_move_path
    except Exception as e:
        msg = f"Failed to move file. Details - {e}\n"
        logger.critical(msg)
        showMbox("Failed to move file","Critical",MB_OK|ICON_STOP)
        sys.exit()