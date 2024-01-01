from metrics.experiment import Experiment
from unittest.mock import patch
from datetime import datetime
from typing import Tuple
from datetime import datetime as dt
from hyperopt import hp
from metrics.crypto_accumulator import CryptoAccumulator


def test_get_experiment_interval(sample_historical_data):
    exp = Experiment(sample_historical_data, skip_days=2, retrain_freq=2)
    start_date, end_date = exp._get_experiment_interval()

    assert isinstance(start_date, datetime)
    assert isinstance(end_date, datetime)
    assert start_date == dt.strptime('2022-12-27', '%Y-%m-%d')
    assert end_date == dt.strptime('2023-01-04', '%Y-%m-%d')


def test__get_train_test_dates(sample_historical_data):
    exp1 = Experiment(sample_historical_data, skip_days=2, retrain_freq=2)
    exp2 = Experiment(sample_historical_data, skip_days=2, retrain_freq=3)

    result1 = exp1._get_train_test_dates()
    result2 = exp2._get_train_test_dates()

    result1_first_expexted = (
        dt.strptime('2022-12-27', '%Y-%m-%d'),
        dt.strptime('2022-12-28', '%Y-%m-%d'))
    result1_last_expexted = (
        dt.strptime('2023-01-02', '%Y-%m-%d'),
        dt.strptime('2023-01-03', '%Y-%m-%d'))
    result2_first_expexted = (
        dt.strptime('2022-12-27', '%Y-%m-%d'),
        dt.strptime('2022-12-29', '%Y-%m-%d'))
    result2_last_expexted = (
        dt.strptime('2023-01-02', '%Y-%m-%d'),
        dt.strptime('2023-01-04', '%Y-%m-%d'))

    assert isinstance(result1, list)
    assert len(result1) == 4
    assert len(result2) == 3
    assert result1[0] == result1_first_expexted
    assert result1[-1] == result1_last_expexted
    assert result2[0] == result2_first_expexted
    assert result2[-1] == result2_last_expexted


def test_kk_strategy(sample_historical_data, sample_parameters, sample_kkmultiple):
    exp1 = Experiment(sample_historical_data, skip_days=2, retrain_freq=2)
    exp2 = Experiment(sample_historical_data, skip_days=2, retrain_freq=3)

    # calculate expected values for retrain_freq = 2

    expected_accumulated1 = 0
    accumulator = CryptoAccumulator(
        sample_historical_data, ('2022-12-29', '2022-12-30'), kkmult=sample_kkmultiple)
    result = accumulator.get_accumulated_value()
    expected_accumulated1 += result.amount_accumulated

    accumulator = CryptoAccumulator(
        sample_historical_data, ('2022-12-31', '2023-01-01'), kkmult=sample_kkmultiple)
    result = accumulator.get_accumulated_value(
        remaining_budget=result.remaining_budget)
    expected_accumulated1 += result.amount_accumulated

    accumulator = CryptoAccumulator(
        sample_historical_data, ('2023-01-02', '2023-01-03'), kkmult=sample_kkmultiple)
    result = accumulator.get_accumulated_value(
        remaining_budget=result.remaining_budget)

    # expected values
    expected_accumulated1 += result.amount_accumulated
    expected_remaining_budget1 = result.remaining_budget

    # calculate expected values for retrain_freq = 3
    expected_accumulated2 = 0
    accumulator = CryptoAccumulator(
        sample_historical_data, ('2022-12-30', '2023-01-01'), kkmult=sample_kkmultiple)
    result = accumulator.get_accumulated_value()
    expected_accumulated2 += result.amount_accumulated

    accumulator = CryptoAccumulator(
        sample_historical_data, ('2023-01-02', '2023-01-04'), kkmult=sample_kkmultiple)
    result = accumulator.get_accumulated_value(
        remaining_budget=result.remaining_budget)

    # expected values
    expected_accumulated2 += result.amount_accumulated
    expected_remaining_budget2 = result.remaining_budget

    with patch('metrics.experiment.train') as mock_train:
        mock_train.return_value = sample_parameters

        result1 = exp1.kk_strategy(space_params={})
        result2 = exp2.kk_strategy(space_params={})

    assert isinstance(result1, tuple)
    assert result1.amount_accumulated == expected_accumulated1
    assert result1.remaining_budget == expected_remaining_budget1
    assert result2.amount_accumulated == expected_accumulated2
    assert result2.remaining_budget == expected_remaining_budget2
