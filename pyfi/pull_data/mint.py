'''
This mannual process of getting cookies won't work long term. The solution will be:
    1) Have the user login once using the selenium API
    2) Store the content in some configuration system

Steps in Script:

'''
import mintapi
import time
import arrow
import sqlite3

from ..config import mint_login, exclude
from .get_mint_cookies import get_session_cookies

database = sqlite3.connect('../accounts.db')
cursor = database.cursor()

mint = mintapi.Mint(mint_login[0], mint_login[1], '7912A452BCC946A7A2079DF3CAC6FE7F',
                    '234e7ea456584249ada51a72756e4916')

def mint_login(cursor):
    '''
    Does the initial login to Mint. Will open a web browser and have the user login if 2FA is
        enabled.

    :param cursor: Pointer to the database login
    :return:
    '''
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
def get_values(mint):
    '''

    :return: net_worth and relevant details of all accounts in list
    '''
    net_worth = mint.get_net_worth()

    accounts = mint.get_accounts()

    return net_worth, accounts

def refresh_accounts():
    mint.initiate_account_refresh()
    time.sleep(180) ## Wait for 3 minutes for everything to refresh.

def write_accounts(accounts, exclude):
    '''

    :return:
    '''
    today = arrow.now().date()
    for account in accounts:
        if account['fiLoginDisplayName'] not in exclude:

