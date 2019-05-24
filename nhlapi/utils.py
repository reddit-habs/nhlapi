import enum
from abc import ABCMeta, abstractmethod
from datetime import date, datetime


class IUrlParam(metaclass=ABCMeta):
    """
    Implement this interface to be compatible with :func:`to_url_param`.
    """

    @abstractmethod
    def to_url_param(self):
        """
        Converts this object into a :class:`str` that can be understood by the NHL API.

        :rtype: str
        """
        raise NotImplementedError


def to_url_param(val):
    """
    This function converts a value to an URL parameter compatible with the NHL API.

    :param val:
        * If `val` implements :class:`IUrlParam` it will be converted using the :meth:`to_url_param` method.
        * If `val` is a :class:`date` or :class:`datetime` it will be converted to the YYYY-MM-DD format.
        * If `val` is a :class:`list` or :class:`tuple` each item inside will be converted with :func:`to_url_param`
          and joined with commas.
        * If `val` is an :class:`int` it will be converted to a :class:`str`.
        * If `val` is a :class:`str` it will be returned.
        * Any other type will raise a :class:`TypeError`.
    """
    if isinstance(val, IUrlParam):
        return val.to_url_param()
    if isinstance(val, (date, datetime)):
        return val.strftime("%Y-%m-%d")
    if isinstance(val, (list, tuple)):
        return ",".join(map(to_url_param, val))
    if isinstance(val, int):
        return str(val)
    if isinstance(val, str):
        return val
    else:
        raise TypeError("Cannot convert '{}' to url param".format(type(val)))


class Year(IUrlParam):
    """
    Represents a 4 digit year. Use this when the API expects a year with 4 digits, as a normal :class:`int` will not
    have leading zeroes.
    """

    def __init__(self, year):
        self.year = year

    def to_url_param(self):
        return "{:04}".format(self.year)


class Season(IUrlParam):
    """
    This class is meant to facilitate the usage of seasons within the API.
    You can create this class with either the `begin`, the `end` parameter
    or both. You need at least one of them.

    This way you can refer to the 2017-2018 season with `Season(begin=2017)`
    or `Season(end=2018)` which makes it less error prone. The endpoints
    always know which format to use.
    """

    def __init__(self, begin=None, end=None):
        if begin is None and end is None:
            raise ValueError("need at least one of begin or end")
        elif begin is None:
            self._begin = end - 1
            self._end = end
        elif end is None:
            self._begin = begin
            self._end = begin + 1
        else:
            if begin + 1 != end:
                raise ValueError("begin is not 1 year less than end")
            self._begin = begin
            self._end = end

    @classmethod
    def fromstr(cls, s):
        assert len(s) == 8
        return Season(begin=int(s[:4]), end=int(s[4:]))

    def __repr__(self):
        return "Season({:04}-{:04})".format(self.begin, self.end)

    def to_url_param(self):
        return "{}{}".format(self.begin, self.end)

    @property
    def begin(self):
        """
        :rtype: int
        """
        return self._begin

    @property
    def end(self):
        """
        :rtype: int
        """
        return self._end


class GameKind(enum.IntEnum):
    PRESEASON = 1
    REGULAR = 2
    PLAYOFFS = 3
    ALLSTARS = 4

    def to_url_param(self):
        return "{:02}".format(self.value)


IUrlParam.register(GameKind)


class GameId(IUrlParam):
    """
    Create a new GameId with the given info.

    :param season: NHL Season
    :param number: game number
    :param kind: kind of game
    :type season: Season
    :type number: int
    :type kind: GameKind
    """

    def __init__(self, season, number, kind=GameKind.REGULAR):
        self._season = season
        self._number = number
        self._kind = kind

    @classmethod
    def fromstr(cls, s):
        assert len(s) == 8
        return GameId(season=Season(begin=int(s[:4])), number=int(s[4:6]), kind=GameKind(int(s[6:])))

    def __repr__(self):
        return "Game({}, {}, {})".format(self._season, self._kind, self._number)

    def to_url_param(self):
        return "{:04}{:02}{:04}".format(self._season.begin, self._kind, self._number)

    @property
    def season(self):
        """
        :rtype: Season
        """
        return self._season

    @property
    def number(self):
        """
        :rtype: int
        """
        return self._number

    @property
    def kind(self):
        """
        :rtype: GameKind
        """
        return self._kind


class TimeOnIce:
    def __init__(self, seconds):
        self._seconds = seconds

    @classmethod
    def fromstr(cls, s):
        parts = s.split(":")
        mins = int(parts[0]) * 60
        secs = int(parts[1])
        return TimeOnIce(mins + secs)

    def str(self):
        mins, secs = divmod(self._seconds, 60)
        return "{:02}:{:02}".format(mins, secs)

    def __repr__(self):
        return "TimeOnIce({})".format(str(self))

    def __add__(self, other):
        return TimeOnIce(self.seconds + other.seconds)

    @property
    def seconds(self):
        return self._seconds
