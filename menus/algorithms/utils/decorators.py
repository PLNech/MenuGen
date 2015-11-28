import functools

__author__ = 'PLNech'


def memoize(obj):
    cache = obj.cache = {}

    @functools.wraps(obj)
    def memoizer(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = obj(*args, **kwargs)
        return cache[key]
    return memoizer

if __name__ == '__main__':
    class Foo:
        @memoize
        def double(self, a):
            Foo.called()
            return a * 2

        @staticmethod
        def called():
            print("Got called!")

        @staticmethod
        @memoize
        def mult(a, b, dictio=None):
            if not dictio:
                dictio = {}
            Foo.called()
            return a * b

    foo = Foo()
    print(foo.double(5))
    print(foo.double(5))

    dictio = {'asd': 2}
    print(foo.mult(5, 4, dictio))
    print(foo.mult(5, 4, dictio))
