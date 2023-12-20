import polars as pl
import pytest
from multiple.multiple import KKMultiple


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
        "buy_thresholds": [0.5, 0.8, 1, 1.6, 2],
        "buy_percentages": [1.0, 0.8, 0.6, 0.4, 0.2]
    }
    1.5
    return class_params


def test_calculate_avg(sample_historical_data, sample_parameters):
    days_moving_avg = sample_parameters["days_moving_avg"]
    buy_thresholds = sample_parameters["buy_thresholds"]
    buy_percentages = sample_parameters["buy_percentages"]

    kkmultiple = KKMultiple(days_moving_avg, buy_thresholds, buy_percentages)

    result = kkmultiple.calculate_avg(sample_historical_data)

    assert result == 125.0  # (120 + 130) / 2


def test_calculate_multiple(sample_historical_data, sample_parameters):
    days_moving_avg = sample_parameters["days_moving_avg"]
    buy_thresholds = sample_parameters["buy_thresholds"]
    buy_percentages = sample_parameters["buy_percentages"]

    kkmultiple = KKMultiple(days_moving_avg, buy_thresholds, buy_percentages)

    result = kkmultiple.calculate_multiple(140, sample_historical_data)

    assert result == 1.12  # 140 / 125.0


def test__find_min_threshold_gt_multiple_index(sample_parameters):

    days_moving_avg = sample_parameters["days_moving_avg"]
    buy_thresholds = sample_parameters["buy_thresholds"]
    buy_percentages = sample_parameters["buy_percentages"]
    kkmultiple = KKMultiple(days_moving_avg, buy_thresholds, buy_percentages)

    kkmultiple.multiple = 1.3

    result = kkmultiple._find_min_threshold_gt_multiple_index()

    assert result == 3  # 4 is the index of 1.6
    assert isinstance(result, int)


def test__find_min_threshold_gt_multiple_index_when_multiple_gt_all(sample_parameters):
    """
    Test the '_find_min_threshold_gt_multiple_index' method of the KKMultiple class
    when the 'multiple' attribute is greater than all thresholds.
    """
    days_moving_avg = sample_parameters["days_moving_avg"]
    buy_thresholds = sample_parameters["buy_thresholds"]
    buy_percentages = sample_parameters["buy_percentages"]
    kkmultiple = KKMultiple(days_moving_avg, buy_thresholds, buy_percentages)

    kkmultiple.multiple = 3.0

    result = kkmultiple._find_min_threshold_gt_multiple_index()

    assert result == None
