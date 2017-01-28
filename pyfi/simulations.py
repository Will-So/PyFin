'''
Various scripts to simulate a year of results. This is critical for simulating when it is possible
to retire.

Notes
---
    - For projections like this, it probably makes more sense to use

TODO
---
    - Make all of the functions pure here)
    - Make it more clear when something
'''
import numpy as np
import pandas as pd

from pyfi.config import (security_properties, target_allocation, royalties,target_monthly_spending,
                     minimum_monthly_spending, guranteed_cash, risk_free_rate)

from pyfi.utilities import calculate_expected_return


def royalty_returns(royalty):
    # Royalties can;t go below 0
    return max(np.random.normal(royalties[royalty].expected_value, royalties[royalty].variance), 0)


def yearly_spend(minimum_monthly_spending, target_monnthly_spending):
    '''

    :param minimum_monthly_spending: int, the minimum possible amount of monthly spending
    :param target_monnthly_spending:

    :return: Dollar Amount of the expected returns
    '''
    minimum_possible = minimum_monthly_spending * 12
    expected_spending = target_monthly_spending * 12
    return max(np.random.normal(expected_spending, expected_spending* .15), minimum_possible)


# TODO: this should be for all, not just lending clu                b
def lc_returns(security_properties):
    '''Lending Club returns. handles the case when bankruptcy occurs
    '''
    if np.random.uniform() > 0.99:
        # Lending club goes bankrupt with probability .01
        if np.random.uniform() > 0.5:
            # Get half back
            returns = -.5
        else:
            # Judge Eliminates everything
            returns = -1
    else:
        returns = np.random.normal(security_properties['lending_club'].expected_value,
                                      security_properties['lending_club'].variance)
    return returns


## TODO incorporate the expected value of individual securities rather than the entire market
## http://quant.stackexchange.com/questions/4589/how-to-simulate-stock-prices-with-a-geometric-brownian-motion
def stock_returns(stock_e_return, stocks):
    '''
    param: stock_e_return The expected value of annual stock returns from now until the end.

    return: float: annual return for a single year

    Uses a normal distribution
    '''
    market_return = np.random.normal(stock_e_return, 0.12)
    for stock in stocks:
        stock



def sim_year(starting_amount, guranteed_cash, royalties, security_properties ):
    """I do this with a single simulation rather than 1000 at once.
    Rather the simulations will be done at the year level.
    """
    simulations = pd.DataFrame()
    stock_cash = stock_returns() * (starting_amount * stock_share)
    royalty_cash = royalty_returns() * 12
    yearly_expend = yearly_spend()

    guranteed_cash = sum(guranteed_cash.values())

    for royality in royalty_cash:


    change = (royalty_cash + stock_cash +
                       guranteed_cash - yearly_expend)

    ending_amount = starting_amount - change

    simulations = simulations.append(pd.DataFrame(
            [[simulation, change, royalty_cash, stock_cash,
                 e_social_security, yearly_expend, ending_amount]]))

    simulations.columns = ['simulation', 'change', 'royalties',
                           'stocks', 'social_security', 'spent',
                           'left']
    simulations = simulations.set_index('simulation')
    return simulations

if __name__ == '__main__':

