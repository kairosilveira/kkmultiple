import pytest
import polars as pl
from datetime import datetime
from multiple.kkmultiple import KKMultiple


@pytest.fixture
def sample_historical_data():
    data = {
        'date': ['2022-12-23', '2022-12-24', '2022-12-25', '2022-12-26', '2022-12-27', '2022-12-28', '2022-12-29', '2022-12-30', '2022-12-31', '2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04'],
        'price': [100, 100, 100, 100, 100, 100, 100, 100, 200, 100, 200, 120, 130,]
    }
    historical_data = pl.DataFrame(data)
    historical_data = historical_data.with_columns([
        pl.col("date").str.to_datetime(),
        pl.col("price").cast(pl.Float64)
    ])
    return historical_data


@pytest.fixture
def sample_kk_parameters():
    class_params = {
        'days_moving_avg': 2,
        'threshold': 1.1,
        'buy_factor': 0.9,
        'sell_factor': 1.2
    }
    return class_params


@pytest.fixture
def sample_kkmultiple(sample_kk_parameters):
    return KKMultiple(**sample_kk_parameters)


@pytest.fixture
def sample_eval_period():
    start_date = datetime.strptime('2023-01-03', '%Y-%m-%d')
    end_date = datetime.strptime('2023-01-04', '%Y-%m-%d')
    return (start_date, end_date)
