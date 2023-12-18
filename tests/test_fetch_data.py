import polars as pl
import pandas as pd
from unittest.mock import patch

from data.fetch_data import get_current_price, get_historical_crypto_data

def test_get_current_price():
    # Test setup
    crypto = 'bitcoin'
    currency = 'usd'
    price = 45000
    response_text = f'{{"{crypto}": {{"{currency}": {price}}}}}'
    expected_data = {f'{crypto}': {f'{currency}': price}}

    # Mock API response
    with patch('data.fetch_data.Session.get') as mock_get:
        mock_get.return_value.text = response_text

        # Execute function
        api_result = get_current_price(crypto, currency)

        # Assertions
        assert api_result == expected_data
        assert isinstance(api_result, dict)
        assert len(api_result) == 1
        assert list(api_result.keys())[0] == crypto
        assert list(api_result[crypto].keys())[0] == currency
        assert api_result[crypto][currency] == price


def test_get_historical_crypto_data():
    # Test setup
    with patch('data.fetch_data.yf.download') as mock_yfinance:
        data = {
            'Date': ['2022-10-10', '2022-10-11', '2022-10-12'],
            'Open': [19446.416016, 19139.000000, 19052.646484],
            'High': [19515.466797, 19241.960938, 19203.199219],
            'Low': [19102.978516, 18925.603516, 19029.757812],
            'Close': [19141.484375, 19051.417969, 19157.445312],
            'Adj Close': [19141.484375, 19051.417969, 19157.445312],
            'Volume': [27425022774, 28711532910, 24950173846]
        }
        df = pd.DataFrame(data)
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)

        # Mock yfinance response
        mock_yfinance.return_value = df

        # Execute function
        price_col = 'Open'
        fetch_result = get_historical_crypto_data('2022-10-10', '2022-10-13', price_col, 'BTC-USD')

        # Assertions
        assert fetch_result.shape == (3, 2)
        assert len(fetch_result.columns) == 2
        assert "Date" in fetch_result.columns
        assert price_col in fetch_result.columns
        assert pl.Datetime in fetch_result.dtypes
        assert pl.Float64 in fetch_result.dtypes
