import pytest
import polars as pl

@pytest.fixture
def sample_historical_data():
    data = {
        'Date': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04'],
        'Open': [100, 110, 120, 130]
    }
    response = pl.DataFrame(data)
    response = response.with_columns([
        pl.col("Date").str.to_datetime(),
        pl.col("Open").cast(pl.Float64)
    ])
    return response


@pytest.fixture
def sample_parameters():
    class_params = {
        "days_moving_avg": 2,
        "buy_params": {0.5: 1.0, 0.8: 0.8, 1: 0.6, 1.6: 0.4, 2: 0.2}
    }
    return class_params