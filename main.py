from data.fetch_data import get_historical_crypto_data
from metrics.experiment import Experiment
from hyperopt import hp
import time


if __name__ == "__main__":

    start_time = time.time()
    historical_data = get_historical_crypto_data(
        "2000-02-01", "2026-12-25", "Open")
    space_params = {
        'buy_thresholds': [hp.uniform(f'buy_thresholds_{i}', 0.5, 3) for i in range(5)],
        'buy_percentages': [1, 0.8, 0.6, 0.4, 0.2],
        'days_moving_avg': hp.quniform('days_moving_avg', 20, 3, 1),
    }
    exp = Experiment(historical_data, retrain_freq=1000, max_evals=3)
    results = exp.run(space_params)

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Elapsed Time: {elapsed_time} seconds")
    print(results)
