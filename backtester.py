import pandas as pd

class Backtester:
    def __init__(self, data, strategy):
        self.data = data
        self.strategy = strategy
        self.trades = []
        self.account_balance = []
        self.position = 0
        self.entry_price = None
        self.trailing_stop_loss = None
        self.trailing_take_profit = None
        self.partial_entry_count = 0
        self.partial_size = 30
        self.sl_factor = 6.5
        self.tp_factor = 12

    def log_trade(self, trade_number, type, entry, exit, profit_loss, balance):
        print(f"Trade #{trade_number}: {type} - Entry: {entry} - Exit: {exit} - {'Profit' if profit_loss > 0 else 'Loss'}: {profit_loss}")
        self.trades.append({
            'trade_number': trade_number,
            'type': type,
            'entry_price': entry,
            'exit_price': exit,
            'profit_loss': profit_loss,
            'current_balance': balance
        })

    def update_trailing_stop(self, current_price, atr_value):
        if self.position != 0:  # Update only if there is an open position
            self.trailing_stop_loss = max(self.trailing_stop_loss,
                                          current_price - atr_value * self.sl_factor) if self.position > 0 else \
                min(self.trailing_stop_loss, current_price + atr_value * self.sl_factor)

    def update_trailing_take_profit(self, current_price, atr_value):
        if self.position == 1:  # Long position
            self.trailing_take_profit = max(self.trailing_take_profit, current_price + atr_value * self.tp_factor)
        elif self.position == -1:  # Short position
            self.trailing_take_profit = min(self.trailing_take_profit, current_price - atr_value * self.tp_factor)

    def run_backtest(self):
        balance = 100000
        trade_count = 0
        total_wins = 0
        total_losses = 0
        atr = self.strategy.calculate_atr()
        upper_band, lower_band = self.strategy.calculate_bollinger_bands()

        signals = self.strategy.generate_signals()
        for i in range(len(self.data) - 1, 0, -1):
            current_price = self.data['Close'][i]
            if pd.isna(atr[i]):
                continue

            if self.position == 0 and not pd.isna(upper_band[i]) and not pd.isna(lower_band[i]):
                if current_price > upper_band[i] and signals[i] == 'BUY':
                    self.position = 1
                    self.entry_price = current_price
                    self.trailing_stop_loss = current_price - atr[i] * self.sl_factor
                    self.partial_entry_count = 1
                    trade_count += 1
                elif current_price < lower_band[i] and signals[i] == 'SELL':
                    self.position = -1
                    self.entry_price = current_price
                    self.trailing_stop_loss = current_price + atr[i] * self.sl_factor
                    self.partial_entry_count = 1
                    trade_count += 1

            elif self.position != 0:
                self.update_trailing_stop(current_price, atr[i])

                if self.partial_entry_count < self.partial_size:
                    if (self.position == 1 and current_price < self.entry_price - atr[i] * 0.2) or \
                            (self.position == -1 and current_price > self.entry_price + atr[i] * 0.2):
                        # Add another part of the position
                        self.entry_price = (self.entry_price * self.partial_entry_count + current_price) / (
                                    self.partial_entry_count + 1)
                        self.partial_entry_count += 1

                if (self.position == 1 and current_price <= self.trailing_stop_loss) or \
                        (self.position == -1 and current_price >= self.trailing_stop_loss):
                    profit_loss = ((
                                               current_price - self.entry_price) / self.entry_price) * balance * 0.1 if self.position == 1 else \
                        ((self.entry_price - current_price) / self.entry_price) * balance * 0.1
                    balance += profit_loss
                    self.log_trade(trade_count, 'Long' if self.position == 1 else 'Short', self.entry_price,
                                   current_price, profit_loss, balance)
                    self.position = 0
                    total_wins += 1 if profit_loss > 0 else 0
                    total_losses += 1 if profit_loss < 0 else 0

            self.account_balance.append(balance)

        results = {
            'Final Balance': balance,
            'Total Trades': trade_count,
            'Total Wins': total_wins,
            'Total Losses': total_losses,
            'Trades': self.trades,
            'Account Balance': self.account_balance
        }
        return results

    def get_account_balance(self):
        return self.account_balance

    def get_trades(self):
        return self.trades
