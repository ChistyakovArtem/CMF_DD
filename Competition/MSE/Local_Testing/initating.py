import gdown
import pandas as pd
import os


def download_train_dataset():
    if not os.path.exists('dataset.zip'):
        import gdown
        gdown.download('https://drive.google.com/uc?export=download&id=1SdzyrOinu-qddwc6t79jLc3XrXL932gJ&confirm=t',
                       'dataset.zip')
        return 1
    else:
        return 0


def create_train_val():
    dataset_for_split = pd.read_csv('dataset.zip', index_col=0, header=[0, 1])
    dataset_for_split.rename(
        columns={
            'Unnamed: 209_level_1': 'count',
            'Unnamed: 210_level_1': 'price',
        },
        level=1,
        inplace=True
    )

    val_size = 200000
    lt_train = dataset_for_split.iloc[:-val_size]
    lt_val = dataset_for_split.iloc[-val_size:]

    compression_opts_train = dict(method='zip',
                                  archive_name='lt_train.csv')
    lt_train.to_csv('lt_train.zip', compression=compression_opts_train)

    compression_opts_val = dict(method='zip',
                                archive_name='lt_val.csv')
    lt_val.to_csv('lt_val.zip', compression=compression_opts_val)


def initiate():
    if download_train_dataset():
        create_train_val()
