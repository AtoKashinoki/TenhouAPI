""" Parse utility module of TenhouAPI
This file contains processes that parse game log.
"""


# types


from typing import (
    Set, Tuple, List, Dict, Iterator, Union
)


# libs


import re
from ..config.game_log_tag import DisplayGameLogTag, DisplayCalls


""" Parse processes 
"""


GAME_END_KEY: Tuple[str, ...] = (
    DisplayGameLogTag.AGARI, DisplayGameLogTag.RYUUKYOKU
)


""" Tage management class """


class TagParser:
    """ Tag of game log manager """

    """ Class attributes """

    _rename_tag: Dict[str, str] = {
        "GO": DisplayGameLogTag.GO,
        "INIT": DisplayGameLogTag.INIT,
        "DORA": DisplayGameLogTag.OPEN_DORA,
        "T": DisplayGameLogTag.P0_DRAW,
        "U": DisplayGameLogTag.P1_DRAW,
        "V": DisplayGameLogTag.P2_DRAW,
        "W": DisplayGameLogTag.P3_DRAW,
        "D": DisplayGameLogTag.P0_DISCARD,
        "E": DisplayGameLogTag.P1_DISCARD,
        "F": DisplayGameLogTag.P2_DISCARD,
        "G": DisplayGameLogTag.P3_DISCARD,
        "N": DisplayGameLogTag.NAKI,
        "REACH": DisplayGameLogTag.REACH,
        "AGARI": DisplayGameLogTag.AGARI,
        "RYUUKYOKU": DisplayGameLogTag.RYUUKYOKU,
    }

    """ Initialize """

    def __init__(self, tag_text: str) -> None:
        """
        Parse constructor, and assign attributes.
        :param tag_text: Text that describes the tag.
        """
        tag, self.__attrs = self.parse(tag_text)
        self.__tag = self._rename_tag[tag]
        return

    def __str__(self):
        return self.__tag

    def __eq__(self, other) -> bool:
        if isinstance(other, TagParser):
            return self.__tag == other.__tag
        elif isinstance(other, str):
            return self.__tag == other
        return False

    """ Instance attributes """

    __tag: str
    @property
    def tag(self) -> str: return self.__tag

    __attrs: Dict[str, str]
    @property
    def attrs(self) -> Dict[str, str]: return self.__attrs

    @property
    def info(self) -> Tuple[str, Dict[str, str]]: return self.__tag, self.__attrs

    """ parse """

    @staticmethod
    def parse(tag_text: str) -> Tuple[str, Dict[str, str]]:
        """
        Parse game log, and return to pick up tags.
        :param tag_text: String of game log text.
        :return: tag name and pick upped tags.
        """

        # split
        attrs_list: str
        name, *attrs_list = tag_text[:-1].split(' ')

        # check special tag
        if re.match(r"\w\d+", name):
            attrs = {"id": name[1:]}
            name = name[0]
            ...
        else:
            # normal tag process
            attrs = {}
            for attr in attrs_list:
                if attr == "": continue
                key, value = attr.split("=")
                attrs[key] = re.sub(r'"', "", value)
                continue
            ...

        return name, attrs

    ...


""" File parse class """


class FileParser:
    """ Parse game log, and manage info """

    """ Class attributes """

    _split_key: str = "><"
    @property
    def split_key(self) -> str: return self._split_key

    _pick_up_tags: Set[str] = (
        "GO",
        "INIT", "DORA",
        "T", "U", "V", "W",
        "D", "E", "F", "G",
        "N", "REACH",
        "AGARI", "RYUUKYOKU",
    )
    @property
    def pick_up_tags(self) -> Set[str]: return self._pick_up_tags

    """ parse class method """

    @classmethod
    def parse(cls, game_log_text: str) -> Tuple[TagParser, ...]:
        """
        Parse game log, and return to pick up tags.
        :param game_log_text: String of game log text.
        :return: pick upped tags.
        """

        result: List[TagParser] = []

        # split tag and loop
        for tag_text in game_log_text[1:-1].split(cls._split_key):

            # get tag name
            tag_match = re.match(r"[A-Z]+[ |\d]", tag_text)
            if tag_match is None: continue

            # pick up tag
            tag_name = tag_match.group()[:-1]
            if tag_name not in cls._pick_up_tags: continue

            # assign tag
            tag = TagParser(tag_text)
            result.append(tag)

            continue

        return tuple(result)

    """ Initialize """

    def __init__(self, game_log_file_path: str) -> None:
        """
        Parse game log, and pick up tags.
        :param game_log_file_path: File path to parse game log.
        """

        # read game log
        with open(game_log_file_path, "r", encoding="utf-8") as f:
            game_log_text = f.read()
            ...
        self.__file_path = game_log_file_path

        # parse
        self.__tags = self.parse(game_log_text)

        return

    """ Instance attributes """

    __file_path: str
    @property
    def file_path(self) -> str: return self.__file_path

    __tags: Tuple[TagParser, ...] = {}
    @property
    def tags(self) -> Tuple[TagParser, ...]: return self.__tags

    ...


""" Game log that parse tag """


