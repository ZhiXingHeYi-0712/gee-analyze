import geopandas as gpd
import pandas as pd
from GeoPoint import GeoPoint
import ee
import warnings
warnings.filterwarnings('ignore')

ee.Initialize()

forest = []
city = []

for kind in [21, 51]:
    for year in [2000, 2005, 2010, 2015]:
        ground_file = 'GIS_data/Pgz_{kind}_{year}'.format(kind=kind, year=year)
        str_kind = {21: 'lin_di', 51: 'cheng_shi'}[kind]
        gdf = gpd.read_file(ground_file)

        for pData in gdf.iterrows():
            p_info = pData[1]['geometry']
            point = GeoPoint(p_info, 'Point')

            for current_year in range(year, year+5):
                point.setDataSets('{}-01-01'.format(current_year), '{}-12-31'.format(current_year),
                                  "MODIS/006/MOD13Q1")
                point.generateNdviData(scale=0.0001)
                if kind == 21:
                    forest.append((year, point.Ndvi.mean()))
                elif kind == 51:
                    city.append((year, point.Ndvi.mean()))

with open('forest.txt', 'w') as f:
    f.write(str(forest))

with open('city.txt', 'w') as f:
    f.write(str(city))





