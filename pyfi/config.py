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

# Asset Correlations
stock_betas = dict(VOO=1, cash=0, VB=1.19, VO=1.09, lc=.2, prosper=.1)

## Asset Allocation
# TODO beta is going to be calculated seperately in future
#Security = namedtuple('security', ['expected_value', 'variance', 'beta'])


"""
Type can be one of three things:
1) stock
2) p2p
3) other -- this can be things like real estate
4) payment -- a type of asset that doesn't have an underlying amount of capital.
    - Social Security
    - Royalty Payments
"""

asset = namedtuple('security', ['expected_value', 'variance', 'beta', 'type'])

# Contains the expected annual return as well as the expected beta
# For each of the assets we are considering.
# TODO all of this needs to be changed. Need to be able to get stock betas
# Also not sure if this is the best data structure.
assets = {'lending_club': asset(.07, .03, 0.2, 'p2p'), 'VB': asset(.07, .30, 1.19, 'stock'),
          'VOO': asset(.07, .12, 1, 'stock'), 'VO': asset(.07 * 1.19, .20, 1.09, 'stock'),
          'prosper': asset(.075, .03, 0.2, 'p2p'), 'real_estate': asset(.04, .05, 0.2, 'other')}


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
payments = {'oil': asset(1500, 500, 0, 'payment'), 'social_security': asset(2500, 0, 0, 'payment')}


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