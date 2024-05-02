# strategy.py
import pandas as pd
import numpy as np


class Strategy:
    def __init__(self, data):
        self.data = data

    def calculate_bollinger_bands(self, window=20, num_std_dev=2):
        rolling_mean = self.data['Close'].rolling(window=window).mean()
        rolling_std = self.data['Close'].rolling(window=window).std()
        upper_band = rolling_mean + num_std_dev * rolling_std
        lower_band = rolling_mean - num_std_dev * rolling_std
        return upper_band, lower_band

    def calculate_moving_average(self, window=20):
        return self.data['Close'].rolling(window=window).mean()

    def calculate_atr(self, window=14):
        high_low = self.data['High'] - self.data['Low']
        high_close = np.abs(self.data['High'] - self.data['Close'].shift())
        low_close = np.abs(self.data['Low'] - self.data['Close'].shift())
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = np.max(ranges, axis=1)
        atr = true_range.rolling(window=window).mean()
        return atr

    def generate_signals(self, window=20, num_std_dev=2):
        upper_band, lower_band = self.calculate_bollinger_bands(window, num_std_dev)
        signals = []
        for i in range(len(self.data)):
            if pd.isna(upper_band[i]) or pd.isna(lower_band[i]):
                signals.append('HOLD')
            elif self.data['Close'][i] > upper_band[i]:
                signals.append('BUY')
            elif self.data['Close'][i] < lower_band[i]:
                signals.append('SELL')
            else:
                signals.append('HOLD')

            if i < 10:
                print(
                    f"Index: {i}, Close: {self.data['Close'][i]}, Upper: {upper_band[i]}, Lower: {lower_band[i]}, Signal: {signals[-1]}")
        return signals
