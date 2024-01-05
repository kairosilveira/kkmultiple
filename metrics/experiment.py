from multiple.kkmultiple import KKMultiple
from train.train import train
from metrics.cumulative_return import CumulativeReturn
import polars as pl
import pandas as pd
from collections import namedtuple
from datetime import timedelta


class Experiment:
    def __init__(self, historical_data: pl.DataFrame, retrain_freq: int = 30, train_days=100, skip_days: int = 300, max_evals: int = 500) -> None:
        self.historical_data = historical_data
        self.retrain_freq = retrain_freq
        self.train_days = train_days
        self.skip_days = skip_days
        self.max_evals = max_evals

    def run(self, space_params):
        ExperimentResult = namedtuple(
            'ExperimentResult',
            ['kk', 'mayer']
        )

        kkresult = self.kkmultiple_strategy(space_params )
        # mayer is not implemented yet
        # mayer_result = self.get_method_result(method='mayer')
        mayer_result = 0
        return ExperimentResult(kk=kkresult,
                                mayer=mayer_result
                                )

    def kkmultiple_strategy(self, space_params, initial_fiat=1000):
        train_test_periods_dict = self._get_train_test_dict()

        fiat = initial_fiat
        crypto = 0.0
        for train_period in train_test_periods_dict:
            start_train, end_train = train_period
            start_test, end_test = train_test_periods_dict[train_period]

            best_params = train(
                space_params, self.historical_data, start_train, end_train, self.max_evals)
            kk = KKMultiple(**best_params)
            trading_data = kk.get_trade_signals_df(
                self.historical_data, start_test, end_test)
            cum_return = CumulativeReturn(trading_data)
            result = cum_return.calculate(fiat, crypto)
            fiat = result.fiat
            crypto = result.crypto
    

        last_price = self.historical_data.filter(
            pl.col('date') == end_test
        )['price'][0]

        

        return fiat + last_price*crypto

    def _get_train_test_dict(self):
        start_date, end_date = self._get_experiment_interval()
        start_test_date = start_date + timedelta(days=self.train_days)

        test_periods = []
        while start_test_date + timedelta(days=self.retrain_freq - 1) <= end_date:
            test_periods.append(
                (start_test_date, start_test_date + timedelta(days=self.retrain_freq - 1))
            )
            start_test_date += timedelta(days=self.retrain_freq)

        train_periods = [
            (start_test - timedelta(days=self.train_days), start_test - timedelta(days=1))
            for start_test, _ in test_periods
        ]

        return dict(zip(train_periods, test_periods))


    def _get_experiment_interval(self):
        start = self.historical_data['date'][0] + \
            pd.Timedelta(days=self.skip_days)
        end = self.historical_data['date'][-1]
        return start, end
