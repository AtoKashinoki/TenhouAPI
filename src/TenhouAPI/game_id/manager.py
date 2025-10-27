""" Tools that manage directory of game ids.
"""


# typing


from typing import (
    Union,
    List,
    Tuple
)

int_or_str = Union[int, str]


# libs


import os.path
import re

from ..config.tenhou_url import TenhouUrlConfig
from ..config.game_id import GameIdConfig
from ..config.manager import WhiteKeyConfig

from ..util.directory_manager import DirectoryManager

from .download import (
    download_game_id_list,
    save_file_from_zipped_bytes,
)
from .extract import extract_game_ids_from_file


""" Game ids directory manager
"""


class GameIdDirectory(DirectoryManager):
    """ Manage directory of game ids """

    """ Config """

    __url_config: Union[type[TenhouUrlConfig], TenhouUrlConfig] = TenhouUrlConfig
    __game_id_config: Union[type[GameIdConfig], GameIdConfig] = GameIdConfig

    @property
    def url_config(self) -> TenhouUrlConfig: return self.__url_config
    @property
    def game_id_config(self) -> GameIdConfig: return self.__game_id_config


    """ Initialize """

    def __init__(
            self,
            save_dir: str = os.path.join("../util", "dist", "game_ids"),
            url_config: TenhouUrlConfig = __url_config(),
            game_id_config: GameIdConfig = __game_id_config()
    ) -> None:
        """
        Assign directory that self save downloaded files.
        :param save_dir: Directory to save downloaded files.
        :param url_config: URL config.
        """
        DirectoryManager.__init__(self, save_dir)
        self.__url_config = url_config
        self.__game_id_config = game_id_config
        return

    """ html build """

    def save_file_from_zipped_bytes(
            self,
            zipped_bytes: bytes,
            save_file_name: str,
    ) -> str:
        """
        Build and save file from zipped bytes.
        :param zipped_bytes:  Bytes data that zipped.
        :param save_file_name: File name of html file.
        :return: Saved file name.
        """

        # save file

        save_file_path = save_file_from_zipped_bytes(
            zipped_bytes,
            self.generate_save_file_path(save_file_name),
            self.__url_config
        )

        return os.path.basename(save_file_path)

    def save_file_from_zipped_file(
            self,
            zipped_file_path: str,
            save_file_name: str = None,
    ) -> str:
        """
        Build and save file from zipped file.
        :param zipped_file_path: File name of html file.
        :param save_file_name: File name of html file.
        :return: Saved file name.
        """
        # generate save file name
        if save_file_name is None:
            save_file_name = self.__url_config.zip_tool.remove_extension(
                os.path.basename(zipped_file_path)
            )
            ...

        # read zipped file

        with open(zipped_file_path, "rb") as f_zipped:
            zipped_bytes = f_zipped.read()
            ...

        # save file

        save_file_path = save_file_from_zipped_bytes(
            zipped_bytes,
            self.generate_save_file_path(save_file_name),
            self.__url_config
        )

        return os.path.basename(save_file_path)

    def save_file_from_zipped_files_dir(
            self,
            zipped_files_dir_path: str,
            white_key: Tuple[str] = WhiteKeyConfig.player_num_4,
    ) -> Tuple[str, ...]:
        """
        Build and save file from zipped files dir.
        :param zipped_files_dir_path: File name of html file.
        :param white_key: White key.
        :return: Saved file names.
        """
        return tuple(
            self.save_file_from_zipped_file(
                os.path.join(zipped_files_dir_path, zipped_file_name)
            )
            for zipped_file_name in os.listdir(zipped_files_dir_path)
            if re.match(f"|".join([f"({key})" for key in white_key]), zipped_file_name)
        )

    """ Download and install """

    def download_and_install(
            self,
            year: int_or_str,
            month: int_or_str,
            day: int_or_str,
            hour: int_or_str,
            save_file_name: str = None,
            sleep_time: Union[int, float] = 5,
    ) -> str:
        """
        Download and install game ids.
        :param year: Target year to download.
        :param month: Target month to download.
        :param day: Target day to download.
        :param hour: Target hour to download.
        :param save_file_name: File name to save
        :param sleep_time: Sleep time of download.
        :return: Saved file name.
        """

        """ Download """

        zipped_bytes = download_game_id_list(
            year, month, day, hour,
            sleep_time=sleep_time,
            url_config=self.__url_config,
        )

        """ Install """

        if save_file_name is None:
            save_file_name = self.__url_config.id_file_name_format.format(
                key=self.__url_config.table_key,
                year=year, month=month, day=day, hour=hour,
            )

        saved_file_path = self.save_file_from_zipped_bytes(
            zipped_bytes, save_file_name
        )

        return saved_file_path

    """ Extract game id from html """

    def extract_game_ids_from_file(
            self, file_name: str,
            white_key: Tuple[str] = WhiteKeyConfig.player_num_4
    ) -> List[str]:
        """
        Extract game id from html file.
        :param file_name: File name of html file.
        :param white_key: White key.
        :return: Extracted game id.
        """
        return extract_game_ids_from_file(
            self.generate_save_file_path(file_name),
            self.__game_id_config,
            white_key,
        )

    ...