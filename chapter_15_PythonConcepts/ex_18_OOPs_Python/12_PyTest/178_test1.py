# 178_test1.py
# Pytest test using a custom marker (@pytest.mark.reg) to tag a regression test.
# The assertion 3 == 4 is false, so this test is expected to fail.
import pytest

@pytest.mark.reg
def test_check():
    assert 3 == 4

# More complex: parametrized tests, expected failures and exception checks -
# the pytest features that replace writing the same test many times.
@pytest.mark.parametrize("a, b, expected", [
    (1, 2, 3),
    (2, 2, 4),
    (10, -5, 5),
])
def test_add(a, b, expected):
    assert a + b == expected


@pytest.mark.parametrize("text, is_valid", [
    ("pramod@example.com", True),
    ("not-an-email", False),
    ("", False),
])
def test_email_validation(text, is_valid):
    assert ("@" in text and "." in text) == is_valid


def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("cannot divide by zero")
    return a / b


def test_divide():
    assert divide(10, 2) == 5
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)


@pytest.mark.skip(reason="not implemented yet")
def test_later():
    assert True


@pytest.mark.xfail(reason="known bug")
def test_known_bug():
    assert 1 == 2