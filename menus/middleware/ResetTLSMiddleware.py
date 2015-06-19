__author__ = 'PLNech'
import threading

_local = threading.local()

stored_items = [
    "MenuManager"
]


class ResetTLSMiddleware(object):
    def process_response(self, request, response):
        self.reset_local()
        return None

    def process_response(self, request, response):
        self.reset_local()
        return None

    @staticmethod
    def reset_local():
        for kw in stored_items:
            if kw in _local.__dict__:
                _local.pop(kw, None)
