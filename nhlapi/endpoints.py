from .props import wrap


def _maybe_join(values):
    if values is not None:
        return ",".join(map(str, values))
    return None


API_BASE_URL = "https://statsapi.web.nhl.com/api/v1"


class NHLAPI:
    def __init__(self, client):
        self._client = client

    def _get(self, endpoint, **params):
        return wrap(self._client.get(API_BASE_URL + endpoint, params))

    def teams(self, id=None, expand=None, stats=None):
        """
        Get the list of teams.

        :param id: team id(s)
        :param expand: expanded information, see API docs
        :param stats: type of stats to show, see API docs
        :type id: int or list[int] or None
        :type expand: str or list[str] or None
        :type stats: str or list[str] or None
        """
        id = _maybe_join(id)
        expand = _maybe_join(expand)
        stats = _maybe_join(stats)

        return self._get("/teams", id=id, expand=expand, stats=stats)

    def divisions(self, id=None):
        """
        Get the list of divisions

        :param id: division id
        :type id: int or None
        """
        if id is not None:
            return self._get("/divisions/" + str(id))
        else:
            return self._get("/divisions")

    def conferences(self, id=None):
        """
        Get the list of conferences

        :param id: conference id
        :type id: int or None
        """
        if id is not None:
            return self._get("/conferences/" + str(id))
        else:
            return self._get("/conferences")

    def people(self, id, stats=False, stats_season=None):
        """
        Get information about a player. Use the stats parameter with a string to get a specific kind of stats.

        :param int id: player id
        :param stats: wether to fetch stats or a specific kind of stats
        :param stats_season: specify for which season to get the stats
        :type stats: bool or str
        :type stats_season: Season
        """
        pass
