import pytest
import sqlite3

from pyfi.pull_data.mint import (mint_login, get_account_details, refresh_accounts,
                                write_accounts, database, cursor)
#from pyfi.config import mint_credentials


MANUAL = False

# Marker for slow functions
slow = pytest.mark.skipif(
    not pytest.config.getoption("--runslow"),
    reason="need --runslow option to run"
)

def test_mint_login_saved(populated_cursor):
    """
    Test whether the login function works

    NOTE: test_login_
    :return:
    """
    mint = mint_login(populated_cursor)

    mint.get_net_worth()

    return mint

# Global for subsequent functions
mint = mint_login(cursor)

@pytest.mark.skipif(MANUAL == False, reason='This requires manual login in order to pull cookies')
def test_mint_new_login(new_cursor):
    """
    This is skipped by default because it requires manual login
    :return:
    """

    mint.get_net_worth()


def test_get_account_details(populated_cursor):
    """
    Tests that the get_account_details function works

    :return:
    """
    mint = mint_login(populated_cursor)

    account_details = get_account_details(mint)
    assert len(account_details) == 2 # Net worth and account details


@slow
def test_refresh_accounts(populated_cursor):
    """
    Takes 3 minutes so skip unless slow enabled

    :param populated_cursor:
    :return:
    """
    mint = mint_login(populated_cursor)

    refresh_accounts(mint)

