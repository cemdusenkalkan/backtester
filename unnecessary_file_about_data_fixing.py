import pandas as pd
import os

file_path = '/Users/cem/Desktop/May Algo/backtester/Binance_BTCUSDT_2023_minute.csv'

if not os.path.exists(file_path):
    print(f"Error: File not found at {file_path}")
else:
    try:

        column_names = ['unix', 'date', 'symbol', 'open', 'high', 'low', 'close', 'volume', 'volume_from', 'tradecount']

        df = pd.read_csv(file_path, delimiter=',', skiprows=1, names=column_names, low_memory=False)

        print("Column names:", df.columns.tolist())

        print("First few rows:\n", df.head())

        df = df[pd.to_numeric(df['unix'], errors='coerce').notnull()]

        df.drop(columns=['unix'], inplace=True)

        df[['date', 'time']] = df['date'].str.split(';', expand=True)

        # Convert relevant columns to numeric types
        df['open'] = pd.to_numeric(df['open'], errors='coerce')
        df['high'] = pd.to_numeric(df['high'], errors='coerce')
        df['low'] = pd.to_numeric(df['low'], errors='coerce')
        df['close'] = pd.to_numeric(df['close'], errors='coerce')
        df['volume'] = pd.to_numeric(df['volume'], errors='coerce')
        df['volume_from'] = pd.to_numeric(df['volume_from'], errors='coerce')
        df['tradecount'] = pd.to_numeric(df['tradecount'], errors='coerce')

        df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'], errors='coerce')
        df.drop(columns=['date', 'time'], inplace=True)

        df = df.dropna(subset=['datetime'])

        new_df = df[['symbol', 'open', 'high', 'low', 'close', 'volume_from', 'volume', 'tradecount']]
        new_df.columns = ['Symbol', 'Open', 'High', 'Low', 'Close', 'Volume BTC', 'Volume USDT', 'Tradecount']

        output_file_path = '/Users/cem/Desktop/May Algo/backtester/output.csv'
        new_df.to_csv(output_file_path, index=False)

        print(f'Converted file saved to {output_file_path}')
    except Exception as e:
        print(f"An error occurred: {e}")
