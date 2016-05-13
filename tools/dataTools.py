# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from datetime import timedelta

def add_days_var(df):
    Date = df.index.values
    df['Days'] = (Date - Date.min())  / np.timedelta64(1,'D')
    return df

def ticker_to_path(ticker, base_dir='data'):
    """Get path for ticker csv data."""
    return base_dir + '/{}.csv'.format(ticker)
    
def get_NYSE_dates():
    """ Get datetime object of dates on which the NYSE was open."""
    df_temp = pd.read_csv(ticker_to_path('SPY'), index_col='Date', parse_dates=True,
                          usecols=['Date'], na_values='nan')
    df_temp = df_temp.sort_index()
    return df_temp.index.values

def get_data_single_field(ticker_list, field, dates='NYSE', 
                             NYSE_dates_only=True, drop_na=False):
    """ Get ticker data for a specified field in a given date range. """
    if dates is 'NYSE':
        dates = get_NYSE_dates()
    df = pd.DataFrame(index=dates)
    print(df)
    if NYSE_dates_only:
        NYSE_dates = get_NYSE_dates()
        df_temp = pd.DataFrame(index=NYSE_dates)
        print(df_temp)
        df = df.join(df_temp, how='inner')
#        print(df)
    for ticker in ticker_list:
        df_temp = pd.read_csv(ticker_to_path(ticker), index_col='Date', parse_dates=True, 
                         usecols=['Date', field], na_values='nan')
        df_temp = df_temp.rename(columns={field : ticker})
        df = df.join(df_temp)
    if drop_na:
        df = df.dropna()
    return df
    
def compute_portfolio_statistics(ticker_list, allocation, start_val, 
                                     start_date='2000-02-01', end_date='2012-09-12',
                                     risk_free_rate=0, 
                                     sampling_freq='D', gen_plot=False):
    # Get dates
    dates = pd.date_range(start_date, end_date, freq=sampling_freq)
    dates = [d + timedelta(days=(7-dates[0].weekday()) % 7) for d in dates]
    price_df = get_data_single_field(ticker_list, field='Adj Close', dates=dates)
    
    # Compute statistics
    price_df = price_df / price_df.ix[0]
    price_df = price_df * allocation
    price_df['Position Vals'] = price_df.sum(axis=1)
    cum_ret = price_df['Position Vals'][-1] - 1
    end_val = start_val * (1 + cum_ret)
    daily_rets = price_df['Position Vals'].pct_change()
    avg_daily_ret = daily_rets[1:].mean()
    risk = daily_rets[1:].std()
    risk_adjusted = (daily_rets[1:] - risk_free_rate).std()
    
    # Get adjustment constant
    adj_factor = {'D': np.sqrt(252),
                  'W': np.sqrt(52),
                  'M' : np.sqrt(12)}
    sharpe_ratio = (adj_factor[sampling_freq] * 
        (avg_daily_ret - risk_free_rate) / risk_adjusted)
    return cum_ret, avg_daily_ret, risk, sharpe_ratio, end_val

def daily_returns(df):
    daily_returns = df.copy()
    daily_returns[1:] = (df[1:] / df[:-1].values) -1
    daily_returns.ix[0] = 0
    return daily_returns