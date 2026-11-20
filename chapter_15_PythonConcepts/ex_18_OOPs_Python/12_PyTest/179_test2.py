# 179_test2.py
# Basic pytest examples: two passing tests (4 != 5) and one deliberately failing
# test (4 == 5), showing that pytest discovers functions named test_* automatically.
import pytest

def test_positive():
    assert 4 != 5


def test_positive2():
    assert 4 != 5

def test_negative():
    assert 4 == 5

# More complex: fixtures for shared setup/teardown and a class-based test
# group. pytest injects the fixture by matching the parameter name.
import pytest


@pytest.fixture
def sample_user():
    user = {"name": "pramod", "role": "SDET"}
    yield user                  # yield = teardown point
    user.clear()


@pytest.fixture(scope="module")
def settings():
    return {"env": "qa", "timeout": 30}


def test_user_name(sample_user):
    assert sample_user["name"] == "pramod"


def test_user_role(sample_user):
    assert sample_user["role"] == "SDET"


def test_settings(settings):
    assert settings["env"] == "qa"
    assert settings["timeout"] > 0


class TestMath:
    def test_add(self):
        assert 2 + 2 == 4

    def test_multiply(self):
        assert 3 * 3 == 9

    @pytest.mark.parametrize("value", [2, 4, 6])
    def test_even(self, value):
        assert value % 2 == 0
