class MyModel:

    @staticmethod
    def install():
        pass
        # !pip install scikit-learn
        # Тут короче когда в ноутбук скопипастите эту штуку на отправку -
        #                               добавьте всякие необходимые инсталлы (как выше)

    def __init__(self):
        pass

    @staticmethod
    def get_x_y(df):
        pass

    def preprocess(self, data):
        pass

    def fit(self, train_df):
        pass

    def predict(self, x):
        price = x['price']
        return price
