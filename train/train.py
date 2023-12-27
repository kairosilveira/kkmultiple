from hyperopt import fmin, tpe, hp
from multiple.kkmultiple import KKMultiple
from metrics.crypto_accumulator import CryptoAccumulator


def objective(params, historical_data, eval_period):
    days_moving_avg = params['days_moving_avg']
    buy_thresholds = sorted(params['buy_thresholds'])
    buy_percentages = params['buy_percentages']
    buy_params = dict(zip(buy_thresholds, buy_percentages))
    kkmult = KKMultiple(days_moving_avg, buy_params)
    obj = CryptoAccumulator(kkmult, historical_data, eval_period)
    crypto_accumulated = obj.accu()
    return -crypto_accumulated


def train():
    space = {
        'buy_thresholds': [hp.uniform(f'buy_thresholds_{i}', 0.5, 3) for i in range(5)],
        'buy_percentages': [1, 0.8, 0.6, 0.4, 0.2],
        'days_moving_avg': hp.quniform('your_param', 20, 500, 1),
    }

    best = fmin(fn=objective, space=space, algo=tpe.suggest, max_evals=100)

    print(best)
