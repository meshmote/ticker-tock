from __future__ import unicode_literals
from pathlib import *
import json


__author__ = 'Robert W. Perkins'


def read_folio(ticker_id):
    #Read txt file at location confirmed by get_folio, then create and return dict object
    lit_path = '{unique_id}{f_ext}'.format(unique_id=ticker_id, f_ext='.txt')
    return json.load(open(lit_path))


def write_folio(ticker_id, folio_dict):
    #Take folio dict object, convert to string, and write to folio file
    lit_path = '{unique_id}{f_ext}'.format(unique_id=ticker_id, f_ext='.txt')
    return json.dump(folio_dict, open(lit_path, 'w'))


def get_folio(path, ticker_id):
    #Use Path object to determine if folio file exists and pass ticker_id to read or write method
    #If folio file does not exist, write an empty folio file
    if path.is_file():
        return read_folio(ticker_id)
    else:
        folio_dict = {}
        write_folio(ticker_id, folio_dict)
        return folio_dict


def read_memberincs():
    #Read mem_incs file, then create and return dict object
    lit_path = '{f_name}{f_ext}'.format(f_name='mem_incs', f_ext='.txt')
    return json.load(open(lit_path))


def write_memberincs(memincs_dict):
    lit_path = '{f_name}{f_ext}'.format(f_name='mem_incs', f_ext='.txt')
    return json.dump(memincs_dict, open(lit_path, 'w'))


def read_closeprice():
    #Read mem_incs file, then create and return dict object
    lit_path = '{f_name}{f_ext}'.format(f_name='close_price', f_ext='.txt')
    return json.load(open(lit_path))


def write_closeprice(closeprice_dict):
    lit_path = '{f_name}{f_ext}'.format(f_name='close_price', f_ext='.txt')
    return json.dump(closeprice_dict, open(lit_path, 'w'))


class TickerUser(object):

    def __init__(self, ticker_id, user_name):
        #Define basic user attributes and transaction methods
        self._ticker_id = ticker_id
        self.user_name = user_name
        self.folio_path = Path('{cur_dir}{unique_id}{f_ext}'.format
                               (cur_dir="./", unique_id=self.ticker_id, f_ext='.txt'))
        self.ticker_folio = get_folio(self.folio_path, self.ticker_id)

    # ticker_id set up as property for later addition of unique id generation
    @property
    def ticker_id(self):
        return self._ticker_id

    @ticker_id.setter
    def ticker_id(self, value):
        self._ticker_id = value


class TickerInc(TickerUser):
    def __init__(self, init_investment, incorp_id, corp_name, pri_shares, pub_shares, ticker_id, user_name, my_market):
        #Extend TickerUser class with methods and attribs of a company
        self.init_investment = init_investment
        self.corp_name = corp_name
        self.incorp_id = incorp_id
        self.ticker_closeprice = my_market.close_price[unicode(incorp_id)]
        self.ticker_dayavg_price = my_market.dayavg_price[unicode(incorp_id)]
        self.ticker_dayvolume = my_market.dayvolume[unicode(incorp_id)]
        self.pri_shares = pri_shares
        self.pub_shares = pub_shares
        super(TickerInc, self).__init__(ticker_id, user_name)

    @property
    def value(self):
        #Return a simple valuation based on public and private share value

        #  assumes public share price and private share price are the same
        #  May add something more tricky later (e.g. discounted cash flow analogs)
        return float(self.ticker_closeprice) * (self.pri_shares + self.pub_shares) - self.init_investment


class TickerMarket(object):

    def __init__(self):
        #Read list of registered incs, get yesterday's closing prices, set initial daily average price to
        #yesterday's close, and set daily volume to zero
        self.member_incs = read_memberincs()
        self.close_price = read_closeprice()
        self.dayavg_price = self.close_price
        self.dayvolume = {i: 0 for i in self.member_incs.iterkeys()}