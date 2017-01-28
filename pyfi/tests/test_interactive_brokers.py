from pyfi.pull_data.interactive_brokers import get_xml_report, parse_xml, write_data
from pyfi.config import ib_credentials
from pyfi.initalize_database import create_asset_tables

import sqlite3

test_get_xml = get_xml_report(ib_credentials)


def test_parse_xml(new_connection):
    df = parse_xml(test_get_xml)
    print(df.head())
    write_data(df, new_connection)


def test_two_writes_fail(new_cursor, new_connection):
    """
    Writing twice should fail. Note that `write_data` automatically commits so the writes
    from the previous test should be done.
    :param new_cursor:
    :return:
    """
    # new_connection = sqlite3.connect(':memory:')
    ib_cursor = new_connection.cursor()

    df = parse_xml(test_get_xml)
    prior_length = len(df)

    ## Write twice this time.
    write_data(df, new_connection)
    write_data(df, new_connection)


    new_results = ib_cursor.execute("""SELECT * FROM stock_accounts""").fetchall()
    print(new_results)
    new_length = len(new_results)

    assert prior_length == new_length