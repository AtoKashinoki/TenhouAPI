""" TenhoAPI.util.download tests
"""


from TenhouAPI.util.download import GameID, GameLog


DIST = "C:\MyProjects\code\Tenhou"



if __name__ == '__main__':
    game_id = GameID(DIST+"\\game_ids")
    ids_dict = game_id.extract_game_ids_from_directory(
        DIST+"\\gz\\2024",
    )
    game_log = GameLog(DIST+"\\game_logs")
    for key in ids_dict.keys():
        for id_ in ids_dict[key]:
            game_log.run_all_processes(id_, sleep_time=0.1)

    ...
