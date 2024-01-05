import polars as pl
from typing import Optional
from datetime import datetime


class KKMultiple:

    def __init__(self, days_moving_avg: int, threshold: float, buy_factor: float = 0.5, sell_factor: float = 2.0) -> None:
        self._validate_params(days_moving_avg, threshold,
                              buy_factor, sell_factor)

        self.days_moving_avg = int(days_moving_avg)
        self.threshold = threshold
        self.buy_factor = buy_factor
        self.sell_factor = sell_factor
        self.multiple = None
        self.trade_period = None

    def _validate_params(self, days_moving_avg: int, threshold: float, buy_factor: float, sell_factor: float):
        error = ValueError(
            "days_moving_avg should be an integer greater than or equal to 1. days_moving_avg={}".format(days_moving_avg))
        if not (isinstance(days_moving_avg, int) or
                (isinstance(days_moving_avg, float) and days_moving_avg.is_integer())) or \
                days_moving_avg < 1:
            raise error

        if not all(isinstance(param, (int, float)) for param in [threshold, buy_factor, sell_factor]):
            raise ValueError(
                "Threshold, buy_factor, and sell_factor should be either int or float.")

    def calculate_avg(self, historical_data: pl.DataFrame, days_moving_avg: Optional[int] = None) -> float:
        """
        Calculate the average of the price column in the historical data.

        Args:
        - historical_data (polars.DataFrame): DataFrame containing historical data, columns are 'Date' and 'Price'.
        - days_moving_avg (Optional[int]): Number of days to consider for the moving average.
        If not provided, the default value from the class attribute will be used.

        Returns:
        - float: The average of the price column over the specified number of days.
        """
        if days_moving_avg is None:
            days_moving_avg = self.days_moving_avg

        price_col = historical_data.columns[1]
        return historical_data[price_col][-days_moving_avg:].mean()

    def calculate_multiple(self, price: float, historical_data: pl.DataFrame, mayer: bool = False) -> float:
        """
        Calculate the ratio of a given price to the moving average of historical data.

        Args:
        - price (float): The current price.
        - historical_data (polars.DataFrame): DataFrame containing historical data.
        - mayer (bool): Flag indicating whether to use a specific Mayer multiple. If True, a 200-day moving average is used.

        Returns:
        - float: The ratio of the given price to the moving average of historical data.
        """
        if mayer:
            days_moving_avg = 200
        else:
            days_moving_avg = self.days_moving_avg

        moving_avg = self.calculate_avg(historical_data, days_moving_avg)
        self.multiple = price / moving_avg
        return self.multiple

    def decide_action(self, multiple: Optional[float] = None):
        """
        Determine the trading action based on the provided or stored multiple.

        Args:
        - multiple (float, optional): The ratio of the current price to the moving average. If not provided,
        the stored 'multiple' attribute will be used.

        Returns:
        - str: The trading action, which can be 'buy', 'sell', or 'none'.

        Raises:
        - ValueError: If 'calculate_multiple' hasn't been called and 'multiple' is not provided.
        """
        if multiple is None and self.multiple is None:
            raise ValueError(
                "Call 'calculate_multiple' before running this method or provide a 'multiple' parameter.")
        elif multiple is None:
            multiple = self.multiple

        if multiple < self.threshold * self.buy_factor:
            return 'buy'
        elif multiple > self.threshold * self.sell_factor:
            return 'sell'
        else:
            return 'none'

    def get_trade_signals_df(self, historical_data, start_date, end_date, include_multiple=False, mayer=False):

        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')

        trade_period = self._get_trade_period_df(
            historical_data, start_date, end_date)
        multiples = self._get_multiples_col(historical_data, mayer)
        actions_col = self._get_actions_col(historical_data, mayer, multiples)

        if not include_multiple:
            return pl.concat([trade_period, actions_col], how='horizontal')
        else:
            return pl.concat([trade_period, multiples, actions_col], how='horizontal')

    def _get_actions_col(self, historical_data, mayer=False, multiples_col=None):

        if multiples_col is None:
            multiples_col = self._get_multiples_col(historical_data, mayer)
        return multiples_col.map_rows(
            lambda row: self.decide_action(row[0]),
            return_dtype=pl.Utf8
        ).rename({"map": "action"})

    def _get_multiples_col(self, historical_data, mayer=False) -> pl.DataFrame:
        """
        Get the multiples calculated based on the provided strategy.

        Args:
        - mayer (bool): If True, calculate multiples using Mayer's method.

        Returns:
        polars.DataFrame: DataFrame containing the calculated multiples.
        """

        if self.trade_period is None:
            raise ValueError(
                "Call '_get_trade_period_df' before running this method")

        return self.trade_period.map_rows(
            lambda row: self.calculate_multiple(
                row[1],
                historical_data.filter(pl.col('date') < row[0]),
                mayer
            ),
            return_dtype=pl.Float64
        ).rename({"map": "multiple"})

    def _get_trade_period_df(self, historical_data, start_date, end_date) -> pl.DataFrame:
        """
        Get the training data within the specified period.

        Returns:
        polars.DataFrame: DataFrame containing the training data.
        """
        self.trade_period = historical_data.filter(
            (pl.col("date") >= start_date) & (pl.col("date") <= end_date))

        return self.trade_period
