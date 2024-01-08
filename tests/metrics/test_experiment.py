from metrics.experiment import Experiment
from unittest.mock import patch
from datetime import datetime
from datetime import datetime as dt
from hyperopt import hp


def test_get_experiment_interval(sample_historical_data):
    exp = Experiment(sample_historical_data, skip_days=2,
                     train_days=2, retrain_freq=2)
    start_date, end_date = exp._get_experiment_interval()

    assert isinstance(start_date, datetime)
    assert isinstance(end_date, datetime)
    assert start_date == dt.strptime('2022-12-25', '%Y-%m-%d')
    assert end_date == dt.strptime('2023-01-04', '%Y-%m-%d')

# data = {
#         'date': ['2022-12-23', '2022-12-24', '2022-12-25', '2022-12-26', '2022-12-27', '2022-12-28', '2022-12-29', '2022-12-30', '2022-12-31', '2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04'],
#         'price': [100, 100, 100, 100, 100, 100, 100, 100, 200, 100, 200, 120, 130,]
#     }

def test_mayers_strategy(sample_historical_data):
    exp1 = Experiment(sample_historical_data, skip_days=8, train_days=2)
    exp2 = Experiment(sample_historical_data, skip_days=2, train_days=2)
    assert exp1.mayers_strategy() == 650
    assert exp2.mayers_strategy() == 1300

def date(date_str1, date_str2):
    return dt.strptime(date_str1, '%Y-%m-%d'), dt.strptime(date_str2, '%Y-%m-%d')


def test__get_train_test_dict(sample_historical_data):
    exp = Experiment(sample_historical_data, skip_days=2,
                     train_days=2, retrain_freq=2)
    train_test_dict = exp._get_train_test_dict()

    expected = {
        date('2022-12-25', '2022-12-26'): date('2022-12-27', '2022-12-28'),
        date('2022-12-27', '2022-12-28'): date('2022-12-29', '2022-12-30'),
        date('2022-12-29', '2022-12-30'): date('2022-12-31', '2023-01-01'),
        date('2022-12-31', '2023-01-01'): date('2023-01-02', '2023-01-03')
    }

    assert train_test_dict == expected


def test_kk_strategy(sample_historical_data, sample_kk_parameters):

    exp = Experiment(sample_historical_data, retrain_freq=3,
                     train_days=3, skip_days=2)

    expected_accumulated = (1000/100)*200
    with patch('metrics.experiment.train') as mock_train:
        mock_train.return_value = sample_kk_parameters

        result = exp.kkmultiple_strategy(space_params={})

    assert result == expected_accumulated
