# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas_datareader import data, wb, stooq
from bsm import bsm_call_imp_vol
from bsm import bsm_call_value
from moving_average_trend import MovingAverageTrend

from time import time
from math import exp, sqrt,log
from random import gauss, seed
from datetime import datetime


def bsm_analytical():
    S0 = 100.
    K = 105.
    T = 1.0
    r = 0.05
    sigma = 0.2
    option_price = bsm_call_value(S0, K, T, r, sigma)
    print("Evaluated option price " + str(option_price))

def monte_carlo_python():
    seed(20000)
    t0 = time()
    S0 = 100.
    K = 105.
    T = 1.0
    r = 0.05
    sigma = 0.2
    M = 50
    dt = T/M
    I = 250000
    
    # Simulating I paths with M time steps
    S = []
    for i in range(I):
        path = []
        for t in range(M + 1):
            if t == 0:
                path.append(S0)
            else:
                z = gauss(0.0, 1.0)
                St = path[t - 1] * exp((r - 0.5 * sigma ** 2) * dt \
                        + sigma * sqrt(dt) * z)
                path.append(St)
        S.append(path)
    
    # Calculating the Monte Carlo estimator
    C0 = exp(-r * T) * sum([max(path[-1] - K, 0) for path in S]) / I
    
    # Result output
    tpy = time() - t0
    print ("European call option value %7.3f" % C0)
    print ("Duration in seconds %7.3f" % tpy)


# BSM SDE: dSt = r*St*delta_t + sigma * St * dZt
# St = St_-_delta_t * exp((r - 0.5 * sigma ^2) * delta_t /
#                                              + sigma * sqrt(delta_t) * z_t)

# C0 = exp(-r*T) 1/I sum(hT(St(i)))     i = 0...I
#                                       hT(ST(i)) = max(ST(i) - K, 0)
def monte_carlo_scipy():
    np.random.seed(20000)
    t0 = time()
    # Parameters
    S0 = 100.
    K = 105.
    T = 1.0
    r = 0.05
    sigma = 0.2
    M = 50
    dt = T/M
    I = 250000
    
    # Simulating I paths with M time step
    S = np.zeros((M + 1, I))
    S[0] = S0
    for t in range (1, M + 1):
        z = np.random.standard_normal(I) # pseudorandom numbers
        S[t] = S[t - 1] * np.exp((r - 0.5 * sigma ** 2) * dt \
                        + sigma * sqrt(dt) * z)

    C0 = exp(-r * T) * np.sum(np.maximum(S[-1] - K, 0)) / I
    # Result output
    tnp1 = time() - t0
    print ("Scipy European call option value %7.3f" % C0)
    print ("Scipy Duration in seconds %7.3f" % tnp1)


# log(St) = log(St-delta_t) + (r - 0.5 * sigma ^ 2) * delta_t + sigma \
#                                                   * sqrt(delta_t) * z_t
def monte_carlo_scipy_full_vectorization():
    np.random.seed(20000)
    t0 = time()
    
    # Parameters
    S0 = 100.
    K = 105.
    T = 1.0
    r = 0.05
    sigma = 0.2
    M = 50
    dt = T / M
    I = 250000

    # Simulating I paths with M time steps
    S = S0 * np.exp(np.cumsum((r - 0.5 * sigma ** 2) * dt
                        + sigma * sqrt(dt)
                        * np.random.standard_normal((M + 1, I)), axis=0))

    S[0] = S0
    # Calculating Monte Carlo estimator
    C0 = exp(-r * T) * (sum(np.maximum(S[-1] - K, 0)) / I)
    
    tnp2 = time() - t0
    print ("Scipy (full vectorization) European call option value %7.3f" % C0)
    print ("Scipy (full vectorization) Duration in seconds %7.3f" % tnp2)
    plt.plot(S[:, :10])
    plt.grid(True)
    plt.xlabel('time step')
    plt.ylabel('index level')
    plt.show()
    
    plt.hist(S[-1], bins=int(S0))
    plt.grid(True)
    plt.xlabel('index level')
    plt.ylabel('frequency')
    plt.show()
    
    plt.hist(np.maximum(S[-1] - K, 0), bins=int(S0))
    plt.grid(True)
    plt.xlabel('option inner value')
    plt.ylabel('frequency')
    plt.ylim(0, 50000)
    plt.show()
    
    
def calculate_implied_volat():
    h5 = pd.HDFStore('../data/vstoxx_data_31032014.h5', 'r')
    futures_data = h5['futures_data'] # VSTOXX futures data
    options_data = h5['options_data'] # VSTOXX options data
    h5.close()
    
    print("Futures data")
    print(futures_data.info())
    print(futures_data[['DATE', 'MATURITY', 'TTM', 'PRICE']].head())

    print("Options data")
    print(options_data.info())
    print(options_data[['DATE', 'MATURITY', 'TTM', 'PRICE']].head())
    
    V0 = 17.6639
    r = 0.01
    tol = 0.5
    options_data['IMP_VOL'] = 0.0
    for option in options_data.index:
        forward = futures_data[futures_data['MATURITY'] == \
                        options_data.loc[option]['MATURITY']]['PRICE'].\
                        values[0]
        if (forward * (1 - tol) < options_data.loc[option]['STRIKE']
                                < forward * (1 + tol)):
            imp_vol = bsm_call_imp_vol(
                V0, #VSTOXX value
                options_data.loc[option]['STRIKE'],
                options_data.loc[option]['TTM'],
                r,
                options_data.loc[option]['PRICE'],
                sigma_est=2.,
                it=100)
            options_data['IMP_VOL'].loc[option] = imp_vol
    plot_data = options_data[options_data['IMP_VOL'] > 0]
    maturities = sorted(set(options_data['MATURITY']))
    print(maturities)
    
    plt.figure(figsize=(8, 6))
    for maturity in maturities:
        data = plot_data[options_data.MATURITY == maturity]
        # select data for this maturity
        plt.plot(data['STRIKE'], data['IMP_VOL'],
                 label=maturity, lw=1.5)
        plt.plot(data['STRIKE'], data['IMP_VOL'], 'r.')
        plt.grid(True)
        plt.xlabel('strike')
        plt.ylabel('implied volatility of volatility')
        plt.legend()
        plt.show()
