
from data.fetch_data import get_historical_crypto_data
from multiple.kkmultiple import KKMultiple
import polars as pl
from datetime import datetime
from collections import namedtuple


class CryptoAccumulator:
    """
    A class representing a Crypto Accumulator that calculates accumulated values based on a specified strategy.

    Args:
    - kkmult (KKMultiple): An instance of the KKMultiple class.
    - historical_data (polars.DataFrame): DataFrame containing historical data.
    - train_period (tuple): A tuple representing the training period (start_date, end_date), ('%Y-%m-%d', '%Y-%m-%d').

    Attributes:
    - kkmult (KKMultiple): An instance of the KKMultiple class.
    - historical_data (polars.DataFrame): DataFrame containing historical data.
    - start_date (datetime): The start date of the training period.
    - end_date (datetime): The end date of the training period.
    - raw_train_data (polars.DataFrame or None): DataFrame containing the training data within the specified period.

    Methods:
    - calculate_accumulated(): Calculate the accumulated value based on the provided strategy.
    - _get_raw_train_data() -> polars.DataFrame: Get the training data within the specified period.
    - _get_multiples(mayer=False) -> polars.DataFrame: Get the multiples calculated based on the provided strategy.
    """

    def __init__(self, kkmult: KKMultiple, historical_data: pl.DataFrame, train_period: tuple) -> None:
        self.kkmult = kkmult
        self.historical_data = historical_data
        start_date, end_date = train_period
        self.start_date = datetime.strptime(start_date, '%Y-%m-%d')
        self.end_date = datetime.strptime(end_date, '%Y-%m-%d')

        self.raw_train_data = None

    def calculate_accumulated(self):
        # this method will be written later
        return

    def _get_raw_train_data(self) -> pl.DataFrame:
        """
        Get the training data within the specified period.

        Returns:
        polars.DataFrame: DataFrame containing the training data.
        """
        self.raw_train_data = self.historical_data.filter(
            (pl.col("date") >= self.start_date) & (pl.col("date") <= self.end_date))

        return self.raw_train_data

    def _get_multiples(self, mayer=False) -> pl.DataFrame:
        """
        Get the multiples calculated based on the provided strategy.

        Args:
        - mayer (bool): If True, calculate multiples using Mayer's method.

        Returns:
        polars.DataFrame: DataFrame containing the calculated multiples.
        """
        self.multiples = self.raw_train_data.map_rows(
            lambda row: self.kkmult.calculate_multiple(
                row[1],
                self.historical_data.filter(pl.col('date') < row[0]),
                mayer
            ),
            return_dtype=pl.Float64
        ).rename({"map": "multiples"})

        return self.multiples

    def _get_buy_percentages(self):
        self.buy_percentages = self.multiples.map_rows(
            lambda row: self.kkmult.get_buy_percentage(row[0]),
            return_dtype=pl.Float64
        ).rename({"map": "buy_percentages"})

        return self.buy_percentages

    def get_train_data(self):
        self.train_data = pl.concat(
            [self.raw_train_data, self.multiples, self.buy_percentages], how="horizontal")
        return self.train_data

    def get_accumulated_value(self, daily_budget=1000):
        AccumulatedResult = namedtuple(
            'AccumulatedResult', ['amount_accumulated', 'remaining_budget'])

        self._get_raw_train_data()
        self._get_multiples()
        self._get_buy_percentages()
        self.get_train_data()

        remaining_budget = 0
        amount_accumulated = 0
        for row in self.train_data.iter_rows():
            date, price, multiple, buy_percentage = row
            day_budget = daily_budget + remaining_budget
            day_budget_use = day_budget*buy_percentage
            day_purchase = day_budget_use/price
            amount_accumulated += day_purchase
            remaining_budget = day_budget - day_budget_use

        return AccumulatedResult(amount_accumulated=amount_accumulated, remaining_budget=remaining_budget)
