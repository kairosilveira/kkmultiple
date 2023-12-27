
from data.fetch_data import get_historical_crypto_data
from multiple.multiple import KKMultiple
import polars as pl
from datetime import datetime


class CryptoAccumulator:
    def __init__(kkmultiple: KKMultiple, historical_data: pl.DataFrame, eval_period: tuple) -> None:
        self.kkmultiple = kkmultiple
        self.historical_data = historical_data
        start_date, end_date = eval_period
        self.start_date = datetime.strptime(start_date, '%Y-%m-%d')
        self.end_date = datetime.strptime(end_date, '%Y-%m-%d')

    def calculate_accumulated(self):
        return

    def _get_eval_period_df(self):
        self.eval_period_df = self.historical_data.filter(
            (pl.col("Date") >= self.start_date) & (pl.col("Date") <= self.end_date))

        return self.eval_period_df
