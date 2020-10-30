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
            point_count = 1
            for mpg in gdf_multiploygons:
                geo = ee.Geometry.MultiPolygon(mpg['geometry']['coordinates'])
                size = mpg['properties']['Shape_Area']
                area = GeoPoint(geometry=geo, name=str_kind+'_'+str(year))

                area.setDataSets('{}-01-01'.format(current_year), '{}-12-31'.format(current_year),
                                 "MODIS/006/MOD13Q1")
                area.generateNdviData(scale=0.0001)
                if len(year_ndvi) == 0:
                    year_ndvi = pd.DataFrame([[area.Ndvi.mean()[0], size]])
                else:
                    year_ndvi = year_ndvi.append([[area.Ndvi.mean()[0], size]])
                print('finish point {}'.format(point_count))
                point_count += 1
            weight_mean = (year_ndvi[0] * year_ndvi[1]).sum() / year_ndvi[1].sum()
            if kind == 21:
                forest.append((current_year, weight_mean))
            elif kind == 51:
                city.append((current_year, weight_mean))
            print('finish {}, {}'.format(str_kind, current_year))

forest_df = pd.DataFrame(forest)
city_df = pd.DataFrame(city)

forest_df.to_csv('forest_data.csv')
city_df.to_csv('city_data.csv')

