import plotly.graph_objects as go
from plotly.subplots import make_subplots
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
        # Prepare data
        trade_indexes = np.arange(len(self.account_balance))
        cumulative_returns = self.calculate_cumulative_returns()
        drawdowns = self.calculate_drawdowns()

        # Create subplots
        fig = make_subplots(
            rows=3, cols=1,
            shared_xaxes=True,
            subplot_titles=("Account Balance", "Cumulative Returns", "Drawdowns"),
            vertical_spacing=0.1
        )

        # Plot Account Balance
        fig.add_trace(
            go.Scatter(x=trade_indexes, y=self.account_balance, mode='lines', name='Account Balance',
                       line=dict(color='RoyalBlue'), hoverinfo='y+name'),
            row=1, col=1
        )

        # Plot Cumulative Returns
        fig.add_trace(
            go.Scatter(x=trade_indexes, y=cumulative_returns, mode='lines', name='Cumulative Returns',
                       line=dict(color='Green'), hoverinfo='y+name'),
            row=2, col=1
        )

        # Plot Drawdowns
        fig.add_trace(
            go.Scatter(x=trade_indexes, y=drawdowns, mode='lines', name='Drawdowns',
                       line=dict(color='Crimson'), hoverinfo='y+name'),
            row=3, col=1
        )

        # Update x-axis and y-axis labels
        fig.update_xaxes(title_text="Trade Number", row=3, col=1)
        fig.update_yaxes(title_text="Balance ($)", row=1, col=1)
        fig.update_yaxes(title_text="Returns (%)", row=2, col=1)
        fig.update_yaxes(title_text="Drawdown (%)", row=3, col=1)

        # Update layout
        fig.update_layout(
            height=900, width=700,
            title_text="Trading Performance Metrics",
            hovermode='x unified'
        )

        # Show plot
        fig.show()
