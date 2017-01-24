"""
Database configutation that is used throughout the test files.
"""

import pytest

@pytest.fixture(scope='module', autouse=True)
def init_empty_sqlite():
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    create_asset_tables(cursor)

    yield cursor # This terminates function running until the session ends
    conn.close()


@pytest.fixture(scope='module', autouse=True)
def init_populated_sqlite():
    credential_conn = sqlite3.connect('../accounts.db')
    credential_cursor = credential_conn.connect()
    yield credential_cursor
    credential_conn.close()