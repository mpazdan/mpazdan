# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


class MovingAverageTrend(object):
    def __init__(self, _stock_data, _margin, _lower_limit, _upper_limit):
        self.stock_data = _stock_data
        self.margin = _margin
        self.lower_limit = _lower_limit
        self.upper_limit = _upper_limit
        
    def calculate_rolling_mean_strategy(self):
        data = self.stock_data
        lname = str(self.lower_limit)
        uname = str(self.upper_limit)
        SD = self.margin
        key_l = lname + 'd'
        self.stock_data[key_l] = np.round(data['Close'].rolling(
                            self.lower_limit).mean(), 2)
        key_u = uname + 'd'
        data[key_u] = np.round(data['Close'].rolling(
                            self.upper_limit).mean(), 2)
        data['trend_diff'] = data[key_l] \
                                        - data[key_u]
        data['Regime'] = np.where(data['trend_diff'] \
                                        > SD, 1, 0)
        data['Regime'] = np.where(data['trend_diff'] \
                                        < -SD, -1, data['Regime'])
        
        data['Market'] = np.log(data['Close'] \
                                    / data['Close'].shift(1))

        data['Strategy'] = data['Regime'].shift(1) \
                                    * data['Market']
                                    
        print("OK")
        print(data[['Market', 'Strategy']].cumsum().apply(np.exp))
        data[['Cum_ret', 'Str_ret']] = \
                            data[['Market', 'Strategy']].cumsum().apply(np.exp)
        print(data[['Cum_ret', 'Str_ret']])
    
    def draw_results(self):
        data = self.stock_data
        lname = str(self.lower_limit)
        uname = str(self.upper_limit)

        plt.figure(figsize=(8, 5))

        plt.subplot(2,1,1)
        plt.plot(data[['Close', lname + 'd', uname + 'd']])

        plt.subplot(2,1,2)
        plt.plot(data['Regime'], lw=1.5)
        plt.ylim([-1.1, 1.1])
        plt.grid(True)
        plt.show()

        plt.figure(figsize=(8,5))
        #plt.plot(data[['Cum_ret', 'Str_ret']])
        plt.plot(data['Cum_ret'], lw='1.5', label='Cumulative return')
        plt.plot(data['Str_ret'], lw='1.5', label='Strategy return')
        plt.legend(loc=0)
        plt.grid(True)
        plt.show()
