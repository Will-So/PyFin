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
    - Make if account[6] multiplatorm by including the account id
    - Add behavior of `other` assets. This should be custom defined by function
'''
import numpy as np
import pandas as pd
import sqlite3

from pyfi.config import (assets, target_allocation, payments, target_monthly_spending,
                         minimum_monthly_spending, risk_free_rate, db_location)
from pyfi.sql_queries import (most_recent_p2p, most_recent_mint_accounts, most_recent_stocks,
                              most_recent_accounts_pending)
from pyfi.utilities import calculate_expected_return

def _main():
    """
    Main driver for simulating code.

    :return:
    """
    stocks =

    sim_year()

def get_asset_amount(assets):
    """
    Gets all asset amounts that are necessary for determining ROI. This should be p2p, stocks,
     and real_estate

    Schehma of stock_amounts:
    date|user_id|site_id|symbol|description|cost_basis|position|positionValue

    Schema of p2p_amounts:
    account|available_cash|account_total|combined_adjusted_NAR|traded_adjusted_NAR|primary_adjusted_NAR|platform|date|change

    :param assets:
    :return:
    """

    cursor = sqlite3.connect(db_location).cursor()

    asset_amounts = {}
    stock_amounts = cursor.execute(most_recent_stocks).fetchall()
    p2p_amounts = cursor.execute(most_recent_p2p).fetchall()
    num_assets = 0 # Keep track to make sure we don't miss any stocks or p2p. Need to do this rather than comparing to length of `assets` because only stock, real estte, and other cover this

    for asset in assets:

        # Handle Stocks
        if assets[asset].type == 'stock':
            num_assets += 1
            for stock in stock_amounts:
                if stock[3] == assets[asset]:
                    asset_amounts[asset] = stock[4]

        # Handle p2p payments
        if assets[asset].type == 'p2p':
            num_assets += 1
            for account in p2p_amounts:
                if account[6] == assets[asset]: # 6 is the platform
                    asset_amounts[asset] = account[2]

        # TODO add real estate

    cursor.close()

    return asset_amounts



def payment_returns(assets, royalty):
    """

    :param assets:
    :param royalty:
    :return:
    """
    # TODO should consider to have this be an AR(2) method or something like that
    return max(np.random.normal(assets[royalty].expected_value, assets[royalty].variance), 0)


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
def p2p_returns(security_properties, bc_recovery):
    '''Lending Club returns. handles the case when bankruptcy occurs
    '''
    if np.random.uniform() > 0.995:
        # Lending club goes bankrupt with probability .005
        if np.random.uniform() > 0.5:
            # Get half back
            returns = -1 * bc_recovery
        else:
            # Judge Eliminates everything
            returns = -1
    else:
        returns = np.random.normal(security_properties['lending_club'].expected_value,
                                      security_properties['lending_club'].variance)
    return returns


## TODO incorporate the expected value of individual securities rather than the entire market
# TODO incorporate randomness around beta
# TODO want to make a stock handler to deal with the weights properly.
def stock_returns(benchmark, stocks):
    '''
    :param benchmark_returns: The returns that have already been simulated for this year
    :param stocks: a dictionary of format {stock_name:(beta, weight)}

    return: float: dictionary of (percentage) returns for each individual security as well as its weight

    Notes
    --
    - Uses a normal distribution to generate a random deviation between the current beta
        and the actual beta.
    - An alternative method:  http://quant.stackexchange.com/questions/4589/how-to-simulate-stock-prices-with-a-geometric-brownian-motion

    '''
    benchmark_returns = calculate_benchmark_returns(benchmark)

    returns = {}
    for stock in stocks:
        returns[stock] = (np.random.normal(benchmark_returns * stocks[stock][0], 0.02),
                          stocks[stock][1])

    return returns


def calculate_benchmark_returns(benchmark):
    """
    Calculate the returns of a benchmark that all other stock


    :return:
    """
    benchmark_return = np.random.normal(benchmark.expected_value,
                                        benchmark.variance)

    return benchmark_return


def other_returns(assets):
    """

    :param assets:
    :return:
    """


def sim_year(starting_amount, assets ):
    """I do this with a single simulation rather than 1000 at once.
    Rather the simulations will be done at the year level.

    :param starting_amount:
    :param guranteed_cash:
    :param securities:

    :return:
    """
    simulations = pd.DataFrame()
    stock_cash = stock_returns() * (starting_amount * stock_share)
    royalty_cash = payment_returns() * 12
    yearly_expend = yearly_spend()

    guranteed_cash = sum(guranteed_cash.values())

    benchmark_return = calculate_benchmark_returns(benchmark=)

    returns =
    for asset in assets:





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

asset_mapper = {'stocks': stock_returns, 'p2p': p2p_returns, 'payment': payment_returns,
                'other': other_returns}


if __name__ == '__main__':
    _main()

