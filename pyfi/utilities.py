def correlation_matrix(**kwargs):
    '''
    This function returns the correlation between the returns of the S&P 500
    and the input securities. I use quarterly values for now as that is the
    minimum common granularity

    :param kwargs: dict of securities with their quarterly returns.
    :return: correlation matrix of securities with S&P 500
    '''
