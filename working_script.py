""" Script for roughwork"""

# import pandas as pd
# import matplotlib.pyplot as plt
import util.stats as stats
import numpy as np
from pprint import pprint


def main():
#     get_portfolio_stats()
    get_optimized_portfolio()


def get_portfolio_stats():
    options = {'symbols': ['SPY', 'AAPL', 'GOOG'],
               'start_date': '2000-02-01',
               'end_date': '2014-12-07',
               'allocation': np.array([0.2, 0.15, 0.65]),
               'start_val': 1e6,
               'sampling_freq': 'W'}
    port_stats = stats.portfolio_statistics(**options)
    pprint(port_stats)


def get_optimized_portfolio():
    options = {'symbols': ['AAPL', 'GOOG', 'IBM'],
               'start_date': '2000-02-01',
               'end_date': '2014-12-07'}
    allocs, port_stats = stats.optimize_portfolio(**options)

    # Print Results
    print('Allocations:')
    pprint(allocs)
    print()
    print('Portfolio statistics:')
    pprint(port_stats)

if __name__ == '__main__':
    main()
