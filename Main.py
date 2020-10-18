from GeoPoint import GeoPoint
import ee

p = GeoPoint([113.216749, 23.228943], 'GuangZhou')
p.setDataSets('2000-01-01', '2020-10-10', "MODIS/006/MOD13A2")
p.generateNdviData(0.0001)
p.getPlot()

