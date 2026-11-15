# test_178.py
# Pytest test using a custom marker (@pytest.mark.reg) to tag a regression test.
# The assertion 3 == 4 is false, so this test is expected to fail.
import pytest

@pytest.mark.reg
def test_check():
    assert 3 == 4