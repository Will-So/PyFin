import pytest
import sqlite3

from pyfi.pull_data.mint import (mint_login, get_account_details, refresh_accounts,
                                write_accounts, database, cursor)
#from pyfi.config import mint_credentials
from pyfi.initalize_database import create_asset_tables

MANUAL = False

def test_mint_login_saved(populated_cursor):
    """
    Test whether the login function works

    NOTE: test_login_
    :return:
    """
    mint = mint_login(populated_cursor)

    mint.get_net_worth()


@pytest.mark.skipif(MANUAL == False, reason='This requires manual login in order to pull cookies')
def test_mint_new_login(new_cursor):
    """
    This is skipped by default because it requires manual login
    :return:
    """
    mint = mint_login(new_cursor)

    mint.get_net_worth()
