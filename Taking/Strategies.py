import numpy as np
import joblib

class ZeroStrategy:

    def __init__(self, df, fees):
        self.dataframe = df
        self.fees = fees

    def get_delta_asset(self, row, usd_position, asset_position):
        return 0


class LGBM:

    def __init__(self, df, fees, mode='ethusdt'):
        self.fees = fees

        features = []
        df['ask_cumvol_0'] = df[mode + ':Binance:Spot_ask_vol_0']
        features.append('ask_cumvol_0')
        for i in range(1, 10):
            df['ask_cumvol_' + str(i)] = df['ask_cumvol_' + str(i - 1)] + \
                                         df[mode + ':Binance:Spot_ask_vol_' + str(i - 1)]
            features.append('ask_cumvol_' + str(i))

        df['bid_cumvol_0'] = df[mode + ':Binance:Spot_bid_vol_0']
        features.append('bid_cumvol_0')
        for i in range(1, 10):
            df['bid_cumvol_' + str(i)] = df['bid_cumvol_' + str(i - 1)] +\
                                         df[mode + ':Binance:Spot_bid_vol_' + str(i - 1)]
            features.append('bid_cumvol_' + str(i))

        for i in [2**i for i in range(13)]:
            df['rel_return_' + str(i)] = np.log(df['midprice']/df['midprice'].shift(i))
            features.append('rel_return_' + str(i))

        model = joblib.load(mode + '_500_model.pkl')

        df['predict'] = model.predict(df[features])

        self.dataframe = df

    def get_delta_asset(self, row, usd_position, asset_position):
        next_midprice = np.exp(row['predict']) * row['midprice_after_latency']

        mode = 'skip'
        if next_midprice > row['ask_price_after_latency'] + self.fees:
            mode = 'buy_asset'
        elif next_midprice < row['bid_price_after_latency'] - self.fees:
            mode = 'sell_asset'

        # print(mode)

        if mode == 'skip':
            return 0

        if mode == 'buy_asset':
            profit = next_midprice - row['ask_price_after_latency'] - self.fees

            return min([profit*40, row['ask_cumvol_0'], usd_position / (row['ask_price_after_latency'] + self.fees)])

        elif mode == 'sell_asset':
            profit = row['bid_price_after_latency'] - self.fees - next_midprice
            return -min([profit*40, row['bid_cumvol_0'], asset_position / (row['bid_price_after_latency'] - self.fees)])
