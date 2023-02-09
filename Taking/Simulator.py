def run_simulation(strategy, mode='ethusdt'):
    df = strategy.dataframe

    usd_position = 500
    asset_position = 500 / df['midprice'].iloc[0]
    fees = strategy.fees

    eps = 1e-9

    logs = {
        'usd_position': [usd_position],
        'asset_position': [asset_position],
        'pnl': [0],
        'price': [df['midprice'].iloc[0]],
        'cumulative_fees': [0],
        'time': [],
        'volume(usd)': [0],
        'volume(asset)': [0]
    }

    for i, row in df.iterrows():

        delta_asset = strategy.get_delta_asset(row, usd_position=usd_position, asset_position=asset_position)
        if delta_asset > 0:
            # buy asset sell usd
            delta_usd = -delta_asset * (row['ask_price_after_latency'] + fees)
        else:
            # buy asset sell usd
            delta_usd = -delta_asset * (row['bid_price_after_latency'] - fees)

        if delta_asset > 0:
            # buy
            assert delta_asset <= row[mode + ':Binance:Spot_ask_vol_0'] + eps, 'Есть пробитие (ask)'
        else:
            assert abs(delta_asset) <= row[mode + ':Binance:Spot_bid_vol_0'] + eps, 'Есть пробитие (bid)'

        # print(usd_position, asset_position, delta_usd, delta_asset)

        new_usd_position = usd_position + delta_usd
        new_asset_position = asset_position + delta_asset

        assert (new_usd_position >= -eps), "Negative usd position"
        assert (new_asset_position >= -eps), "Negative asset position"

        usd_position = new_usd_position
        asset_position = new_asset_position

        logs['usd_position'].append(usd_position)
        logs['asset_position'].append(asset_position)
        logs['pnl'].append(usd_position + asset_position * row['midprice'] - 1000)
        logs['price'].append(row['midprice'])
        logs['cumulative_fees'].append(logs['cumulative_fees'][-1] + abs(delta_usd) * fees)
        logs['time'].append(row['exchange_ts'])
        logs['volume(usd)'].append(logs['volume(usd)'][-1] + abs(delta_usd))
        logs['volume(asset)'].append(logs['volume(asset)'][-1] + abs(delta_asset))

    return logs
