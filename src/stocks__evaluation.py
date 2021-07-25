    # -*- coding: utf-8 -*-
import time
import random
import selenium_ctrl
import change_tracker
import interrupter_thread
import global_page_paths as gpp

from datetime import datetime
from db_engine import DbEngine
from optparse import OptionParser
from pandas_datareader import data

from smsapi.client import SmsApiPlClient

def read_stock_data(source, symbol,
                    start_date='1/1/2015',
                    end_date=datetime.today().strftime('%d/%m/%Y')):
    stock_data = data.DataReader(symbol, data_source=source,
                                start=start_date,
                                end=end_date)
    return stock_data.reset_index()

def get_one_of_value(browser, xpath1, xpath2):
    symbol_lower = None
    value = None
    if browser.check_element_by_xpath(xpath1):
        symbol_lower, value = browser.get_element_by_xpath(xpath1)
    elif browser.check_element_by_xpath(xpath2):
        symbol_lower, value = browser.get_element_by_xpath(xpath2)
        
    return symbol_lower, value

def get_one_of_value_global(browser, xpath1, xpath2):
    symbol_lower = None
    value = None
    if browser.check_element_by_xpath(xpath1):
        symbol_lower, value = browser.get_element_by_xpath_global(xpath1)
    elif browser.check_element_by_xpath(xpath2):
        symbol_lower, value = browser.get_element_by_xpath_global(xpath2)

    return symbol_lower, value

def get_stooq_data(mdb_engine):

    #username="MP ctw"
    #token="NmqSXibumJiWI3iRStf3dvXdwURtaarc5PVPGODH"
    #client=SmsApiPlClient(access_token=token)
    #send_results = client.sms.send(to="694927941", message="Hello ctw")
    #for result in send_results:
    #    print(result.id, result.points, result.error)

    stop_processing = False
    #interrupter = interrupter_thread.InterrupterThread(stop_processing)
    #interrupter.start()

    tracker_thread = change_tracker.ChangeTracker(mdb_engine)
    tracker_thread.start()

    #start selenium thread
    browser = selenium_ctrl.SeleniumCtrl()
    browser.start()
    browser.join()

    selenium_ctrl.connect()

    for tab in range(1,3,1):
        try:
            print("TAB {}".format(tab))
            url ='https://stooq.pl/t/tr/?m=2&l=' + str(tab)
            browser.new_tab_global(url, tab)
            time.sleep(random.randint(1,3))
        except ConnectionError:
            selenium_ctrl.connect()
            continue

    while True:
        try:
            print("SWITCH TAB GLOBAL")
            browser.switch_tab_global()
            for index in range(1, 50, 1):
                _, code = get_one_of_value_global(browser, gpp.get_symbol(str(index)), str(index))
                _, change = get_one_of_value_global(browser, gpp.get_change(str(index)), str(index))
                #print("Instrument: " + code.text + " change: " + change.text)
                if change and change.text:
                    print("Instrument: " + code.text + " change: " + change.text)
                    change = float(change.text.strip(" %"))
                    if change > 5.0 or change < -5.0:
                        tracker_thread.add_to_be_monitored(code)
            time.sleep(random.randint(2, 4))
        except KeyboardInterrupt:
            break

    tracker_thread.set_interrupt(True)
    browser.close()


def create_db_connection():
    connection_string = "postgresql://ctw_user:gumtree321@localhost:5432/ctw_db"
    mdb_engine = DbEngine(connection_string)
    return mdb_engine.get_instance()

if __name__ == "__main__":
    parser = OptionParser("Options for stocks evaluation")

    parser.add_option("-s", "--source", type=str,
                      help="Source of the trade data", dest="data_source")
    parser.add_option("-c", "--company", type=str,
                      help="Company symbol (__all__ means all companies)",
                      dest="company_sym")
    parser.add_option('-m', "--margin", type=int,
                      help="Margin for moving average", dest='margin')
    parser.add_option('-l', "--lower_trend", type=int,
                      help="Lower trading days margin for moving average \
                            trend strategy", dest="lower_trend")
    parser.add_option('-u', "--upper_trend", type=int,
                      help="Upper trading days margin for moving average \
                            trend strategy", dest="upper_trend")

    
    (options, args) = parser.parse_args()
    mdb_engine = create_db_connection()
    get_stooq_data(mdb_engine)
    #plot_finance() # not working - not enough parameters to unpack in stock data
    #plot_excersises_various()
    #plot_excersises_boxplot()
    #plot_excersises_hist()
    #plot_excersises_scattered()
    #plot_excersises_2graph()
    #plot_excersises_2axis()
    #plots_excersises_simple()
    #evaluate_stocks(options)
    #calculate_implied_volat()
    #bsm_analytical()
    #monte_carlo_python()
    #monte_carlo_scipy()
    #monte_carlo_scipy_full_vectorization()
