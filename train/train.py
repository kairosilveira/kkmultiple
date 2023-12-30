from hyperopt import fmin, tpe
from multiple.kkmultiple import KKMultiple
from metrics.crypto_accumulator import CryptoAccumulator
from functools import partial


def objective(params, historical_data, train_period):
    days_moving_avg = params['days_moving_avg']
    buy_thresholds = sorted(params['buy_thresholds'])
    buy_percentages = params['buy_percentages']
    buy_params = dict(zip(buy_thresholds, buy_percentages))
    kkmult = KKMultiple(days_moving_avg, buy_params)
    metric_calculator = CryptoAccumulator(historical_data=historical_data, eval_period=train_period, kkmult=kkmult)
    crypto_accumulated = metric_calculator.get_accumulated_value()
    return -crypto_accumulated.amount_accumulated


def train(space_params, historical_data, train_period, max_evals):
    best = fmin(
        fn=partial(objective, historical_data=historical_data,
                   train_period=train_period),
        space=space_params,
        algo=tpe.suggest,
        max_evals=max_evals)

    buy_thresholds = sorted(list(best.values())[:-1])
    buy_percentages = space_params['buy_percentages']
    buy_params = dict(zip(buy_thresholds, buy_percentages))

    best_formated = {
        'days_moving_avg': best['days_moving_avg'],
        'buy_params': buy_params
    }
    return best_formated
