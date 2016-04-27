# -*- coding: utf-8 -*-
"""
Created on Sat Apr 23 18:08:07 2016

@author: charlie
                                                                                                                            """
import matplotlib.pyplot as plt
    
def plot_from_100(df):
    df_temp = df / df.ix[0] * 100
    df_temp.plot(title='Normalised Stock Prices (2010)')
    plt.xlabel('Time')
    plt.ylabel('Normalised stock price')