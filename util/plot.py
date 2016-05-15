import matplotlib.pyplot as plt
    
def plot_from_100(df):
    df_temp = df / df.ix[0] * 100
    df_temp.plot(title='Normalised Stock Prices (2010)')
    plt.xlabel('Time')
    plt.ylabel('Normalised stock price')