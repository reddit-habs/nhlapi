import pytest
from nhlapi.utils import GameId, GameKind, IUrlParam, Season


def test_season_begin():
    x = Season(begin=2017)
    assert x.begin == 2017
    assert x.end == 2018


def test_season_end():
    x = Season(end=2018)
    assert x.begin == 2017
    assert x.end == 2018


def test_season_both():
    x = Season(2017, 2018)
    assert x.begin == 2017
    assert x.end == 2018


def test_season_none():
    with pytest.raises(ValueError):
        Season()


def test_game_code():
    x = GameId(Season(end=2018), 1000)
    assert isinstance(x, IUrlParam)
    assert x.to_url_param() == "2017021000"
    assert x.kind == GameKind.REGULAR
