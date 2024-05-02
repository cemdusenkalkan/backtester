import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

class PerformanceMetrics:
    def __init__(self, trades, account_balance):
        self.trades = trades
        self.account_balance = account_balance

    def calculate_cumulative_returns(self):
        initial_balance = self.account_balance[0]
        cumulative_returns = np.array(self.account_balance) / initial_balance - 1
        return cumulative_returns

    def calculate_sharpe_ratio(self, risk_free_rate=0.0):
        returns = np.diff(self.account_balance) / self.account_balance[:-1]
        excess_returns = returns - risk_free_rate
        sharpe_ratio = np.mean(excess_returns) / np.std(excess_returns) * np.sqrt(252)
        return sharpe_ratio

    def calculate_drawdowns(self):
        max_balance = np.maximum.accumulate(self.account_balance)
        drawdowns = (self.account_balance - max_balance) / max_balance
        return drawdowns

    def plot_results(self):
        sns.set(style='whitegrid')
        plt.figure(figsize=(12, 8))

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