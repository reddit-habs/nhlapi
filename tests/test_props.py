from nhlapi.props import PropDict, PropList, wrap

d = {"name": "abcdef", "info": {"age": 28, "height": 180}, "qualities": ["nice", "funny"]}
a = [1, dict(), []]
d = wrap(d)
a = wrap(a)


def test_wrap():
    assert isinstance(d, PropDict)
    assert isinstance(a, PropList)
    assert isinstance(wrap(3), int)


def test_dict_access():
    assert d.name == "abcdef"
    assert d["name"] == "abcdef"
    assert d.get("name") == "abcdef"


def test_list_access():
    assert a[0] == 1
    assert a.get(0) == 1


def test_dict_wrap_dict():
    assert isinstance(d.info, PropDict)
    assert isinstance(d["info"], PropDict)
    assert isinstance(d.get("info"), PropDict)


def test_list_wrap_dict():
    assert isinstance(a[1], PropDict)
    assert isinstance(a.get(1), PropDict)


def test_dict_wrap_list():
    assert isinstance(d.qualities, PropList)
    assert isinstance(d["qualities"], PropList)
    assert isinstance(d.get("qualities"), PropList)


def test_list_wrap_list():
    assert isinstance(a[2], PropList)
    assert isinstance(a.get(2), PropList)


def test_dict_contains():
    assert "info" in d


def test_list_contains():
    assert 1 in a


def test_dict_iter():
    assert set(iter(d)) == set(["name", "info", "qualities"])


def test_list_iter():
    vals = list(iter(a))
    assert vals[0] == 1
    assert isinstance(vals[1], PropDict)
    assert isinstance(vals[2], PropList)


def test_dict_len():
    assert len(d) == 3


def test_list_len():
    assert len(a) == 3


def test_dict_keys():
    assert set(d.keys()) == set(["name", "info", "qualities"])


def test_dict_values():
    vals = list(d.values())
    assert "abcdef" in vals
    assert any(isinstance(x, PropDict) for x in vals)
    assert any(isinstance(x, PropList) for x in vals)


def test_dict_items():
    keys = set()
    vals = []
    for key, val in d.items():
        keys.add(key)
        vals.append(val)
    assert keys == set(["name", "info", "qualities"])
    assert "abcdef" in vals
    assert any(isinstance(x, PropDict) for x in vals)
    assert any(isinstance(x, PropList) for x in vals)


def test_list_reversed():
    vals = list(reversed(a))
    assert vals[2] == 1
    assert isinstance(vals[1], PropDict)
    assert isinstance(vals[0], PropList)
