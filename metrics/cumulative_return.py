import polars as pl
from functools import namedtuple


class CumulativeReturn:
    """
    CumulativeReturn class for calculating cumulative returns based on trading data.

    Args:
    - trading_data (pl.DataFrame): DataFrame containing trading data with columns 'date', 'price', and 'action'.

    Attributes:
    - trading_data (pl.DataFrame): DataFrame containing trading data with columns 'date', 'price', and 'action'.
    """

    def __init__(self, trading_data: pl.DataFrame) -> None:
        self.trading_data = trading_data

    def calculate(self, initial_fiat: float = 1000, initial_crypto: float = 0) -> namedtuple:
        """
        Calculates cumulative returns based on the provided initial fiat and crypto values.

        Args:
        - initial_fiat (float, optional): Initial amount of fiat currency (default is 1000).
        - initial_crypto (float, optional): Initial amount of cryptocurrency (default is 0).

        Returns:
        - namedtuple: A named tuple with fields 'crypto', 'fiat', and 'total_in_fiat'.
          - crypto (float): Final amount of cryptocurrency.
          - fiat (float): Final amount of fiat currency.
          - total_in_fiat (float): Total value in fiat currency after trading.
        """
        CumulativeResults = namedtuple(
            'CumulativeResults',
            ['crypto', 'fiat', 'total_in_fiat']
        )
        fiat_money = initial_fiat
        crypto = initial_crypto
        for date, price, action in self.trading_data.iter_rows():
            if action == 'buy' and fiat_money != 0:
                crypto = fiat_money / price
                fiat_money = 0.0
            elif action == 'sell' and crypto != 0:
                fiat_money = price * crypto
                crypto = 0.0

        return CumulativeResults(
            crypto=crypto,
            fiat=fiat_money,
            total_in_fiat=fiat_money + price * crypto
        )
