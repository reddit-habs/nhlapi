import json
from collections import OrderedDict


class PropDict:
    """
    This class is a thin wrapper around a :class:`collections.abc.Mapping`. It is used to provide
    access to the mapping via attributes recursively and lazily.
    """

    __slots__ = ["_nhlapi_inner_"]

    def __init__(self, inner):
        """
        Avoid constructing this object directly. It's best to use :func:`wrap`.
        """
        self._nhlapi_inner_ = inner

    def __contains__(self, key):
        return key in self._nhlapi_inner_

    def __iter__(self):
        return iter(self._nhlapi_inner_)

    def __len__(self):
        return len(self._nhlapi_inner_)

    def __getitem__(self, key):
        return wrap(self._nhlapi_inner_[key])

    def __getattr__(self, name):
        return wrap(self._nhlapi_inner_[name])

    def __repr__(self):
        return repr(self._nhlapi_inner_)


class PropList:
    """
    This class is a thin wrapper around a :class:`collections.abc.Sequence`. It is used to wrap the
    mappings inside the sequence recursively and lazily.
    """

    __slots__ = ["_nhlapi_inner_"]

    def __init__(self, inner):
        self._nhlapi_inner_ = inner

    def __contains__(self, val):
        return val in self._nhlapi_inner_

    def __iter__(self):
        for val in self._nhlapi_inner_:
            yield wrap(val)

    def __len__(self):
        return len(self._nhlapi_inner_)

    def __reversed__(self):
        for val in reversed(self._nhlapi_inner_):
            yield wrap(val)

    def __getitem__(self, index):
        return wrap(self._nhlapi_inner_[index])

    def __repr__(self):
        return repr(self._nhlapi_inner_)


_mapping_types = (dict, OrderedDict)
_sequence_types = (list, tuple)
_get_types = (PropDict, PropList) + _mapping_types + _sequence_types


def wrap(val):
    """
    This function will wrap the given value into a :class:`PropDict` if it's a mapping, into a :class:`PropList` if it's
    a sequence or return the value if it's of any other type. This is the best way of wrapping a JSON document so that
    it can be accessed via attributes.

    :param val: Value to be wrapped if necessary
    :type val: :class:`collections.abc.Mapping` or :class:`collections.abc.Sequence` or any
    :rtype: PropDict, PropList or any
    """
    if isinstance(val, _mapping_types):
        return PropDict(val)
    if isinstance(val, _sequence_types):
        return PropList(val)
    return val


def get(obj, key, default=None):
    """
    This function behaves like :meth:`dict.get`. If the key or index is not
    found inside the object, the default value is returned.

    :param obj: A list/sequence or dictionary/mapping compatible with this function.
    :param key: A list/sequence index or a dictionary/mapping key.
    :type obj: :class:`PropDict` or :class:`PropList` or :class:`collections.abc.Mapping` or
               :class:`collections.abc.Sequence`
    :type key: `int` or `str` or `any`
    :return: value for `key` or `default`
    """
    if isinstance(obj, (PropDict, PropList)):
        try:
            return obj[key]
        except (IndexError, KeyError):
            return default
    else:
        raise TypeError("cannot use get() on type " + str(type(obj)))


def keys(obj):
    """
    This function returns an iterator that yields the object's keys.

    :param obj: A dictionary/mapping compatible with this function.
    :type obj: :class:`PropDict` or :class:`collections.abc.Mapping`
    :return: iterator of keys
    """
    if isinstance(obj, PropDict):
        return obj._nhlapi_inner_.keys()
    elif isinstance(obj, _mapping_types):
        return obj.keys()
    else:
        raise TypeError("cannot use keys() on type " + str(type(obj)))


def values(obj):
    """
    This function returns an iterator that yields the object's values.

    :param obj: A dictionary/mapping compatible with this function.
    :type obj: :class:`PropDict` or :class:`collections.abc.Mapping`
    :return: iterator of values
    """
    if isinstance(obj, PropDict):
        for val in obj._nhlapi_inner_.values():
            yield wrap(val)
    elif isinstance(obj, _mapping_types):
        return obj.values()
    else:
        raise TypeError("cannot use values() on type " + str(type(obj)))


def items(obj):
    """
    This function returns an iterator that yields the object's keys and values as a pair.

    :param obj: A dictionary/mapping compatible with this function.
    :type obj: :class:`PropDict` or :class:`collections.abc.Mapping`
    :return: iterator of tuples, first element is key, second element is value
    """
    if isinstance(obj, PropDict):
        for key, val in obj._nhlapi_inner_.items():
            yield key, wrap(val)
    elif isinstance(obj, _mapping_types):
        return obj.items()
    else:
        raise TypeError("cannot use items() on type " + str(type(obj)))


def json_dump(obj, fp=None, **kwargs):
    """
    This function will dump the given object as JSON. If `fp` is not `None`, this function will write to the
    file object given by `fp` instead of serializing the JSON to a :class:`str`.

    :param obj: A list/sequence or dictionary/mapping compatible with this function.
    :param fp: If provided, fp should be a writable file object.
    :param kwargs: Any other argument will be passed on to :func:`json.dump` or :func:`json.dumps`.
    :type obj: :class:`PropDict` or :class:`PropList` or `any`
    :returns: If `fp` is provided, this function returns `None`. Otherwise it returns a :class:`str`.
    """

    def dump(val):
        if fp is not None:
            json.dump(val, fp, **kwargs)
        else:
            return json.dumps(val, **kwargs)

    if isinstance(obj, (PropDict, PropList)):
        return dump(obj._nhlapi_inner_)
    else:
        return dump(obj)
