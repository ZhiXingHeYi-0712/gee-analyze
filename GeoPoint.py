import ee
import pandas as pd
import matplotlib.axis, matplotlib.pyplot as plt


class GeoPoint():
    def __init__(self, geometry, name: str):
        '''
        初始化点。
        :param geometry: 地理位置，传入list, tuple或ee.Geometry.Point产生的对象。
                         list, tuple经度在前，纬度在后
        '''
        ee.Initialize()
        self.Geometry: ee.Geometry = geometry

        self.Name = name

        if not isinstance(geometry, ee.Geometry):
            self.Gee_geometry = ee.Geometry.Point(geometry)
        else:
            self.Gee_geometry = geometry

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

    def generateNdviData(self, scale=0) -> None:
        '''
        :param scale 缩放倍率
        获取NDVI的主函数。
        在调用此函数前必须先调用setDataSets()函数，否则会引发错误。
        '''
        # 提示运行setDataSets()
        if self.images == None or self.BandName == None:
            raise Exception('run setDataSets() first.')

        # 框定图片范围
        geo_values: ee.List = self.images.filterBounds(self.Gee_geometry) \
            .select(self.BandName).getRegion(geometry=self.Gee_geometry, scale=30)

        # 转成python原生list，[0]是题头。
        geo_values_list: list = geo_values.getInfo()
        data = pd.DataFrame(geo_values_list[1:], columns=geo_values_list[0])

        # 将GEE提供的时间戳转换成时间字符串
        data['datetime'] = pd.to_datetime(data['time'], unit='ms', utc=False)
        strTime = data.datetime.map(lambda x: x.strftime('%Y-%m-%d'))
        data['datetime'] = strTime

        # 变相的排序
        data.set_index('time', inplace=True)

        # 所有要的数据列，datetime和波段名称
        result_col = ['datetime'] + self.BandName
        raw_result = data[result_col]

        # 除去NaN
        result = raw_result.dropna()

        # 部分数据集需要缩放
        result['NDVI'] *= scale

        self.Ndvi: pd.DataFrame = result

    def getPlot(self):
        '''
        ndvi绘图。
        必须先调用getNdviDataFrame函数
        '''
        plot: matplotlib.axis.Axis = self.Ndvi.plot.line(x='datetime', y='NDVI', title=self.Name, rot=90)
        plt.tight_layout()
        plot.get_figure().savefig('./ndvi_image/{figure_name}.png'.format(figure_name=self.Name))