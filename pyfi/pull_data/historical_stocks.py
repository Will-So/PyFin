import arrow
import pandas as pd
from yahoo_finance import Share, YQLResponseMalformedError
import sys
import sqlite3

from pyfi.config import logger, db_location, assets

if __name__ == '__main__':
    sys.exit(get_and_save_stock_prices(assets))


def get_and_save_stock_prices(securities):
    """
    Gets stock

    :return:
    """
    connection = sqlite3.connect(db_location)
    stocks = [symbol for symbol in assets if assets[symbol].type == 'stock']
    stocks.append('SPY')  # This is the benchmark price. Makes more sense to run this one than VOO because it has a longer history
    prices = get_yearly_prices(stocks)
    prices.to_sql('historical_stocks', connection, index=False,
          if_exists='replace')


def get_yearly_prices(securities):
    """
    Gets the prices

    :param securities: ['VO', 'VB', 'VOO']
    :return: datafarme of prices with dates.

    Example
    ---
    >>> df = get_yearly_prices(['VO', 'VB', 'VOO', 'SPY'])
    >>> print(df)
    symbol        date       price
    0      VB  2013-02-19   88.959999
    1      VB  2010-02-19   58.439999
    2      VO  2008-02-19   70.410004
    3     SPY  1993-02-19     43.5625
    4      VB  2009-02-19   35.720001


    """
    prices = dict()
    shares = dict()  # Holds the `Share` object of each share
    for security in securities:
        date = arrow.utcnow()  # We restart the date after each security
        shares[security] = Share(security)

        while True:  # Keep iterating until we can't get any more data

            start_date = str(date.replace(days=-5).date())
            end_date = str(date.date())

            # The 0 here is becaue the API returns a list of dates. We only have one
            # Date here so we always just want the first item.
            try:
                prices[security, str(date.date())] = shares[security].get_historical(start_date,
                                                                                     end_date)[0]['Close']
                date = date.replace(years=-1)

            except YQLResponseMalformedError:
                logger.info("Last available entry for {} at {}".format(security, str(date.date())))
                break

    df = pd.DataFrame.from_dict(prices, orient='index')
    df.index = pd.MultiIndex.from_tuples(df.index)
    df = df.reset_index()
    df = df.rename(columns={'level_0': 'symbol', 'level_1': 'date', 0: 'price'})

    return df