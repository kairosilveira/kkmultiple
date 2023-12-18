class KKMultiple:
    def __init__(self, days_moving_avg, buy_thresholds, sell_threshold=None) -> None:
        self.days_moving_avg = days_moving_avg
        self.buy_thresholds = buy_thresholds
        self.sell_threshold = sell_threshold

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
        return price / moving_avg


