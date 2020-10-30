import ee
import geopandas as gpd
import json
from GeoPoint import GeoPoint
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

ee.Initialize()
forest = []
city = []
for kind in [21, 51]:
    area = None
    for year in [2000, 2005, 2010, 2015]:
        db_name = 'GIS_data/guangzhou_{}.gdb'.format(kind)
        str_kind = {21: 'lin_di', 51: 'cheng_shi'}[kind]
        layer_name = 'gzS{}'.format(year)

        gdf = gpd.read_file(db_name, layer=layer_name)
        gdf.to_crs('EPSG:4326', inplace=True)
        gdf_multiploygons = json.loads(gdf.to_json())['features']

        for current_year in range(year, year+5):
            year_ndvi = pd.DataFrame()


            geo = ee.FeatureCollection(gdf_multiploygons)

            area = GeoPoint(geometry=geo, name=str_kind+'_'+str(year))

            area.setDataSets('{}-01-01'.format(current_year), '{}-12-31'.format(current_year),
                             "MODIS/006/MOD13Q1")
            ndvi = area.getNdviMean(scale=0.0001)

            if kind == 21:
                forest.append((current_year, ndvi))
            elif kind == 51:
                city.append((current_year, ndvi))
            print('finish {}, {}'.format(str_kind, current_year))

forest_df = pd.DataFrame(forest)
city_df = pd.DataFrame(city)

forest_df.to_csv('forest_data.csv')
city_df.to_csv('city_data.csv')
