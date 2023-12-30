import pytest
import polars as pl
from multiple.kkmultiple import KKMultiple


@pytest.fixture
def sample_historical_data():
    data = {
        'date': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04'],
        'price': [100, 140, 120, 130]
    }
    response = pl.DataFrame(data)
    response = response.with_columns([
        pl.col("date").str.to_datetime(),
        pl.col("price").cast(pl.Float64)
    ])
    return response


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
