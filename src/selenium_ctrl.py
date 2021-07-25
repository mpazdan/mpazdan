# -*- coding: utf-8 -*-
import threading
import requests
import hacked_requester
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException


class SeleniumCtrl(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.driver = None
        self.tab_counter = 0
        self.current_tab = 0
        self.active_tab = 0
        self.symbol_array = dict()
        self.global_tab_counter = 0
        self.global_current_tab = 0
        self.global_active_tab = 0
        self.global_index_array = dict()

        
    def run(self):
        chrome_options = Options()
        #chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_experimental_option("detach", True)
        #chrome_options.add_argument('--proxy-server=null')
        #chrome_options.add_experimental_option("disable-dev-shm-usage", True)
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--profile-directory=Default')
        chrome_options.add_argument("--disable-plugins-discovery");
        #chrome_options.add_argument("--start-maximized")
        #chrome_options.add_argument("--incognito")

        #chrome_options.add_argument("--headless")

        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.delete_all_cookies()
        self.driver.set_window_size(1, 1)
        self.driver.set_window_position(0, 0)

        
    def new_tab(self, url, symbol_lower=None):
        self.driver.execute_script("window.open('about:blank', 'tab{}');".format(str(self.tab_counter)))
        self.driver.switch_to.window("tab{}".format(self.tab_counter))
        self.driver.get(url)
        #print("Tab counter {}, symbol_lower {}".format(self.tab_counter, symbol_lower))
        self.symbol_array[self.tab_counter] = symbol_lower
        self.tab_counter += 1

    def switch_tab(self):
        if not self.tab_counter:
            return
        next_tab_no = self.current_tab % self.tab_counter
        #print("Next tab no: {}".format(next_tab_no))
        self.driver.switch_to.window("tab{}".format(next_tab_no))
        self.active_tab = next_tab_no
        self.current_tab += 1

    def new_tab_global(self, url, index=None):
        self.driver.execute_script("window.open('about:blank', 'tab{}');".format(str(self.global_tab_counter)))
        self.driver.switch_to.window("tab{}".format(self.global_tab_counter))
        self.driver.get(url)
        # print("Tab counter {}, symbol_lower {}".format(self.tab_counter, symbol_lower))
        self.global_index_array[self.global_tab_counter] = index
        self.global_tab_counter += 1


    def switch_tab_global(self):
        next_tab_no = self.global_current_tab % self.global_tab_counter
        #print("Next tab no: {}".format(next_tab_no))
        self.driver.switch_to.window("tab{}".format(next_tab_no))
        self.global_active_tab = next_tab_no
        self.global_current_tab += 1

    def get_element_by_tag_name(self, tag_name):
        if self.active_tab not in self.symbol_array.keys():
            raise Exception("Exceeded symbol list array size")
        return (self.symbol_array[self.active_tab], self.driver.find_element_by_tag_name(tag_name))

    def get_element_by_global_tag_name(self, tag_name):
        if self.global_active_tab not in self.globa_index_array.keys():
            raise Exception("Exceeded symbol list array size")
        return (self.global_index_array[self.active_tab], self.driver.find_element_by_tag_name(tag_name))


    def check_element_by_xpath(self, xpath):
        try:
            self.driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return False
        return True


    def get_element_by_xpath(self, xpath):
        if self.active_tab not in self.symbol_array.keys():
            raise Exception("Exceeded symbol list array size")
        #return (self.symbol_array[self.active_tab], self.driver.find_element_by_xpath(xpath))
        #print("Active tab: {}, symbol {}".format(self.active_tab, self.symbol_array[self.active_tab]))
        return (self.get_active_tab_symbol(), self.driver.find_element_by_xpath(xpath))


    def get_element_by_xpath_global(self, xpath):
        if self.active_tab not in self.global_index_array.keys():
            raise Exception("Exceeded symbol list array size")
        #return (self.symbol_array[self.active_tab], self.driver.find_element_by_xpath(xpath))
        #print("Active tab: {}, symbol {}".format(self.active_tab, self.symbol_array[self.active_tab]))
        return (self.get_active_tab_symbol_global(), self.driver.find_element_by_xpath(xpath))

    def get_active_tab_symbol(self):
        if self.active_tab not in self.symbol_array.keys():
            raise Exception("Exceeded symbol list array size")
        #print("Active tab: {}, symbol {}".format(self.active_tab, self.symbol_array[self.active_tab]))
        return self.symbol_array[self.active_tab]

    def get_active_tab_symbol_global(self):
        if self.global_active_tab not in self.global_index_array.keys():
            raise Exception("Exceeded symbol list array size")
        #print("Active tab: {}, symbol {}".format(self.active_tab, self.symbol_array[self.active_tab]))
        return self.global_index_array[self.global_active_tab]


    def close(self):
        self.driver.quit()

def connect(port_no=44327):
    s = requests.Session()
    s.mount('https://stooq.com', hacked_requester.SourcePortAdapter(port_no))
    return s
