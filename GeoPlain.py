import geopandas as gpd
from GeoPoint import GeoPoint
import ee
from GeoInfoFormatter import GeoInfo
import warnings
warnings.filterwarnings("ignore")

ee.Initialize()

df = gpd.read_file('GIS_data/Pgz_21_2000/Pgz_21_2000.shp')


i = 0
try:
    for pData in df.iterrows():
        p_info = pData[1]['geometry']
        point = GeoPoint(p_info, 'Point')
        point.setDataSets('2000-01-01', '2000-12-31', "MODIS/006/MOD13Q1")
        point.generateNdviData(scale=0.0001)
        point.Ndvi.mean()
        i+=1
        print("finish {}.".format(i))
except:
    with open('current.txt', 'w') as f:
        f.write(str(i))
finally:
    gdf = result.getGeoDataFrame()
    gdf.to_file('guangzhou_ndvi_mean.shp')