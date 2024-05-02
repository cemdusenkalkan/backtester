# data_manager.py

import pandas as pd


class DataManager:
    def load_data(self, filename):
        data = pd.read_csv(filename)
        return data
