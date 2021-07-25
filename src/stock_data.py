# -*- coding: utf-8 -*-
from decimal import Decimal
from datetime import datetime
import re

class StockDataWebElems(object):
    def __init__(self):
        self.symbol = None
        self.last_value = None
        self.change_value = None
        self.change_perc = None
        self.date_value = None
        self.time_value = None
        self.high_value = None
        self.low_value = None
        self._52w_change_value = None
        self._52w_change_perc = None
        self._52w_high = None
        self._52w_low = None
        self.open_value = None
        self.prev_value = None
        self.bid_value = None
        self.bid_amount = None
        self.ask_value = None
        self.ask_amount = None
        self.volume_value = None
        self.turnover_value = None
        self.open_int_value = None
        self.no_trades_value = None
        self._52w_change_value = None
        self._52w_change_perc = None
        self._52w_high = None
        self._52w_low = None
        self._52w_all = None
        self.open_value = None
        self.prev_value = None
        self.bid_value = None
        self.bid_amount = None
        self.ask_value = None
        self.ask_amount = None
        self.volume_value = None
        self.turnover_value = None
        self.open_int_value = None
        self.no_trades_value = None

    def __str__(self):
        return " - Symbol: {symbol}\n" \
               " - Last value: {last_value}\n" \
               " - Change value: {change_value}\n" \
               " - Change percentage: {change_perc}\n" \
               " - Date value: {date_value}\n" \
               " - Time value: {time_value}\n" \
               " - High value: {high_value}\n" \
               " - Low value: {low_value}\n" \
               " - Change value in 52w: {_52w_change_value}\n" \
               " - Change perc in 52w: {_52w_change_perc}\n" \
               " - Change in 52w (all): {_52w_all}\n" \
               " - Open value: {open_value}\n" \
               " - Previous value: {prev_value}\n" \
               " - Bid value: {bid_value}\n" \
               " - Bid amount: {bid_amount}\n" \
               " - Ask value: {ask_value}\n" \
               " - Ask amount: {ask_amount}\n" \
               " - Turnover: {turnover}\n" \
               " - Open int value: {open_int}\n" \
               " - Number of trades: {no_of_trades}\n".format(symbol=self.symbol if self.symbol else "",
                                                            last_value=self.last_value.text if self.last_value else "",
                                                            change_value=self.change_value.text if self.change_value else "",
                                                            change_perc=self.change_perc.text if self.change_perc else "",
                                                            date_value=self.date_value.text if self.date_value else "",
                                                            time_value=self.time_value.text if self.time_value else "",
                                                            high_value=self.high_value.text if self.high_value else "",
                                                            low_value=self.low_value.text if self.low_value else "",
                                                            _52w_change_value=self._52w_change_value.text if self._52w_change_value else "",
                                                            _52w_change_perc=self._52w_change_perc.text if self._52w_change_perc else "",
                                                            _52w_all=self._52w_all.text if self._52w_all else "",
                                                            open_value=self.open_value.text if self.open_value else "",
                                                            prev_value=self.prev_value.text if self.prev_value else "",
                                                            bid_value=self.bid_value.text if self.bid_value else "",
                                                            bid_amount=self.bid_amount.text if self.bid_amount else "",
                                                            ask_value=self.ask_value.text if self.ask_value else "",
                                                            ask_amount=self.ask_amount.text if self.ask_amount else "",
                                                            turnover=self.turnover_value.text if self.turnover_value else "",
                                                            open_int=self.open_int_value.text if self.open_int_value else "",
                                                            no_of_trades=self.no_trades_value.text if self.no_trades_value else "")

    def set_symbol(self, symbol):
        self.symbol = symbol


def get_multiplier(web_elem):
    multiplier = 1
    if web_elem.text.endswith('k'):
        multiplier = 1000
    elif web_elem.text.endswith('m'):
        multiplier = 1000000

    return multiplier

