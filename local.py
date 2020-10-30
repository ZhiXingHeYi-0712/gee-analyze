import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = 'SimSun'  # 宋体字

def fitLinearRegress(x, y):
    """
    自定义的线性拟合函数
    Parameters
    ----------
    x : TYPE：实数，一维数组
        DESCRIPTION：自变量
    y : TYPE：实数，一维数组
        DESCRIPTION：因变量

    Returns
    -------
    yy : TYPE：实数，一维数组
        DESCRIPTION：拟合后的线性方程与x对应计算值
    strLabel : TYPE：字符串
        DESCRIPTION：用字符串表达的线性方程，例如 3x + 4 的形式

    """
    x = pd.to_numeric(x)
    y = pd.to_numeric(y).dropna()
    d = np.polyfit(x, y, 1)  # 调用numpy模块的一次多项式拟合函数
    strSign = ['-', '+']  # 截距的符号列表，正或者负
    print(d)
    iSign = int((np.sign(d[1]) + 1)/2)  # 根据截距正负值得到符号的位置，用到了sign函数
    #构造一个字符串，用来表达一次多项式函数的形式
    strLabel = '{:.2f}x {} {:.2f}'.format(d[0], strSign[iSign], np.abs(d[1]))
    f = np.poly1d(d)  # 生成多项式
    yy = f(x)  # 然后用多项式计算x值的拟合值
    return yy, strLabel

city = pd.read_csv('guangzhou/mian/city_data.csv')
guangzhou_stats_file = pd.ExcelFile('guangzhou_stats.xlsx')
guangzhou_stats = pd.read_excel(guangzhou_stats_file).T.iloc[2:, :]
guangzhou_stats.rename(columns={2:'建成区绿化覆盖率(%)', 12: '单位人均绿地(公顷/万人)'}, inplace=True)


city.set_index('year', inplace=True)

city = city.join(guangzhou_stats)

city = city.iloc[1:-1, :]
p = city.plot.line(y=['建成区绿化覆盖率(%)', '单位人均绿地(公顷/万人)'], rot=45,
                   title='广州市人均绿地与建成区绿化覆盖率随时间变化图', secondary_y=['建成区绿化覆盖率(%)'], 
                   xticks=[i for i in range(2001, 2019)])
plt.tight_layout()
p.get_figure().savefig('gov.png', dpi=300)
# p = city.plot.scatter(x='NDVI', y='单位人均绿地(公顷/万人)',  title='NDVI与人均绿地散点图')
# plt.tight_layout()
# p.get_figure().savefig('scatter1.png', dpi=300)

# p = city.plot.scatter(x='NDVI', y='建成区绿化覆盖率(%)', 
#                       title='NDVI与建成区绿化覆盖率散点图')
# plt.tight_layout()
# p.get_figure().savefig('scatter2.png', dpi=300)
# city['人均绿地'] = pd.to_numeric(city['人均绿地'])
# city['建成区绿化覆盖率(%)'] = pd.to_numeric(city['建成区绿化覆盖率(%)'])
# city.corr(method='pearson', min_periods=1)
