from collections import namedtuple


class KKMultiple:
    def __init__(self, days_moving_avg, buy_thresholds, buy_percentages) -> None:
        self.days_moving_avg = days_moving_avg
        self.buy_thresholds = buy_thresholds
        self.buy_percentages = buy_percentages
        self.multiple = None

    def calculate_avg(self, historical_data):
        """
        Calculate the moving average of the price column in the historical data.

        Args:
        - historical_data (polars.DataFrame): DataFrame containing historical data.

        Returns:
        - float: The moving average of the price column over the specified number of days.
        """
        price_col = historical_data.columns[1]
        return historical_data[price_col][-self.days_moving_avg:].mean()

    def calculate_multiple(self, price, historical_data):
        """
        Calculate the ratio of a given price to the moving average of historical data.

        Args:
        - price (float): The current price.
        - historical_data (polars.DataFrame): DataFrame containing historical data.

        Returns:
        - float: The ratio of the given price to the moving average of historical data.
        """
        moving_avg = self.calculate_avg(historical_data)
        self.multiple = price / moving_avg
        return self.multiple

    def _find_min_threshold_gt_multiple_index(self):
        passed_threshholds = [
            threshold for threshold in self.buy_thresholds if threshold > self.multiple]
        if passed_threshholds:
            min_threshold = min(passed_threshholds)
            index_min_threshold = self.buy_thresholds.index(min_threshold)
            return index_min_threshold
        else:
            return None

    def name(self):

        if not self.multiple:
            raise ValueError(
                "Calculate the 'multiple' before accessing the buy name. Use the 'calculate_multiple' method first.")

        min_threshold_gt_multiple_index = self._find_min_threshold_gt_multiple_index()

        return self.buy_percentages[min_threshold_gt_multiple_index]
