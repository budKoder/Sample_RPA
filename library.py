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


def update_json(json_data):
    """
    update config.json file
    :param json_data: to update data
    """
    try:
        with open('config.json', 'w+', encoding='UTF8') as make_file:
            json.dump(json_data, make_file, indent='\t')
    except Exception as e:
        msg = f"Failed to update json file. Details - {e}\n"
        logger.critical(msg)
        showMbox("Failed to update json file", "Critical", MB_OK|ICON_STOP)
        sys.exit()


def update_single_tag(tag,val):
    """
    update single tag json data
    :param tag: tag to update
    :param val: value to update
    """
    data = read_json()
    data[tag] = val
    update_json(data)


def update_double_tag(tag,subtag,val):
    """
    update double tag json data
    :param tag: upper tag
    :param subtag: sub tag
    :param val: value to update
    """
    data = read_json()
    data[tag][subtag] = val
    update_json(data)