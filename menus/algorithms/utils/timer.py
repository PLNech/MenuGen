__author__ = 'PLNech'

import datetime


# noinspection PyPep8Naming, decorator...
class timer():
    def __init__(self, name):
        self.name = name

    def __call__(self, f):
        decorator_self = self

        def wrapped(*args, **kwargs):
            start = datetime.datetime.now()
            ret = f(*args, **kwargs)
            end = datetime.datetime.now()
            total_seconds = (end - start).total_seconds()
            print("%s: %f seconds" % (decorator_self.name, total_seconds))
            return ret

        return wrapped
