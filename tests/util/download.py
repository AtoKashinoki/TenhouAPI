""" TenhoAPI.util.download.GameID tests
"""


from TenhouAPI.util.download import GameID, GameLog


if __name__ == '__main__':
    ids = GameID().run_all_processes(2025, 9, 14, 0)
    print(GameLog().run_all_processes(ids[0]))
    ...
