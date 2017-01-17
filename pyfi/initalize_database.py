import sqlite3

conn = sqlite3.connect('accounts.db')
cursor = conn.cursor()

def getTables():
   """
   Get a list of all tables
   """
   cmd = "SELECT name FROM sqlite_master WHERE type='table'"
   cursor.execute(cmd)
   names = [row[0] for row in cursor.fetchall()]
   return names

def is_table(nameTbl):
   """
   Determine if a table exists
   """
   return (nameTbl in getTables())


def create_tables():
    '''
    Creates tables if they don't already exist
    :return:
    '''
    if not is_table('mint_accounts'):
        cursor.execute('''CREATE TABLE mint_accounts
                 (date text, account text, change real, balance real)''')

    if not is_table('stock_accounts'):
        cursor.execute('''CREATE TABLE stock_accounts
        (account text, balance real, change real)''')

    if not is_table('p2p_accounts'):
        cursor.execute('''CREATE TABLE p2p_accounts
        (account text, balance real, change real)''')


if __name__ == '__main__':
    create_tables()