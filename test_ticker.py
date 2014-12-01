from __future__ import unicode_literals
import pytest
from ticker import *


__author__ = 'Robert W. Perkins'


def tickermarket_setup():
    t_market = TickerMarket()
    return t_market


def tickerinc_setup():
    #For inits where a folio file exists
    investment = 10000.0
    inc_id = 10001
    corp_name = "Test Corp"
    pri_shares = 1000
    pub_shares = 100
    ticker_id = 20001
    user_name = 'First User'
    my_corp = TickerInc(investment, inc_id, corp_name, pri_shares, pub_shares, ticker_id, user_name, my_market)
    return my_corp


def tickerinc_setup2():
    #Different ticker_id for case where folio file does not exist
    investment = 10000.0
    inc_id = 10002
    corp_name = "Other Test Corp"
    pri_shares = 1000
    pub_shares = 100
    ticker_id = 20045
    user_name = 'Second User'
    my_corp = TickerInc(investment, inc_id, corp_name, pri_shares, pub_shares, ticker_id, user_name, my_market)
    return my_corp


def tickerinc_setup3(my_market):
    #Setup to test initialization with an existing market object
    investment = 10000.0
    inc_id = 10012
    corp_name = "Other Test Corp"
    pri_shares = 1000
    pub_shares = 100
    ticker_id = 20045
    user_name = 'Second User'
    my_corp = TickerInc(investment, inc_id, corp_name, pri_shares, pub_shares, ticker_id, user_name, my_market)
    return my_corp


def test_object_exists():
    my_corp = tickerinc_setup()
    assert isinstance(my_corp, TickerInc)


def test_attrib_inits():
    my_corp = tickerinc_setup()
    assert my_corp.value == 1000.0
    assert my_corp.incorp_id == 10012
    assert my_corp.ticker_id == 20001
    assert my_corp.corp_name == 'Tweet Proxy'
    assert my_corp.pri_shares == 1000
    assert my_corp.pub_shares == 100
    assert my_corp.user_name == 'First User'


def test_read_todict():
    #Make sure 20001.txt is present and contains the string version of the assert before running this test
    my_corp = tickerinc_setup()
    assert my_corp.ticker_folio == {'Scrub Dub': 15, 'Drone Pies': 30, 'Tweet Proxy': 25, 'Robo Nanny': 100}


def test_write_fromdict():
    #make sure 20045.txt is not present before running this test (should be a way to automate this)
    my_corp = tickerinc_setup2()
    assert my_corp.ticker_folio == {}
    assert my_corp.folio_path.is_file()


def test_ticker_marketinit():
    t_market = tickermarket_setup()
    assert isinstance(t_market, TickerMarket)
    assert type(t_market.member_incs) is dict
    assert t_market.member_incs == {u'10010': 'Scrub Dub', u'10011': 'Drone Pies', u'10012': 'Tweet Proxy',
                                    u'10013': 'Robo Nanny'}
    assert t_market.close_price == {u'10010': u'10.0', u'10011': u'35.0', u'10012': u'120.0', u'10013': u'5.0'}
    assert t_market.dayavg_price == {u'10010': u'10.0', u'10011': u'35.0', u'10012': u'120.0', u'10013': u'5.0'}
    assert t_market.dayvolume == {u'10010': 0, u'10011': 0, u'10012': 0, u'10013': 0}


def test_corpinit2market():
    t_market = tickermarket_setup()
    my_corp = tickerinc_setup3(t_market)
    assert my_corp.ticker_closeprice == unicode(120.0)
    assert my_corp.ticker_dayavg_price == unicode(120.0)
    assert my_corp.ticker_dayvolume == 0
