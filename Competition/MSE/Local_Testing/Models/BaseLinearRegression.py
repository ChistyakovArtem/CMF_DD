# --- 1088.6742596626282 seconds ---
# 0.01024202712417327

class MyModel:

    @staticmethod
    def install():
        pass
        # !pip install scikit-learn
        # Тут короче когда в ноутбук скопипастите эту штуку на отправку -
        #                               добавьте всякие необходимые инсталлы (как выше)

    def __init__(self):
        self.install()
        from sklearn.preprocessing import StandardScaler
        from sklearn.linear_model import LinearRegression

        self.columns_to_pick = None

        self.scaler = StandardScaler()
        self.lin_reg = LinearRegression()
        pass

    @staticmethod
    def get_x_y(df):
        df['delta'] = df['price'].shift(60) - df['price']
        df = df.dropna()
        x = df.drop(columns=['delta'])
        y = df['delta']
        return [x, y]

    def preprocess(self, data):
        data = data[self.columns_to_pick]
        data = data.fillna(0)
        return data

    def fit(self, train_df):
        self.columns_to_pick = train_df.columns[train_df.isna().sum(axis=0) < 70000]
        train_df = self.preprocess(train_df)

        x, y = self.get_x_y(train_df)

        self.scaler.fit(x)
        x = self.scaler.transform(x)

        self.lin_reg.fit(x, y)

    def predict(self, x):
        price = x['price']

        x = self.preprocess(x)
        x = self.scaler.transform(x)
        delta = self.lin_reg.predict(x)
        return price + delta
