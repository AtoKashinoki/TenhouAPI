""" Functools that extract game ids.
"""


# typing


from typing import List, Tuple

# libs


import re

from ..config.game_id import GameIdConfig


""" Extract game ids processes
"""


""" Extract """


def extract_game_ids_from_file(
        file_path: str,
        game_id_config: GameIdConfig = GameIdConfig(),
        white_key: Tuple[str, ...] = ("00a9", "00e9"),
) -> List[str]:
    """
    Extract game id from html file.
    :param file_path:  File name of html file.
    :param game_id_config: Config of game id.
    :param white_key: White key.
    :return: Extracted game id.
    """

    print("Extracting game id from {html} file.".format(html=file_path))

    # get file contains
    with open(file_path, "r", encoding="utf-8") as f_html:
        content = f_html.read()
        ...

    # extract game ids
    results = re.findall(game_id_config.game_id_format, content)

    # choice white result
    results = [
        result
        for result in results
        if result[17:21] in white_key
    ]

    return results