from train.train import train
from metrics.crypto_accumulator import CryptoAccumulator
from multiple.kkmultiple import KKMultiple

if __name__ == "__main__":
    # train()
    print("run")

    params = {
        'days_moving_avg': 200,
        'buy_params': {
            0.1: 1.0,
            0.5: 0.8,
            0.9: 0.6,
            1.5: 0.4,
            2.0: 0.2
        }
    }

    kk = KKMultiple(**params)
    kk.calculate_avg()
