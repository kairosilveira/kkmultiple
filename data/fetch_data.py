import yfinance as yf
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

def get_current_price(crypto = 'bitcoin', currency = 'usd'):
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
    'ids':crypto,
    'vs_currencies':currency
    }
    session = Session()
    session.headers.update(headers)
    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        return data
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

def get_historical_crypto_data(start_date, end_date, price_col,ticker = "BTC-USD"): 
    bitcoin_data = yf.download(ticker, start=start_date, end=end_date)
    return bitcoin_data[price_col]