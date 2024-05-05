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
        trade_count = 0
        total_wins = 0
        total_losses = 0
        entry_price = None  # Initialize to None
        risk_per_trade = 0.1
        tp_factor = 8
        sl_factor = 5.3

        atr = self.strategy.calculate_atr()  # Calculate ATR
        signals = self.strategy.generate_signals()

        for i in range(len(self.data) - 1, 0, -1):
            if pd.isna(atr[i]):
                continue

            current_price = self.data['Close'][i]
            trade_risk = balance * risk_per_trade
            trade_size = trade_risk / atr[i]
            commission = trade_size / 750

            if position != 0:
                if position > 0:  # Long position
                    if current_price <= entry_price - atr[i] * sl_factor:
                        loss = trade_size + commission
                        balance -= loss
                        print(f"Trade #{trade_count}: Long - Entry: {entry_price} - Exit: {current_price} - Loss: {loss}")
                        self.log_trade(trade_count, 'Long', entry_price, current_price, -loss, balance)
                        position = 0
                        total_losses += 1
                    elif current_price >= entry_price + atr[i] * tp_factor:
                        profit = trade_size * tp_factor - commission
                        balance += profit
                        print(f"Trade #{trade_count}: Long - Entry: {entry_price} - Exit: {current_price} - Profit: {profit}")
                        self.log_trade(trade_count, 'Long', entry_price, current_price, profit, balance)
                        position = 0
                        total_wins += 1
                elif position < 0:  # Short position
                    if current_price >= entry_price + atr[i] * sl_factor:
                        loss = trade_size + commission
                        balance -= loss
                        print(f"Trade #{trade_count}: Short - Entry: {entry_price} - Exit: {current_price} - Loss: {loss}")
                        self.log_trade(trade_count, 'Short', entry_price, current_price, -loss, balance)
                        position = 0
                        total_losses += 1
                    elif current_price <= entry_price - atr[i] * tp_factor:
                        profit = trade_size * tp_factor - commission
                        balance += profit
                        print(f"Trade #{trade_count}: Short - Entry: {entry_price} - Exit: {current_price} - Profit: {profit}")
                        self.log_trade(trade_count, 'Short', entry_price, current_price, profit, balance)
                        position = 0
                        total_wins += 1

            if position == 0:
                if signals[i] == 'BUY':
                    position = 1
                    entry_price = current_price
                    trade_count += 1
                elif signals[i] == 'SELL':
                    position = -1
                    entry_price = current_price
                    trade_count += 1

            self.account_balance.append(balance)

        results = {
            'Final Balance': balance,
            'Total Trades': trade_count,
            'Total Wins': total_wins,
            'Total Losses': total_losses,
            'Trades': self.trades,
            'Account Balance': self.account_balance
        }

        print(f"Total Trades: {trade_count}, Total Wins: {total_wins}, Total Losses: {total_losses}")

        return results

    def log_trade(self, trade_number, type, entry, exit, profit_loss, balance):
        self.trades.append({
            'trade_number': trade_number,
            'type': type,
            'entry_price': entry,
            'exit_price': exit,
            'profit_loss': profit_loss,
            'current_balance': balance
        })

    def get_account_balance(self):
        return self.account_balance

    def get_trades(self):
        return self.trades
