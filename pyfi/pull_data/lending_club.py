'''
Pull data from lending club. Much of this code is taken from Will Sorenson's Lending Club
    project.


When dealing with additional accounts, add the config file to __main__
'''
import sqlite3
import requests
import pandas as pd
import arrow
import sys

from pyfi.config import main_config, db_location, logger

connection = sqlite3.connect(db_location)
cursor = connection.cursor()


def pull_account_status(lc_config):
    """
    Retrieves all of the important account details from lending_club

    :param lc_config:
    :return:
    """
    headers = {'Authorization': lc_config['credentials']}

    r = requests.get('https://api.lendingclub.com/api/investor/{version}/accounts/{investor_id}/summary/'.format(
        version='v1', investor_id=main_config['investor_id']), headers=headers)

    assert r.status_code == 200, "LC API Pull failed"

    summary = r.json()

    summary = pd.io.json.json_normalize(summary)

    # Rename columns for consistency with the rest of the project
    summary = summary.rename(columns={'netAnnualizedReturn.combinedAdjustedNAR': 'combined_adjusted_NAR',
                            'netAnnualizedReturn.primaryAdjustedNAR': 'primary_adjusted_NAR',
                            'netAnnualizedReturn.tradedAdjustedNAR': 'traded_adjusted_NAR',
                            'investorId': 'account', 'availableCash': 'available_cash',
                            'accountTotal': 'account_total'})

    important_columns = ['account', 'available_cash', 'account_total', 'combined_adjusted_NAR',
                         'traded_adjusted_NAR', 'primary_adjusted_NAR']

    summary = summary[important_columns] ## Keep only the columns we are interested in

    return summary


def write_summary(previous_info, today, df, connection):
    """
    Writes the summary data to SQL if it has not already been written today.

    :param df: pd.DataFrame containing all of the values of interst.
    :return:
    """

    df['platform'] = 'lending_club'
    df['date'] = today

    if previous_info:
        previous_balance = previous_info[1] # 1 is the second value in the tuple
    else:
        previous_balance = 0

    df['change'] = df.account_total - previous_balance

    df.to_sql('p2p_accounts', connection, if_exists='append', index=False)


def handle_account(config, conn):
    """
    Retrieves data for a lending club account and writes to database.

    :param config: dictionary that contains all configuration info for a lending club account
    :return:
    """
    cursor = conn.cursor()
    previous_info = cursor.execute("""SELECT date, account_total FROM p2p_accounts
                                       WHERE account = "{investor_id}" ORDER BY date DESC
                                       LIMIT 1""".format(investor_id=config['investor_id'])
                                   ).fetchone()

    today = str(arrow.now().date())

    # Don't want to bother with anything if results are already entered
    if previous_info and previous_info[0] == today:
        logger.info("Already logged lending club today; not writing results to df.")
        return False

    lc_summary = pull_account_status(main_config)
    write_summary(previous_info, today, lc_summary, conn)
    logger.info('Finished writing lending Club Results')


if __name__ == '__main__':
    handle_account(main_config, connection)

