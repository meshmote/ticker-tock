__author__ = 'Robert W. Perkins'

from pathlib import *
import ast


def read_folio(path):

    with open(path, 'r') as inf:
        return ast.literal_eval(inf.read())


def write_folio(path):

    pass


def get_folio(path):
    if path.is_file():
        return read_folio(path)
    else:
        return write_folio(path)


class TickerUser(object):

    def __init__(self, ticker_id, user_name):
        #Define basic user attributes and transaction methods
        self._ticker_id = ticker_id
        self.user_name = user_name
        self.folio_path = Path('{cur_dir}{unique_id}{f_ext}'.format
                               (cur_dir="./", unique_id=self.ticker_id, f_ext='.txt'))
        self.ticker_folio = get_folio(self.folio_path)

    @property
    def ticker_id(self):
        return self._ticker_id

    @ticker_id.setter
    def ticker_id(self, value):
        self._ticker_id = value


class TickerInc(TickerUser):
    def __init__(self, init_investment, incorp_id, corp_name, pri_shares, pub_shares, ticker_id, user_name):
        #Extend TickerUser class with methods and attribs of a company
        self.init_investment = init_investment
        self.corp_name = corp_name
        self._incorp_id = incorp_id
        self.pri_shares = pri_shares
        self.pub_shares = pub_shares
        self._ticker_price = init_investment / pri_shares
        super(TickerInc, self).__init__(ticker_id, user_name)

    @property
    def value(self):
        #Return a simple valuation based on public and private share value

        #  assumes public share price and private share price are the same
        #  May add something more tricky later (e.g. discounted cash flow analogs)
        return self._ticker_price * (self.pri_shares + self.pub_shares) - self.init_investment

    @property
    def ticker_price(self):
        return self._ticker_price

    @ticker_price.setter
    def ticker_price(self, value):
        self._ticker_price = value

    @property
    def incorp_id(self):
        return self._incorp_id

    @incorp_id.setter
    def incorp_id(self, value):
        self._incorp_id = value


