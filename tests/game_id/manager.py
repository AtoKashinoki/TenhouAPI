""" Test src of manager of game id directory
"""


import os
from TenhouAPI.game_id.manager import GameIdDirectory


DIST = "../tenhou_data/game_ids"


if __name__ == "__main__":

    game_id_directory = GameIdDirectory(DIST)

    game_id_directory.download_and_install(
        2025, 10, 4, 0,
        sleep_time=0.5
    )

    lst_d = os.listdir(DIST)
    print("", lst_d[0], "", sep="\n")

    ids = game_id_directory.extract_game_ids_from_file(lst_d[0])
    print("", ids[0], "", sep="\n")

    ...
