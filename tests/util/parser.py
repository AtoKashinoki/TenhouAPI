""" Tenhou.util.purser tests
"""


from TenhouAPI.util import parse

import os


DIST = "C:\MyProjects\code\Tenhou"


if __name__ == '__main__':
    log_list= os.listdir(DIST+"\\game_logs")
    print(log_list)
    games = parse.GameLogParser(os.path.join(DIST+"\\game_logs", log_list[0]))
    for game in games:
        print(tuple(map(str, game)))
    ...