# sqlalchemy object -> to be transform
class StockData(object):
    def __init__(self, stock_data_web_elem):
        if stock_data_web_elem.symbol:
            self.symbol = stock_data_web_elem.symbol.strip()
        else:
            self.symbol = "Unknown symbol"

        if stock_data_web_elem.last_value and stock_data_web_elem.last_value.text:
            self.last_value = Decimal(stock_data_web_elem.last_value.text.strip(" zł"))
        else:
            self.last_value = 0

        if stock_data_web_elem.change_value and stock_data_web_elem.change_value.text:
            self.change_value = Decimal(stock_data_web_elem.change_value.text)
        else:
            self.change_value = 0
        self.change_perc = Decimal(stock_data_web_elem.change_perc.text.strip("()%")) if stock_data_web_elem.change_perc and stock_data_web_elem.change_perc.text else 0

        self.datetime_value = datetime.now()
        if stock_data_web_elem.date_value and stock_data_web_elem.time_value and stock_data_web_elem.date_value.text and stock_data_web_elem.time_value.text:
            date_string = stock_data_web_elem.date_value.text + " " + stock_data_web_elem.time_value.text.split(".")[0]
            self.datetime_value = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")

        self.high_value = Decimal(stock_data_web_elem.high_value.text) if stock_data_web_elem.high_value and stock_data_web_elem.high_value.text else 0
        self.low_value = Decimal(stock_data_web_elem.low_value.text) if stock_data_web_elem.low_value and stock_data_web_elem.low_value.text else 0
        self._52w_change_value = Decimal(stock_data_web_elem._52w_change_value.text) if stock_data_web_elem._52w_change_value and stock_data_web_elem._52w_change_value.text else 0
        self._52w_change_perc = Decimal(stock_data_web_elem._52w_change_perc.text.strip("()%")) if stock_data_web_elem._52w_change_perc and  stock_data_web_elem._52w_change_perc.text else 0

        self._52w_high = 0
        self._52w_low = 0
        if stock_data_web_elem._52w_all:
            # _52_regex_str = "[0-9a-zA-Z]+\s+_52w_low: 52W High\/Low\s+([0-9\.]+)\s+([0-9\.]+)"
            _52_regex_str = "52W High\/Low\s+([0-9\.]+)\s+([0-9\.]+)"
            _52_regex = re.compile(_52_regex_str)
            _52_regex_res = re.search(_52_regex, stock_data_web_elem._52w_all.text)
            if _52_regex_res and len(_52_regex_res.groups()) == 2:
                self._52w_high = Decimal(_52_regex_res.group(1))
                self._52w_low = Decimal(_52_regex_res.group(2))

        self.open_value = Decimal(stock_data_web_elem.open_value.text) if stock_data_web_elem.open_value and stock_data_web_elem.open_value.text  else 0
        self.prev_value = Decimal(stock_data_web_elem.prev_value.text) if stock_data_web_elem.prev_value and stock_data_web_elem.prev_value.text else 0

        self.bid_value = 0
        if stock_data_web_elem.bid_value and stock_data_web_elem.bid_value.text:
            multiplier = get_multiplier(stock_data_web_elem.bid_value)
            self.bid_value = Decimal(stock_data_web_elem.bid_value.text.strip(' xkm')) * multiplier

        self.bid_amount = 0
        if stock_data_web_elem.bid_amount and stock_data_web_elem.bid_amount.text:
            multiplier = get_multiplier(stock_data_web_elem.bid_amount)
            self.bid_amount = Decimal(stock_data_web_elem.bid_amount.text.strip(' xkm')) * multiplier

        self.ask_value = 0
        if stock_data_web_elem.ask_value and stock_data_web_elem.ask_value.text:
            multiplier = get_multiplier(stock_data_web_elem.ask_value)
            self.ask_value = Decimal(stock_data_web_elem.ask_value.text.strip(' xkm')) * multiplier

        self.ask_amount = 0
        if stock_data_web_elem.ask_amount and stock_data_web_elem.ask_amount.text:
            multiplier = get_multiplier(stock_data_web_elem.ask_amount)
            self.ask_amount = Decimal(stock_data_web_elem.ask_amount.text.strip(' xkm')) * multiplier

        self.volume_value = 0
        if stock_data_web_elem.volume_value and stock_data_web_elem.volume_value.text:
            multiplier = get_multiplier(stock_data_web_elem.volume_value)
            self.volume_value = Decimal(stock_data_web_elem.volume_value.text.strip(' xkm')) * multiplier

        self.turnover_value = 0
        if stock_data_web_elem.turnover_value and stock_data_web_elem.turnover_value.text:
            multiplier = get_multiplier(stock_data_web_elem.turnover_value)
            self.turnover_value = Decimal(stock_data_web_elem.turnover_value.text.strip(' xkm')) * multiplier

        self.open_int_value = 0
        if stock_data_web_elem.open_int_value and stock_data_web_elem.open_int_value.text:
            multiplier = get_multiplier(stock_data_web_elem.open_int_value)
            #print(stock_data_web_elem.open_int_value)
            self.open_int_value = Decimal(stock_data_web_elem.open_int_value.text.strip(' xkm')) * multiplier

        self.no_trades_value = 0
        if stock_data_web_elem.no_trades_value and stock_data_web_elem.no_trades_value.text:
            #print(stock_data_web_elem.no_trades_value.text)
            multiplier = get_multiplier(stock_data_web_elem.no_trades_value)
            self.no_trades_value = Decimal(stock_data_web_elem.no_trades_value.text.strip(' xkm').replace(' ', '')) * multiplier
