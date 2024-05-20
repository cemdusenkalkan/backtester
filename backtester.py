import pandas as pd

class Backtester:
    def __init__(self, data, strategy):
        self.data = data
        self.strategy = strategy
        self.trades = []
        self.account_balance = []

    def run_backtest(self, risk_per_trade=0.1, tp_factor=15, sl_factor=4.5):
        balance = 100000  # Starting balance
        position = 0
        trade_count = 0
        entry_price = None

        atr = self.strategy.calculate_atr()
        signals = self.strategy.generate_signals()

        for i in range(len(self.data) - 1, 0, -1):
            if pd.isna(atr[i]):
                continue

            current_price = self.data['Close'][i]
            trade_risk = balance * risk_per_trade
            trade_size = trade_risk / atr[i]
            commission = max(1, trade_size * 0.001)  # Ensure a minimum commission

            if position != 0:
                if position > 0:  # Long position
                    if current_price <= entry_price - atr[i] * sl_factor:
                        loss = trade_size + commission
                        balance -= loss
                        self.log_trade(trade_count, entry_price, current_price, -loss, balance)
                        position = 0
                    elif current_price >= entry_price + atr[i] * tp_factor:
                        profit = trade_size * tp_factor - commission
                        balance += profit
                        self.log_trade(trade_count, entry_price, current_price, profit, balance)
                        position = 0
                elif position < 0:  # Short position
                    if current_price >= entry_price + atr[i] * sl_factor:
                        loss = trade_size + commission
                        balance -= loss
                        self.log_trade(trade_count, entry_price, current_price, -loss, balance)
                        position = 0
                    elif current_price <= entry_price - atr[i] * tp_factor:
                        profit = trade_size * tp_factor - commission
                        balance += profit
                        self.log_trade(trade_count, entry_price, current_price, profit, balance)
                        position = 0

            if position == 0:
                if signals[i-1] == 'BUY':
                    position = 1
                    entry_price = current_price
                    trade_count += 1
                    print(f"Trade #{trade_count}: BUY at {entry_price}")
                elif signals[i-1] == 'SELL':
                    position = -1
                    entry_price = current_price
                    trade_count += 1
                    print(f"Trade #{trade_count}: SELL at {entry_price}")

            self.account_balance.append(balance)

        results = {
            'Final Balance': balance,
            'Total Trades': trade_count,
            'Trades': self.trades,
            'Account Balance': self.account_balance
        }

        return results

    def log_trade(self, trade_number, entry, exit, profit_loss, balance):
        self.trades.append({
            'trade_number': trade_number,
            'entry_price': entry,
            'exit_price': exit,
            'profit_loss': profit_loss,
            'current_balance': balance
        })
