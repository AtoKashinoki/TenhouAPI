""" Functools that extract game ids.
"""


# typing


from typing import List


# libs


import re

from ..config.game_id import GameIdConfig


""" Extract game ids processes
"""


""" Extract """


def extract_game_ids_from_file(
        file_path: str,
        game_id_config: GameIdConfig = GameIdConfig(),
) -> List[str]:
    """
    Extract game id from html file.
    :param file_path:  File name of html file.
    :param game_id_config: Config of game id.
    :return: Extracted game id.
    """

    print("Extracting game id from {html} file.".format(html=file_path))

    # get file contains
    with open(file_path, "r", encoding="utf-8") as f_html:
        content = f_html.read()
        ...

    # extract game ids
    results = re.findall(game_id_config.game_id_format, content)

    return results