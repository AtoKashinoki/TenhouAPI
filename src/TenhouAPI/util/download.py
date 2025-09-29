""" Download utility module of TenhouAPI.
This file contains processes that download from "Tenhou" .
"""

# types


from typing import (
    Union, List,
)
int_or_str = Union[int, str]


# libs


import os
import re

import gzip
from time import sleep

import urllib.request



""" Download utilities 
"""


""" utilities """


def download(url, headers=None) -> bytes:
    """
    Download file function.
    :param url: File URL to download.
    :param headers: Request headers.
    :return: Downloaded file.
    """
    # request
    req = urllib.request.Request(url, headers=headers)

    # check response
    with urllib.request.urlopen(req) as response:
        if not response.status == 200:
            raise RuntimeError(response.status)
        result: bytes = response.read()

    return result


""" Game ID """


class GameID:
    """ Download game ids processes. """

    """ Class attributes """

    _base_url: str = "http://tenhou.net/sc/raw/dat/"
    @property
    def base_url(self) -> str: return self._base_url

    def gen_file_url(self, file_name: str) -> str: return self._base_url + file_name + self._zip

    _file_name_format: str = "scc{year:04d}{month:02d}{day:02d}{hour:02d}.html"
    @property
    def file_name_format(self) -> str: return self._file_name_format

    _file_name_format_keys: List[str] = ["year", "month", "day", "hour"]
    @property
    def file_name_keys(self) -> List[str]: return self._file_name_format_keys

    @property
    def file_name_length(self) -> int:
        """ Length of file name. """
        const_len = len(re.sub(r"{\w+:\d\dd}", "", self._file_name_format))
        value_lens = re.findall(r":\d\dd}", self._file_name_format)
        value_len = sum(int(value[2:-2]) for value in value_lens)
        return const_len + value_len

    _zip: str = ".gz"
    @property
    def file_name(self) -> str: return self._zip

    def zip_file_name(self, file_name: str) -> str: return file_name + self._zip

    """ Initialize """

    def __init__(self, save_dir: str = os.path.join(".", "dist", "game_ids")) -> None:
        """
        Assign directory that self save downloaded files.
        :param save_dir: Directory to save downloaded files.
        """
        self.__save_dir = save_dir
        return

    """ Instance attributes """

    __save_dir: str
    @property
    def save_dir(self) -> str: return self.__save_dir
    @save_dir.setter
    def save_dir(self, save_dir: str) -> None: self.__save_dir = save_dir

    def gen_save_file_path(self, file_name: str) -> str:
        """
        Generate and return  save file path.
        :param file_name: File name.
        :return: Generated save file path.
        """
        return os.path.join(self.__save_dir, file_name)

    """ Download processes """

    def download_game_list(
            self,
            year: int_or_str,
            month: int_or_str,
            day: int_or_str,
            hour: int_or_str,
            sleep_time: int = 5
    ) -> Union[bytes, None]:
        """
        Download game list from Tenhou.
        :param year: Year to download.
        :param month: Month to download.
        :param day: Day to download.
        :param hour: Hour to download.
        :param sleep_time: Sleep time.
        :return: Downloaded game list.
        """

        """ Generate file name """

        # generate
        file_name = self._file_name_format.format(
            year=year, month=month, day=day, hour=hour
        )

        # check
        if not len(file_name) == self.file_name_length:
            raise TypeError(
                "Invalid format of arguments. Not match length of file_name."
            )

        """ Download file """

        file_url = file_url = self.gen_file_url(file_name)
        print("Downloading: {url}".format(url=file_url))

        headers = {"User-Agent": "Mozilla/5.0"}

        sleep(sleep_time)
        result = download(file_url, headers=headers)

        return result

    """ html build """

    def save_html_file(self, data: bytes, file_name: str) -> str:
        """
        Build and save html file.
        :param data:  Bytes data of gz.
        :param file_name: File name of html file.
        :return: Html file path.
        """

        """ make dist """

        # check exists and make dir
        if not os.path.exists(self.__save_dir):
            os.makedirs(self.__save_dir)
            ...

        """ save file """

        # save file path
        file_path = self.gen_save_file_path(file_name)
        gz_file_path = self.zip_file_name(file_path)

        print("Building game ids html file: {path}".format(path=file_path))

        # save gz
        with open(gz_file_path, "wb") as f_gz:
            f_gz.write(data)
            ...

        # unpack gz and save html
        with gzip.open(gz_file_path, "rb") as f_in:
            with open(file_path, "wb") as f_out:
                f_out.write(f_in.read())
                ...
            ...

        # rm gz
        os.remove(gz_file_path)

        return file_path

    """ Extract game id from html """

    @staticmethod
    def extract_game_ids(file_name: str) -> List[str]:
        """
        Extract game id from html file.
        :param file_name:  File name of html file.
        :return: Extracted game id.
        """

        print("Extracting game id from {html} file.".format(html=file_name))

        # get file contains
        with open(file_name, "r", encoding="utf-8") as f_html:
            content = f_html.read()
            ...

        # extract game ids
        results = re.findall(r"log=\d{10}gm-.{4}-.{4}-.{8}", content)

        return results

    """ Run all processes """

    def run_all_processes(
            self,
            year: int_or_str,
            month: int_or_str,
            day: int_or_str,
            hour: int_or_str,
            sleep_time: int = 5
    ) -> List[str]:
        """
        Run downloading, building html file and extract game id from html file.
        :param year: Year to download.
        :param month: Month to download.
        :param day: Day to download.
        :param hour: Hour to download.
        :param sleep_time: Sleep time.
        :return: Got game id.
        """

        print("Getting game ids from {}/{}/{} {}:00~{}:59.".format(
            year, month, day, hour, hour)
        )

        # download gz file of game id list
        bytes_data = self.download_game_list(year, month, day, hour, sleep_time)

        # build html
        file_name = self._file_name_format.format(
            year=year, month=month, day=day, hour=hour
        )
        saved_file_path = self.save_html_file(bytes_data, file_name)

        # extract ids
        game_ids = self.extract_game_ids(saved_file_path)

        return game_ids

    ...


