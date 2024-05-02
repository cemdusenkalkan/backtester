# main.py

from data_manager import DataManager
from backtester import Backtester
from performance_metrics import PerformanceMetrics
from strategy import Strategy


def main():
    data_manager = DataManager()
    data = data_manager.load_data('btc_data.csv')

    strategy = Strategy(data)

    backtester = Backtester(data, strategy)
    results = backtester.run_backtest()
    metrics = PerformanceMetrics(results['Trades'], results['Account Balance'])
    cumulative_returns = metrics.calculate_cumulative_returns()
    sharpe_ratio = metrics.calculate_sharpe_ratio()

    metrics.plot_results()

    print("Sharpe Ratio:", sharpe_ratio)
    print("Cumulative Returns:", cumulative_returns[-1])


if __name__ == "__main__":
    main()
