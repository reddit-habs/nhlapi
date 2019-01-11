import enum
from abc import ABCMeta


class Param(metaclass=ABCMeta):
    def as_text(self):
        raise NotImplementedError


class Season(Param):
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
            assert begin + 1 == end
            self._begin = begin
            self._end = end

    @classmethod
    def fromstr(cls, s):
        assert len(s) == 8
        return Season(begin=int(s[:4]), end=int(s[4:]))

    def __repr__(self):
        return "Season({:04}-{:04})".format(self.begin, self.end)

    def as_text(self):
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

    def as_text(self):
        return "{:02}".format(self.value)


Param.register(GameKind)


class GameId(Param):
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

    def as_text(self):
        """
        Use this method to get the game's 10 digit code.

        :rtype: str
        """
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
