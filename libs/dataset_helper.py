import pandas as pd


class Dataset():
    woreda = pd.read_csv('assets/data/woreda.csv')
    hc = pd.read_csv('assets/data/hc.csv')
    hp = pd.read_csv('assets/data/hp.csv')
    hc_mb = pd.read_csv('assets/data/hc_mb.csv')
    hp_mb = pd.read_csv('assets/data/hp_mb.csv')

    @staticmethod
    def merged_woreda_hc():
        return pd.merge(Dataset.woreda, Dataset.hc, on='woreda', how='inner')

    @staticmethod
    def merged_woreda_hp():
        return pd.merge(Dataset.woreda, Dataset.hp, on='woreda', how='inner')

    @staticmethod
    def merged_woreda_hc_mb():
        return pd.merge(Dataset.woreda, Dataset.hc_mb, on='woreda', how='inner')

    @staticmethod
    def merged_woreda_hp_mb():
        return pd.merge(Dataset.woreda, Dataset.hp_mb, on='woreda', how='inner')
