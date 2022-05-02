import json
import sys

from message_box import showMbox,MB_OK,ICON_STOP
from logging_pack import logger


def read_json():
    """
    read config.json
    :return: json object
    """
    try:
        with open('config.json','r') as f:
            json_data = json.load(f)
        return json_data
    except Exception as e:
        msg = f"Cannot Read config.json file. Details - {e}\n"
        logger.critical(msg)
        showMbox("Cannot read config.json","Critical",MB_OK|ICON_STOP)
        sys.exit()


def read_single_tag(tag):
    """
    read single tag json data
    :param tag: tag name to read
    :return: tag information
    """
    try:
        data = read_json()
        return data[tag]
    except Exception as e:
        msg = f"Failed to read json file. Details - {e}\n"
        logger.critical(msg)
        showMbox("Failed to read json file","Critical",MB_OK|ICON_STOP)
        sys.exit()


def read_double_tag(tag, sub_tag):
    """
    read double tag json data
    :param tag: upper tag name
    :param sub_tag: sub tag name
    :return: tag information
    """
    try:
        data = read_json()
        return data[tag][sub_tag]
    except Exception as e:
        msg = f"Failed to read json file. Details - {e}\n"
        logger.critical(msg)
        showMbox("Failed to read json file", "Critical", MB_OK|ICON_STOP)
        sys.exit()