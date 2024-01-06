from hyperopt import fmin, tpe
from multiple.kkmultiple import KKMultiple
from metrics.cumulative_return import CumulativeReturn
from functools import partial
from typing import Dict, Union
from datetime import datetime
import polars as pl


def objective(params: Dict[str, Union[float, int]], historical_data: pl.DataFrame, 
              start_train_period: datetime, end_train_period: datetime) -> float:
    """
    Objective function for hyperparameter optimization using Hyperopt.

    Args:
    - params (Dict[str, Union[float, int]]): Hyperparameters for KKMultiple class.
    - historical_data (pl.DataFrame): DataFrame containing historical data.
    - start_train_period (datetime): Start date for training period.
    - end_train_period (datetime): End date for training period.

    Returns:
    - float: Negative of the total fiat value after trading for optimization.
    """
    params['days_moving_avg'] = int(params['days_moving_avg'])
    kkmult = KKMultiple(**params)
    trading_data = kkmult.get_trade_signals_df(
        historical_data, start_train_period, end_train_period)
    cum_return = CumulativeReturn(trading_data)
    result = cum_return.calculate()
    return -result.total_in_fiat


def train(space_params: Dict[str, float], historical_data: pl.DataFrame, 
          start_train_period: datetime, end_train_period: datetime, max_evals: int) -> Dict[str, Union[dict, float, int]]:
    """
    Train function for hyperparameter optimization using Hyperopt.

    Args:
    - space_params (Dict[str, Union[dict, float, int]]): Search space for hyperparameters.
    - historical_data (pl.DataFrame): DataFrame containing historical data.
    - start_train_period (datetime): Start date for training period.
    - end_train_period (datetime): End date for training period.
    - max_evals (int): Maximum number of evaluations for Hyperopt.

    Returns:
    - Dict[str, Union[dict, float, int]]: Best hyperparameters found during optimization.
    """
    best = fmin(
        fn=partial(objective,
                   historical_data=historical_data,
                   start_train_period=start_train_period,
                   end_train_period=end_train_period),
        space=space_params,
        algo=tpe.suggest,
        max_evals=max_evals)
    return best
