
from multiple.kkmultiple import KKMultiple
import polars as pl
from datetime import datetime
from collections import namedtuple
from typing import Tuple


class CryptoAccumulator:
    """
    A class representing a Crypto Accumulator that calculates accumulated values based on a specified strategy.

    Args:
    - historical_data (polars.DataFrame): DataFrame containing historical data.
    - eval_period (Tuple[str, str] | Tuple[datetime, datetime]): A tuple representing the training period (start_date, end_date), ('%Y-%m-%d', '%Y-%m-%d').
    - method (str, optional): The strategy method to use. Defaults to "kk".
    - kkmult (KKMultiple, optional): An instance of the KKMultiple class. Required if method is "kk".

    Attributes:
    - kkmult (KKMultiple | None): An instance of the KKMultiple class.
    - historical_data (polars.DataFrame): DataFrame containing historical data.
    - start_date (datetime): The start date of the training period.
    - end_date (datetime): The end date of the training period.
    - raw_train_data (polars.DataFrame | None): DataFrame containing the training data within the specified period.
    """
    possible_methods = ['kk', 'buy_every_day', 'mayer']

    def __init__(self, historical_data: pl.DataFrame, eval_period: Tuple[str, str] | Tuple[datetime, datetime], method: str = "kk", kkmult: KKMultiple | None = None) -> None:
        self.kkmult = kkmult
        self.historical_data = historical_data
        self.start_date, self.end_date = eval_period
        self.method = method

        if method == "kk" and kkmult == None:
            raise ValueError(
                "If method is 'kk' a KKMultiple object must be specified")

        if method not in self.possible_methods:
            raise ValueError(
                f"The method '{method}' is not one of the possible methods: {self.possible_methods}")

        if not isinstance(self.start_date, datetime):
            self.start_date = datetime.strptime(self.start_date, '%Y-%m-%d')
            self.end_date = datetime.strptime(self.end_date, '%Y-%m-%d')

        self.raw_train_data = None

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

        self._get_raw_train_data()
        self._get_multiples()
        self._get_buy_percentages()
        self.train_data = pl.concat(
            [self.raw_train_data, self.multiples, self.buy_percentages], how="horizontal")
        return self.train_data

    def get_accumulated_value(self, daily_budget=1000, remaining_budget=0, mayer_threshold=2.4):
        if self.method == 'kk':
            return self.kk(daily_budget, remaining_budget)
        if self.method == 'buy_every_day':
            return self.buy_every_day(daily_budget)
        if self.method == 'mayer':
            return self.mayer(daily_budget, mayer_threshold)

    def kk(self, daily_budget, remaining_budget):
        AccumulatedResult = namedtuple(
            'AccumulatedResult', ['amount_accumulated', 'remaining_budget'])
        self.get_train_data()
        amount_accumulated = 0
        for row in self.train_data.iter_rows():
            date, price, multiple, buy_percentage = row
            day_budget = daily_budget + remaining_budget
            day_budget_use = day_budget*buy_percentage
            day_purchase = day_budget_use/price
            amount_accumulated += day_purchase
            remaining_budget = day_budget - day_budget_use
        return AccumulatedResult(amount_accumulated=amount_accumulated, remaining_budget=remaining_budget)

    def buy_every_day(self, daily_budget):
        eval_data = self._get_raw_train_data()
        amount_accumulated = 0
        for row in eval_data.iter_rows():
            date, price = row
            amount_accumulated += daily_budget/price

        # row[1] is the column price of eval_data: eval_data['price']
        values_bought = [daily_budget/row[1]
                         for row in eval_data.iter_rows()]
        return sum(values_bought)

    def mayer(self, daily_budget, mayer_threshold):
        # not implemented yet
        # maybe you can use _get_multiples method with parameter mayer.
        # please find a better name for these methods: kk, buy_every_day, mayer
        pass
