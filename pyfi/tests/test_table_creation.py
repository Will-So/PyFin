from ..initalize_database import create_asset_tables, get_tables

import sqlite3


def test_table_creation():
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    assert len(get_tables(cursor)) == 0
    create_asset_tables()
    assert len(get_tables(cursor)) == 3

