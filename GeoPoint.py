import ee
import pandas as pd
import matplotlib.axis, matplotlib.pyplot as plt
import shapely.geometry.point
from Utils import *


class GeoPoint():
    def __init__(self, geometry, name: str):
        '''
        初始化点。
        :param geometry: 地理位置，传入list, tuple, ee.Geometry.Point,或shapely.geometry.point.Point产生的对象。
                         list, tuple经度在前，纬度在后
        '''
        self.Geometry: ee.Geometry = geometry

        self.Name = name

        if isinstance(geometry, ee.Geometry) or isinstance(geometry, ee.FeatureCollection):
            self.Gee_geometry = geometry
        elif isinstance(geometry, shapely.geometry.point.Point):
            self.Gee_geometry = ee.Geometry.Point([geometry.x, geometry.y])
        else:
            self.Gee_geometry = ee.Geometry.Point(geometry)

    def setDataSets(self, start_date: str, end_date: str, dataset: str = 'LANDSAT/LC08/C01/T1_8DAY_NDVI') -> None:
        '''
        设置GEE图像获取的起止日期和数据集。
        :param start_date: 开始日期，格式YYYY-mm-dd, 例如2013-10-21
        :param end_date: 结束日期，同开始日期格式
        :param dataset: 数据卫星。内容参考 https://developers.google.cn/earth-engine/datasets/catalog
        '''
        self.images: ee.ImageCollection = ee.ImageCollection(dataset).filterDate(start_date, end_date).filterBounds(
            self.Gee_geometry)
        self.BandName: list = self.images.first().bandNames().getInfo()[:1]

    def generateNdviData(self, scale=1) -> None:
        '''
        :param scale 缩放倍率
        获取NDVI的主函数。
        在调用此函数前必须先调用setDataSets()函数，否则会引发错误。
        '''
        # 提示运行setDataSets()
        if self.images == None or self.BandName == None:
            raise Exception('run setDataSets() first.')

        # 框定图片范围
        geo_values: ee.List = self.images.select(self.BandName).getRegion(geometry=self.Gee_geometry, scale=500)

        # 转成python原生list，[0]是题头。
        geo_values_list: list = geo_values.getInfo()
        data = pd.DataFrame(geo_values_list[1:], columns=geo_values_list[0])

        # 将GEE提供的时间戳转换成时间字符串
        data['datetime'] = pd.to_datetime(data['time'], unit='ms', utc=False)
        strTime = data.datetime.map(lambda x: x.strftime('%Y-%m-%d'))
        data['datetime'] = strTime
        data['datetime'] = pd.to_datetime(data['datetime'])

        # 变相的排序
        data.sort_values(by=['datetime'])

        # 所有要的数据列，datetime和波段名称
        result_col = ['datetime'] + self.BandName
        raw_result = data[result_col]

        # 除去NaN
        result = raw_result.dropna()

        # 部分数据集需要缩放
        result['NDVI'] *= scale

        self.Ndvi: pd.DataFrame = result

    def getNdviMean(self, scale=1):
        if self.images == None or self.BandName == None:
            raise Exception('run setDataSets() first.')

        # 框定图片范围
        geo_values: ee.List = self.images.select(self.BandName).getRegion(geometry=self.Gee_geometry, scale=500)

        # 转成python原生list，[0]是题头。
        geo_values_list: list = geo_values.getInfo()
        data = pd.DataFrame(geo_values_list[1:], columns=geo_values_list[0])

        # 将GEE提供的时间戳转换成时间字符串
        data['datetime'] = pd.to_datetime(data['time'], unit='ms', utc=False)
        data.dropna(inplace=True)
        return data.mean()['NDVI'] * scale

    def drawPlot(self, kind : str = 'default'):
        '''
        ndvi绘图。
        必须先调用getNdviDataFrame函数
        :param kind: 图表类似，可取'default', 'Mix'
        default是按时间画标准图
        Mix是取每年的最高、最低值和平均数
        '''
        if kind == 'default':
            plot: matplotlib.axis.Axis = self.Ndvi.plot.line(x='datetime', y='NDVI', title=self.Name, rot=90)
        else:
            df = dfSplitByDate(self.Ndvi)
            plot = df.plot.line(x = 'year', y=['max', 'min', 'mean'])
        plt.tight_layout()
        plot.get_figure().savefig('./ndvi_image/{figure_name}.png'.format(figure_name=self.Name))

    def saveData(self):
        self.Ndvi.to_csv('./{}_data.csv'.format(self.Name))