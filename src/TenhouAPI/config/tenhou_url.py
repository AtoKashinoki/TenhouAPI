""" Url configs of tenhou
"""


# types


# libs


import re

from ..util.config import ConfigBase
from ..util.zip import ZipBase, Gzip


""" Url configs
"""


""" Tenhou url """


class TenhouUrlConfig(ConfigBase):
    """ Url configs of tenhou """

    """ Settings """

    table_key: str = "scc"
    zip_tool: type[ZipBase] = Gzip

    """ Root url """

    root: str = "http://tenhou.net"

    """ Game ids """

    # generate url

    ids_directory: str = root + "/sc/raw/dat/"

    def generate_id_list_url(
            self,
            file_name: str,
    ) -> str:
        """
        Generate id list url.
        :param file_name: Name of file to generate.
        :return: Url of ids file.
        """
        return self.ids_directory + self.zip_tool.add_extension(file_name)

    # file name

    id_file_name_format: str = "{key}{year:04d}{month:02d}{day:02d}{hour:02d}.html"

    @property
    def file_name_length(self) -> int:
        """
        Return file name length.
        :return: Length of file name.
        """
        id_file_name_format = self.id_file_name_format.replace("{key}", str(self.table_key))
        const_len = len(re.sub(r"{\w+:\d\dd}", "", id_file_name_format))
        value_lens = re.findall(r":\d\dd}", id_file_name_format)
        value_len = sum(int(value[2:-2]) for value in value_lens)
        return const_len + value_len

    """ Game logs """

    game_log_file = root + "/0/log/?"

    def generate_game_log_url(self, game_id: str) -> str:
        """
        Generate game log url.
        :param game_id: Game id to download.
        :return: game log url.
        """
        return self.game_log_file + game_id.replace("log=", "")

    ...
