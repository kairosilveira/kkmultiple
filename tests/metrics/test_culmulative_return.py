from metrics.cumulative_return import CumulativeReturn
from datetime import datetime


def test_calculate(sample_historical_data, sample_kkmultiple):
    start_date = datetime.strptime('2022-12-30', '%Y-%m-%d')
    end_date = datetime.strptime('2023-01-03', '%Y-%m-%d')
    trading_data = sample_kkmultiple.get_trade_signals_df(
        sample_historical_data, start_date, end_date)

    cum_return = CumulativeReturn(trading_data)
    result = cum_return.calculate()
    
    assert isinstance(result.total_in_fiat, float)
    assert result.total_in_fiat == (1000/100)*200/120*120


def test_calculate_buy(sample_historical_data, sample_kkmultiple):
    start_date = datetime.strptime('2023-01-03', '%Y-%m-%d')
    end_date = datetime.strptime('2023-01-04', '%Y-%m-%d')
    trading_data = sample_kkmultiple.get_trade_signals_df(
        sample_historical_data, start_date, end_date)

    cum_return = CumulativeReturn(trading_data)
    result = cum_return.calculate()
    assert isinstance(result.total_in_fiat, float)
    assert result.total_in_fiat == (1000/120)*130
