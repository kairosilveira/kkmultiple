from data.fetch_data import get_historical_crypto_data
from metrics.experiment import Experiment
from hyperopt import hp
import time


if __name__ == "__main__":

    start_time = time.time()
    historical_data = get_historical_crypto_data(
        "2000-02-01", "2028-12-25", "Open")

    print(historical_data)
    space_params = {
        'days_moving_avg': hp.quniform('days_moving_avg', 5, 300, 1),
        'threshold': hp.uniform('threshold', 0.5, 3),
        'buy_factor': hp.uniform('buy_factor', 0.0, 5.0),
        'sell_factor': hp.uniform('sell_factor', 0.0, 5.0),

    }
    exp = Experiment(historical_data, retrain_freq=30,
                     train_days=180, skip_days=300, max_evals=10)
    results = exp.run(space_params)

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Training Time: {elapsed_time} seconds")
    print(results)
