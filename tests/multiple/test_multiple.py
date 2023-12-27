import polars as pl
import pytest
from multiple.kkmultiple import KKMultiple

def test_invalid_initialization():
    with pytest.raises(ValueError, match="days_moving_avg should be an integer greater than or equal to 1"):
        KKMultiple(days_moving_avg=0, buy_params={
                   0.5: 1.0, 0.8: 0.8, 1: 0.6, 1.6: 0.4, 2: 0.2})

    with pytest.raises(ValueError, match="buy_params keys must be sorted in ascending order, and values must be sorted in descending order."):
        KKMultiple(days_moving_avg=2, buy_params={
                   0.5: 1.0, 0.8: 0.8, 1: 0.6, 0.6: 0.4, 2: 0.2})


def test_calculate_avg(sample_historical_data, sample_parameters):
    days_moving_avg = sample_parameters["days_moving_avg"]
    buy_params = sample_parameters["buy_params"]

    kkmultiple = KKMultiple(days_moving_avg, buy_params)

    result = kkmultiple.calculate_avg(sample_historical_data)

    assert result == 125.0  # (120 + 130) / 2


def test_calculate_multiple(sample_historical_data, sample_parameters):
    days_moving_avg = sample_parameters["days_moving_avg"]
    buy_params = sample_parameters["buy_params"]

    kkmultiple = KKMultiple(days_moving_avg, buy_params)

    result = kkmultiple.calculate_multiple(140, sample_historical_data)

    assert result == 1.12  # 140 / 125.0


def test__find_min_threshold_gt_multiple(sample_parameters):

    days_moving_avg = sample_parameters["days_moving_avg"]
    buy_params = sample_parameters["buy_params"]

    kkmultiple = KKMultiple(days_moving_avg, buy_params)

    kkmultiple.multiple = 1.3

    result = kkmultiple._find_min_threshold_gt_multiple()

    assert result == 1.6
    assert isinstance(result, float)


def test__find_min_threshold_gt_multiple_when_multiple_gt_all(sample_parameters):
    """
    Test the '_find_min_threshold_gt_multiple' method of the KKMultiple class
    when the 'multiple' attribute is greater than all thresholds.
    """
    days_moving_avg = sample_parameters["days_moving_avg"]
    buy_params = sample_parameters["buy_params"]

    kkmultiple = KKMultiple(days_moving_avg, buy_params)

    kkmultiple.multiple = 3.0

    result = kkmultiple._find_min_threshold_gt_multiple()

    assert result == None


def test_get_buy_percentage_with_calculated_multiple(sample_historical_data, sample_parameters):
    days_moving_avg = sample_parameters["days_moving_avg"]
    buy_params = sample_parameters["buy_params"]

    kkmultiple = KKMultiple(days_moving_avg, buy_params)
    kkmultiple.calculate_multiple(140, sample_historical_data)

    result = kkmultiple.get_buy_percentage()

    # Corresponds to the buy percentage associated with the calculated multiple.
    assert result == 0.4


def test_get_buy_percentage_with_provided_multiple(sample_parameters):
    days_moving_avg = sample_parameters["days_moving_avg"]
    buy_params = sample_parameters["buy_params"]

    kkmultiple = KKMultiple(days_moving_avg, buy_params)

    result = kkmultiple.get_buy_percentage(multiple=1.5)

    # Corresponds to the buy percentage associated with the provided multiple.
    assert result == 0.4


def test_get_buy_percentage_without_calculated_or_provided_multiple(sample_parameters):
    days_moving_avg = sample_parameters["days_moving_avg"]
    buy_params = sample_parameters["buy_params"]

    kkmultiple = KKMultiple(days_moving_avg, buy_params)

    with pytest.raises(ValueError, match="Call 'calculate_multiple' before running this method or provide a 'multiple' parameter."):
        kkmultiple.get_buy_percentage()
