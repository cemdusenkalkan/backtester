import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd


class PerformanceMetrics:
    def __init__(self, trades, account_balance):
        self.trades = trades
        self.account_balance = account_balance

    def calculate_cumulative_returns(self):
        initial_balance = self.account_balance[0]
        cumulative_returns = np.array(self.account_balance) / initial_balance - 1
        return cumulative_returns

    def calculate_sharpe_ratio(self):
        returns = self.account_balance.pct_change().dropna()
        mean_return = returns.mean()
        std_return = returns.std()
        sharpe_ratio = mean_return / std_return

        # Handle NaN or infinity
        if np.isnan(sharpe_ratio) or np.isinf(sharpe_ratio):
            sharpe_ratio = np.nan

        return sharpe_ratio

        sharpe_ratio = np.mean(excess_returns) / std_excess_returns * np.sqrt(252)
        return sharpe_ratio

    def calculate_drawdowns(self):
        max_balance = np.maximum.accumulate(self.account_balance)
        drawdowns = (self.account_balance - max_balance) / max_balance
        return drawdowns

    def plot_results(self, top_results=None):
        sns.set(style='whitegrid')
        plt.figure(figsize=(12, 8))

        if top_results:
            for i, result in enumerate(top_results):
                trade_indexes = range(len(result['Account Balance']))
                plt.subplot(311)
                plt.plot(trade_indexes, result['Account Balance'], label=f'Result {i+1}')
            plt.title('Account Balance per Trade', fontsize=10)
            plt.ylabel('Balance ($)', fontsize=9)
            plt.legend(loc='upper left')

            plt.subplot(312)
            for i, result in enumerate(top_results):
                cumulative_returns = np.array(result['Account Balance']) / result['Account Balance'][0] - 1
                trade_indexes = range(len(result['Account Balance']))
                plt.plot(trade_indexes, cumulative_returns, label=f'Result {i+1}')
            plt.title('Cumulative Returns per Trade', fontsize=10)
            plt.ylabel('Returns (%)', fontsize=9)
            plt.legend(loc='upper left')

            plt.subplot(313)
            for i, result in enumerate(top_results):
                max_balance = np.maximum.accumulate(result['Account Balance'])
                drawdowns = (result['Account Balance'] - max_balance) / max_balance
                trade_indexes = range(len(result['Account Balance']))
                plt.plot(trade_indexes, drawdowns, label=f'Result {i+1}')
            plt.title('Drawdowns per Trade', fontsize=10)
            plt.ylabel('Drawdown (%)', fontsize=9)
            plt.xlabel('Trade Number', fontsize=9)
            plt.legend(loc='upper left')
        else:
            trade_indexes = range(len(self.account_balance))

            plt.subplot(311)
            plt.plot(trade_indexes, self.account_balance, color='steelblue', label='Account Balance')
            plt.title('Account Balance per Trade', fontsize=10)
            plt.ylabel('Balance ($)', fontsize=9)
            plt.legend(loc='upper left')

            plt.subplot(312)
            cumulative_returns = self.calculate_cumulative_returns()
            plt.plot(trade_indexes, cumulative_returns, color='darkgreen', label='Cumulative Returns')
            plt.title('Cumulative Returns per Trade', fontsize=10)
            plt.ylabel('Returns (%)', fontsize=9)
            plt.legend(loc='upper left')

            plt.subplot(313)
            drawdowns = self.calculate_drawdowns()
            plt.plot(trade_indexes, drawdowns, color='crimson', label='Drawdowns')
            plt.title('Drawdowns per Trade', fontsize=10)
            plt.ylabel('Drawdown (%)', fontsize=9)
            plt.xlabel('Trade Number', fontsize=9)
            plt.legend(loc='upper left')

        plt.tight_layout()
        plt.show()
