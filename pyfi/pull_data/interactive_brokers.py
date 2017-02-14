"""
Sources:
    - http://interactivebrokers.github.io/tws-api/introduction.html#gsc.tab=0

Notes:
    - User ID is for the case when we want to deal with multi-user
    - site_id is for the case when we have multiple different brokerages.

"""
import xml.etree.ElementTree as ET
import requests
from lxml import objectify
import pandas as pd
import sqlite3
import arrow
import time
from retry import retry

from pyfi.config import ib_credentials, db_location, logger

today = str(arrow.now().date())


@retry(tries=5, delay=20)
def get_xml_report(ib_credentials):
    """
    Generates the XML report

    :param ib_credentials:
    :return:
    """
    generate_report = requests.get('https://gdcdyn.interactivebrokers.com/Universal/servlet/FlexStatementService'
                                                '.SendRequest?t={TOKEN}&q={QUERY_ID}&v=3'.format(TOKEN=ib_credentials['token'],
                                                QUERY_ID=ib_credentials['flex_id']))

    parsed_response = ET.fromstring(generate_report.text)
    report_id = int(parsed_response[1].text) # 1 is just the element of the id.

    get_data = requests.get('https://gdcdyn.interactivebrokers.com/Universal/servlet/FlexStatement'
    'Service.GetStatement?q={REFERENCE_CODE}&t={TOKEN}&v=3'.format(REFERENCE_CODE=report_id,
                                                              TOKEN=ib_credentials['token']))

    if not get_data:
        raise ValueError # Forces retry yet again

    return get_data.text


def parse_xml(xml_data):
    '''
    Given raw XML data, get all of the most important data from it.

    :param xml_data: A string generated from a requests file.
    :return: pandas DataFrame in the perfect format
    '''

    root = objectify.fromstring(xml_data)

    # Get the details of the current positions
    position_details = {}
    positions = root['FlexStatements']['FlexStatement'].OpenPositions
    for child in positions.getchildren():
        child = dict(child.attrib)
        print(child.keys())
        position_details[child['symbol']] = dict(cost_basis=
                                                 child['costBasisMoney'], position=child['position'],
                                                 positionValue=child['positionValue'], description=
                                                 child['description'], date=today, user_id=1, site_id=1)


    # Get summary amount of cash and total net position

    equity = root['FlexStatements']['FlexStatement']['EquitySummaryInBase']
    equity = equity['EquitySummaryByReportDateInBase'].attrib

    cash = equity['cash']

    # Update the old dictionary to contain cash
    position_details.update({'cash': {'cost_basis': cash,
                                      'description': 'cash',
                                      'position': cash,
                                      'positionValue': cash,
                                      'date': today,
                                      'user_id':1, 'site_id':1}})

    for key in equity:
        if key not in ['totalLong', 'cash', 'total']:  # total is the balance
            del equity[key]

    return pd.DataFrame(position_details).T # by default the symbol is a column


def write_data(df, connection):
    '''
    Writes dataframe to database

    :param df: Dataframe with all IB data
    :return:
    '''
    cursor = connection.cursor()

    # Check to make sure that site id and user_id is the same
    previous_info = cursor.execute("""SELECT date, site_id, positionValue FROM stock_accounts
                                       WHERE user_id= "{user_id}"  AND site_id = {site_id} ORDER BY date DESC
                                       LIMIT 1""".format(user_id=1, site_id=1)
                                   ).fetchone()

    if previous_info and previous_info[0] == today:
        logger.info("Already logged to stocks_today; not writing results to df.")
    else:
        df.to_sql('stock_accounts', connection, if_exists='append', index=True, index_label='symbol')


if __name__ == '__main__':
    xml_data = get_xml_report(ib_credentials)
    processed_data = parse_xml(xml_data)
    print(processed_data)
    write_data(processed_data, sqlite3.connect(db_location))
