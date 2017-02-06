"""
This will eventually be changed to test config and will be what the various tests are going to be
tested against.

TODO
---
    - Use Security for the expected returns as well.
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

asset = namedtuple('security', ['expected_value', 'variance', 'beta'])

# Contains the expected annual return as well as the expected beta
# For each of the assets we are considering.
# TODO all of this needs to be changed. Need to be able to get stock betas
# Also not sure if this is the best data structure.
assets = {'lending_club': asset(.07, .03, 0.2), 'VB': asset(.07, .30, 1.19),
                    'VOO': asset(.07, .12, 1), 'VO': asset(.07 * 1.19, .20, 1.09),
                    'prosper': asset(.075, .03, 0.2), 'real_estate': asset(.04, .05, 0.2)}


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
royalties = {'oil': asset(1500, 500, 0)}

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