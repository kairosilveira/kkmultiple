from data.fetch_data import get_historical_crypto_data
from multiple.kkmultiple import KKMultiple
from train.train import train
from metrics.crypto_accumulator import CryptoAccumulator
import polars as pl
import pandas as pd
import datetime
from collections import namedtuple


class Experiment:
    def __init__(self, historical_data: pl.DataFrame, retrain_freq: int = 30, skip_days: int = 500, max_evals: int = 500) -> None:
        self.historical_data = historical_data
        self.retrain_freq = retrain_freq
        self.skip_days = skip_days
        self.max_evals = max_evals

    def run(self, space_params, initial_budget=0):
        ExperimentResult = namedtuple(
            'ExperimentResult', ['kkstrategy', 'buy_every_day_strategy'])

        kkresult = self.kk_strategy(space_params, initial_budget)
        buy_everyday_result = self.buy_every_day_strategy()
        return ExperimentResult(kkstrategy=kkresult,
                                buy_every_day_strategy=buy_everyday_result)

    def kk_strategy(self, space_params, initial_budget=0):
        AccumulatedResultExperiment = namedtuple(
            'AccumulatedResultExperiment', ['amount_accumulated', 'remaining_budget'])

        remaining_budget = initial_budget
        amount_accumulated = 0
        train_test_periods = self._get_train_test_dates()
        for i in range(len(train_test_periods)-1):
            train_period = train_test_periods[i]
            test_period = train_test_periods[i+1]
            best_params = train(
                space_params, self.historical_data, train_period, self.max_evals)
            kk = KKMultiple(**best_params)
            print("best_params: ", best_params)
            ca = CryptoAccumulator(
                historical_data=self.historical_data, eval_period=test_period, kkmult=kk)
            result = ca.get_accumulated_value(
                remaining_budget=remaining_budget)
            amount_accumulated += result.amount_accumulated
            remaining_budget += result.remaining_budget
            print(train_period)
            print(test_period)

        return AccumulatedResultExperiment(amount_accumulated=amount_accumulated, remaining_budget=remaining_budget)

    def buy_every_day_strategy(self):
        start, end = self._get_experiment_interval()
        experiment_data = self.historical_data.filter(
            (pl.col("date") >= start) & (pl.col("date") <= end))

        ca = CryptoAccumulator(
            historical_data=experiment_data, eval_period=(start, end), method="buy_every_day")
        accumulated = ca.get_accumulated_value(method='buy_every_day')

        return accumulated

    def _get_train_test_dates(self):
        start, end = self._get_experiment_interval()

        date_range = pd.date_range(
            start, end, freq=pd.Timedelta(days=self.retrain_freq+1))

        time_delta = pd.Timedelta(days=self.retrain_freq)
        return [(current_date, current_date + time_delta) for current_date in date_range]

    def _get_experiment_interval(self):
        start = self.historical_data['date'][0] + \
            pd.Timedelta(days=self.skip_days)
        end = self.historical_data['date'][-1]

        return start, end
