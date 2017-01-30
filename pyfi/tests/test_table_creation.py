from ..initalize_database import (create_asset_tables, get_tables, create_net_worth_table,
                                  create_credentials_table)

import sqlite3


def test_asset_creation():
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    assert len(get_tables(cursor)) == 0
    create_asset_tables(cursor)
    assert len(get_tables(cursor)) == 4
    create_credentials_table(cursor)
    create_net_worth_table(cursor)

