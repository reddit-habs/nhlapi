import enum


class Season:
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

    def __repr__(self):
        return "Season({:04}-{:04})".format(self.begin, self.end)

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

    def concat(self):
        """
        This method returns the season identifier in concatenated form.

            >>> Season(begin=2017).concat()
            "20172018"

        :rtype: str
        """
        return "{}{}".format(self._begin, self._end)


class GameKind(enum.IntEnum):
    PRESEASON = 1
    REGULAR = 2
    PLAYOFFS = 3
    ALLSTARS = 4

    def __format__(self, spec):
        return "{:02}".format(self.value)


class GameId:
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

    def code(self):
        """
        Use this method to get the game's 10 digit code.

        :rtype: str
        """
        return "{:04}{}{:04}".format(self._season.begin, self._kind, self._number)

    def __repr__(self):
        return "Game({}, {}, {})".format(self._season, self._kind, self._number)
