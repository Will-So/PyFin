from ..initalize_database import create_asset_tables, getTables

import sqlite3


def test_table_creation():
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    assert len(getTables(cursor)) == 0
    create_asset_tables()
    assert len(getTables(cursor)) == 3

