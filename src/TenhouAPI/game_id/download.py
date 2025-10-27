""" Game id tools that download from tenhou.
"""


# types


from typing import (
    Union,
)

int_or_str = Union[int, str]


# libs


import os.path
from time import sleep

from ..util.download import download

from ..config.tenhou_url import TenhouUrlConfig


""" Download game id processes
"""



""" Download functions """


def download_game_id_list(
        year: int_or_str,
        month: int_or_str,
        day: int_or_str,
        hour: int_or_str,
        sleep_time: sleep = 5,
        url_config: TenhouUrlConfig = TenhouUrlConfig()
) -> Union[bytes, None]:
    """
    Download game id list from Tenhou.
    :param year: Year to download.
    :param month: Month to download.
    :param day: Day to download.
    :param hour: Hour to download.
    :param sleep_time: Sleep time.
    :param url_config: URL config.
    :return: Downloaded game list bytes.
    """

    """ generate file name"""

    file_name = url_config.id_file_name_format.format(
        key=url_config.table_key, year=year, month=month, day=day, hour=hour
    )

    # check length
    if not len(file_name) == url_config.file_name_length:
        raise TypeError(
            "Invalid format of arguments. Not match length of file_name."
        )

    """ Download file """

    file_url = url_config.generate_id_list_url(url_config, file_name)
    print("Downloading: {url}".format(url=file_url))

    headers = {"User-Agent": "Mozilla/5.0"}

    result = download(file_url, headers=headers)

    sleep(sleep_time)

    return result


""" Unzip bytes and save file """


def save_file_from_zipped_bytes(
        zipped_bytes: bytes,
        save_file_path: str,
        url_config: TenhouUrlConfig = TenhouUrlConfig(),
) -> str:
    """
    Save file of tenhou from by zipped bytes data.
    :param zipped_bytes: zipped bytes data.
    :param save_file_path: File name to save.
    :param url_config: URL config.
    :return: Saved html file path.
    """
    # generate zip file path
    zip_file_path = url_config.zip_tool.add_extension(save_file_path)

    print("Building game ids html file: {path}".format(path=save_file_path))

    # save gz
    with open(zip_file_path, "wb") as f_gz:
        f_gz.write(zipped_bytes)
        ...

    # unzip and save
    url_config.zip_tool.unzip(zip_file_path, save_file_path)

    # rm gz
    os.remove(zip_file_path)

    return save_file_path
