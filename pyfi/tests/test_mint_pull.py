import pytest
import sqlite3

from pyfi.pull_data.mint import (mint_login, get_account_details, refresh_accounts,
                                write_accounts, database, cursor)
from pyfi.config import
from pyfi.initalize_database import create_asset_tables

MANUAL = False




def test_mint_login_saved(init_sqlite):
    """
    Test whether the login function works

    NOTE: test_login_
    :return:
    """
    credential_conn = sqlite3.connect('../accounts.db')
    credential_cursor = credential_conn.connect()
    ius, thx = mint_login(credential_cursor)
    assert len(ius) == len(thx) > 20 # Just picked a large number. Is 32 at the time of writing


@pytest.mark.skipif(MANUAL == False)
def test_mint_new_login():
    """
    This is skipped by default because it requires manual login
    :return:
    """

