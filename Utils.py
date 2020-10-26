import pandas as pd
import numpy as np

def dfSplitByDate(dataframe: pd.DataFrame):
    yearRange = dfGetYearCount(dataframe)
    result = pd.DataFrame()
    for year in range(yearRange[0], yearRange[1]+1):
        yearData = dataframe.set_index('datetime')[str(year)]
        yearResult = pd.DataFrame({
            'year': year,
            'max': np.max(yearData),
            'min': np.min(yearData),
            'mean': np.mean(yearData)
        })
        result = result.append(yearResult)
    return result



def dfGetYearCount(dataframe: pd.DataFrame) -> tuple:
    years = pd.DatetimeIndex(dataframe['datetime']).year
    return (years[0], years[-1])