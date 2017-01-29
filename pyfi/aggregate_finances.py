'''
Given all the different types of assets ingested, aggregate all them together

Steps
---
1) Retrieve data from SQL (p2p accounts, interactive_brokers, mint_accounts)
2) Do the necessary aggregation steps to calculate total net worth and other statistics
3) Write those to table

'''
from pyfi.config import db_location
from pyfi.sql_queries import (most_recent_accounts_receivable, most_recent_mint_accounts,
                              most_recent_p2p, most_recent_stocks)

import arrow
import sqlite3
from collections import defaultdict

today = str(arrow.now().date())


def get_most_recent_assets(db_location):
    '''

    :param db_location:
    :return:
    '''
    cursor = sqlite3.connect(db_location).cursor()
    assets = defaultdict(int)
    asset_data = cursor.execute(most_recent_mint_accounts).fetchall()




    return assets


def calculate(assets):
    """
    Given a dict of assets,

    :param assets:
    :return:
    """
    net_worth = 0

    # Take the sum of all the assets
    for asset in assets.values():
        net_worth += asset

    debt =
    stocks =
    retirement =
    accounts_receivable =
    p2p_total =
    net_worth = p2p_total + accounts_receivable + retirement + stocks - debt
    previous_net_worth =
    difference =

    return_rate = net_worth / previous_net_worth# Return on investments

    return dict(difference=difference, previous_net_worth=previous_net_worth, net_worth=net_worth,
                p2p_total=p2p_total, accounts_receivable=accounts_receivable, retirement=retirement,
                stocks=stocks, debt=debt, return_rate=return_rate)


if __name__ == '__main__':
    assets = get_most_recent_assets(db_location)
    calculated_values = calculate(assets)