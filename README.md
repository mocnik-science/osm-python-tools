# OSMPythonTools

The python package `OSMPythonTools` provides easy access to [OpenStreetMap (OSM)](http://www.openstreetmap.org) related services, amongst them an [Overpass endpoint](http://wiki.openstreetmap.org/wiki/Overpass_API) and [Nominatim](http://nominatim.openstreetmap.org).

## Installation

To install `OSMPythonTools`, you will need `python3` and `pip` ([How to install pip](https://pip.pypa.io/en/stable/installing/)). Then execute:
```
pip install OSMPythonTools
```

## Usage

### Nominatim

OSM data contains numerous place names. Nominatim is a reverse geocoder which is able to identify geometries in OSM data corresponding to a given string. If you are, for example, interested in the German town Heidelberg, you can query:
```python
from OSMPythonTools.nominatim import Nominatim
nominatim = Nominatim()
heidelberg = nominatim.query('Heidelberg')
```
The result of this query is an object which contains a number of functions to access the data. Most important, the area id can be accessed:
```python
heidelberg.getAreaId()
# 3600285864
```
This raw data provided by Nominatim potentially contains more than one geometry. The function `getAreaId` only returns the area id of the first geometry. The (complete) raw data of the answer by Nominatim can be accessed:
```python
heidelberg.toJSON()
# [{'place_id': '580259', 'licence': 'Data © OpenStreetMap ...
```

As a default, `OSMPythonTools.Nominatim` uses the endpoint `https://nominatim.openstreetmap.org/search`. If another one should be used, for example, a local one, corresponding data can be provided:
```python
nominatim = Nominatim(endpoint='https://nominatim.openstreetmap.org/search')
```
The data is automatically cached into a the directory `./cache`. If another directory shall be used, the directory name can be provided:
```python
nominatim = Nominatim(cacheDir='cache')
```
In case of numerous requests, one may want to delay the requests. The fetching process can, for example, be instructed to wait 2 seconds between the queries sent to Nominatim:
```python
nominatim = Nominatim(waitBetweenQueries=2)
```
Also combinations of `endpoint`, `cacheDir`, and `waitBetweenQueries` can be used.

### Overpass Turbo

OSM data can be accessed using the [http://wiki.openstreetmap.org/wiki/Overpass_API](Overpass API). While the Overpass API is powerful, it cannot automatically reverse geocode place names. We thus use Nominatim again to query the area id of, for example, NYC:
```python
from OSMPythonTools.nominatim import Nominatim
nominatim = Nominatim()
nyc = nominatim.query('NYC')
```
Overpass queries are simple enough to be written by hand, but we will demonstrate how to use the `overpassQueryBuilder`:
```python
from OSMPythonTools.overpass import overpassQueryBuilder
query = overpassQueryBuilder(area=nyc.getAreaId(), elementType='node', selector='"highway"="bus_stop"', out='body')
```
The variable `query` is just a string containing the query:
```
'area(3600175905)->.searchArea;node(area.searchArea);node._["highway"="bus_stop"]; out body;'
```
We can now query an Overpass endpoint:
```python
from OSMPythonTools.overpass import Overpass
overpass = Overpass()
busStops = overpass.query(query)
```
Please observe that the constructor of the class `Overpass` again accepts the parameters `endpoint`, `cacheDir`, and `waitBetweenQueries`.
To query historical data, we can easily add a date:
```python
overpass.query(query, date='2014-01-01T00:00:00Z')
```
Also a timeout can be set:
```python
overpass.query(query, timeout=25)
```

The result of the overpass query is an object containing several functions to easily access the data. All elements returned by the query can be accessed:
```python
busStops.elements()
# [{'type': 'node', 'id': 42467507, 'lat': 40.701424, 'lon': -73.943064, 'tags': ...
```
Also only elements of a certain type can be accessed:
```python
busStops.nodes()
busStops.ways()
busStops.relations()
busStops.areas()
```
In our case, the query only contains nodes because we explicitly queried only for nodes.

In many cases, the number of elements shall be counted. This can easily be achieved using the corresponding functions:
```python
busStops.countElements()
# 542
busStops.countNodes()
# 542
busStops.countWays()
# 0
busStops.countRelations()
# 0
busStops.countAreas()
# 0
```
Overpass queries contain information about the verbosity of the result. If the verbosity is `body`, like in our example, all important information about the bus stops is returned. If `count` is used instead, only the number of elements is returned. The function `busStops.elements()` will return a list of elements in the first case, and `None` in the second case. The function `busStops.countElements()` will return the number of elements in both cases.

Data about a bus stop can easily be accessed as a python dictionary. The first bus stop in the list can be accessed by `busStops.elements()[0]`:
```python
{'type': 'node', 'id': 42467507, 'lat': 40.701424, 'lon': -73.943064, 'tags': {'asset_ref': '2030', 'highway': 'bus_stop', 'location': 'Broadway / Thornton Street', 'name': 'Broadway / Thornton Street', 'route_ref': 'B46;B46-LTD'}}
```
Accordingly, the latitude and longitude, and the tags can, for example, be accessed by:
```python
busStops.elements()[0]['lat']
busStops.elements()[0]['lon']
busStops.elements()[0]['tags']
```

Not only the data itself but also meta data about the query can be accessed. We can, for example, test whether the query was valid:
```python
busStops.isValid()
# True
```
Also the raw data can be accessed:
```python
busStops.toJSON()
```
Also other meta data provided by the overpass endpoint can be accessed:
```python
busStops.version()
busStops.generator()
busStops.timestamp_osm_base()
busStops.timestamp_area_base()
busStops.copyright()
busStops.remark()
```

### Data Tools

The package contains tools to easily assess the data. Imagine the following example: we try to understand how the number of roads has developed over time in different towns. We are not only interested in the number of roads in general, but also to different kind of roads. We first fomulate different "dimensions", for example, the temporal dimension, the dimension of different towns, and the dimension of different roads (this example is [part of the repository](https://github.com/mocnik-science/osm-python-tools/blob/master/examples/example.py)):
```python
from OSMPythonTools.nominatim import Nominatim
from OSMPythonTools.overpass import Overpass, overpassQueryBuilder
from OSMPythonTools.data import Data, dictRangeYears, ALL

from collections import OrderedDict

dimensions = OrderedDict([
  ('year', dictRangeYears(2013, 2017.5, 1)),
  ('town', OrderedDict({
    'heidelberg', 'Heidelberg, Germany',
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

def fetch(year, town, typeOfRoad):
    areaId = nominatim.query(town).getAreaId()
    query = overpassQueryBuilder(area=areaId, elementType='way', selector='"highway"="' + typeOfRoad + '"', out='count')
    return overpass.query(query, date=year, timeout=60).countElements()

data = Data(fetch, dimensions)
```
The object `data` contains the results of the queries and can be imagined as being a table (this is similar to the package [xarray](http://xarray.pydata.org), which is also internally used):
```
                              value
town       typeOfRoad year
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
As it has a representation as a string, it can even be printed in the interactive python interpreter in a human readable way. The data can also be restricted to one value for some dimension, for example, to the town Vienna:
```python
data.select(town='vienna')
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
data.select(town='vienna', year=2014, typeOfRoad='secondary')
# 1560
```
Instead of providing explicit values for a dimension, we can also provide the value `ALL`. The corresponding dimension is not restricted, but the values are relocated to columns:
```python
data.select(typeOfRoad=ALL, town='vienna')
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
data.select(typeOfRoad=['primary', 'secondary'], town='vienna')
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
The data can be analyzed (number of values, mean value, standard derivation, etc.):
```python
data.describe(typeOfRoad=ALL, town='vienna')
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

Instead of computing table representations, the data can also be plotted by using the same syntax to restrict the data:
```python
data.plot(town='manhattan', typeOfRoad=ALL)
```
![data.plot(town='manhattan', typeOfRoad=ALL)](https://github.com/mocnik-science/osm-python-tools/blob/master/examples/plot-manhattan.png)

Also the primary roads from different towns can be compared:
```python
data.plot(town=ALL, typeOfRoad='primary')
```
![data.plot(town=ALL, typeOfRoad='primary')](https://github.com/mocnik-science/osm-python-tools/blob/master/examples/plot-primary.png)

The rows correspond to the x axis, and the columsn to the y axis. It is thus important to restrict the number of row dimensions until only one row dimension is left. The rows should only contain numerical values, when being plotted. If the values are not numerical, a bar plot can be used:
```python
data.plotBar(town='manhattan', year=ALL)
```
![data.plotBar(town='manhattan', year=ALL)](https://github.com/mocnik-science/osm-python-tools/blob/master/examples/plotbar-manhattan.png)

When two values shall be compared, a scatter plot can be used. The following plot compares the number of primary roads in Vienna (x axis) to the number of primary roads in Manhattan (y axis):
```python
data.plotScatter('vienna', 'manhattan', town=['vienna', 'manhattan'], typeOfRoad='primary')
```
![data.plotScatter('vienna', 'manhattan', town=['vienna', 'manhattan'], typeOfRoad='primary')](https://github.com/mocnik-science/osm-python-tools/blob/master/examples/plotscatter-primary.png)

When the plots (`plot`, `plotBar`, and `plotScatter`) are generated, they are (on most systems) shown in a graphical user interface. If the parameter `filename` is added, the data is instead saved to the corresponding file:
```python
data.plot(town='manhattan', typeOfRoad=ALL, filename='manhattan.pdf')
```

The data is encapsulated inside an object. It can, however, be accessed in different formats:
```python
data.getDataFrame()    # as a pandas DataFrame
data.getDataset()      # as a xarray Dataset
data.getDict()         # as a python dictionary
data.getCSV()          # as comma separated values
data.excelClipboard()  # Excel format, copied to clipboard
```
Information about the packages [xarray](http://xarray.pydata.org) and [pandas](http://pandas.pydata.org) can be found on their websites.

The following commands are not documented:
* `drop`: drop a row
* `apply`: apply a function to the data
* `toColumn`: apply `select` and produce a column from the resulting data
* `renameColumns`: rename a column
* `selectColumns`: select a number of columns
* `showPlot`: different plot can be combined (by using `showPlot=False`); the function `showPlot` is then called to show the plot.

## Author

This application is written and maintained by Franz-Benjamin Mocnik, <mail@mocnik-science.net>.

(c) by Franz-Benjamin Mocnik, 2017.

The code is licensed under the [GPL-3](https://github.com/mocnik-science/osm-python-tools/blob/master/LICENSE.md).
