"""
This mannual process of getting cookies won't work long term. The solution will be:
    1) Have the user login once using the selenium API
    2) Store the content in some configuration system

Steps in Script:
    1) Log in to Mint. Go through 2fa if necessary
    2) (optional) refresh accounts
    3) Get all account details
    4) Write all the changes to database; also write the difference.

"""
import mintapi
import time
import arrow
import sqlite3

from pyfi.config import mint_login, exclude
from pyfi.pull_data.get_mint_cookies import get_session_cookies

database = sqlite3.connect('../accounts.db')
cursor = database.cursor()

mint = mintapi.Mint(mint_login[0], mint_login[1], '7912A452BCC946A7A2079DF3CAC6FE7F',
                    '234e7ea456584249ada51a72756e4916')


def mint_login(cursor):
    """
    Does the initial login to Mint. Will open a web browser and have the user login if 2FA is
        enabled.

    :param cursor: Pointer to the database login
    :return:
    """
    # Order by name to insure that ius comes before thx.
    cookies = cursor.execute('''SELECT * from cookies
                                WHERE name in ('mint_ius', 'mint_thx')
                                ORDER BY name ASC''').fetchall()

    if len(cookies) == 2:
        ius, thx = cookies[0], cookies[1]
    else:
        ## Get the cookies by opening up selenium. If 2FA is enabled,
        ##  the user will be required to enter it in.
        ius, thx = get_session_cookies(mint_login[0], mint_login[1])
        cursor.execute("""INSERT INTO cookies values ('mint_ius', ?)""", ius)
        cursor.execute("""INSERT INTO cookies values ('mint_thx', ?)""", thx)

    return mintapi.Mint(mint_login[0], mint_login[1], ius, thx)


# TODO: Not all of the accounts that are listed here are relevant. Deal with this in future
# functions
def get_account_details(mint):
    """
    Gets all account details

    :param mint: mint object that is already logged in
    :return:  net_worth and relevant details of all accounts in list
    """
    net_worth = mint.get_net_worth()

    accounts = mint.get_accounts()

    return net_worth, accounts


def refresh_accounts():
    """
    Refreshes the account and waits for 3 minutes until the accounts are done updating.
    :return:
    """
    mint.initiate_account_refresh()
    time.sleep(180)  ## Wait for 3 minutes for everything to refresh.


## TODO: Might want to make this default to no investment accounts
def write_accounts(account_details, exclude, cursor):
    """
    Writes all account details to database, including the change from the previous time.

    :param account_details: Mint account details, containing all information in a dict
    :param exclude: accounts that should be ignore
    :param cursor: cursor to handle writing to database
    :return: Nothing; writes to database
    """
    today = arrow.now().date()
    for account in account_details:
        if (account['fiLoginDisplayName'] not in exclude and
                    account['accountType'] != 'investment'):
            account_name = account['fiLoginDisplayName']
            previous_balance = cursor.execute("""SELECT balance FROM mint_accounts
                                       WHERE account = {account} ORDER BY date DESC
                                       LIMIT 1""".format(account=account['fiLoginDisplayName'])).fetch()

            # Case when there is a new account that the database hasn't seen before
            if not previous_balance:
                previous_balance = 0

            balance = account['currentBalance']
            change = balance - previous_balance

            cursor.execute("""INSERT INTO mint_accounts VALUES
                            ({today}, {account}, {change}, {balance})""".format(
                today=today, account=account_name, change=change, balance=balance
            ))
