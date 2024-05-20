import pandas as pd
import numpy as np
from sklearn.model_selection import ParameterSampler
from backtester import Backtester
from performance_metrics import PerformanceMetrics


class HyperparameterOptimization:
    def __init__(self, data, strategy_class):
        self.data = data
        self.strategy_class = strategy_class

    def run_experiment(self, params):
        strategy = self.strategy_class(self.data,
                                       bollinger_window=params['bollinger_window'],
                                       bollinger_std_dev=params['bollinger_std_dev'])
        risk_per_trade = 0.1
        backtester = Backtester(self.data, strategy)
        result = backtester.run_backtest(risk_per_trade=risk_per_trade,
                                         tp_factor=params['tp_factor'],
                                         sl_factor=params['sl_factor'])
        metrics = PerformanceMetrics(result['Trades'], result['Account Balance'])
        sharpe_ratio = metrics.calculate_sharpe_ratio()

        if np.isnan(sharpe_ratio) or np.isinf(sharpe_ratio):
            sharpe_ratio = -np.inf
        else:
            sharpe_ratio = max(min(sharpe_ratio, 100), -100)

        return sharpe_ratio

    def random_search(self, param_distributions, n_iter=100):
        param_list = list(ParameterSampler(param_distributions, n_iter=n_iter))
        results = []
        for params in param_list:
            score = self.run_experiment(params)
            results.append((params, score))
        return sorted(results, key=lambda x: x[1], reverse=True)
