from datetime import date

import pytest
from nhlapi.endpoints import NHLAPI
from nhlapi.utils import Season


class MockClient:
    def get(self, url, params=None):
        self.url = url
        self.params = params


def test_teams():
    mock = MockClient()
    api = NHLAPI(mock)
    api.teams(8, expand=["foo", "bar"], stats="single")

    assert mock.url == "https://statsapi.web.nhl.com/api/v1/teams"
    assert mock.params["teamId"] == "8"
    assert mock.params["expand"] == "foo,bar"
    assert mock.params["stats"] == "single"


def test_teams_stats():
    mock = MockClient()
    api = NHLAPI(mock)
    api.team_stats(8)

    assert mock.url == "https://statsapi.web.nhl.com/api/v1/teams/8/stats"


def test_teams_divisions():
    mock = MockClient()
    api = NHLAPI(mock)
    api.divisions()

    assert mock.url == "https://statsapi.web.nhl.com/api/v1/divisions"


def test_teams_divisions_id():
    mock = MockClient()
    api = NHLAPI(mock)
    api.divisions(1)

    assert mock.url == "https://statsapi.web.nhl.com/api/v1/divisions/1"


def test_teams_conferences():
    mock = MockClient()
    api = NHLAPI(mock)
    api.conferences()

    assert mock.url == "https://statsapi.web.nhl.com/api/v1/conferences"


def test_teams_conferences_id():
    mock = MockClient()
    api = NHLAPI(mock)
    api.conferences(1)

    assert mock.url == "https://statsapi.web.nhl.com/api/v1/conferences/1"


def test_people_simple():
    mock = MockClient()
    api = NHLAPI(mock)
    api.people(5000)

    assert mock.url == "https://statsapi.web.nhl.com/api/v1/people/5000"


def test_people_stats():
    mock = MockClient()
    api = NHLAPI(mock)
    api.people(5000, stats="single", stats_season=Season(end=2018))

    assert mock.url == "https://statsapi.web.nhl.com/api/v1/people/5000/stats"
    assert mock.params["stats"] == "single"
    assert mock.params["season"] == "20172018"


def test_schedule_date():
    mock = MockClient()
    api = NHLAPI(mock)
    api.schedule(expand=["foo", "bar"], date=date(2018, 1, 1))

    assert mock.url == "https://statsapi.web.nhl.com/api/v1/schedule"
    assert mock.params["expand"] == "foo,bar"
    assert mock.params["date"] == "2018-01-01"


def test_schedule_team_range():
    mock = MockClient()
    api = NHLAPI(mock)
    api.schedule(8, start_date=date(2018, 1, 1), end_date=date(2018, 6, 1))

    assert mock.url == "https://statsapi.web.nhl.com/api/v1/schedule"
    assert mock.params["teamId"] == "8"
    assert mock.params["startDate"] == "2018-01-01"
    assert mock.params["endDate"] == "2018-06-01"


def test_schedule_bad_args():
    mock = MockClient()
    api = NHLAPI(mock)
    with pytest.raises(ValueError):
        api.schedule(date=date.today(), start_date=date(2018, 1, 1), end_date=date(2018, 6, 1))


def test_standings_season():
    mock = MockClient()
    api = NHLAPI(mock)
    api.standings(expand="foo", season=Season(2017))

    assert mock.url == "https://statsapi.web.nhl.com/api/v1/standings/byLeague"
    assert mock.params["expand"] == "foo"
    assert mock.params["season"] == "20172018"


def test_standings_date():
    mock = MockClient()
    api = NHLAPI(mock)
    api.standings(expand="foo", date=date(2017, 1, 1))

    assert mock.url == "https://statsapi.web.nhl.com/api/v1/standings/byLeague"
    assert mock.params["expand"] == "foo"
    assert mock.params["date"] == "2017-01-01"


def test_standings_bad_args():
    mock = MockClient()
    api = NHLAPI(mock)
    with pytest.raises(ValueError):
        api.standings(date=date.today(), season=Season(end=2018))
