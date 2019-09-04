import pandas as pd
import geopandas as gpd


class Dataset():
    woreda = pd.read_csv('assets/data/woreda.csv')
    hc = pd.read_csv('assets/data/hc.csv')
    hp = pd.read_csv('assets/data/hp.csv')
    hc_mb = pd.read_csv('assets/data/hc_mb.csv')
    hp_mb = pd.read_csv('assets/data/hp_mb.csv')
    district_map = gpd.read_file('assets/map/districts/OptimizationDist.shp')
    district_map = district_map.to_crs(epsg=4201)

    region_map = gpd.read_file('assets/map/regions/Eth_Region_2013.shp')
    region_map = region_map.to_crs(epsg=4201)

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

    @staticmethod
    def merged_district_map():
        return Dataset.district_map.set_index('W_NAME').join(Dataset.woreda.set_index('wname'))
