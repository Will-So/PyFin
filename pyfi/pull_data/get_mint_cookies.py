'''
This will be an adaptation of the code in `mintapi` that opens selenium and starts the login.

If my PR isn't merged, I may just write the class here instead.
'''
import time


def get_session_cookies(username, password):
    '''
    Function pulled from mintiapi.api; original version defined in a class
    and required a `self` argument.
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
        return {
            'ius_session': driver.get_cookie('ius_session')['value'],
            'thx_guid': driver.get_cookie('thx_guid')['value']
        }
    finally:
        driver.close()


class WMint(mintapi.Mint):
    def get_investments(self):
        """
        Gets all investments in the link:

        https://mint.intuit.com/investment.event

        Steps:
            1) Get investment account IDs
            2) The format of it will be https://mint.intuit.com/investment.event#location:{"accountId":"8536885"}

        """

        accounts = self.get_accounts()
        investment_account_ids = [account['accountId'] for account in accounts if
                                  account['accountType'] == 'investment']

        investment_dict = dict()  # dict of dataframes
        for id in investment_account_ids:
            url = '{}/investment.event?accountId={id}'.format(MINT_ROOT_URL, id=8928652)
            r = requests.get(url)
            import pdb;
            pdb.set_trace()
            print(r.text)
            print(url)
            try:
                positions = pd.read_html(url, attrs={'class': 'portfolio'})  # This will be the actual html that is read
                investment_account_ids[id] = positions
            except ValueError:
                print("Couldn't retrieve positions for table {}".format(id))

        return investment_dict  # TODO check what the other items are returning