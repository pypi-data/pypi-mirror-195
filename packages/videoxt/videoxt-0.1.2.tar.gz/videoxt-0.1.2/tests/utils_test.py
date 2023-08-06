import pytest

from videoxt.extractors import utils


def test_timestamp_to_seconds():
    assert utils.timestamp_to_seconds("1") == 1
    assert utils.timestamp_to_seconds("1:2") == 62
    assert utils.timestamp_to_seconds("1:2:3") == 3723
    assert utils.timestamp_to_seconds("1:2:3:4") == 93564