"""  Utility tools of "__repr__" method.
"""

# types


from typing import (
    Tuple,
    Dict,
    Any,
    TypeVar
)


T = TypeVar("T")


# libs


from abc import ABC


""" Representation method tools.
"""


""" Convert data to arg string """


def arg_str(data: Any) -> str:
    """
    Generate argument string from data.
    :param data: Data to convert.
    :return: Generated argument string.
    """
    if isinstance(data, str):
        return f"'{data}'"
    return str(data)


def convert_args_string(*args: Any, **kwargs: Any) -> str:
    """
    Convert arguments string to arg string.
    :param args: Arguments to convert.
    :param kwargs: Keywords to convert.
    :return: Argument string.
    """
    # kwargs
    kwarg_strings = tuple(
        f"{key}={arg_str(value)}"
        for key, value in kwargs.items()
    )

    # args
    args_strings = tuple(
        map(arg_str, args)
    )

    return ", ".join(
        args_strings + kwarg_strings
    )


""" Representation string format """


REPR_FORMAT: str = "{class_name}({arguments})"


def generate_representation(
        class_name: str,
        *args: Tuple[Any, ...],
        **kwargs: Dict[str, Any],
) -> str:
    """
    Generate a string representation of a class instance.
    :param class_name: Class name to generate string representation for.
    :param args: Arguments to generate string representation for.
    :param kwargs: Keyword arguments to generate string representation for.
    :return: String representation.
    """
    return REPR_FORMAT.format(
        class_name=class_name,
        arguments=convert_args_string(*args, **kwargs),
    )


""" Decorate "__repr__" method """""


# repr base class


class ReprBase(ABC):
    """ Representation base class """

    """ Assign arguments of representation string """

    __value_name_and_keyword: Dict[str, str]

    def __init__(self, value_name_and_keyword: Dict[str, str]):
        """
        Assign arguments of representation string.
        :param value_name_and_keyword: \
        Value name and keyword arguments of representation string.
        """
        self.__value_name_and_keyword = value_name_and_keyword
        return

    """ Output representation string """

    def __repr__(self) -> str:
        """ Return representation string """
        kwargs = {
            keyword: getattr(self, name)
            for keyword, name in self.__value_name_and_keyword.items()
        }
        return generate_representation(
            class_name=self.__class__.__name__,
            **kwargs
        )

    @property
    def __representation__(self) -> str:
        """ Return representation string """
        return self.__repr__()

    ...
