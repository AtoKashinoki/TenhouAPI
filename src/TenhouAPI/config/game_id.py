""" Config of game id.
"""


# typing


# libs


from ..util.config import ConfigBase


""" Game id configs
"""


class GameIdConfig(ConfigBase):
    """Configs of game id. """

    """ game id format """

    game_id_format = r"log=\d{10}gm-.{4}-.{4}-.{8}"

    ...