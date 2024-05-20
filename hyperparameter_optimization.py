import pandas as pd
import numpy as np
from backtester import Backtester
from performance_metrics import PerformanceMetrics

class HyperparameterOptimization:
    def __init__(self, data, strategy_class):
        self.data = data
        self.strategy_class = strategy_class

    def run_experiment(self, params):
        strategy = self.strategy_class(self.data,
                                       bollinger_window=params[0],
                                       bollinger_std_dev=params[1])
        risk_per_trade = 0.1
        backtester = Backtester(self.data, strategy)
        result = backtester.run_backtest(risk_per_trade=risk_per_trade,
                                         tp_factor=params[3],
                                         sl_factor=params[2])
        account_balance = result['Account Balance']
        trades = result['Trades']
        metrics = PerformanceMetrics(trades, account_balance)
        sharpe_ratio = metrics.calculate_sharpe_ratio()

        # Ensure the Sharpe ratio is finite
        if np.isnan(sharpe_ratio) or np.isinf(sharpe_ratio):
            return 1e10  # Return a large finite value to discard this set of parameters
        else:
            return -sharpe_ratio  # Negate because skopt minimizes the objective
