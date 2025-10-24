""" Tenhou.util.purser tests
"""
from TenhouAPI.config import DisplayGameLogTag
from TenhouAPI.game_log import parse

import os


DIST = r"C:\MyProjects\code\tenhou_data"


if __name__ == '__main__':
    log_list= os.listdir(DIST+"\\game_logs")
    print(log_list)
    games = parse.GameLogParser(os.path.join(DIST + "\\game_logs", log_list[0]))
    for game in games:
        for tag in game:
            if tag not in (
                DisplayGameLogTag.P0_DRAW,
                DisplayGameLogTag.P0_DISCARD,
            ): continue
            print(tag.info)
            continue
        break
    ...
