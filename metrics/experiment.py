from multiple.kkmultiple import KKMultiple
from train.train import train
from metrics.crypto_accumulator import CryptoAccumulator
import polars as pl
import pandas as pd
from collections import namedtuple


class Experiment:
    def __init__(self, historical_data: pl.DataFrame, retrain_freq: int = 30, skip_days: int = 500, max_evals: int = 500) -> None:
        self.historical_data = historical_data
        self.retrain_freq = retrain_freq
        self.skip_days = skip_days
        self.max_evals = max_evals

    def run(self, space_params, initial_budget=0):
        ExperimentResult = namedtuple(
            'ExperimentResult',
            ['kkstrategy', 'buy_every_day_strategy', 'mayer']
        )

        kkresult = self.get_method_result(
            method='kk', space_params=space_params, initial_budget=initial_budget)

        buy_everyday_result = self.get_method_result(method='buy_every_day')

        # mayer is not implemented yet
        # mayer_result = self.get_method_result(method='mayer')
        mayer_result = 0
        return ExperimentResult(kkstrategy=kkresult,
                                buy_every_day_strategy=buy_everyday_result,
                                mayer=mayer_result
                                )

    def get_method_result(self, method='kk', space_params=None, initial_budget=0):
        if method == 'kk':
            if space_params == None:
                raise ValueError(
                    "space_params should be provided if method = kk")
            return self.kk_strategy(space_params, initial_budget= initial_budget)
        else:
            start, end = self._get_experiment_interval()
            accumulator = CryptoAccumulator(
                historical_data=self.historical_data, eval_period=(start, end), method=method)
            accumulated = accumulator.get_accumulated_value()
            return accumulated

    def kk_strategy(self, space_params, initial_budget=0):
        AccumulatedResultExperiment = namedtuple(
            'AccumulatedResultExperiment',
            ['amount_accumulated', 'remaining_budget']
        )

        remaining_budget = initial_budget
        amount_accumulated = 0
        train_test_periods = self._get_train_test_dates()
        for train_period, test_period in zip(train_test_periods, train_test_periods[1:]):
            best_params = train(
                space_params, self.historical_data, train_period, self.max_evals)
            kk = KKMultiple(**best_params)
            accumulator = CryptoAccumulator(
                historical_data=self.historical_data, eval_period=test_period, kkmult=kk)

            result = accumulator.get_accumulated_value(
                remaining_budget=remaining_budget)

            amount_accumulated += result.amount_accumulated
            remaining_budget = result.remaining_budget

        return AccumulatedResultExperiment(
            amount_accumulated=amount_accumulated,
            remaining_budget=remaining_budget
        )

    def _get_train_test_dates(self):
        start, end = self._get_experiment_interval()

        date_range = pd.date_range(
            start, end, freq=pd.Timedelta(days=self.retrain_freq))

        time_delta = pd.Timedelta(days=self.retrain_freq-1)
        return [(current_date, current_date + time_delta) for current_date in date_range
                if current_date + time_delta <= end]

    def _get_experiment_interval(self):
        start = self.historical_data['date'][0] + \
            pd.Timedelta(days=self.skip_days)
        end = self.historical_data['date'][-1]

        return start, end
