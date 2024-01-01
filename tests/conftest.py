import pytest
import polars as pl
from multiple.kkmultiple import KKMultiple
from metrics.crypto_accumulator import CryptoAccumulator
from functools import namedtuple


@pytest.fixture
def sample_historical_data():
    data = {
        'date': ['2022-12-25', '2022-12-26', '2022-12-27', '2022-12-28', '2022-12-29', '2022-12-30', '2022-12-31', '2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04'],
        'price': [100, 100, 100, 100, 100, 100, 100, 100, 140, 120, 130,]
    }
    historical_data = pl.DataFrame(data)
    historical_data = historical_data.with_columns([
        pl.col("date").str.to_datetime(),
        pl.col("price").cast(pl.Float64)
    ])
    return historical_data


@pytest.fixture
def sample_parameters():
    class_params = {
        "days_moving_avg": 2,
        "buy_params": {0.5: 1.0, 0.8: 0.8, 1: 0.6, 1.6: 0.4, 2: 0.2}
    }
    return class_params


@pytest.fixture
def sample_kkmultiple(sample_parameters):
    return KKMultiple(**sample_parameters)


@pytest.fixture
def sample_eval_period():
    return ('2023-01-03', '2023-01-04')
