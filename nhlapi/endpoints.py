from datetime import date, datetime

from .utils import Param


def _to_str(val):
    if isinstance(val, Param):
        return val.as_text()
    if isinstance(val, (date, datetime)):
        return val.strftime("%Y-%m-%d")
    if isinstance(val, (list, tuple)):
        return ",".join(map(_to_str, val))
    return str(val)


def _maybe(val, func=_to_str):
    if val is not None:
        return func(val)
    return None


API_BASE_URL = "https://statsapi.web.nhl.com/api/v1"


class NHLAPI:
    """
    Initialize this class with the client you wish to use. It works transparently with the synchronous and asynchronous
    clients.

    Every method in this class returns a :class:`nhlapi.props.PropDict`, a special kind of dictionary that can access
    items with attribute access. For instance, here's how to get information about teams::

        api = NHLAPI(nhlapi.io.Client())
        result = api.teams()
        for team in result.teams:
            print(team.id, team.name, team.venue.name)

    And the printed output would be::

        1 New Jersey Devils Prudential Center
        2 New York Islanders Barclays Center
        3 New York Rangers Madison Square Garden
        ...

    """

    def __init__(self, client):
        self._client = client

    def _get(self, endpoint, **params):
        params = {key: val for key, val in params.items() if val is not None}
        return self._client.get(API_BASE_URL + endpoint, params)

    def teams(self, id=None, *, expand=None, stats=None):
        """
        Get the list of teams. Use the expand parameter, either as a str or list of str to get more information.

        `Docs <https://gitlab.com/dword4/nhlapi/blob/master/stats-api.md#teams>`__

        :param id: team id(s)
        :param expand: expanded information, see API docs
        :param stats: type of stats to show, see API docs
        :type id: int or list[int]
        :type expand: str or list[str]
        :type stats: str or list[str]
        """
        return self._get("/teams", teamId=_maybe(id), expand=_maybe(expand), stats=_maybe(stats))

    def team_stats(self, team_id):
        """
        Get information about the team's stats.

        `Docs <https://gitlab.com/dword4/nhlapi/blob/master/stats-api.md#team-stats>`__

        :param int team_id: team id
        """
        return self._get("/teams/{}/stats".format(team_id))

    def boxscore(self, game_id):
        """
        Get information about a game's boxscore.

        `Docs <https://gitlab.com/dword4/nhlapi/blob/master/stats-api.md#game>`__

        :param GameId or int game_id: game id
        """
        return self._get("/game/{}/boxscore".format(_to_str(game_id)))

    def content(self, game_id):
        """
        Get detailed media information about a game.

        `Docs <https://gitlab.com/dword4/nhlapi/blob/master/stats-api.md#game>`__

        :param GameId or int game_id: game id
        """
        return self._get("/game/{}/content".format(_to_str(game_id)))

    def divisions(self, id: int = None):
        """
        Get the list of divisions

        `Docs <https://gitlab.com/dword4/nhlapi/blob/master/stats-api.md#divisions>`__

        :param id: division id
        :type id: int or None
        """
        if id is not None:
            return self._get("/divisions/{}".format(id))
        else:
            return self._get("/divisions")

    def conferences(self, id=None):
        """
        Get the list of conferences

        `Docs <https://gitlab.com/dword4/nhlapi/blob/master/stats-api.md#conferences>`__

        :param id: conference id
        :type id: int
        """
        if id is not None:
            return self._get("/conferences/{}".format(id))
        else:
            return self._get("/conferences")

    def people(self, id, *, stats=None, stats_season=None):
        """
        Get information about a player. Use the stats parameter with a string to get a specific kind of stats.

        `Docs <https://gitlab.com/dword4/nhlapi/blob/master/stats-api.md#people>`__

        :param int id: player id
        :param stats: wether to fetch stats or a specific kind of stats
        :param stats_season: specify for which season to get the stats
        :type stats: bool or str
        :type stats_season: nhlapi.utils.Season
        """
        params = {}
        if stats:
            url = "/people/{}/stats".format(id)
            params["stats"] = stats
            if stats_season:
                params["season"] = stats_season.as_text()
        else:
            url = "/people/{}".format(id)
        return self._get(url, **params)

    def schedule(self, team_id=None, *, expand=None, date=None, start_date=None, end_date=None):
        """
        Get information about the schedule. Use the date parameters to filter for a specific date.

        `Docs <https://gitlab.com/dword4/nhlapi/blob/master/stats-api.md#schedule>`__

        :param int team_id: team id
        :param expand: expanded information, see API docs
        :param date: specific date
        :param start_date: start date of a date span
        :param end_date: end date of a date span
        :type expand: str or list[str]
        :type date: datetime.date
        :type start_date: datetime.date
        :type end_date: datetime.date
        """
        if date is not None and (start_date is not None or end_date is not None):
            raise ValueError("cannot set both of date and start_date/end_date")
        return self._get(
            "/schedule",
            teamId=_maybe(team_id, str),
            expand=_maybe(expand),
            date=_maybe(date),
            startDate=_maybe(start_date),
            endDate=_maybe(end_date),
        )

    def standings(self, *, expand=None, season=None, date=None):
        """
        Get information about the standings. Use the season or date parameter to filter for a specific season or date.

        `Docs <https://gitlab.com/dword4/nhlapi/blob/master/stats-api.md#standings>`__

        :param expand: expanded information, see API docs
        :param season: get standings for this season
        :param date: get standings at this date
        :type expand: str or list[str]
        :type season: nhlapi.utils.Season
        :type date: datetime.date
        """
        if season is not None and date is not None:
            raise ValueError("pick either season or date")
        return self._get("/standings/byLeague", season=_maybe(season), date=_maybe(date), expand=_maybe(expand))
