# data_manager.py

import pandas as pd
import numpy as np


class DataManager:
    def load_data(self, filename):
        data = pd.read_csv(filename, delimiter=';')  # because my file uses this as delimiter.
        data.columns = data.columns.str.strip()

        data.fillna(method='ffill', inplace=True)
        data.fillna(method='bfill', inplace=True)

        for column in ['Open', 'High', 'Low', 'Close', 'Volume BTC', 'Volume USDT']:
            daily_change = data[column].pct_change().abs()
            outlier_mask = daily_change > 0.5
            data.loc[outlier_mask, column] = np.nan
            data[column].fillna(method='ffill', inplace=True)

        print("Data loaded and processed:", data.head())
        return data







