import pytest
import polars as pl
from multiple.kkmultiple import KKMultiple
from datetime import datetime


# TESTS INIT
def test_validate_params_valid():
    # Valid parameters
    kk = KKMultiple(days_moving_avg=10, threshold=0.5,
                    buy_factor=0.2, sell_factor=2.0)
    assert kk is not None


def test_validate_params_invalid_days_moving_avg():
    # Invalid days_moving_avg
    with pytest.raises(ValueError, match="days_moving_avg should be an integer greater than or equal to 1"):
        KKMultiple(days_moving_avg=0, threshold=0.5,
                   buy_factor=0.2, sell_factor=2.0)


def test_validate_params_invalid_param_types():
    # Invalid parameter types
    with pytest.raises(ValueError, match="Threshold, buy_factor, and sell_factor should be either int or float."):
        KKMultiple(days_moving_avg=10, threshold='invalid',
                   buy_factor=0.2, sell_factor=2.0)

# TESTS METHODS


def test_calculate_avg(sample_historical_data, sample_kkmultiple):
    result = sample_kkmultiple.calculate_avg(sample_historical_data)

    assert result == 125.0  # (120 + 130) / 2


def test_calculate_multiple(sample_historical_data, sample_kkmultiple):
    result = sample_kkmultiple.calculate_multiple(140, sample_historical_data)

    assert result == 1.12  # 140 / 125.0


def test_decide_action(sample_kkmultiple):
    sample_kkmultiple.multiple = 1
    action1 = sample_kkmultiple.decide_action()
    sample_kkmultiple.multiple = 0.98
    action2 = sample_kkmultiple.decide_action()
    action3 = sample_kkmultiple.decide_action(1.321)

    assert action1 == 'none'
    assert action2 == 'buy'
    assert action3 == 'sell'


def test__get_trade_period_df(sample_historical_data, sample_kkmultiple, sample_eval_period):
    start_date, end_date = sample_eval_period
    trade_period = sample_kkmultiple._get_trade_period_df(
        sample_historical_data, start_date, end_date)

    assert isinstance(trade_period, pl.DataFrame)
    assert trade_period.shape == (2, 2)
    assert trade_period["date"][0] == start_date
    assert trade_period["date"][-1] == end_date
    assert "date" in trade_period.columns
    assert "price" in trade_period.columns
    assert pl.Datetime in trade_period.dtypes
    assert pl.Float64 in trade_period.dtypes


def test__get_multiples_col(sample_historical_data, sample_kkmultiple, sample_eval_period):
    start_date, end_date = sample_eval_period
    sample_kkmultiple._get_trade_period_df(
        sample_historical_data, start_date, end_date)
    multiples = sample_kkmultiple._get_multiples_col(sample_historical_data)

    mult_dict = multiples.to_dict()
    print(mult_dict)
    assert isinstance(multiples, pl.DataFrame)
    assert pl.Float64 in multiples.dtypes
    assert multiples.shape == (2, 1)
    assert mult_dict['multiple'][0] == 120/150
    assert mult_dict['multiple'][1] == 130/160


def test__get_actions_col(sample_historical_data, sample_kkmultiple, sample_eval_period):
    start_date = datetime.strptime('2022-12-30', '%Y-%m-%d')
    end_date = datetime.strptime('2023-01-01', '%Y-%m-%d')
    sample_kkmultiple._get_trade_period_df(
        sample_historical_data, start_date, end_date)

    actions = sample_kkmultiple._get_actions_col(
        sample_historical_data).to_dict()

    assert actions['action'][0] == 'none'
    assert actions['action'][1] == 'sell'
    assert actions['action'][2] == 'buy'


def test_get_trade_signals_df(sample_historical_data, sample_kkmultiple, sample_eval_period):
    start_date, end_date = sample_eval_period
    df_trade_signals = sample_kkmultiple.get_trade_signals_df(
        sample_historical_data, start_date, end_date)

    assert df_trade_signals.shape == (2, 3)
    assert 'price' in df_trade_signals.columns
    assert 'action' in df_trade_signals.columns
    assert 'date' in df_trade_signals.columns
    assert 'multiple' not in df_trade_signals.columns

    df_trade_signals = sample_kkmultiple.get_trade_signals_df(
        sample_historical_data, start_date, end_date, True)
    assert 'multiple' in df_trade_signals.columns
