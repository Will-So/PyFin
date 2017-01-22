"""
This will eventually be changed to test config and will be what the various tests are going to be
tested against.

TODO
---
    - Use Security for the expected returns as well.
"""
from collections import namedtuple
import os

## Login Credentials
mint_login = ('wil.sorenson@gmail.com', os.environ['MINT_PASSWORD'])

## Mint accounts to exclude ## fiLoginDisplayName
exclude = ['Lending Club', 'Interactive Brokers']

# Stocks
Stock = namedtuple('stock', ['beta', 'share'])
stocks = {'SPY': [1, ], 'cash': [0, ]}
## Asset Allocation
# TODO beta is going to be calculated seperately in future
Security = namedtuple('security', ['expected_value', 'variance', 'beta'])



security_properties = {'lending_club': Security(.07, .03), 'stock_market': Security(.07, .12),
                    'prosper': (.075, .03), 'real_estate': (.04, .05)}

target_allocation = {'lending_club': .666, 'resl_estate': 0, 'prosper':0}


## The allocation of the stock market will be everything else
target_allocation['stock_market'] = 1 - sum(target_allocation.values())

monthly_budget = 3500

# Target cash will be the amount of available cash that we always want to stay above.
#  For now, it can be defined as monthly_budget * 2

target_cash = monthly_budget * 2

'''
These are assets whose returns can't go below 0 but do have a certain amount of uncertainty
'''
royalties = {'oil': Security(1500, 500)}

## Some assets will have completely fixed returns. In this case,
## they should be stored in this dict.
guranteed_cash = {'social_security': 3500}

minimum_monthly_spending = 2500
target_monthly_spending = 3500
monthly_spending_standard_deviation = .12


'''
3 months is usually a good risk-free ratehttp://www.investopedia.com/terms/r/risk-freerate.asp

# https://fred.stlouisfed.org/series/DTB3
'''

risk_free_rate = .052