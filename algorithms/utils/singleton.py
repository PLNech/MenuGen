__author__ = 'PLNech'


class Singleton(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            # noinspection PyArgumentList
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance
