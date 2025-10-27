"""
Utility tools that manage directory.
"""


# typing


from typing import (
    List
)


# libs


from abc import ABC

import os

""" Directory manager
"""


class DirectoryManager(ABC):
    """
    Manage directory tool.
    """

    """ Save directory processes """

    __save_dir: str

    @property
    def save_dir(self) -> str:
        return self.__save_dir

    @save_dir.setter
    def save_dir(self, save_dir: str) -> None:
        self.__save_dir = save_dir

    def generate_save_file_path(self, file_name: str) -> str:
        """
        Generate and return  save file path.
        :param file_name: File name.
        :return: Generated save file path.
        """
        print(self.__save_dir, file_name)
        return os.path.join(self.__save_dir, file_name)

    """ Initializer """

    def __init__(self, save_dir: str) -> None:
        """
        Assign directory to manage.
        :param save_dir: Directory path to manage.
        """
        self.__save_dir = save_dir
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
            ...
        return

    """ Util methods """

    def listdir(self) -> List[str]:
        """
        List all files in directory.
        :return: File list.
        """
        return os.listdir(self.save_dir)

    ...
