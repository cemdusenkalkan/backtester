# main.py

from data_manager import DataManager
from backtester import Backtester
from performance_metrics import PerformanceMetrics

def main():
    # Load data
    data_manager = DataManager()
    data = data_manager.load_data('your_data.csv')

    # Backtest
    backtester = Backtester(data)
    results = backtester.run_backtest()

    # Calculate performance metrics
    metrics = PerformanceMetrics(results)
    cumulative_profits = metrics.calculate_cumulative_profits()
    sharpe_ratio = metrics.calculate_sharpe_ratio()

    # Visualize results using PerformanceMetrics
    metrics.plot_results()

    print("Sharpe Ratio:", sharpe_ratio)

if __name__ == "__main__":
    main()
