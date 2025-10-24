""" Test processes that manage game log directory """


import os
from TenhouAPI.game_log.manager import GameLogDirectory


DIST = "../tenhou_data/game_logs"

id_ = "log=2025100400gm-00b9-0000-bea485e0"


if __name__ == '__main__':

    game_log_manager = GameLogDirectory(DIST)

    file_path = game_log_manager.download_and_install(
        id_, sleep_time=0.5
    )

    print(os.listdir(DIST))

    ...
