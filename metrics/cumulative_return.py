import polars as pl
from functools import namedtuple


class CumulativeReturn:
    def __init__(self, trading_data: pl.DataFrame,) -> None:
        self.trading_data = trading_data

    def calculate(self, initial_fiat: float = 1000,  initial_crypto: float = 0):

        CumulativeResults = namedtuple(
            'CumulativeResults',
            ['crypto', 'fiat', 'total_in_fiat']
        )
        fiat_money = initial_fiat
        crypto = initial_crypto
        for date, price, action in self.trading_data.iter_rows():
            if action == 'buy' and fiat_money!=0:
                crypto = fiat_money/price
                fiat_money = 0.0
            elif action == 'sell' and crypto != 0:
                fiat_money = price*crypto
                crypto = 0.0

        return CumulativeResults(
            crypto=crypto,
            fiat=fiat_money,
            total_in_fiat=fiat_money + price*crypto
        )
