"""
Database configutation that is used throughout the test files.
"""

import pytest
import sqlite3

from pyfi.initalize_database import create_asset_tables
from pyfi.config import db_location


@pytest.fixture(scope='module', autouse=True)
def new_cursor():
    conn = sqlite3.connect(':memory:')
    new_cursor = conn.cursor()
    create_asset_tables(new_cursor) # Initialize database tables

    yield new_cursor # This terminates function running until the session ends
    conn.close()


@pytest.fixture(scope='module', autouse=True)
def populated_cursor():
    credential_conn = sqlite3.connect(db_location)
    credential_cursor = credential_conn.cursor()
    yield credential_cursor
    credential_conn.close()


def pytest_addoption(parser):
    parser.addoption("--runslow", action="store_true",
        help="run slow tests")

@pytest.fixture(scope='module', autouse=True)
def new_connection():
    """
    Necessary in the case that we are writing using the Pandas API
    """
    conn = sqlite3.connect(':memory:')
    conn_cursor = conn.cursor()
    create_asset_tables(conn_cursor)
    yield conn
    conn.close()