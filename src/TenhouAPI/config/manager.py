"""
Configs of white keys in directory manager.
"""


# typing


# libs


from ..util.config import ConfigBase


""" Configs
"""


class WhiteKeyConfig(ConfigBase):
    """
    White keys of directory manager.
    """

    player_num_4 = ("00a1", "00a9", )
    player_num_3 = ("00b1", "00b9", )

    ...
