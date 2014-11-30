__author__ = 'Robert W. Perkins'


import pytest
from ticker import TickerInc


def set_up():
    #For inits where a folio file exists
    investment = 10000.0
    inc_id = 10001
    corp_name = "Test Corp"
    pri_shares = 1000
    pub_shares = 100
    ticker_id = 20001
    user_name = 'First User'
    my_corp = TickerInc(investment, inc_id, corp_name, pri_shares, pub_shares, ticker_id, user_name)
    return my_corp


def set_up2():
    #Different ticker_id for case where folio file does not exist
    investment = 10000.0
    inc_id = 10002
    corp_name = "Other Test Corp"
    pri_shares = 1000
    pub_shares = 100
    ticker_id = 20045
    user_name = 'Second User'
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


def test_read_todict():
    #Make sure 20001.txt is present and contains the string version of the assert before running this test
    my_corp = set_up()
    assert my_corp.ticker_folio == {'Scrub Dub': 15, 'Drone Pies': 30, 'Tweet Proxy': 25, 'Robo Nanny': 100}



def test_write_fromdict():
    #make sure 20045.txt is not present before running this test (should be a way to automate this)
    my_corp = set_up2()
    assert my_corp.ticker_folio == {}
    assert my_corp.folio_path.is_file()