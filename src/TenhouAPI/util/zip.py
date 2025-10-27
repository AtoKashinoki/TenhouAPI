""" Utility tools of zip file.
"""


# typing


from typing import (
    Callable,
)


# libs


import os
import gzip
from abc import ABC, abstractmethod


""" Tools of zip file
"""


""" Base """


class ZipBase(ABC):
    """ Zip class base """

    """ Extension """

    EXTENSION: str = None

    """ Functools """

    @staticmethod
    def unzip(
            file_path: str,
            result_path: str = None,
    ) -> None:
        """
        Unpack zip file and save result.
        :param file_path: Zip file path to unzip.
        :param result_path: Unzipped file path.
        :return: None
        """

        print(f"Unzipping: {file_path}")

        # check exists
        if os.path.exists(result_path):
            print(f"Unzipping is already done: {result_path}")
            return

        # unpack gz and save html
        with gzip.open(file_path, "rb") as f_in:
            with open(result_path, "wb") as f_out:
                f_out.write(f_in.read())
                ...
            ...

        return

    @staticmethod
    @abstractmethod
    def add_extension(file_path: str, extension: str = EXTENSION) -> str:
        """
        Add zip file extension.
        :param file_path: File path to add extension.
        :param extension: Extension to add.
        :return: Added file path.
        """
        return ...

    @staticmethod
    @abstractmethod
    def remove_extension(file_path: str, extension: str = EXTENSION) -> str:
        """
        Remove zip file extension.
        :param file_path: File path to remove extension.
        :param extension: Extension to remove.
        :return: Removed file path.
        """
        return ...

    ...


""" Gzip """


class Gzip(ZipBase):
    """ Tools of gzip file """

    """ Extension """

    EXTENSION = ".gz"

    @staticmethod
    def add_extension(file_path: str, extension: str = EXTENSION) -> str:
        return file_path + extension

    @staticmethod
    def remove_extension(file_path: str, extension: str = EXTENSION) -> str:
        return file_path[:-len(extension)]

    ...