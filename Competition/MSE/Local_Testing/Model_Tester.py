import pandas as pd
import numpy as np
from tqdm.notebook import tqdm
from sklearn.metrics import mean_squared_error as mse
import matplotlib.pyplot as plt


class Dataloader():
    def __init__(
            self,
            dataframe: pd.DataFrame,
            window_size: int,
            step_size: int,
            horizon: int,
            first_pred: int
    ):
        self.df = dataframe
        self.window_size = window_size
        self.step_size = step_size
        self.horizon = horizon
        self.first_pred = first_pred
        assert self.first_pred > self.window_size
        feat_idx = []
        target_idx = []
        for i in range(self.first_pred, self.df.shape[0], self.step_size):
            feat_idx.append(range(i-self.horizon-self.window_size+1, i-self.horizon+1))
            target_idx.append(i)
        self.feat_idx = feat_idx
        self.target_idx = target_idx

    def __len__(self):
        return len(self.feat_idx)

    def __iter__(self):
        self.iter = 0
        return self

    def __next__(self):
        if self.iter < len(self.feat_idx):
            feat = self.df.iloc[self.feat_idx[self.iter]]
            target = self.df.iloc[self.target_idx[self.iter], -1]
            self.iter += 1
            return feat, target
        else:
            raise StopIteration


class ForecastingModel:

    @staticmethod
    def download_dataframe():
        import os  # default installed lib
        if not os.path.exists('train_dataset.zip'):
            import gdown
            gdown.download('https://drive.google.com/uc?export=download&id=1SdzyrOinu-qddwc6t79jLc3XrXL932gJ&confirm=t', 'train_dataset.zip')

    def read_dataframe(self):
        path = 'train_dataset.zip'
        if self.mode == 'test':
            path = 'lt_train.zip'
        elif self.mode == 'train':
            self.download_dataframe()
        else:
            raise AttributeError('Wrong mode')

        self.train_df = pd.read_csv(path, index_col=0, header=[0, 1])
        self.train_df.rename(
            columns={
                'Unnamed: 209_level_1': 'count',
                'Unnamed: 210_level_1': 'price',
            },
            level = 1,
            inplace = True
        )

    def fit_model(self):
        self.model.fit(self.train_df)

    def __init__(self, mode, model):
        self.train_df = None
        self.model = model
        self.mode = mode

        self.read_dataframe()
        self.fit_model()

    def forecast(self, x):
        prediction = self.model.predict(x)
        return np.array(prediction).flatten()[0]


def test_model(model):
    dataset = pd.read_csv('lt_val.zip', index_col=0, header=[0, 1])
    dataset.rename(
        columns={
            'Unnamed: 209_level_1': 'count',
            'Unnamed: 210_level_1': 'price',
        },
        level=1,
        inplace=True
    )
    dataset.head()

    window_size = 1

    loader = Dataloader(
        dataframe=dataset,
        window_size=window_size,
        step_size=1,
        horizon=60,
        first_pred=1060
    )

    forecaster = ForecastingModel(mode='test', model=model)

    import time
    start_time = time.time()

    pred = []
    target = []

    for feat, _target in loader:
        pred.append(forecaster.forecast(feat))
        target.append(_target)

    exec_time = time.time() - start_time
    mse_loss = mse(pred, target)

    return {
        'exec_time': exec_time,
        'mse_loss': mse_loss,
        'forecaster': forecaster
    }
