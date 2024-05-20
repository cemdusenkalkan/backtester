from data_manager import DataManager
from performance_metrics import PerformanceMetrics
from strategy import Strategy
from hyperparameter_optimization import HyperparameterOptimization
import pandas as pd
from skopt.space import Real, Integer
from skopt import gp_minimize
from tqdm import tqdm
import numpy as np


def main():
    data_manager = DataManager()
    data = data_manager.load_data('output.csv')

    # Clean the data to ensure no NaN or infinite values
    data = data.replace([np.inf, -np.inf], np.nan).dropna()

    strategy_class = Strategy
    optimizer = HyperparameterOptimization(data, strategy_class)

    # Define the parameter space
    param_space = [
        Integer(10, 50, name='bollinger_window'),
        Real(1.5, 3.5, name='bollinger_std_dev'),
        Real(0.6, 1.2, name='sl_factor'),
        Integer(3, 25, name='tp_factor')
    ]

    # Known best parameters and their Sharpe ratio
    best_known_params = {
        'bollinger_std_dev': 3.31555931074553,
        'bollinger_window': 12,
        'sl_factor': 1.1204578278118884,
        'tp_factor': 19
    }
    best_known_sharpe_ratio = 0.1  # The Sharpe ratio from these parameters

    # Initial points for Bayesian optimization
    x0 = [
        [best_known_params['bollinger_window'], best_known_params['bollinger_std_dev'],
         best_known_params['sl_factor'], best_known_params['tp_factor']]
    ]
    y0 = [-best_known_sharpe_ratio]  # Negated because skopt minimizes the objective

    # Run Bayesian optimization with progress bar
    n_calls = 100  # Number of iterations for Bayesian optimization
    with tqdm(total=n_calls) as pbar:
        def update_pbar(x):
            pbar.update(1)
            return optimizer.run_experiment(x)

        res = gp_minimize(update_pbar, param_space, n_calls=n_calls, random_state=42, n_jobs=-1, x0=x0, y0=y0)

    best_params = {
        'bollinger_window': res.x[0],
        'bollinger_std_dev': res.x[1],
        'sl_factor': res.x[2],
        'tp_factor': res.x[3]
    }

    best_sharpe_ratio = -res.fun

    print(f"\nBest Parameters: {best_params}\n")
    print(f"Best Sharpe Ratio: {best_sharpe_ratio}\n")

    # Save results to CSV
    results_df = pd.DataFrame(res.x_iters, columns=['bollinger_window', 'bollinger_std_dev', 'sl_factor', 'tp_factor'])
    results_df['sharpe_ratio'] = -res.func_vals
    results_df.to_csv('bayesian_optimization_results.csv', index=False)

    print(f"Total trades with best parameters: {len(res.x_iters)}")
    print(f"Best results saved to bayesian_optimization_results.csv")


if __name__ == "__main__":
    main()
