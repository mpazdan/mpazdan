import threading
import selenium_ctrl
import time
import random
import page_paths as pp
from stock_data import StockDataWebElems
from stock_data import StockData
from db_engine import DbSession
from selenium.common.exceptions import NoSuchElementException

class ChangeTracker(threading.Thread):
    def __init__(self, mdb_engine):
        threading.Thread.__init__(self)
        self.thread_lock = threading.Lock()
        self.mdb_engine = mdb_engine
        self.interrupt_condition = False
        self.to_be_monitored = set()
        self.monitored = set()
        self.browser = None
        self.db_session = None

    def run(self):
        self.browser = selenium_ctrl.SeleniumCtrl()
        self.browser.start()
        self.browser.join()

        self.db_session = DbSession(self.mdb_engine)

        while not self.interrupt_condition:
            new_symbols = self.to_be_monitored - self.monitored
            print ("New SYMBOLS {}".format(new_symbols))
            self.open_new_tabs(new_symbols)
            # should be full run through all tabs before new tab will be opened, but expected that new tabs won't occure too often
            self.monitor_tabs()

        self.browser.close()

    def monitor_tabs(self):
        self.browser.switch_tab()
        try:
            stock_object = StockDataWebElems()

            symbol_lower, stock_object.last_value = self.get_one_of_value(pp.last_xpath1, pp.last_xpath2)
            stock_object.set_symbol(symbol_lower)
            _, stock_object.change_value = self.get_one_of_value(pp.change_value_xpath1, pp.change_value_xpath2)
            _, stock_object.change_perc = self.get_one_of_value(pp.change_perc_xpath1, pp.change_perc_xpath2)
            _, stock_object.date_value = self.get_one_of_value(pp.date_xpath1, pp.date_xpath2)
            _, stock_object.time_value = self.get_one_of_value(pp.time_xpath1, pp.time_xpath2)
            _, stock_object.high_value = self.get_one_of_value(pp.high_xpath1, pp.high_xpath2)
            _, stock_object.low_value = self.get_one_of_value(pp.low_xpath1, pp.low_xpath2)
            _, stock_object._52w_change_value = self.get_one_of_value(pp._52w_change_value_xpath1,
                                                                      pp._52w_change_value_xpath2)
            _, stock_object._52w_change_perc = self.get_one_of_value(pp._52w_change_perc_xpath1,
                                                                     pp._52w_change_perc_xpath2)
            _, stock_object._52w_all = self.get_one_of_value(pp._52w_all_xpath1, pp._52w_all_xpath2)
            _, stock_object.open_value = self.get_one_of_value(pp.open_xpath1, pp.open_xpath2)
            _, stock_object.prev_value = self.get_one_of_value(pp.prev_xpath1, pp.prev_xpath2)
            _, stock_object.bid_value = self.get_one_of_value(pp.bid_value_xpath1, pp.bid_value_xpath2)
            _, stock_object.bid_amount = self.get_one_of_value(pp.bid_amount_xpath1, pp.bid_amount_xpath2)
            _, stock_object.ask_value = self.get_one_of_value(pp.ask_value_xpath1, pp.ask_value_xpath2)
            _, stock_object.ask_amount = self.get_one_of_value(pp.ask_amount_xpath1, pp.ask_amount_xpath2)
            _, stock_object.volume_value = self.get_one_of_value(pp.volume_xpath1, pp.volume_xpath2)
            _, stock_object.turnover_value = self.get_one_of_value(pp.turnover_xpath1, pp.turnover_xpath2)
            _, stock_object.open_int_value = self.get_one_of_value(pp.open_int_xpath1, pp.open_int_xpath2)
            _, stock_object.no_trades_value = self.get_one_of_value(pp.no_trades_xpath1, pp.no_trades_xpath2)

            symbol_lower = symbol_lower if symbol_lower else "Unknown symbol"
            print(symbol_lower + ":\n" + str(stock_object))
            db_object = StockData(stock_object)
            print(db_object)
            self.db_session.persist_tick(db_object)
            print("-----------------------------------")

        except NoSuchElementException:
            pass

        time.sleep(random.randint(2, 4))

    def get_one_of_value(self, xpath1, xpath2):
        symbol_lower = None
        value = None
        if self.browser.check_element_by_xpath(xpath1):
            symbol_lower, value = self.browser.get_element_by_xpath(xpath1)
        elif self.browser.check_element_by_xpath(xpath2):
            symbol_lower, value = self.browser.get_element_by_xpath(xpath2)

        return symbol_lower, value

    def open_new_tabs(self, new_symbols):
        new_symbols = self.new_to_be_monitored()
        for symbol in new_symbols:
            if symbol:
                print("NEW SYMBOL {}".format(symbol))
                try:
                    symbol_lower = symbol.strip().lower()
                    url = 'https://stooq.com/q/?s=' + symbol_lower
                    self.browser.new_tab(url, symbol_lower)
                    self.monitored.add(symbol_lower)
                    time.sleep(random.randint(1, 5))
                except ConnectionError:
                    continue

    def add_to_be_monitored(self, symbol):
        self.thread_lock.acquire()
        self.to_be_monitored.add(symbol.text.lower())
        self.thread_lock.release()

    def new_to_be_monitored(self):
        self.thread_lock.acquire()
        result = self.to_be_monitored - self.monitored
        self.thread_lock.release()
        return result

    def set_interrupt(self, interrupt_condition):
        self.thread_lock.acquire()
        self.interrupt_condition = interrupt_condition
        self.thread_lock.release()
