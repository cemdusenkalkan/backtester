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
        entry_price = None  # Initialize to None
        risk_per_trade = 0.1
        tp_factor = 15
        sl_factor = 4.5  # Stop loss at 1x ATR

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
                # Update for position checking
                if position > 0:  # Long position
                    if current_price <= entry_price - atr[i] * sl_factor:
                        loss = trade_size + commission
                        balance -= loss
                        print(f"Trade #{trade_count}: Entry: {entry_price} - Stop/TP: {entry_price - atr[i] * sl_factor}/{entry_price + atr[i] * tp_factor} - Loss: {loss} - Current Balance: {balance}")
                        self.log_trade(trade_count, entry_price, current_price, -loss, balance)
                        position = 0
                    elif current_price >= entry_price + atr[i] * tp_factor:
                        profit = trade_size * tp_factor - commission
                        balance += profit
                        print(f"Trade #{trade_count}: Entry: {entry_price} - Stop/TP: {entry_price - atr[i] * sl_factor}/{entry_price + atr[i] * tp_factor} - Profit: {profit} - Current Balance: {balance}")
                        self.log_trade(trade_count, entry_price, current_price, profit, balance)
                        position = 0
                elif position < 0:  # Short position
                    if current_price >= entry_price + atr[i] * sl_factor:
                        loss = trade_size + commission
                        balance -= loss
                        print(f"Trade #{trade_count}: Entry: {entry_price} - Stop/TP: {entry_price + atr[i] * sl_factor}/{entry_price - atr[i] * tp_factor} - Loss: {loss} - Current Balance: {balance}")
                        self.log_trade(trade_count, entry_price, current_price, -loss, balance)
                        position = 0
                    elif current_price <= entry_price - atr[i] * tp_factor:
                        profit = trade_size * tp_factor - commission
                        balance += profit
                        print(f"Trade #{trade_count}: Entry: {entry_price} - Stop/TP: {entry_price + atr[i] * sl_factor}/{entry_price - atr[i] * tp_factor} - Profit: {profit} - Current Balance: {balance}")
                        self.log_trade(trade_count, entry_price, current_price, profit, balance)
                        position = 0

            if position == 0:
                if signals[i-1] == 'BUY':
                    position = 1
                    entry_price = current_price
                    trade_count += 1
                elif signals[i-1] == 'SELL':
                    position = -1
                    entry_price = current_price
                    trade_count += 1

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

    def get_account_balance(self):
        return self.account_balance

    def get_trades(self):
        return self.trades
