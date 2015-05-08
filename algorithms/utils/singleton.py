__author__ = 'PLNech'


# noinspection PyPep8Naming
class singleton(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            # noinspection PyArgumentList
            cls._instance = object.__new__(cls, *args, **kwargs)
            print("Singleton created: %s" % cls)
        else:
            print("Returning Singleton: %s" % cls)
        return cls._instance
