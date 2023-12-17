class KKMetric:
    def __init__(self, days_moving_avg, buy_thresholds, sell_threshold=None) -> None:
        self.days_moving_avg = days_moving_avg
        self.buy_thresholds = buy_thresholds
        self.sell_threshold = sell_threshold


    def calculate_avg(self, historical_data):
        
        pass


    def calculate_multiple(self, price, historical_data):
        moving_avg = self.calculate_avg(historical_data)
        return price/moving_avg


