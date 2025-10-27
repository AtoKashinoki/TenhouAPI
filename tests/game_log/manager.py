""" Test processes that manage game log directory """


import os
from TenhouAPI.game_log.manager import GameLogDirectory
from TenhouAPI.game_id.manager import GameIdDirectory


DIST = "../tenhou_data/"


if __name__ == '__main__':

    ids = GameIdDirectory(DIST+"game_ids").extract_game_ids_from_file(
        "scc2025100400.html"
    )

    game_log_manager = GameLogDirectory(DIST+"game_logs")

    for id_ in ids:
        file_path = game_log_manager.download_and_install(
            id_, sleep_time=0.5
        )

    print(os.listdir(DIST))

    ...
