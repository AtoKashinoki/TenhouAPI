""" Config utilities tests
"""


from TenhouAPI.util.config import ConfigBase


class Config(ConfigBase):
    """ Test config class """

    test1: str = "test1"
    test2 = 2

    ...


if __name__ == "__main__":

    conf = Config()

    print(eval(repr(conf)))

    ...

