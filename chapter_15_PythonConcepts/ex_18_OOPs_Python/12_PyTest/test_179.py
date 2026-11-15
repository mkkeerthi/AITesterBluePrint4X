# test_179.py
# Basic pytest examples: two passing tests (4 != 5) and one deliberately failing
# test (4 == 5), showing that pytest discovers functions named test_* automatically.
import pytest

def test_positive():
    assert 4 != 5


def test_positive2():
    assert 4 != 5

def test_negative():
    assert 4 == 5
