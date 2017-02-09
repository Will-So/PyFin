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

from pyfi.config import mint_credentials, included_investments, refresh, logger, GENERATE_TEST, db_location
from pyfi.pull_data.get_mint_cookies import get_session_cookies
from pyfi.utilities import generate_test_data

database = sqlite3.connect(db_location)
cursor = database.cursor()

# Useful for dev but not necessary atm
# mint = mintapi.Mint(mint_credentials[0], mint_credentials[1], '7912A452BCC946A7A2079DF3CAC6FE7F',
#                     '234e7ea456584249ada51a72756e4916')


def execute_pull():
    """
    Main execution logic for pulling data from mint

    :return:
    """
    mint = mint_login(cursor)
    logger.info("Login successful")
    if refresh:
        logger.info("Started refreshing")
        refresh_accounts(mint)
        logger.info("Refreshed accounts")

    net_worth, account_details = get_account_details(mint)

    if GENERATE_TEST:
        generate_test_data(account_details, 'account_details')

    logger.info("Successfully retrieved {} accounts".format(len(account_details)))
    write_accounts(account_details=account_details,
                   included_investments=included_investments, cursor=cursor)
    logger.info("Finished pulling data from mint")


def mint_login(cursor):
    """
    Does the initial login to Mint. Will open a web browser and have the user login if 2FA is
        enabled.

    :param cursor: Pointer to the database login
    :return:
    """
    # Order by name to insure that ius comes before thx.
    cookies = cursor.execute('''SELECT * from credentials
                                WHERE name in ('mint_ius', 'mint_thx')
                                ORDER BY name ASC''').fetchall()

    if len(cookies) == 2:
        # query returns a list of tuples, always want the values ([1] element)
        ius, thx = cookies[0][1], cookies[1][1]
    else:
        ## Get the cookies by opening up selenium. If 2FA is enabled,
        ##  the user will be required to enter it in.
        values = get_session_cookies(mint_credentials[0], mint_credentials[1])
        ius, thx = values['ius_session'], values['thx_guid']
        cursor.execute("""INSERT INTO credentials values ('mint_ius', ?)""", (ius, ))
        cursor.execute("""INSERT INTO credentials values ('mint_thx', ?)""", (thx, ))
        database.commit()
        database.close()

    return mintapi.Mint(mint_credentials[0], mint_credentials[1], ius, thx)


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


def refresh_accounts(mint):
    """
    Refreshes the account and waits for 3 minutes until the accounts are done updating.
    :return:
    """
    mint.initiate_account_refresh()
    time.sleep(180)  ## Wait for 3 minutes for everything to refresh.


## TODO: Might want to make this default to no investment accounts
def write_accounts(account_details, included_investments, cursor):
    """
    Writes all account details to database, including the change from the previous time.

    :param account_details: Mint account details, containing all information in a dict
    :param exclude: accounts that should be ignore
    :param cursor: cursor to handle writing to database

    :return: Nothing; writes to database
    """
    today = str(arrow.now().date()) # Don't want to deal with datetime representation
    for account in account_details:
        account_name = account['accountName']
        if account_name in included_investments or account['accountType'] != 'investment':
            # Want to include investments only if they are explicitly allowed for.
            ## Both accountName and accountId are required. accountName is the user readable
            ## but not unique
            account_id = account['accountId']
            account_type = account['accountType']
            print(account_id)
            previous_info = cursor.execute("""SELECT date, balance FROM mint_accounts
                                       WHERE account_id = "{account_id}" ORDER BY date DESC
                                       LIMIT 1""".format(account_id=account_id)).fetchone()

            # Case when there is a new account that the database hasn't seen before
            if not previous_info:
                previous_balance = 0
            else:
                previous_balance = previous_info[1]

            # Calculate variables to be retrieved
            balance = account['currentBalance']
            if account_type == 'credit':
                balance = -balance
            change = balance - previous_balance
            print(previous_info, today)

            if previous_info is None or previous_info[0] != today:
                cursor.execute("""INSERT INTO mint_accounts VALUES
                               ("{today}", "{account}", {account_id}, {change}, {balance},
                               "{account_type}")""".format(
                                today=today, account=account_name, change=change,
                                balance=balance, account_id=account_id,
                                account_type=account_type))

                logger.info("Wrote {}, {} to database".format(account_name, account_id))
            else:
                logger.warn("Accounts have already been updated today; skipping now.")

    database.commit()
    database.close()


if __name__ == '__main__':
    execute_pull()