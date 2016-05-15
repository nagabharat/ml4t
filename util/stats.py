""" Tools for doing stats on portfolios."""

from datetime import timedelta
import util.data_tools as data_tools

import pandas as pd
import numpy as np
from scipy.optimize import minimize

def portfolio_statistics(symbols, allocation, start_val,
                            start_date='2000-02-01', end_date='2012-09-12',
                            risk_free_rate=0, sampling_freq='D'):
    """ Return portfolio statistics for specified tickers and dates."""

    # Get dates and ensure they start on a monday
    dates = pd.date_range(start_date, end_date, freq=sampling_freq)
    dates = [d + timedelta(days=(7-dates[0].weekday()) % 7) for d in dates]
    price_df = data_tools.get_data_single_field(symbols, field='Adj Close',
                                                dates=dates)

    # Get adjustment constant (depends on sampling frequency)
    adj_factor = {'D': np.sqrt(252),
                  'W': np.sqrt(52),
                  'M' : np.sqrt(12)}

    # Normalise data frame, and assign allocations.
    price_df = price_df / price_df.ix[0]
    price_df = price_df * allocation
    price_df['Position Vals'] = price_df.sum(axis=1)

    # Compute statistics
    cum_ret = price_df['Position Vals'][-1] - 1
    end_val = start_val * (1 + cum_ret)
    daily_rets = price_df['Position Vals'].pct_change()
    avg_daily_ret = daily_rets[1:].mean()
    risk = daily_rets[1:].std()
    risk_adjusted = (daily_rets[1:] - risk_free_rate).std()
    sharpe_ratio = (adj_factor[sampling_freq] *
                    (avg_daily_ret - risk_free_rate) / risk_adjusted)

    return cum_ret, avg_daily_ret, risk, sharpe_ratio, end_val

def optimize_portfolio(symbols, start_date, end_date,
                          risk_free_rate=0):
    """ TODO: Write docstring"""

    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(start_date, end_date)
    price_df = data_tools.get_data_single_field(symbols, field='Adj Close',
                                                dates=dates)

    # Define sharpe_ratio subfunction
    def neg_sharpe_ratio(allocation, price_df):
        price_df = price_df * allocation
        price_df['Position Vals'] = price_df.sum(axis=1)
        daily_rets = price_df['Position Vals'].pct_change()
        avg_daily_ret = daily_rets[1:].mean()
        risk_adjusted = (daily_rets[1:] - risk_free_rate).std()
        return -np.sqrt(252) * (avg_daily_ret - risk_free_rate) / risk_adjusted

    # Optimize allocation to maximize sharpe ratio
    price_df = price_df / price_df.ix[0]
    n_symbols = len(symbols)
    constraints = ({'type' : 'eq', 'fun' : lambda alloc: 1 - alloc.sum()})
    options = {'fun' : neg_sharpe_ratio,
               'x0' : np.ones(n_symbols) / n_symbols,
               'args' : (price_df),
               'method' : 'SLSQP',
               'bounds' : [(0, 1) for s in range(n_symbols)],
               'constraints' : constraints,
               'options' : {'disp' : False}}
    res = minimize(**options)
    allocs = res.x
    cum_ret, avg_daily_ret, risk, sharpe_ratio, end_val = \
        portfolio_statistics(symbols, allocs, 1, start_date, end_date)

    return allocs, cum_ret, avg_daily_ret, risk, sharpe_ratio
