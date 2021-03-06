from __future__ import unicode_literals
from pathlib import *
import json


__author__ = 'Robert W. Perkins'


def read_folio(ticker_id):
    #Read txt file at location confirmed by get_folio, then create and return dict object
    lit_path = '{unique_id}{f_ext}'.format(unique_id=ticker_id, f_ext='.txt')
    with open(lit_path, 'r') as file_handle:
        return json.load(file_handle)


def write_folio(ticker_id, folio_dict):
    #Take folio dict object, convert to string, and write to folio file
    lit_path = '{unique_id}{f_ext}'.format(unique_id=ticker_id, f_ext='.txt')
    with open(lit_path, 'w') as file_handle:
        return json.dump(folio_dict, file_handle)


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
    #Read mem_incs file, then create and return dict object with ticker
    lit_path = '{f_name}{f_ext}'.format(f_name='mem_incs', f_ext='.txt')
    with open(lit_path, 'r') as file_handle:
        return json.load(file_handle)


def write_memberincs(memincs_dict):
    lit_path = '{f_name}{f_ext}'.format(f_name='mem_incs', f_ext='.txt')
    with open(lit_path, 'w') as file_handle:
        return json.dump(memincs_dict, file_handle)


def read_closeprice():
    #Read mem_incs file, then create and return dict object
    lit_path = '{f_name}{f_ext}'.format(f_name='close_price', f_ext='.txt')
    with open(lit_path, 'r') as file_handle:
        return json.load(file_handle)


def write_closeprice(closeprice_dict):
    lit_path = '{f_name}{f_ext}'.format(f_name='close_price', f_ext='.txt')
    with open(lit_path, 'w') as file_handle:
        return json.dump(closeprice_dict, file_handle)


def read_opensellorders():
    #Read open_sellorders file into dict, return list of TickerOrder objects
    lit_path = '{f_name}{f_ext}'.format(f_name='open_sellorders', f_ext='.txt')
    with open(lit_path, 'r') as file_handle:
        order_dict = json.load(file_handle)
    return [SellOrder(i, order_dict[i][0], order_dict[i][1], order_dict[i][2]) for i in order_dict]


def write_opensellorders(opensellorders_list):
    #Read components from list of TickerOrder objects to dict, then write dict to open_orders.txt
    openorders_dict = {opensellorders_list[i].owner: [opensellorders_list[i].corp, opensellorders_list[i].price,
                                                      opensellorders_list[i].num_4sale] for i in opensellorders_list}
    lit_path = '{f_name}{f_ext}'.format(f_name='open_sellorders', f_ext='.txt')
    with open(lit_path, 'w') as file_handle:
        return json.dump(openorders_dict, file_handle)


def read_openbuyorders():
    #Read open_orders file into dict, return list of TickerOrder objects
    lit_path = '{f_name}{f_ext}'.format(f_name='open_buyorders', f_ext='.txt')
    with open(lit_path, 'r') as file_handle:
        order_dict = json.load(file_handle)
    return [BuyOrder(i, order_dict[i][0], order_dict[i][1], order_dict[i][2]) for i in order_dict]


def write_openbuyorders(openorders_list):
    #Read components from list of TickerOrder objects to dict, then write dict to open_orders.txt
    openorders_dict = {openorders_list[i].owner: [openorders_list[i].corp, openorders_list[i].price,
                                                  openorders_list[i].num_4sale] for i in openorders_list}
    lit_path = '{f_name}{f_ext}'.format(f_name='open_buyorders', f_ext='.txt')
    with open(lit_path, 'w') as file_handle:
        return json.dump(openorders_dict, file_handle)


def load_users():
    #
    pass


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
    def __init__(self, init_investment, inc_id, corp_name, pri_shares, pub_shares, ticker_id, user_name, my_market):
        #Extend TickerUser class with methods and attribs of a company
        self.init_investment = init_investment
        self.corp_name = corp_name
        self.inc_id = inc_id
        self.ticker_closeprice = my_market.close_price[unicode(inc_id)]
        self.ticker_dayavg_price = my_market.dayavg_price[unicode(inc_id)]
        self.ticker_dayvolume = my_market.dayvolume[unicode(inc_id)]
        self.pri_shares = pri_shares
        self.pub_shares = pub_shares
        super(TickerInc, self).__init__(ticker_id, user_name)

    @property
    def value(self):
        # Return a simple valuation based on public and private share value

        #  assumes public share price and private share price are the same
        #  May add something more tricky later (e.g. discounted cash flow analogs)
        return float(self.ticker_closeprice) * (self.pri_shares + self.pub_shares) - self.init_investment


class TickerMarket(object):

    def __init__(self):
        # Read list of registered incs, get yesterday's closing prices, set initial daily average price to
        # yesterday's close, set daily volume to zero, and read open_orders.txt into a list of TickerOrder objects
        self.member_incs = read_memberincs()
        self.close_price = read_closeprice()
        self.dayavg_price = self.close_price
        self.dayvolume = {i: 0 for i in self.member_incs.iterkeys()}
        self.open_buyorderlist = read_openbuyorders()
        self.open_sellorderlist = read_opensellorders()

    def has_sellorder(self, corp, price):
        # Return true if a sell order exists in open_orderlist at or below the provided price for the given company
        good_offer = False
        for i in self.open_sellorderlist:
            if i.corp == corp and i.price <= price:
                good_offer = True
                break
        return good_offer

    def best_sellprice(self, corp, price):
        # Return the best price available for the given company, if a sell order for that company exists
        if self.has_sellorder(corp, price):
            best_price = price
            for i in self.open_sellorderlist:
                if i.corp == corp and i.price <= best_price:
                    best_price = i.price
            return best_price
        else:
            return None

    def has_buyorder(self, corp, price):
        # Return true if a buy order exists in open_orderlist at or above the provided price for the given company
        good_offer = False
        for i in self.open_buyorderlist:
            if i.corp == corp and i.price >= price:
                good_offer = True
                break
        return good_offer

    def best_buyprice(self, corp, price):
        # Return the best price available for the given company, if a buy order for that company exists
        if self.has_sellorder(corp, price):
            best_price = price
            for i in self.open_buyorderlist:
                if i.corp == corp and i.price >= best_price:
                    best_price = i.price
            return best_price
        else:
            return None

    def execute_buyorder(self, new_buyorder):
        purchase_remaining = new_buyorder.quant
        while self.has_buyorder(new_buyorder.corp, new_buyorder.price):
            pass


class TickerOrder(object):

    def __init__(self, owner, corp, price, quant):
        self.owner = owner
        self.corp = corp
        self.price = price
        self.quant = quant


class BuyOrder(TickerOrder):
    pass


class SellOrder(TickerOrder):
    pass

