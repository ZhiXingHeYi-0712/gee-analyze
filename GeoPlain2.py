import ee
import geopandas as gpd
import json
from GeoPoint import GeoPoint
import pandas as pd
import matplotlib.pyplot as plt

ee.Initialize()
forest = []
city = []
for kind in (21, ):
    area = None
    for year in (2000, 2005, 2010, 2015):
        db_name = 'GIS_data/guangzhou_{}.gdb'.format(kind)
        str_kind = {21: 'lin_di', 51: 'cheng_shi'}[kind]
        layer_name = 'gz{}'.format(year)

        gdf = gpd.read_file(db_name, layer=layer_name)
        gdf.to_crs('EPSG:4326', inplace=True)
        gdf_json = json.loads(gdf.to_json())['features'][0]['geometry']['coordinates']
        geo = ee.Geometry.MultiPolygon(gdf_json)
        area = GeoPoint(geometry=geo, name=str_kind+'_'+str(year))
        for current_year in range(year, year+5):
            area.setDataSets('{}-01-01'.format(current_year), '{}-12-31'.format(current_year), "MODIS/006/MOD13Q1")
            area.generateNdviData(scale=0.0001)
            if kind == 21:
                forest.append((current_year, area.Ndvi.mean()[0]))
            elif kind == 51:
                city.append((current_year, area.Ndvi.mean()[0]))

with open('forest.txt', 'w') as f:
    f.write(forest)

with open('city.txt', 'w') as f:
    f.write(city)

