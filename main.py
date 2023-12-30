from data.fetch_data import get_historical_crypto_data
from metrics.experiment import Experiment
from hyperopt import hp



if __name__ == "__main__":

    historical_data = get_historical_crypto_data(
        "2021-02-01", "2023-12-29", "Open")

    space_params = {
        'buy_thresholds': [hp.uniform(f'buy_thresholds_{i}', 0.5, 3) for i in range(5)],
        'buy_percentages': [1, 0.8, 0.6, 0.4, 0.2],
        'days_moving_avg': hp.quniform('days_moving_avg', 20, 500, 1),
    }
    exp = Experiment(historical_data, max_evals=200)
    results = exp.run(space_params)

    print(results)