from hyperopt import fmin, tpe
from multiple.kkmultiple import KKMultiple
from metrics.crypto_accumulator import CryptoAccumulator
from metrics.cumulative_return import CumulativeReturn
from functools import partial


def objective(params, historical_data, start_train_period, end_train_period):

    params['days_moving_avg']=int(params['days_moving_avg'])
    kkmult = KKMultiple(**params)
    trading_data = kkmult.get_trade_signals_df(
        historical_data, start_train_period, end_train_period)
    cum_return = CumulativeReturn(trading_data)
    result = cum_return.calculate()
    return -result.total_in_fiat


def train(space_params, historical_data, start_train_period, end_train_period, max_evals):
    best = fmin(
        fn=partial(objective,
                   historical_data=historical_data,
                   start_train_period=start_train_period,
                   end_train_period=end_train_period),
        space=space_params,
        algo=tpe.suggest,
        max_evals=max_evals)

    return best
