import pickle
from yahoo_finance import Share,  YQLResponseMalformedError
import arrow
import sqlite3

from pyfi.config import db_location


def get_yearly_prices(securities):
    """
    Gets the prices

    :param securities: ['VO', 'VB', 'VOO']
    :return: List of historical prices by year

    Example
    ---
    >>> get_yearly_prices(['VO', 'VB', 'VOO'])
    {('VB', '2013-02-19'): '87.400002',
     ('VB', '2014-02-19'): '111.209999',
     ('VB', '2015-02-19'): '121.010002',
     ('VB', '2016-02-19'): '100.440002',
     ...
     ('VOO', '2017-02-19'): '215.84'}}

    Notes
    ---
    -

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
                print("Last available entry for {} at {}".format(security, str(date.date())))
                break

    return prices


def correlation_matrix(**securities):
    '''
    This function returns the correlation between the returns of the S&P 500
    and the input securities. I use quarterly values for now as that is the
    minimum common granularity

    :param kwargs: dict of securities with their quarterly returns.
    :return: correlation matrix of securities with S&P 500
    '''
    


def calculate_expected_return(beta, alpha, risk_free_rate, market_returns):
    """
    Calculates the expected return of a stock based on the CAPM model.

    http://www.investopedia.com/exam-guide/cfa-level-1/portfolio-management/capm-capital-asset-pricing-model.asp

    :param beta:
    :param risk_free_rate:
    :param market_returns:
    :return:

    Notes
    ---
    - 3 months treasury bill is risk free rate
         http://www.investopedia.com/terms/r/risk-freerate.asp
    - Given how low treasury bills are, this is nearly equivelant to simple $\beta * market\_returns$

    """
    return risk_free_rate + beta * (market_returns - risk_free_rate)


def generate_test_data(obj, name):
    """
    Generates a pickle file for an object that can be used to write tests for


    :param obj: Object to be picked
    :param name: name of the pickle file
    :return:
    """
    with open('tests/{}'.format(name), 'wb') as f:
        pickle.dump(obj, f)

def save_yearly_prices(connection):
    """

    :return:
    """

def get_and_save_stock_prices():
    """

    :return:
    """
    connection = sqlite3.connect(db_location)
