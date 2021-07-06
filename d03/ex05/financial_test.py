import re
import pytest
from financial import financial


@pytest.fixture
# Test Total revenue
def test():
    return financial('MSFT', 'Total Revenue')


# Test wrong ticker
def test1():
    with pytest.raises(ValueError, match='Wrong ticker'):
        financial('TICKER', 'Total Revenue')


# Test error with row
def test2():
    with pytest.raises(ValueError, match='Error with row'):
        financial('MSFT', 'rowerror')


# Test type return
def test3(test):
    assert isinstance(test, tuple)


# Test len return
def test4(test):
    assert len(test) == 6


# Test type elements return
def test5(test):
    for elem in test:
        assert isinstance(elem, str)


# Test row name return
def test6(test):
    assert test[0] == 'Total Revenue'


# Test correct values return
def test8(test):
    for elem in test[1:]:
        assert re.match(r'\d{2,3},\d{3},000', elem)
