import json
from collections.abc import Mapping, Sequence


class PropDict(Mapping):
    __slots__ = ["_inner"]

    def __init__(self, inner):
        self._inner = inner

    def __contains__(self, key):
        return key in self._inner

    def __iter__(self):
        return iter(self._inner)

    def __len__(self):
        return len(self._inner)

    def __getitem__(self, key):
        return wrap(self._inner[key])

    def __getattr__(self, name):
        return wrap(self._inner[name])

    def __repr__(self):
        return repr(self._inner)

    def get(self, key, default=None):
        return wrap(self._inner.get(key, default))

    def keys(self):
        return self._inner.keys()

    def values(self):
        for val in self._inner.values():
            yield wrap(val)

    def items(self):
        for key, val in self._inner.items():
            yield key, wrap(val)

    def json(self, pretty=False):
        if pretty:
            return json.dumps(self._inner, indent=2)
        else:
            return json.dumps(self._inner)


class PropList(Sequence):
    __slots__ = ["_inner"]

    def __init__(self, inner):
        self._inner = inner

    def __contains__(self, val):
        return val in self._inner

    def __iter__(self):
        for val in self._inner:
            yield wrap(val)

    def __len__(self):
        return len(self._inner)

    def __reversed__(self):
        for val in reversed(self._inner):
            yield wrap(val)

    def __getitem__(self, index):
        return wrap(self._inner[index])

    def __repr__(self):
        return repr(self._inner)

    def get(self, index, default=None):
        try:
            return wrap(self._inner[index])
        except IndexError:
            return default

    def json(self, pretty=False):
        if pretty:
            return json.dumps(self._inner, indent=2)
        else:
            return json.dumps(self._inner)


def wrap(val):
    if isinstance(val, list):
        return PropList(val)
    elif isinstance(val, dict):
        return PropDict(val)
    return val
