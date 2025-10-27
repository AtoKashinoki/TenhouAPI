""" Tools that manage directory of game logs.
"""


# typing


from typing import (
    Union,
)


# libs


import os.path

from ..config.tenhou_url import TenhouUrlConfig

from ..util.directory_manager import DirectoryManager

from .download import download_game_log, save_game_log
from .parse import GameLogParser


""" Game logs directory manager
"""


class GameLogDirectory(DirectoryManager):
    """ Manage directory of game logs """

    """ URL config """

    __url_config: Union[type[TenhouUrlConfig], TenhouUrlConfig] = TenhouUrlConfig

    """ Initialize """

    def __init__(
            self,
            save_dir: str = os.path.join("../util", "dist", "game_logs"),
            url_config: TenhouUrlConfig = __url_config(),
    ) -> None:
        """
        Assign directory that downloads game log files.
        :param save_dir: Directory path to save game log files.
        :param url_config: URL config.
        """
        DirectoryManager.__init__(self, save_dir)
        self.__url_config = url_config
        return

    """ Save game log file """

    def save_game_log(self, bytes_data: bytes, file_name: str) -> str:
        """
        Build and save game log file.
        :param bytes_data: Bytes data of game log.
        :param file_name: File name to generate.
        :return: Generated file path.
        """

        """ Save file """

        file_path = save_game_log(
            bytes_data,
            self.generate_save_file_path(file_name),
        )

        return file_path

    def download_and_install(
            self,
            game_id: str,
            file_name: str = None,
            sleep_time: float = 5,
    ) -> str:
        """
        Download and install game log.
        :param game_id: Game id to download.
        :param file_name: File name to generate.
        :param sleep_time: Sleep time.
        :return: Saved file path.
        """

        """ Download """

        bytes_ = download_game_log(
            game_id,
            sleep_time = sleep_time,
            url_config = self.__url_config,
        )

        """ Install """

        if file_name is None:
            file_name = game_id

        saved_file_path = self.save_game_log(
            bytes_, file_name
        )

        return saved_file_path

    """ Parse game log """

    def parse(self, file_name: str) -> GameLogParser:
        """
        Return game log parser.
        :param file_name: Game log name to parse.
        :return: Game log parser.
        """
        return GameLogParser(
            self.generate_save_file_path(file_name)
        )

    ...
