import requests

from .props import wrap


class Client:
    def __init__(self, headers=None):
        self._sess = requests.Session()
        if headers:
            self._sess.headers.update(headers)

    def get(self, url, params=None):
        resp = self._sess.get(url, params=params)
        resp.raise_for_status()
        return wrap(resp.json())
