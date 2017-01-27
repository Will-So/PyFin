from pyfi.pull_data.lending_club import pull_account_status, write_summary, handle_account
from pyfi.config import main_config
from pyfi.initalize_database import create_asset_tables

import sqlite3
import arrow


def test_pull_account():
    df = pull_account_status(main_config)

    assert len(df.columns) == 6 # Number of columns
    assert len(df) == 1 # Number or rows


def test_handle_accounts():
    '''
    Also tests write_summary
    :return:
    '''
    new_connection = sqlite3.connect(':memory:')
    temp_cursor = new_connection.cursor()
    create_asset_tables(temp_cursor)

    handle_account(main_config, new_connection)

    results = temp_cursor.execute("""SELECT date, account_total FROM p2p_accounts
                                       WHERE account = "{investor_id}" ORDER BY date DESC
                                       LIMIT 1""".format(investor_id=main_config['investor_id'])
                                   ).fetchone()
    today = str(arrow.now().date())
    assert results[0] == today