from multiple.multiple import KKMultiple
from data.fetch_data import get_historical_crypto_data

kk_multiple = KKMultiple(days_moving_avg=5, buy_thresholds=[1, 2, 3,4,5])

def test_calculate_avg():
    historical_data = get_historical_crypto_data('2014-12-01', '2023-12-31', 'Open', 'BTC-USD')  
    expected_avg = 42310.965625
    actual_avg = kk_multiple.calculate_avg(historical_data)
    assert actual_avg == expected_avg

def test_calculate_multiple():
    historical_data = get_historical_crypto_data('2014-12-01', '2023-12-31', 'Open', 'BTC-USD')  
    price = 100
    expected_multiple = 0.0023634535048501393
    actual_multiple = kk_multiple.calculate_multiple(price, historical_data)
    assert actual_multiple == expected_multiple 