""" Game log """


class GameLog:
    """ Download game log processes. """

    """ Class attributes """

    _base_url: str = "http://tenhou.net/0/log/?"
    @property
    def base_url(self) -> str: return self._base_url

    def gen_game_log_url(self, game_id: str) -> str:
        """
        Generate game log url.
        :param game_id: Game id to download.
        :return: game log url.
        """
        return self._base_url + game_id.replace("log=", "")

    """ Initialize """

    def __init__(self, save_dir: str=os.path.join(".", "dist", "game_logs")) -> None:
        """
        Assign directory that downloads game log files.
        :param save_dir: Directory path to save game log files.
        """
        self.__save_dir = save_dir
        return

    """ Instance attributes """

    __save_dir: str
    @property
    def save_dir(self) -> str: return self.__save_dir

    def gen_save_file_path(self, file_name: str) -> str:
        """
        Generate and return save file path.
        :param file_name: File name to generate.
        :return: Generated file path.
        """
        return os.path.join(self.__save_dir, file_name)

    """ Download processes """

    def download_game_log(self, game_id: str, sleep_time: int = 5) -> bytes:
        """
        Download game log file.
        :param game_id: Game id to download.
        :param sleep_time: Sleep time.
        :return: Game log file.
        """

        # gen url
        game_log_url = self.gen_game_log_url(game_id)

        # download
        header = {"User-Agent": "Mozilla/5.0"}

        print("Downloading: {url}".format(url=game_log_url))

        sleep(sleep_time)
        result = download(game_log_url, headers=header)

        return result

    """ Save game log file """

    def save_game_log(self, bytes_data: bytes, file_name: str) -> str:
        """
        Build and save game log file.
        :param bytes_data: Bytes data of game log.
        :param file_name: File name to generate.
        :return: Generated file path.
        """

        """ Make dist """

        # check exists and make dir
        if not os.path.exists(self.__save_dir):
            os.makedirs(self.__save_dir)
            ...

        """ Save file """

        # gen file path
        file_path = self.gen_save_file_path(file_name)

        print("Building game log file: {path}".format(path=file_path))

        # make and write game log file.
        with open(file_path, "wb") as f_mjlog:
            f_mjlog.write(bytes_data)
            ...

        return file_path

    """ run all processes """

    def run_all_processes(self, game_id: str, sleep_time: int = 5) -> str:
        """
        Run downloading and building game log file.
        :param game_id: Game id to download.
        :param sleep_time: Sleep time.
        :return: Downloaded file path.
        """

        print("Getting game log from {game_id}".format(game_id=game_id))

        # download game log
        game_log = self.download_game_log(game_id, sleep_time)

        # save game log
        file_path = self.save_game_log(game_log, game_id)

        return file_path

    ...

