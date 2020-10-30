import geopandas as gpd
from GeoPoint import GeoPoint
import ee
from GeoInfoFormatter import GeoInfo
import warnings
warnings.filterwarnings("ignore")

ee.Initialize()

df = gpd.read_file('guangzhou/guangzhou_poly.shp')
result = GeoInfo()

for year in range(2000, 2020):
    for i, pData in enumerate(df.iterrows()):
        p_info = pData[1]['geometry']
        point = GeoPoint(p_info, 'Point')
        point.setDataSets('{}-01-01'.format(year), '{}-12-31'.format(year), "MODIS/006/MOD13Q1")
        point.generateNdviData(scale=0.0001)
        result.addGeoData(point.Ndvi.mean()[0], (p_info.x, p_info.y))
        print('finish {}, point {}'.format(year, i))
    gdf = result.getGeoDataFrame()
    gdf.to_file('guangzhou_ndvi_mean_{}.shp'.format(year))
    print('finish {}'.format(year))
