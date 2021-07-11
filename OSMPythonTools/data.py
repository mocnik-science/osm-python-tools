from collections import OrderedDict
import datetime as dt
import itertools
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
import xarray as xr

import OSMPythonTools

def dictRange(start, end, step=1):
    return OrderedDict([(x, x) for x in range(start, end, step)])

def dictRangeYears(start, end, step=1):
    def yearToString(year):
        y = int(year)
        f = year - y
        timespanYear = (dt.datetime(y + 1, 1, 1) - dt.datetime(y, 1, 1))
        return (dt.datetime(y, 1, 1) + f * timespanYear).isoformat() + 'Z'
    return OrderedDict([(year, yearToString(year)) for year in np.arange(start, end, step)])

class All:
    def __repr__(self):
        return 'ALL'
ALL = All()

class Data:
    def __init__(self, arg1, arg2):
        self._dataset = None
        self._dataFrame = None
        if callable(arg1) and isinstance(arg2, OrderedDict):
            fetch = arg1
            dimensions = arg2
            self._dimensions = dimensions
            data = list(map(lambda params: fetch(*params), itertools.product(*[[v for v in dimension.values()] for dimension in dimensions.values()])))
            for dim, v in reversed(dimensions.items()):
                data = [data[i:i+len(v)] for i in range(0, len(data), len(v))]
            self._dataset = xr.DataArray(data=data[0], dims=list(dimensions.keys()), coords=[list(v.keys()) for v in dimensions.values()]).to_dataset(name='value')
        elif isinstance(arg1, Data) and isinstance(arg2, xr.Dataset):
            self._dimensions = arg1._dimensions
            self._dataset = arg2
        elif isinstance(arg1, Data) and isinstance(arg2, list) and all(isinstance(df, xr.Dataset) for df in arg2):
            self._dimensions = arg1._dimensions
            self._dataset = xr.merge(map(lambda d: d.getDataset(), arg2))
        elif isinstance(arg1, Data) and isinstance(arg2, pd.DataFrame):
            self._dimensions = arg1._dimensions
            self._dataFrame = arg2
        elif isinstance(arg1, Data) and isinstance(arg2, list) and all(isinstance(df, pd.DataFrame) for df in arg2):
            self._dimensions = arg1._dimensions
            self._dataFrame = pd.concat(arg2, axis=1)
        elif isinstance(arg1, Data) and isinstance(arg2, Data):
            self._dimensions = arg1._dimensions
            self._dataset = arg2.getDataset()
        elif isinstance(arg1, Data) and isinstance(arg2, list) and all(isinstance(df, Data) for df in arg2):
            self._dimensions = arg1._dimensions
            self._dataset = xr.merge(map(lambda d: d.getDataset(), arg2))
    
    def __repr__(self):
        return '\n' + self.getDataFrame().to_string() + '\n'
    
    def _raiseException(self, msg):
        OSMPythonTools._raiseException('Data', msg)
    
    def __freeDimensions(self, **kwargs):
        return [k for k in self._dimensions.keys() if k not in kwargs.keys() or type(kwargs[k]) is list]
    
    def __freeDimensionsWithRange(self, **kwargs):
        return dict([(k, v) for k, v in kwargs.items() if type(v) is list])
    
    def __fixedDimensions(self, **kwargs):
        return dict([(k, v) for k, v in kwargs.items() if type(v) is not list])
    
    def getDataFrame(self, valueName='value'):
        if self._dataFrame is not None:
            return self._dataFrame
        else:
            self._dataFrame = self._dataset.to_dataframe()
            self._dataset = None
            return self._dataFrame
    
    def getDataset(self):
        if self._dataset is not None:
            return self._dataset
        else:
            self._dataset = self._dataFrame.to_xarray()
            self._dataFrame = None
            return self._dataset
    
    def getDict(self, **kwargs):
        return self.getDataFrame(**kwargs).to_dict()
    
    def select(self, *args, **kwargs):
        if len(args) == 0 and len(kwargs) == 0:
            return self
        elif len(args) == 0:
            sel = self.__select(**kwargs)
            return Data(self, sel) if isinstance(sel, xr.Dataset) else sel
        elif len(kwargs) == 0:
            sels = list(map(lambda x: self.__select(**x), args))
            if not all(isinstance(sel, xr.Dataset) for sel in sels):
                self._raiseException('If more than one selection is used, each of them has to contain a free dimension.')
            return Data(self, self)
        self._raiseException('Use either only keyword arguments, or dictionaries as parameter.')
    
    def __select(self, valueName=None, **kwargs):
        # select all
        allVariables = [k for k, v in kwargs.items() if v is ALL]
        if len(allVariables) > 0:
            if len(allVariables) > 1:
                self._raiseException('It is only allowed to use one ALL dimension.')
            allVariable = allVariables[0]
            allVariableValues = list(self._dimensions[allVariable].keys())
            if not valueName:
                valueName = allVariableValues
            elif len(allVariableValues) != len(valueName):
                self._raiseException('The length of the list for \'valueName\' must equal the number of values for the free dimension.')
            return self.__select(**dict([(k, v) for k, v in kwargs.items() if k is not allVariable]), **{allVariable: allVariableValues}, valueName=valueName)
        # select list
        freeDimensionsWithRange = self.__freeDimensionsWithRange(**kwargs)
        if len(freeDimensionsWithRange) == 1:
            if len(freeDimensionsWithRange) != 1:
                self._raiseException('If you use a list as \'valueName\', you have to use exactly one dimension with a range.')
            freeVariable, freeValues = list(freeDimensionsWithRange.items())[0]
            if not valueName:
                valueName = freeValues
            elif len(freeValues) != len(valueName):
                self._raiseException('The length of the list for \'valueName\' must equal the number of values for the free dimension.')
            das = []
            for x, name in zip(freeValues, valueName):
                das += [self.__renameDataset(self.__select(**self.__fixedDimensions(**kwargs), **{freeVariable: x}), name)]
            return xr.merge(das)
        # select one
        if len(self.__freeDimensions(**kwargs)) == 0:
            return self.getDataset().sel(**kwargs).to_array().item()
        else:
            if not valueName:
                valueName = 'value'
            return self.__renameDataset(self.getDataset().sel(**kwargs).drop(self.__fixedDimensions(**kwargs).keys()), valueName)
    
    def drop(self, **kwargs):
        d = self.getDataset().copy()
        for k, v in kwargs.items():
            d = d.drop(v if type(v) is list else [v], dim=k)
        return Data(self, d)
    
    @classmethod
    def __renameDataset(cls, ds, name):
        currentName = list(ds.data_vars.keys())[0]
        return ds.rename({currentName: name})
    
    def show(self):
        print(self)
    
    def getCSV(self):
        return self.getDataFrame().to_csv()
    
    def excelClipboard(self):
        self.getDataFrame().to_clipboard()
    
    def describe(self, toNumber=True, **kwargs):
        dataFrame = self.select(**kwargs).getDataFrame()
        if toNumber:
            dataFrame = dataFrame.astype(np.float64)
        print('\n' + dataFrame.describe().to_string() + '\n')
    
    def showPlot(self, showPlot=True, filename=None):
        if showPlot:
            if filename:
                plt.savefig(filename)
            else:
                plt.show(block=False)
    
    def resetColorCycle(self):
        plt.gca().set_prop_cycle(None)
    
    def plot(self, *args, plotTitle=None, showPlot=True, filename=None, **kwargs):
        dataFrame = self.select(*args, **kwargs).getDataFrame()
        if dataFrame.index.nlevels > 1:
            self._raiseException('Please restrict the dataset such that only one index is left.')
        ax = dataFrame.plot()
        plt.ticklabel_format(useOffset=False, style='plain')
        plt.title(plotTitle if plotTitle else kwargs)
        self.showPlot(showPlot=showPlot, filename=filename)
        return self
    
    def plotBar(self, *args, plotTitle=None, showPlot=True, filename=None, **kwargs):
        dataFrame = self.select(*args, **kwargs).getDataFrame()
        if dataFrame.index.nlevels > 1:
            self._raiseException('Please restrict the dataset such that only one index is left.')
        dataFrame.plot.bar()
        plt.title(plotTitle if plotTitle else kwargs)
        self.showPlot(showPlot=showPlot, filename=filename)
        return self
    
    def plotScatter(self, xName, yName, *args, plotTitle=None, showPlot=True, filename=None, **kwargs):
        dataFrame = self.select(*args, **kwargs).getDataFrame()
        ax = dataFrame.plot.scatter(x=xName, y=yName)
        dataFrame.apply(lambda row: ax.annotate(row.name, row.values), axis=1)
        plt.title(plotTitle if plotTitle else yName + ' vs ' + xName)
        self.showPlot(showPlot=showPlot, filename=filename)
        return self
    
    def apply(self, f):
        dataFrame = self.getDataFrame()
        df = dataFrame.apply(lambda x: f(dataFrame, x))
        if isinstance(df, pd.Series):
            df = df.to_frame(name='value')
        return Data(self, df)
    
    def toColumn(self, *args, **kwargs):
        dataFrame = self.select(*args, **kwargs).getDataFrame()
        if dataFrame.index.nlevels > 1:
            self._raiseException('Please restrict the dataset such that only one index is left.')
        return dataFrame.squeeze()
    
    def renameColumns(self, f):
        return Data(self, self.getDataFrame().rename(columns=f))
    
    def selectColumns(self, *cols):
        return Data(self, self.getDataFrame()[list(cols)])
