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
        'buy_percentages': [hp.uniform(f'buy_percentages_{i}', 0.0, 1.0) for i in range(5)],
        'days_moving_avg': hp.quniform('days_moving_avg', 20, 300, 1),
    }
    exp = Experiment(historical_data, retrain_freq=10, max_evals=30, skip_days=300)
    results = exp.run(space_params)

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Training Time: {elapsed_time} seconds")
    print(results)