class GameLogParser:
    """ Manage game log class """

    """ Class attributes """

    _default_file_parse: FileParser = FileParser
    @property
    def default_file_parse(self) -> FileParser: return self._default_file_parse

    """ Initialize """

    def __init__(
            self,
            game_log_file_path: str,
            file_parser: type[FileParser] = _default_file_parse
    ) -> None:
        """
        Parse game log, and assign result.
        :param game_log_file_path: File path of game log.
        :param file_parser: FileParser class.
        """

        # file parse
        file_parsed = file_parser(game_log_file_path)

        # split game log
        game_logs = []
        game_log = []

        for tag in file_parsed.tags:

            if tag == "GO":
                self.__game_tag = tag
                continue

            game_log.append(tag)

            if tag not in GAME_END_KEY: continue

            game_logs.append(tuple(game_log))
            game_log = []

            continue


        self.__game_logs = tuple(game_logs)
        return

    """ Instance attributes """

    __game_log_file_path: str
    @property
    def game_log_file_path(self) -> str: return self.__game_log_file_path

    __game_tag: TagParser
    @property
    def game_tag(self) -> TagParser: return self.__game_tag

    __game_logs: Tuple[Tuple[TagParser, ...], ...]
    @property
    def game_logs(self) -> Tuple[Tuple[TagParser, ...], ...]: return self.__game_logs

    def __getitem__(self, idx: int) -> Tuple[TagParser, ...]:
        """
        Return game log info by index.
        :param idx: Index of game log info.
        :return: Game log info by index.
        """
        return self.__game_logs[idx]

    def __len__(self): return len(self.__game_logs)

    def __iter__(self) -> Iterator[Tuple[TagParser, ...]]: return iter(self.__game_logs)

    ...


""" Attribute parser """


RESULT_FORMAT =\
    Dict[str, Union[str, int, Dict[str, Union[int, Tuple[int, ...], None]], None]]
PARSE_M_RESULT: RESULT_FORMAT= {
    "m": None,
    "type": None,
    "from": None,
    "details": {"tiles": None, "called_idx": None}
}


def parse_m_attribute_of_chi(chi_m: int,) -> RESULT_FORMAT:
    """
    Parse game log attribute of chi.
    :param chi_m: Game log attribute.
    :return: Parsed game log attribute.
    """
    # copy result format
    result = PARSE_M_RESULT.copy()

    # generate result values
    from_who = chi_m & 0x3
    t = chi_m >> 10
    base_tile_id = t // 3
    tiles = tuple(base_tile_id+i for i in range(3))
    called_idx = t % 3

    # assign result
    result["m"] = chi_m
    result["type"] = "chi"
    result["from"] = from_who
    result["details"]["tiles"] = tiles
    result["details"]["called_idx"] = called_idx

    return result


def parse_m_attribute_of_pon(pon_m: int) -> RESULT_FORMAT:
    """
    Parse game log attribute of pon.
    :param pon_m: Game log attribute.
    :return: Parsed game log attribute.
    """
    # copy result format
    result = PARSE_M_RESULT.copy()

    # generate result values
    from_who = pon_m & 0x3
    t = pon_m >> 9
    base_tile_id = t // 3
    tiles = tuple(base_tile_id for _ in range(3))
    called_idx = t % 3

    # assign result
    result["m"] = pon_m
    result["type"] = DisplayCalls.CHI
    result["from"] = from_who
    result["details"]["tiles"] = tiles
    result["details"]["called_idx"] = called_idx

    return result


def parse_m_attribute_of_kakan(kakan_m: int)  -> RESULT_FORMAT:
    """
    Parse game log attribute of kakan.
    :param kakan_m: Game log attribute.
    :return: Parsed game log attribute.
    """
    # copy result format
    result = PARSE_M_RESULT.copy()

    # generate result values
    from_who = None
    t = kakan_m >> 9
    base_tile_id = t // 3
    tiles = tuple(base_tile_id for _ in range(4))

    # assign result
    result["m"] = DisplayCalls.PON
    result["type"] = DisplayCalls.KAKAN
    result["from"] = from_who
    result["details"]["tiles"] = tiles
    result["details"]["called_idx"] = None

    return result


def parse_m_attribute_of_daiminkan(daiminkan_m: int) -> RESULT_FORMAT:
    """
    Parse game log attribute of daiminkan.
    :param daiminkan_m: Game log attribute.
    :return: Parsed game log attribute.
    """
    # copy result format
    result = PARSE_M_RESULT.copy()

    # generate result values
    from_who = daiminkan_m & 0x3
    t = daiminkan_m >> 8
    base_tile_id = t // 4
    tiles = tuple(base_tile_id for _ in range(4))
    called_idx = t % 4

    # assign result
    result["m"] = DisplayCalls.PON
    result["type"] = DisplayCalls.DAIMINKAN
    result["from"] = from_who
    result["details"]["tiles"] = tiles
    result["details"]["called_idx"] = called_idx

    return result


def parse_m_attribute(m: int) -> RESULT_FORMAT:
    """
    Parse game log attribute.
    :param m: Game log attribute.
    :return: Parsed game log attribute.
    """
    if m&0x0004: result = parse_m_attribute_of_chi(m)
    elif m&0x0008: result = parse_m_attribute_of_pon(m)
    elif m&0x0010: result = parse_m_attribute_of_kakan(m)
    else: result = parse_m_attribute_of_daiminkan(m)
    return result
