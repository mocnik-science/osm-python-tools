[back to readme](../../../)

# Data Tools

The module contains tools for easily collecting, mining, and drawing data from OSM. It is meant to be used in combination with the other modules. To use this module, OSMPythonTools must be installed with all optional dependecies:
```bash
pip install OSMPythonTools[all]
```

## Querying data

Imagine the following example: we try to understand how the number of roads has developed over time in different cities. We are not only interested in the number of roads in general, but also to different kind of roads. We first fomulate different ‘dimensions’, for example, the temporal dimension, the dimension of different cities, and the dimension of different roads (this example is [part of the repository](https://github.com/mocnik-science/osm-python-tools/blob/master/examples/example.py)):
```python
from OSMPythonTools.nominatim import Nominatim
from OSMPythonTools.overpass import Overpass, overpassQueryBuilder
from OSMPythonTools.data import Data, dictRangeYears, ALL

from collections import OrderedDict

dimensions = OrderedDict([
  ('year', dictRangeYears(2013, 2017.5, 1)),
  ('city', OrderedDict({
    'heidelberg': 'Heidelberg, Germany',
    'manhattan': 'Manhattan, New York',
    'vienna': 'Vienna, Austria',
  })),
  ('typeOfRoad', OrderedDict({
    'primary': 'primary',
    'secondary': 'secondary',
    'tertiary': 'tertiary',
  })),
])
```
Having defined the requirements for the dimensions, we can now mine the data (mining the data takes a while due to limited resources of the endpoint):
```python
nominatim = Nominatim()
overpass = Overpass()

def fetch(year, city, typeOfRoad):
    areaId = nominatim.query(city).areaId()
    query = overpassQueryBuilder(area=areaId, elementType='way', selector='"highway"="' + typeOfRoad + '"', out='count')
    return overpass.query(query, date=year, timeout=60).countElements()

data = Data(fetch, dimensions)
```
The object `data` contains the results of the queries and can be imagined as being a table (this is similar to the package [xarray](http://xarray.pydata.org), which is also internally used):
```
                              value
city       typeOfRoad year
heidelberg primary    2013.0    281
                      2014.0    403
                      ...
           secondary  2013.0    282
                      2014.0    371
                      ...
           tertiary   2013.0    229
                      2014.0    285
                      ...
manhattan  primary    2013.0    346
                      2014.0    407
                      ...
vienna     primary    2013.0    998
                      2014.0   1284
                      ...
```
As it has a representation as a string, it can even be printed in the interactive python interpreter in a human readable way.

## Filtering the result of a query

The queried data can be restricted to one value for some dimension, for example, to the city of Vienna:
```python
data.select(city='vienna')
```
This yields a table only containing the values for Vienna:
```
                   value
typeOfRoad year
primary    2013.0    998
           2014.0   1284
           2015.0   1462
           2016.0   1619
           2017.0   1719
secondary  2013.0   1381
           2014.0   1560
           2015.0   1713
           2016.0   1892
           2017.0   2022
tertiary   2013.0   1235
           2014.0   1420
           2015.0   1540
           2016.0   1706
           2017.0   1802
```
Also the number of secondary roads in Vienna in 2014 can be accessed:
```python
data.select(city='vienna', year=2014, typeOfRoad='secondary')
# 1560
```
Instead of providing explicit values for a dimension, we can also provide the value `ALL`. The corresponding dimension is not restricted, but the values are relocated to columns:
```python
data.select(typeOfRoad=ALL, city='vienna')
```
This yields the following table:
```
        primary  secondary  tertiary
year
2013.0      998       1381      1235
2014.0     1284       1560      1420
2015.0     1462       1713      1540
2016.0     1619       1892      1706
2017.0     1719       2022      1802
```
Assume that only primary and secondary roads are of interest. In this case, we write:
```python
data.select(typeOfRoad=['primary', 'secondary'], city='vienna')
```
This yields the following table:
```
        primary  secondary
year
2013.0      998       1381
2014.0     1284       1560
2015.0     1462       1713
2016.0     1619       1892
2017.0     1719       2022
```

## Analyzing the result of the query

The queried data can be analyzed (number of values, mean value, standard derivation, etc.) as follows:
```python
data.describe(typeOfRoad=ALL, city='vienna')
```
This yields:
```
           primary    secondary     tertiary
count     5.000000     5.000000     5.000000
mean   1416.400000  1713.600000  1540.600000
std     286.042479   255.515753   225.623137
min     998.000000  1381.000000  1235.000000
25%    1284.000000  1560.000000  1420.000000
50%    1462.000000  1713.000000  1540.000000
75%    1619.000000  1892.000000  1706.000000
max    1719.000000  2022.000000  1802.000000
```

## Visualizing the result of the query

Instead of computing table representations, the data can also be plotted by using the same syntax to restrict the data:
```python
data.plot(city='manhattan', typeOfRoad=ALL)
```

![data.plot(city='manhattan', typeOfRoad=ALL)](https://github.com/mocnik-science/osm-python-tools/blob/master/examples/plot-manhattan.png)

Also the primary roads from different cities can be compared:
```python
data.plot(city=ALL, typeOfRoad='primary')
```

![data.plot(city=ALL, typeOfRoad='primary')](https://github.com/mocnik-science/osm-python-tools/blob/master/examples/plot-primary.png)

The rows correspond to the x axis, and the columns to the y axis. It is thus important to restrict the number of row dimensions until only one row dimension is left. The rows should only contain numerical values, when being plotted. If the values are not numerical, a bar plot can be used:
```python
data.plotBar(city='manhattan', year=ALL)
```

![data.plotBar(city='manhattan', year=ALL)](https://github.com/mocnik-science/osm-python-tools/blob/master/examples/plotbar-manhattan.png)

When two values shall be compared, a scatter plot can be used. The following plot compares the number of primary roads in Vienna (x axis) to the number of primary roads in Manhattan (y axis):
```python
data.plotScatter('vienna', 'manhattan', city=['vienna', 'manhattan'], typeOfRoad='primary')
```

![data.plotScatter('vienna', 'manhattan', city=['vienna', 'manhattan'], typeOfRoad='primary')](https://github.com/mocnik-science/osm-python-tools/blob/master/examples/plotscatter-primary.png)

When the plots (`plot`, `plotBar`, and `plotScatter`) are generated, they are (on most systems) shown in a graphical user interface. If the parameter `filename` is added, the data is instead saved to the corresponding file:
```python
data.plot(city='manhattan', typeOfRoad=ALL, filename='manhattan.pdf')
```

## Exporting the result of the query

The queried data is encapsulated inside an object. It can, however, be accessed in different formats:
```python
data.getDataFrame()    # as a pandas DataFrame
data.getDataset()      # as a xarray Dataset
data.getDict()         # as a python dictionary
data.getCSV()          # as comma separated values
data.excelClipboard()  # Excel format, copied to clipboard
```
Information about the packages [xarray](http://xarray.pydata.org) and [pandas](http://pandas.pydata.org) can be found on their websites.

## Undocumented methods

The following methods are not documented:
* `drop`: drop a row
* `apply`: apply a function to the data
* `toColumn`: apply `select` and produce a column from the resulting data
* `renameColumns`: rename a column
* `selectColumns`: select a number of columns
* `showPlot`: different plot can be combined (by using `showPlot=False`); the function `showPlot` is then called to show the plot.

## Further example: more complex query

One might want to access and aggregate more complex data. In contrast to the examples above, one can also query for single users contributing different types of elements to a certain region.  First, we define again the different dimensions:
```python
from OSMPythonTools.nominatim import Nominatim
from OSMPythonTools.overpass import Overpass, overpassQueryBuilder
from OSMPythonTools.data import Data, dictRangeYears, ALL

from collections import OrderedDict

dimensions = OrderedDict([
  ('elementType', OrderedDict({
    'node': 'node',
    'way': 'way',
    'relation': 'relation',
  })),
  ('user', OrderedDict({
    'franz-benjamin': 'franz-benjamin',
    'tyr_asd': 'tyr_asd',
  })),
])
```

Then, we have to determine the ID of the area we would like to examine. As an example, we can determine this ID for Heidelberg:
```python
nominatim = Nominatim()
areaId = nominatim.query('Heidelberg').areaId()
```

Finally, the data can be queried as follows:
```python
overpass = Overpass()

def fetch(elementType, user):
    query = overpassQueryBuilder(area=areaId, elementType=elementType, since='2017-01-01T00:00:00Z', to='2017-02-01T00:00:00Z', user=user, out='meta')
    return overpass.query(query, timeout=500).countElements()

data = Data(fetch, dimensions)
```
Note that we have restricted the query to a certain short period. On might easily use a temporal dimension to add further periods of time.

As before, the object `data` contains the results of the queries and can be imagined as being a table:
```
                            value
elementType user
node        franz-benjamin     43
            tyr_asd            24
way         franz-benjamin      7
            tyr_asd             7
relation    franz-benjamin      0
            tyr_asd             1
```
