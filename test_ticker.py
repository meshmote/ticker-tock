from __future__ import unicode_literals
import pytest
from ticker import *


__author__ = 'Robert W. Perkins'


def tickermarket_setup():
    t_market = TickerMarket()
    return t_market


def tickerinc_setup(my_market):
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


def tickerinc_setup2(my_market):
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
    #Setup to test TickerInc initialization with an existing TickerMarket object
    investment = 10000.0
    inc_id = 10012
    corp_name = "Tweet Proxy"
    pri_shares = 1000
    pub_shares = 100
    ticker_id = 20045
    user_name = 'Second User'
    my_corp = TickerInc(investment, inc_id, corp_name, pri_shares, pub_shares, ticker_id, user_name, my_market)
    return my_corp


def test_object_exists():
    t_market = tickermarket_setup()
    my_corp = tickerinc_setup(t_market)
    assert isinstance(my_corp, TickerInc)


def test_attrib_inits():
    t_market = tickermarket_setup()
    my_corp = tickerinc_setup(t_market)
    assert my_corp.value == 36200.0
    assert my_corp.inc_id == 10001
    assert my_corp.ticker_id == 20001
    assert my_corp.corp_name == 'Test Corp'
    assert my_corp.pri_shares == 1000
    assert my_corp.pub_shares == 100
    assert my_corp.user_name == 'First User'


def test_read_todict():
    # Test that folio.txt file reads correctly into dict attrib
    # Make sure 20001.txt is present and contains the string version of the assert before running this test
    t_market = tickermarket_setup()
    my_corp = tickerinc_setup(t_market)
    assert my_corp.ticker_folio == {'10010': 15, '10011': 30, '10012': 25, '10013': 100}


def test_write_fromdict():
    # Test that a blank folio.txt is written if no folio file present
    # make sure 20045.txt is not present before running this test (should be a way to automate this)
    t_market = tickermarket_setup()
    my_corp = tickerinc_setup2(t_market)
    assert my_corp.ticker_folio == {}
    assert my_corp.folio_path.is_file()


def test_ticker_marketinit():
    # Check for accurate reading of mem_incs.txt and close_price.txt into dict attribs, correct setting of initial
    # dayavg prices to previous days closing prices, and initializing of dayvolume to zero
    t_market = tickermarket_setup()
    assert isinstance(t_market, TickerMarket)
    assert t_market.member_incs == {"10010": "Scrub Dub", "10011": "Drone Pies", "10012": "Tweet Proxy",
                                    "10013": "Robo Nanny", "10001": "Test Corp", "10002": "Other Test Corp"}
    assert t_market.close_price == {"10010": "10.0", "10011": "35.0", "10012": "120.0", "10013": "5.0", "10001": "42.0",
                                    "10002": "20.0"}
    assert t_market.dayavg_price == {"10010": "10.0", "10011": "35.0", "10012": "120.0", "10013": "5.0",
                                     "10001": "42.0", "10002": "20.0"}
    assert t_market.dayvolume == {"10010": 0, "10011": 0, "10012": 0, "10013": 0, "10001": 0, "10002": 0}

    # Check that open_orders.txt has been translated correctly into list of TickerOrder objects
    assert t_market.open_sellorderlist[0].corp == "10001"
    assert t_market.open_sellorderlist[1].owner == "20003"
    assert t_market.open_sellorderlist[2].price == 50
    assert t_market.open_sellorderlist[0].num_4sale == 35


def test_tickermarket_methods():
    t_market = tickermarket_setup()

    # Test no sell order for this company
    assert t_market.has_sellorder("11111", 45) is False

    # Test above, between, and below existing order prices
    assert t_market.has_sellorder("10010", 10) is False
    assert t_market.has_sellorder("10010", 27) is True
    assert t_market.has_sellorder("10010", 100) is True

    # Test exactly on existing order prices
    assert t_market.has_sellorder("10010", 50) is True
    assert t_market.has_sellorder("10010", 45) is True
    assert t_market.has_sellorder("10010", 24) is True

    # Test above and below best price
    assert t_market.best_sellprice("10010", 27) == 24
    assert t_market.best_sellprice("10010", 10) is None
    assert t_market.best_sellprice("10010", 100) is 24

    # Test no price for this company
    assert t_market.best_sellprice("11111", 100) is None


def test_corpinit2market():
    # Check that initialized TickerIncs get their initial price information correctly from the TickerMarket object
    t_market = tickermarket_setup()
    my_corp = tickerinc_setup3(t_market)
    assert my_corp.ticker_closeprice == unicode(120.0)
    assert my_corp.ticker_dayavg_price == unicode(120.0)
    assert my_corp.ticker_dayvolume == 0


def test_buyorder():

    user_db = load_users()
    t_market = tickermarket_setup()
    new_buyorder = BuyOrder("20020", "10200", 27, 100)
    t_market.execute_buyorder(new_buyorder)
    for i in user_db:
        if user_db[i].ticker_id == "20020":
            assert user_db[i].ticker_folio["10200"] == 1000
        if user_db[i].ticker_id == "20021":
            assert user_db[i].ticker_folio["10200"] == 500


### Add data structure and methods for sell, buy orders, sale transactions, spot price computation,
### and end of trading actions
### Add data structures for product and feature descriptions (for other users to read)
### Add upvote, downvote structures for private to public transition
### Add data structures for cash management system