"""
Orchastrates the daily updates and checks to make sure all historical data from stocks is still there.
"""
import sqlite3
from pyfi.config import assets, db_location, main_config

from pyfi.pull_data.historical_stocks import get_and_save_stock_prices
from pyfi.pull_data.lending_club import pull_lending_club
from pyfi.pull_data.interactive_brokers import _main as pull_interactive_brokers
from pyfi.pull_data.mint import execute_pull as pull_mint
from pyfi.aggregate_finances import _main as aggregate_finances


def check_stocks():
    """
    Updating this data is only required when we add a symbol.
    :return:
    """
    current_stocks = [stock for stock in assets if type == 'stock']

    # Get old Stocks
    cursor = sqlite3.connect(db_location).cursor()
    old_stocks = cursor.execute('SELECT DISTINCT(symbol) from historical_stocks').fetchall()

    old_stocks, current_stocks = set(old_stocks), set(current_stocks)

    if current_stocks ^ old_stocks:
        # Save stock prices to the new database
        get_and_save_stock_prices(assets)

    cursor.close()


def daily_update():
    connection = sqlite3.connect(db_location)
    pull_lending_club(main_config, connection)
    pull_interactive_brokers()
    pull_mint()
    aggregate_finances()


if __name__ == '__main__':
    check_stocks()
    daily_update()
