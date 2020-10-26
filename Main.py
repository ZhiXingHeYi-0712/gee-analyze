from GeoPoint import GeoPoint
import pandas as pd
import matplotlib.pyplot as plt
import ee
ee.Initialize()
plt.rcParams['font.family'] = 'SimSun'

loc = pd.read_csv('location.csv')

for _, line in loc.iterrows():
    p = GeoPoint(list(line[1:]), line[0])
    p.setDataSets('2000-01-01', '2019-12-31', "MODIS/006/MOD13Q1")
    p.generateNdviData(scale=0.0001)
    p.drawPlot(kind='Mix')
    # p.saveData()

