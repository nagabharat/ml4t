# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import tools.dataTools as dataTools
#import tools.plotTools as plotTools
import numpy as np

def linear_regression(X,y, l=0):
    params = np.linalg.solve(X.T.dot(X) + l, X.T.dot(y))
    alpha = params[0]
    beta = params[1]
    return alpha, beta

def main():
    
    # Load data for specified dates
    ticker_list = ['SPY', 'AAPL']
    field = 'Adj Close'
    sd = '2005-12-31'
    ed = '2014-12-07'
    dates = pd.date_range(sd, ed)
    df = dataTools.get_data_single_field(ticker_list, field, dates=dates)

    # Get daily returns
    df = df.pct_change()
    df.ix[0] = 0
        
#    # Get summary stats
#    mean = df.mean()
#    std = df.std()
#    kurtosis = df.kurtosis()
#    
#    print 'Mean: {}'.format(mean)
#    print 'Standard deviations: {}'.format(std)
#    print 'Kurtosis: {}'.format(kurtosis)
    
    # Plot histogram with summary stats
#    df['SPY'].hist(bins=20, label='SPY', alpha=0.5)  
#    plt.hold(True)
#    df['AAPL'].hist(bins=20, label='AAPL', alpha=0.5)  
#    plt.legend()
    
    # Linear regression
    X = df['SPY'].values
    X = np.hstack((np.ones([len(X), 1]), X[:,np.newaxis]))
    y = df['AAPL'].values
    alpha, beta = linear_regression(X, y, l=0)
#    beta2,beta1, alpha = np.polyfit(X,y,2) 
    x_vals = df['SPY'].values
    y_vals = alpha + beta*x_vals
    
    # Scatter plot
    df.plot(kind='scatter', x='SPY', y='AAPL', lw=0)
    plt.plot(x_vals, y_vals, color='r', linewidth=2)
    plt.axis('equal')

#    plt.axvline(mean, linestyle='dashed', linewidth=5, color='w')
#    plt.axvline(mean+std, linestyle='dashed', linewidth=2, color='g')
#    plt.axvline(mean-std, linestyle='dashed', linewidth=2, color='g')
#    plt.legend(('mean', 'std'))
    plt.show()
                                             
#    # Plot data with rolling mean
#    ax = df.plot(title='SPY and FAKE2')
#    roll = df.rolling(window=20)
#    r_mean = roll.mean()
#    r_mean.plot(ax=ax)
#    
#    # Add sd bands
#    r_std = roll.std()
#    (r_mean + 2*r_std).plot(ax=ax)
#    (r_mean - 2*r_std).plot(ax=ax)
# 
#    # Add legend   
#    ax.legend(['SPY','Rolling mean','+2 STD','-2 STD'], loc='upper left',
#              fontsize=7)
#    ax.set_ylabel('Price')
#    
#    # Save plot / set params
#    fig = plt.gcf()
#    fig.set_size_inches(6,4)
#    font = {'size' : 8,
#            'weight' : 'normal'}
#    plt.rc('font', **font)
#    fig.savefig('test.pdf', dpi=600)
    
if __name__ == '__main__':
    main()
