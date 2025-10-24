""" Utility functions that download from internet.
"""


# types

# libs


from urllib.request import Request, urlopen


""" Utility functions
"""


""" download from internet """


def download(url: str, headers=None) -> bytes:
    """
    Download file function.
    :param url: File URL to download.
    :param headers: Request headers.
    :return: Downloaded file.
    """
    # request
    req = Request(url, headers=headers)

    # check response
    with urlopen(req) as response:
        if not response.status == 200:
            raise RuntimeError(response.status)
        result: bytes = response.read()

    return result

