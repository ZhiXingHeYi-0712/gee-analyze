import geopandas as gpd
from shapely.geometry import Point

class GeoInfo:
    def __init__(self):
        self.ndvis = []
        self.geometrys = []
        self.data = {
            'name': self.ndvis,
            'geometry': self.geometrys
        }

    def getGeoDataFrame(self):
        return gpd.GeoDataFrame(self.data, crs='EPSG:4236')

    def addNdvi(self, name : str):
        self.ndvis.append(name)

    def addGeometry(self, loc : tuple):
        self.geometrys.append(Point(loc))

    def addGeoData(self, ndvi : float, loc : tuple):
        self.addNdvi(ndvi)
        self.addGeometry(loc)

    def addGeoDataList(self, geodataList : list):
        for i in geodataList:
            self.addNdvi(i[0])
            self.addGeometry(i[1])

