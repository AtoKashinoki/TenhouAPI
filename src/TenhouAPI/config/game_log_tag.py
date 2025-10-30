"""  Config of tag in game log.
"""


# typing


# libs


from ..util.config import ConfigBase


""" Tag Constants
"""


""" Tag """


class DisplayGameLogTag(ConfigBase):
    """
    Tag for displaying game log
    """

    GO = "GO"
    INIT = "INIT"
    OPEN_DORA = "OPEN_D"
    P0_DRAW = "P0_DRAW"
    P1_DRAW = "P1_DRAW"
    P2_DRAW = "P2_DRAW"
    P3_DRAW = "P3_DRAW"
    P0_DISCARD = "P0_DISC"
    P1_DISCARD = "P1_DISC"
    P2_DISCARD = "P2_DISC"
    P3_DISCARD = "P3_DISC"
    NAKI = "NAKI"
    REACH = "REACH"
    AGARI = "AGARI"
    RYUUKYOKU = "END"

    DRAWS = (P0_DRAW, P1_DRAW, P2_DRAW, P3_DRAW)
    DISCARDS = (P0_DISCARD, P1_DISCARD, P2_DISCARD, P3_DISCARD)

    ...


""" Call """


class DisplayCalls(ConfigBase):
    """
    Configs for displaying calls
    """

    CHI = "chi"
    PON = "pon"
    KAKAN = "kakan"
    DAIMINKAN = "daiminkan"

    ...


class CallTarget(ConfigBase):
    """
    Configs for calling target
    """

    FRONT = 0
    RIGHT = 1
    LEFT = 2

    ...
