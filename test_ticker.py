__author__ = 'Robert W. Perkins'


import pytest
from ticker import TickerInc


def set_up():
    investment = 10000.0
    inc_id = 10001
    corp_name = "Test Corp"
    pri_shares = 1000
    pub_shares = 100
    ticker_id = 20001
    user_name = 'First User'
    my_corp = TickerInc(investment, inc_id, corp_name, pri_shares, pub_shares, ticker_id, user_name)
    return my_corp


def test_object_exists():
    my_corp = set_up()
    assert isinstance(my_corp, TickerInc)


def test_attrib_inits():
    my_corp = set_up()
    assert my_corp.value == 1000.0
    assert my_corp.incorp_id == 10001
    assert my_corp.ticker_id == 20001
    assert my_corp.corp_name == 'Test Corp'
    assert my_corp.pri_shares == 1000
    assert my_corp.pub_shares == 100
    assert my_corp.user_name == 'First User'



#def test_setter():
    #my_corp = set_up()
    #my_corp.value = 20000.0
    #assert my_corp.value == 20000.0