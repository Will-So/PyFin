'''
This will be an adaptation of the code in `mintapi` that opens selenium and starts the login.

If my PR isn't merged, I may just write the class here instead.
'''
import time
from pyfi.config import db_location, logger
import sqlite3


def get_session_cookies(username, password):
    '''
    Function pulled from mintiapi.api; original version defined in a class
    and required a `self` argument. This version also saves the data into a database so it doesn't have
    to be done each time.

    :param username: Mint username
    :param password: Mint password
    :return: ius_session, and thx_guid in string form; also writes to database
    '''
    try:
        from selenium import webdriver
        driver = webdriver.Chrome()
    except Exception as e:
        raise RuntimeError("ius_session not specified, and was unable to load "
                           "the chromedriver selenium plugin. Please ensure "
                           "that the `selenium` and `chromedriver` packages "
                           "are installed.\n\nThe original error message was: " +
                           (e.args[0] if len(e.args) > 0 else 'No error message found.'))

    driver.get("https://www.mint.com")
    driver.implicitly_wait(20)  # seconds
    driver.find_element_by_link_text("Log In").click()

    driver.find_element_by_id("ius-userid").send_keys(username)
    driver.find_element_by_id("ius-password").send_keys(password)
    driver.find_element_by_id("ius-sign-in-submit-btn").submit()

    # Wait until logged in, just in case we need to deal with MFA.
    while not driver.current_url.startswith('https://mint.intuit.com/overview.event'):
        time.sleep(1)

    try:

        values = {
            'ius_session': driver.get_cookie('ius_session')['value'],
            'thx_guid': driver.get_cookie('thx_guid')['value']
        }
        cursor = sqlite3.connect(db_location)
        ius, thx = values['ius_session'], values['thx_guid']
        cursor.execute("""INSERT INTO credentials values ('mint_ius', ?)""", (ius,))
        cursor.execute("""INSERT INTO credentials values ('mint_thx', ?)""", (thx,))
        cursor.commit()
        cursor.close()
        logger.info("Wrote cookies to database")

        return values['ius_session'], values['thx_guid']

    finally:
        driver.close()

