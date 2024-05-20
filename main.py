from data_manager import DataManager
from performance_metrics import PerformanceMetrics
from strategy import Strategy
from hyperparameter_optimization import HyperparameterOptimization
import pandas as pd
from scipy.stats import uniform, randint

def main():
    data_manager = DataManager()
    data = data_manager.load_data('btc_data.csv')

    strategy_class = Strategy

    optimizer = HyperparameterOptimization(data, strategy_class)

    # Define the parameter distributions
    param_distributions = {
        'tp_factor': randint(3, 26),
        'sl_factor': uniform(0.6, 0.6),
        'bollinger_window': randint(10, 51),
        'bollinger_std_dev': uniform(1.5, 2.0)
    }

    results = optimizer.random_search(param_distributions, n_iter=100)

    # Save results to CSV
    results_df = pd.DataFrame([{'params': result[0], 'sharpe_ratio': result[1]} for result in results])
    results_df.to_csv('random_search_optimization_results.csv', index=False)

    best_result = results[0]
    best_params = best_result[0]
    best_sharpe_ratio = best_result[1]

    print(f"\nBest Parameters: {best_params}\n")
    print(f"Best Sharpe Ratio: {best_sharpe_ratio}\n")

if __name__ == "__main__":
    main()
