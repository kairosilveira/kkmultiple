from train.train import train
from metrics.crypto_accumulator import CryptoAccumulator
from multiple.kkmultiple import KKMultiple
from data.fetch_data import get_historical_crypto_data
from hyperopt import hp

if __name__ == "__main__":

    space_params = {
        'buy_thresholds': [hp.uniform(f'buy_thresholds_{i}', 0.5, 3) for i in range(5)],
        'buy_percentages': [1, 0.8, 0.6, 0.4, 0.2],
        'days_moving_avg': hp.quniform('days_moving_avg', 20, 500, 1),
    }
    historical_data = get_historical_crypto_data(
        '2015-01-01', '2020-01-01', 'Open')
    train_period = ('2019-10-01', '2019-12-31')
    train(space_params, historical_data, train_period, 200)
