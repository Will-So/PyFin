'''
Given all the different types of assets ingested, aggregate all them together

Steps
---
1) Retrieve data from SQL (p2p accounts, interactive_brokers, mint_accounts)
2) Do the necessary aggregation steps to calculate total net worth and other statistics
3) Write those to table

'''
from pyfi.config import db_location, logger
from pyfi.sql_queries import (most_recent_accounts_pending, most_recent_mint_accounts,
                              most_recent_p2p, most_recent_stocks, most_recent_net_worth)

import arrow
import sqlite3
from collections import defaultdict
import pandas as pd

today = str(arrow.now().date())

connection = sqlite3.connect(db_location)


def get_most_recent_assets(connection):
    '''
    Pandas is going to be advantageous here because

    :param db_location:
    :return:
    '''
    # cursor = connection.cursor()
    # assets = defaultdict(int)
    # asset_data = cursor.execute(most_recent_mint_accounts).fetchall()

    assets = pd.read_sql(most_recent_mint_accounts, connection)

    return assets

def get_most_recent_investments(connection):
    """

    :return:
    """
    investments = pd.read_sql(most_recent_stocks, connection)

    return investments


# TODO This still needs to be written with more flexibility. For now I'll make it a constant because its just cash
def get_retirement_accounts():
    """

    :return:
    """


def calculate(connection, assets, investments):
    """
    Given a dict of assets,

    :param assets:
    :return:
    """
    net_worth = 0

    # Take the sum of all the assets
    cursor = connection.cursor()

    debt = assets.query('account_type == "credit"').balance.sum()
    cash = assets.query('account_type == "debit"').balance.sum()
    stocks = investments.positionValue.sum()
    retirement = assets.query('account_type == "investment"')

    accounts_receivable = pd.read_sql(most_recent_accounts_pending, connection)
    accounts_receivable = accounts_receivable.amount.sum()

    p2p_total = pd.read_sql(most_recent_p2p, connection).account_total.sum()
    net_worth = p2p_total + accounts_receivable + retirement + stocks - debt + cash

    try:
        previous_net_worth = cursor.execute(most_recent_net_worth).fetchone()[0]
    except KeyError:
        logger.warning("Not networth data found, assuming previous networth was 0")
        previous_net_worth = 0

    difference = net_worth - previous_net_worth

    return_rate = net_worth / previous_net_worth# Return on investments

    return dict(difference=difference, previous_net_worth=previous_net_worth, net_worth=net_worth,
                p2p_total=p2p_total, accounts_receivable=accounts_receivable, retirement=retirement,
                stocks=stocks, debt=debt, return_rate=return_rate)


def write_net_worth(values, connection):
    """

    :param values:
    :return:
    """
    pd.to_sql(values, connection)



if __name__ == '__main__':
    assets = get_most_recent_assets(connection)
    investments = get_most_recent_investments(connection)
    calculated_values = calculate(connection, assets, investments)
    write_net_worth(calculated_values, connection)