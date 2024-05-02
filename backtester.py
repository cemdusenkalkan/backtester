
import pandas as pd


class Backtester:
    def __init__(self, data, strategy):
        self.data = data
        self.strategy = strategy
        self.trades = []
        self.account_balance = []

    def run_backtest(self):
        balance = 100000  # Starting balance
        position = 0
        risk_per_trade = 0.1
        tp_factor = 3  # Take profit at 3x the risk
        sl_factor = 1  # Stop loss at 1x ATR

        atr = self.strategy.calculate_atr()  # Calculate ATR
        signals = self.strategy.generate_signals()

        for i in range(1, len(self.data)):
            if pd.isna(atr[i]):
                continue  # Skip if ATR is not available

            current_price = self.data['Close'][i]
            trade_risk = balance * risk_per_trade
            trade_size = trade_risk / atr[i]

            if position != 0:
                if position > 0:  # Long position
                    if current_price <= entry_price - atr[i] * sl_factor:
                        balance -= trade_size  # Stop loss hit
                        position = 0
                    elif current_price >= entry_price + atr[i] * tp_factor:
                        balance += trade_size * tp_factor  # Take profit hit
                        position = 0
                elif position < 0:  # Short position
                    if current_price >= entry_price + atr[i] * sl_factor:
                        balance -= trade_size  # Stop loss hit
                        position = 0
                    elif current_price <= entry_price - atr[i] * tp_factor:
                        balance += trade_size * tp_factor  # Take profit hit
                        position = 0

            if signals[i-1] == 'BUY' and position == 0:
                position = 1  # Go long
                entry_price = current_price
            elif signals[i-1] == 'SELL' and position == 0:
                position = -1  # Go short
                entry_price = current_price

            self.account_balance.append(balance)

        results = {
            'Final Balance': balance,
            'Total Trades': len(self.trades),
            'Trades': self.trades,
            'Account Balance': self.account_balance
        }

        return results


    def get_account_balance(self):
        return self.account_balance

    def get_trades(self):
        return self.trades
