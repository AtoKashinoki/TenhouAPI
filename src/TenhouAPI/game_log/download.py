""" Game log tools that download from tenhou,
"""


# typing


# libs


from time import sleep

from ..util.download import download

from ..config.tenhou_url import TenhouUrlConfig


""" Game log tools
"""


""" Download function """


def download_game_log(
        game_id: str,
        sleep_time: float = 5,
        url_config: TenhouUrlConfig = TenhouUrlConfig(),
) -> bytes:
    """
    Download game log from tenhou.
    :param game_id: Game id to download.
    :param sleep_time: Sleep time.
    :param url_config: URL config.
    :return: Downloaded game log bytes.
    """

    # gen url
    game_log_url = url_config.generate_game_log_url(url_config, game_id)

    # download
    header = {"User-Agent": "Mozilla/5.0"}

    print("Downloading: {url}".format(url=game_log_url))

    result = download(game_log_url, headers=header)

    sleep(sleep_time)

    return result


""" Save function """


def save_game_log(
        bytes_data: bytes,
        file_path: str,
) -> str:
    """
    Save game log file from bytes.
    :param bytes_data: Bytes data to save.
    :param file_path: File path to save.
    :return: Saved game log file path.
    """

    print("Building game log file: {path}".format(path=file_path))

    # make and write game log file.
    with open(file_path, "wb") as f_mjlog:
        f_mjlog.write(bytes_data)
        ...

    return file_path
