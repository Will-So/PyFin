'''
This will eventually be changed to test config and will be what the various tests are going to be
tested against.
'''
from collections import namedtuple

Security = namedtuple('security', ['expected_value', 'variance'])

expected_returns = {'lending_club': .07, 'stock_market':.07,
                    'prosper': .075, 'real_estate': .04}

target_allocation = {'lending_club': .666, 'resl_estate': 0, 'prosper':0}


## The allocation of the stock market will be everything else
target_allocation['stock_market'] = 1 - sum(target_allocation.values())

monthly_budget = 3500

# Target cash will be the amount of available cash that we always want to stay above.
#  For now, it can be defined as monthly_budget * 2

target_cash = monthly_budget * 2

royalties = {'oil': Security(1500, 500)}

minimum_monthly_spending = 2500
target_monthly_spending = 3500

