"""
Initalizes databases if they have not already been created.

Notes
---
- Currently single user. In the future, it may make more sense to include more users
    in the same database

"""
from pyfi.config import logger

import sqlite3

conn = sqlite3.connect('accounts.db')
cursor = conn.cursor()


def get_tables(cursor):
    """
   Get a list of all tables
   """
    cmd = "SELECT name FROM sqlite_master WHERE type='table'"
    cursor.execute(cmd)
    names = [row[0] for row in cursor.fetchall()]
    return names


def is_table(cursor, table_name):
    """
   Determine if a table exists
   """
    return (table_name in get_tables(cursor))


# TODO: Determine whether this is really the best way to store everything
# I am already doing something similar in the networth table. It may be more
# noteworthy to
def create_asset_tables(cursor):
    '''
    Creates tables if they don't already exist
    '''

    if not is_table(cursor, 'mint_accounts'):
        logger.info("Creating mint_accounts table")
        cursor.execute('''CREATE TABLE mint_accounts
                 (date text, account text, account_id text, change real, balance real,
                 account_type text)''')

    if not is_table(cursor, 'stock_accounts'):
        logger.info("Creating stock_accounts table")
        cursor.execute('''CREATE TABLE stock_accounts
        (date text, user_id text, site_id text, symbol text, description text,
         cost_basis real, position real, positionValue real)''')

    if not is_table(cursor, 'p2p_accounts'):
        logger.info("Creating p2p_accounts table")
        cursor.execute('''CREATE TABLE p2p_accounts
        (account text, available_cash real, account_total real, combined_adjusted_NAR real,
          traded_adjusted_NAR real, primary_adjusted_NAR real, platform text, date text, change real)''')

    if not is_table(cursor, 'pending_payments'):
        logger.info("Creating pending_payments")
        cursor.execute("""CREATE TABLE pending_payments
        (date text, amount real, due_date text, note text, resolved int)""")


def create_credentials_table(cursor):
    '''
    Create a cookies table if it doesn't already exist
    '''
    if not is_table(cursor, 'credentials'):
        cursor.execute("""CREATE TABLE credentials
        (name text, value text)""")


def create_net_worth_table(cursor):
    '''
    Creates a net worth table; this is equivalent to a previous excel sheet
        I have used in the past.

    :param cursor:
    :return:
    '''
    if not is_table(cursor, 'net_worth'):
        cursor.execute('''CREATE TABLE net_worth
                 (date text, net_worth real, difference real, days_between real,
                 return_rate real, cash real, debt real, p2p real, stocks real,
                 retirement real, accounts_receivable real, previous_net_worth real)''')
    else:
        logger.info("net worth table already created")


if __name__ == '__main__':
    logger.info("Checking if tables already exist and initializing them"
                "if they don\'t")
    create_credentials_table(cursor)
    create_asset_tables(cursor)
    create_net_worth_table(cursor)
