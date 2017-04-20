"""
This will eventually be changed to test config and will be what the various tests are going to be
tested against.

TODO
---
    - Use Security for the expected returns as well.
    - If a stock is added to `assets`, it should automatically trigger rerunning the file
"""
from collections import namedtuple
import os
import logging
import sys

# Tell app whether to refresh the files
refresh = False
GENERATE_TEST = False

config_path =  os.path.dirname(os.path.abspath(__file__))
db_location = os.path.join(config_path, 'accounts.db')

## Login Credentials
mint_credentials = ('wil.sorenson@gmail.com', os.environ['MINT_PASSWORD'])

ib_credentials = {'token': 278534427760283813354678, 'flex_id': 225259}

## Mint accounts to exclude ## fiLoginDisplayName
exclude = ['Lending Club', 'Interactive Brokers']
included_investments = ['Will IRA']


## Asset Allocation
"""
Type can be one of three things:
1) stock
2) p2p
3) other -- this can be things like real estate
4) payment -- a type of asset that doesn't have an underlying amount of capital.
    - Social Security
    - Royalty Payments
"""

# This is the initial initilization. Later, `amount` will be appendded onto the asset.
assets = {}
assets['lending_club'] = dict(expected_returns=.07, variance=.03, beta=.2, type='p2p')
assets['VB'] =  dict(expected_returns=.07, variance=.30, beta=1.19, type='stock')
assets['VOO' ] = dict(expected_returns=.07 * 1.3, variance=.12, beta=1, type='stock')
assets['VO'] = dict(expected_returns=.07 * 1.20, variance=.20, beta=.20, type='stock')
assets['prosper'] =  dict(expected_returns=.075, variance=.03, beta=.2, type='p2p')
assets['real_estate'] = dict(expected_returns=.04, variance=.05, beta=.2, type='other')
assets['net_cash'] = dict(expected_returns=0, variance=0, beta=0, type='other') # I don't think I need to store net cash here actually.
# Asset should have

target_allocation = {'lending_club': .666, 'resl_estate': 0, 'prosper':0}


## The allocation of the stock market will be everything else
target_allocation['stock_market'] = 1 - sum(target_allocation.values())

monthly_budget = 3500

# Target cash will be the amount of available cash that we always want to stay above.
#  For now, it can be defined as monthly_budget * 2

target_cash = monthly_budget * 2

'''
These are assets whose returns can't go below 0 but do have a certain amount of uncertainty

These are also special because they are monetary payments rather than actual payments.
'''
assets['oil']= dict(expected_returns = 1500, variance=500, beta=0, type='payment')
assets['social_security'] = dict(expected_returns = 2762, variance=0, beta=0, type='payment')

for asset in assets:
    keys = assets[asset].keys()
    set_difference = set(keys) ^ set(['variance', 'expected_returns', 'beta', 'type'])
    assert set_difference == set(), "Found the following uncommon Keys: {}".format(set_difference)

"""
The following values should be set up by the user and represent their general behavior.

For the financial advisor, a good way to phrase this is:
    1) In a given month how much do you usually spend?
    2) What is the least you've spent in a given month assuming all normal Fixed expenses (e.g., mortgage)
    3) How many times in a month do you spend more than `target_monthly_spending` * 1.68

From those values

"""

# TODO Might want to have unexpected spending as well
minimum_monthly_spending = 2500
target_monthly_spending = 3500
monthly_spending_standard_deviation = .12


'''
3 months is usually a good risk-free ratehttp://www.investopedia.com/terms/r/risk-freerate.asp

# https://fred.stlouisfed.org/series/DTB3
'''

risk_free_rate = .0052 # Rate of the three month bond

# Setup logging for entire project
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# create a file handler
# TODO Change logger directory so everything is logged at the same level
log_directory = os.path.join(config_path, 'pyfi.log')
handler = logging.FileHandler(log_directory)
handler.setLevel(logging.INFO)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)

# Also move all loggers to stdout. Can be useful for dev
stdout_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stdout_handler)


## Lending Club
main_config = dict(credentials=os.environ['LENDING_CLUB_API'], investor_id=5809260,
                   portfolio_id=65013027)