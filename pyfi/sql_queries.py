"""
SQL Queries for getting the most recent dataframes. This has been cluttering up main scripts
and the lgoic hasn't been that interesting so it's going here. For the sake of expediancy,
I'm going to assume that all pulls except for accounts receivable:

Notes
--
- Most recent of each thing
    http://stackoverflow.com/questions/1140064/sql-query-to-get-most-recent-row-for-each-instance-of-a-given-key
    - If this starts causing problems just implement that
"""


most_recent_mint_accounts = """select * from mint_accounts where date == date('now', 'localtime')
"""

most_recent_p2p = """select * from p2p_accounts where date == date('now', 'localtime')
"""

most_recent_stocks = """select * from stock_accounts where date == date('now', 'localtime')
"""
most_recent_accounts_pending = """select * from pending_payments where resolved = 0"""

most_recent_net_worth = """select date, net_worth from net_worth
                           order by date DESC limit 1"""