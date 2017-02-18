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
import sys
from datetime import datetime

today = str(arrow.now().date())

connection = sqlite3.connect(db_location)

def _main():
    assets = get_most_recent_assets(connection)
    # import pdb; pdb.set_trace()
    investments = get_most_recent_stocks(connection)
    calculated_values = calculate(connection, assets, investments)
    write_net_worth(calculated_values, connection)


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


def get_most_recent_stocks(connection):
    """
    Get all stock investments

    :return:
    """
    investments = pd.read_sql(most_recent_stocks, connection)

    return investments


def get_retirement_accounts(cursor):
    """
    Gets any retirement accounts that aren't availalbe in Mint. This currently isn't the case
    so the method is empty

    :return:
    """


def calculate(connection, assets, investments):
    """
    Given a dict of assets, calculate everything needed for the net_worth table.

    Return Rate is calculated as
    $$ \frac{Current\_Value - Old\_Value}{Old_\Value} * \frac{365}{days\_between} $$

    :param connection: Connection to SQLite database
    :param investments: Investments calculated
    :param assets: assets retrieved from Mint. May contain debt and retirement values as well.
    :return: Dictionary of relevant fields
    """
    cursor = connection.cursor()

    debt = assets.query('account_type == "credit"').balance.sum()
    cash = assets.query('account_type == "bank"').balance.sum()
    stocks = investments.positionValue.sum()
    retirement = assets.query('account_type == "investment"').balance.sum()
    import pdb; pdb.set_trace()

    accounts_receivable = pd.read_sql(most_recent_accounts_pending, connection)
    accounts_receivable = accounts_receivable.amount.sum()

    p2p_total = pd.read_sql(most_recent_p2p, connection).account_total.sum()
    net_worth = p2p_total + accounts_receivable + retirement + stocks + debt + cash
    assert net_worth > 10000, "Net Worth too low; something weird happened"

    try:
        net_worth_info = cursor.execute(most_recent_net_worth).fetchone()
        logger.info("Net Worth: {}".format(net_worth_info))

        days_between = (datetime.strptime(net_worth_info[0], '%Y-%m-%d') -
                        datetime.strptime(today, '%Y-%m-%d'))

        logger.info("Days Between: {}".format(days_between))
        days_between = days_between.days # from timedelta to int

        # Only assign a new net_worth if it hasn't happened yet.
        if net_worth_info[0] == today: # Still do this in case less than 24 hours difference but more than 1 day
            logger.info("Net worth already logged today! Not writing again")
            sys.exit() # At this point, we want to completely stop running the script
        else:
            previous_net_worth = net_worth_info[1]

    except TypeError: # When no data is stored in the database
        logger.warning("Not networth data found, assuming previous networth was 0")
        previous_net_worth = 0
        days_between = 0

    difference = net_worth - previous_net_worth

    try:
        return_rate = ((net_worth - previous_net_worth)/ previous_net_worth) *\
                      (365 / days_between)# Return on investments
    except ZeroDivisionError: # Case when previous_net_worth is undefined
        return_rate = 0

    return dict(difference=difference, previous_net_worth=previous_net_worth, net_worth=net_worth,
                p2p=p2p_total, accounts_receivable=accounts_receivable, retirement=retirement,
                stocks=stocks, debt=debt, return_rate=return_rate, date=today,
                days_between=days_between, cash=cash)


def write_net_worth(values, connection):
    """

    :param values:
    :return:
    """
    # import pdb; pdb.set_trace()
    df = pd.DataFrame.from_dict(values, orient='index').T
    df.to_sql('net_worth', connection, index=False, if_exists='append')
    logger.info("Finished writing to net worth")


if __name__ == '__main__':
    sys.exit(_main())