import sqlite3

conn = sqlite3.connect('accounts.db')
cursor = conn.cursor()

def getTables(cursor):
   """
   Get a list of all tables
   """
   cmd = "SELECT name FROM sqlite_master WHERE type='table'"
   cursor.execute(cmd)
   names = [row[0] for row in cursor.fetchall()]
   return names

def is_table(cursor, nameTbl):
   """
   Determine if a table exists
   """
   return (nameTbl in getTables(cursor))


def create_asset_tables(cursor):
    '''
    Creates tables if they don't already exist
    :return:
    '''
    if not is_table(cursor, 'mint_accounts'):
        cursor.execute('''CREATE TABLE mint_accounts
                 (date text, account text, change real, balance real)''')

    if not is_table(cursor, 'stock_accounts'):
        cursor.execute('''CREATE TABLE stock_accounts
        (account text, balance real, change real)''')

    if not is_table(cursor, 'p2p_accounts'):
        cursor.execute('''CREATE TABLE p2p_accounts
        (account text, balance real, change real)''')


def create_cookies_table(cursor):
    '''

    :param cursor:
    :return:
    '''
    if not is_table(cursor, 'cookies'):
        cursor.execute("""CREATE TABLE cookies
        (name text, cookie text)""")

if __name__ == '__main___':
    create_cookies_table(cursor)
    create_asset_tables(cursor)