"""
Initalizes databases if they have not already been created.

Notes
---
- Currently single user. In the future, it may make more sense to include more users
    in the same database

"""

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
        cursor.execute('''CREATE TABLE mint_accounts
                 (date text, account text, account_id text, change real, balance real,
                 account_type text)''')

    if not is_table(cursor, 'stock_accounts'):
        cursor.execute('''CREATE TABLE stock_accounts
        (date text, account text, stock text, balance real, change real)''')

    if not is_table(cursor, 'p2p_accounts'):
        cursor.execute('''CREATE TABLE p2p_accounts
        (account text, available_cash real, account_total real, combinedAdjustedNar real,
          tradedAdjustedNAR real, primaryAdjustedNAR real, platform text, date text, change real)''')


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
                 (date text, total real, difference real, days_between real,
                 return real, cash real, debt real, p2p real, stocks real,
                 retirement real, accounts_receivable real)''')
    else:
        print("net worth table already created")

if __name__ == '__main__':
    print("Checking if tables already exist and initializing them"
          "if they don\'t")
    create_credentials_table(cursor)
    create_asset_tables(cursor)
    create_net_worth_table(cursor)