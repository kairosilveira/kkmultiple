import polars as pl
from typing import Optional


class KKMultiple:
    """
    A class for calculating buy percentages based on historical data and predefined parameters.

    Args:
    - days_moving_avg (int): Number of days for calculating the moving average of historical data.
    - buy_params (dict): A dictionary defining buy percentages(values) associated with specific thresholds(keys).

    Attributes:
    - days_moving_avg (int): Number of days for calculating the moving average.
    - buy_params (dict): Dictionary defining buy percentages associated with specific thresholds.
    - multiple (float or None): The ratio of the current price to the moving average.
      Calculated using the 'calculate_multiple' method.

    Methods:
    - calculate_avg(historical_data): Calculate the moving average of the price column in historical data.
    - calculate_multiple(price, historical_data): Calculate the ratio of a given price to the moving average.
    - _find_min_threshold_gt_multiple(multiple=None): Find the minimum buy threshold greater than a given multiple.
    - get_buy_percentage(multiple=None): Retrieve the buy percentage based on the provided or stored multiple.
    - _validate_params(days_moving_avg, buy_params): Validate the provided parameters for days_moving_avg and buy_params.

    Note:
    - Ensure to call 'calculate_multiple' before using 'get_buy_percentage' to set the 'multiple' attribute.
    - Use '_validate_params' to ensure the provided parameters are valid during class initialization.

    Example Usage:
    ```
    class_params = {
        "days_moving_avg": 10,
        "buy_params": {0.5: 0.2, 1.0: 0.5, 1.5: 0.8}
    }
    kkmultiple = KKMultiple(**class_params)
    kkmultiple.calculate_multiple(current_price, historical_data)
    buy_percentage = kkmultiple.get_buy_percentage()
    ```
    """

    def __init__(self, days_moving_avg: int, buy_params: dict) -> None:
        self._validate_params(days_moving_avg, buy_params)

        self.days_moving_avg = days_moving_avg
        self.buy_params = buy_params
        self.multiple = None

    def _validate_params(self, days_moving_avg: int, buy_params: dict):
        # days_moving_avg
        error = ValueError(
            "days_moving_avg should be an integer greater than or equal to 1. days_moving_avg={}".format(days_moving_avg))
        if not (isinstance(days_moving_avg, int) or (isinstance(days_moving_avg, float) and days_moving_avg.is_integer())) or days_moving_avg < 1:
            raise error

        # buy_params
        sorted_keys = sorted(buy_params.keys())
        sorted_values = sorted(buy_params.values(), reverse=True)

        if sorted_keys != list(buy_params.keys()) or sorted_values != list(buy_params.values()):
            raise ValueError(
                "buy_params keys must be sorted in ascending order, and values must be sorted in descending order. {}".format(buy_params))

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

    def _find_min_threshold_gt_multiple(self, multiple=None):
        """
        Find the minimum buy threshold greater than a given multiple.

        Args:
        - multiple (float, optional): The ratio of the current price to the moving average.
        If None, the stored 'multiple' attribute will be used.

        Returns:
        - float or None: The minimum buy threshold greater than the provided or stored multiple.
        If no threshold is found, returns None.
        """
        if multiple is None:
            multiple = self.multiple
        buy_thresholds = list(self.buy_params.keys())
        passed_threshholds = [
            threshold for threshold in buy_thresholds if threshold > multiple]
        if passed_threshholds:
            min_threshold = min(passed_threshholds)
            return min_threshold
        else:
            return None

    def get_buy_percentage(self, multiple: Optional[float] = None):
        """
        Retrieve the buy percentage from buy_params based on the provided or stored multiple.

        Args:
        - multiple (float, optional): The ratio of the current price to the moving average.
        If None, the stored 'multiple' attribute will be used if available.

        Returns:
        - float: The buy percentage retrieved from buy_params according to the multiple.
        """
        if multiple is None and self.multiple is None:
            raise ValueError(
                "Call 'calculate_multiple' before running this method or provide a 'multiple' parameter.")
        elif multiple is None:
            multiple = self.multiple

        threshold = self._find_min_threshold_gt_multiple(multiple)
        return 0.0 if threshold is None else self.buy_params[threshold]
