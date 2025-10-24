""" Utility tools of config processes.
"""


# types


from typing import (
    Dict,
     Any
)


# libs


from abc import ABC
import re
from .repr import ReprBase


""" Utility tools
"""


""" config base class """


class ConfigBase(ReprBase, ABC):
    """ Base class of config object """

    """ Initialize  """

    def __init__(self, **kwargs) -> None:
        """
        Assign instance attributes to class attributes.
        :param kwargs: Value that overwrite.
        """

        # assign config values
        self.__assign_cls_attrs_to_ins()
        self.__assign_args_to_ins_attrs(kwargs)

        # repr process
        value_name_and_keyword = {
            keyword: keyword
            for keyword in self.configs.keys()
        }
        ReprBase.__init__(self, value_name_and_keyword)

        return

    """ Get attributes of config """

    @property
    def configs(self) -> Dict[str, Any]:
        """
        Return attributes of config.
        :return: Config attributes.
        """
        return {
            key: value
            for key, value in self.__dict__.items()
            if re.match(r"^__?", key) is None
        }

    """ Assign instance attributes to class attributes """

    def __assign_cls_attrs_to_ins(self) -> None:
        """
        Assign class attributes to instance attributes.
        :return: None
        """
        for key, value in self.__class__.__dict__.items():

            if re.match(r"^__?", key) is not None:
                continue

            try: setattr(self, key, value)
            except AttributeError: ...
            continue

        return

    def __assign_args_to_ins_attrs(
            self,
            kwargs: Dict[str, Any]
    ) -> None:
        """
        Assign instance attributes to class attributes.
        :param kwargs: Keyword arguments to assign to instance attributes.
        :return: None
        """
        for key, value in kwargs.items():
            setattr(self, key, value)
            continue
        return

    ...
