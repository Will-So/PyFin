import pickle


def correlation_matrix(**securities):
    '''
    This function returns the correlation between the returns of the S&P 500
    and the input securities. I use quarterly values for now as that is the
    minimum common granularity

    :param kwargs: dict of securities with their quarterly returns.
    :return: correlation matrix of securities with S&P 500
    '''
    


def calculate_expected_return(beta, risk_free_rate, market_returns):
    """
    Calculates the expected return of a stock based on the CAPM model.

    http://www.investopedia.com/exam-guide/cfa-level-1/portfolio-management/capm-capital-asset-pricing-model.asp

    3 months treasury bill is risk free rate
    http://www.investopedia.com/terms/r/risk-freerate.asp

    :param beta:
    :param risk_free_rate:
    :param market_returns:
    :return:
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