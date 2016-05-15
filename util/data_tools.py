import pandas as pd

def ticker_to_path(ticker, base_dir='data'):
    """Get path for ticker csv data."""
    return base_dir + '/{}.csv'.format(ticker)
    
def get_NYSE_dates():
    """ Get datetime object of dates on which the NYSE was open."""
    df_temp = pd.read_csv(ticker_to_path('SPY'), index_col='Date', 
                          parse_dates=True, usecols=['Date'], na_values='nan')
    df_temp = df_temp.sort_index()
    return df_temp.index.values

def get_data_single_field(symbols, field, dates='NYSE', 
                             NYSE_dates_only=True, drop_na=False):
    """ Get ticker data for a specified field.
    
    Optionally specify dates by passing a datetime object. By default, the 
    returned dataframe will return only dates on which the NYSE was open.        
    """
    if dates is 'NYSE':
        dates = get_NYSE_dates()
    df = pd.DataFrame(index=dates)
    if NYSE_dates_only:
        NYSE_dates = get_NYSE_dates()
        df_temp = pd.DataFrame(index=NYSE_dates)
        df = df.join(df_temp, how='inner')
    for ticker in symbols:
        df_temp = pd.read_csv(ticker_to_path(ticker), index_col='Date', parse_dates=True, 
                         usecols=['Date', field], na_values='nan')
        df_temp = df_temp.rename(columns={field : ticker})
        df = df.join(df_temp)
    if drop_na:
        df = df.dropna()
    return df
    
#def add_days_var(df):
#    Date = df.index.values
#    df['Days'] = (Date - Date.min())  / np.timedelta64(1,'D')
#    return df
    