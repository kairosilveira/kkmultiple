import yfinance as yf
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import polars as pl


def get_current_price(crypto='bitcoin', currency='usd'):
    """
    Get the current price of a cryptocurrency in a specified currency.

    Parameters:
    - crypto (str): The cryptocurrency symbol or ID (default is 'bitcoin').
    - currency (str): The currency in which the price is required (default is 'usd').

    Returns:
    - dict: A dictionary containing the current price data of the specified cryptocurrency
      against the specified currency.

    Example:
    - get_current_price('bitcoin', 'usd') returns:
      {'bitcoin': {'usd': 58000}}
    """
    url = "https://api.coingecko.com/api/v3/simple/price"
    headers = {
        'Accepts': 'application/json',
    }
    parameters = {
        'ids': crypto,
        'vs_currencies': currency
    }
    session = Session()
    session.headers.update(headers)
    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        return data
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)


def get_historical_crypto_data(start_date, end_date, price_col, ticker="BTC-USD"):
    """
    Get historical cryptocurrency data within a specified date range.

    Parameters:
    - start_date (str): The start date in 'YYYY-MM-DD' format.
    - end_date (str): The end date in 'YYYY-MM-DD' format.
    - price_col (str): The column containing the desired price data.
    - ticker (str): The cryptocurrency ticker symbol (default is "BTC-USD").

    Returns:
    - polars.DataFrame: A Polars DataFrame containing historical price data of the specified cryptocurrency
      between the specified start and end dates.

    Example:
    - get_historical_crypto_data('2023-01-01', '2023-12-31', 'Close', 'BTC-USD') returns:
      shape: (365, 2)
      ┌────────────────┬───────────┐
      │ Date           │ Price     │
      │ ───────────────┼───────────┤
      │ 2023-01-01     │ 47000.0   │
      │ 2023-01-02     │ 48000.0   │
      │ ...            │ ...       │
      │ 2023-12-30     │ 60000.0   │
      │ 2023-12-31     │ 62000.0   │
      └────────────────┴───────────┘
    """

    bitcoin_data = yf.download(ticker, start=start_date, end=end_date)

    # Convert pandas DataFrame to Polars DataFrame
    polars_df = pl.DataFrame(bitcoin_data.reset_index())

    # Select the specified columns
    polars_df = polars_df.select(
        ["Date", price_col]).rename({"Date": "date",price_col: 'price'})
    return polars_df
