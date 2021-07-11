[back to readme](../../../)

# Overpass API

## Performing queries

OSM data can be accessed using the [Overpass API](http://wiki.openstreetmap.org/wiki/Overpass_API). While the Overpass API is powerful, it cannot automatically reverse geocode place names. We thus use Nominatim again to query the area ID of, for example, NYC:
```python
from OSMPythonTools.nominatim import Nominatim
nominatim = Nominatim()
nyc = nominatim.query('NYC')
```

Overpass queries are simple enough to be written by hand, but we will demonstrate how to use the `overpassQueryBuilder`:
```python
from OSMPythonTools.overpass import overpassQueryBuilder
query = overpassQueryBuilder(area=nyc, elementType='node', selector='"highway"="bus_stop"', out='body')
```
The area ID can be provided in different formats, either in one of the standard formats explained in the [general remarks](general-remarks.md), or as a number (possibly incremented by 2400000000 or 3600000000 like described in the Overpass API documentation).  As an alternative to the above query, the following queries would, for instance, provide the same results:
```python
query = overpassQueryBuilder(area=nyc.areaId(), elementType='node', selector='"highway"="bus_stop"', out='body')
query = overpassQueryBuilder(area='relation/175905', elementType='node', selector='"highway"="bus_stop"', out='body')
query = overpassQueryBuilder(area='relation 175905', elementType='node', selector='"highway"="bus_stop"', out='body')
```
Instead of an area, one can also use a bounding box:
```python
query = overpassQueryBuilder(bbox=[48.1, 16.3, 48.3, 16.5], elementType='node', selector='"highway"="bus_stop"', out='body')
```
The variable `query` is just a string containing the query:
```
'area(3600175905)->.searchArea;(node["highway"="bus_stop"](area.searchArea);); out body;'
```
Conditions can be provided by using the `conditions` parameter, either as a string in case of one condition only or as a list of strings in case of several conditions:
```python
query = overpassQueryBuilder(bbox=[48.1, 16.3, 48.3, 16.5], elementType='node', selector='"highway"="bus_stop"', conditions='count_tags() > 6', out='body')
```
Also, the geometry can be included in the download:
```python
query = overpassQueryBuilder(bbox=[48.1, 16.3, 48.3, 16.5], elementType='node', selector='"highway"="bus_stop"', out='body', includeGeometry=True)
```

If not only one `elementType` or `selector` shall be queried for, also lists can be provided for both parameters:
```python
query = overpassQueryBuilder(area=nominatim.query('London'), elementType=['node', 'way'], selector=['"name"~"Tesco"', 'opening_hours'])
```
The resulting query accordingly lists all nodes and ways in the area of London, which have a key `name` with a value containing `Tesco` and a tag `opening_hours`:
```
'area(3600065606)->.searchArea;(node["name"~"Tesco"][opening_hours](area.searchArea);way["name"~"Tesco"][opening_hours](area.searchArea);); out body;'
```

In addition to the aforenamed parameters, a starting date (`since`) and potentially an ending data (`to`) can be provided.  To restrict the query further, a user who created or edited the data can be provided by the username (`user`) or the user ID (`userid`).  Both the parameter `user` and the parameter `userid` accept either one value or a list.  As an example, a query can be generated like follows:
```python
query = overpassQueryBuilder(area=nominatim.query('Heidelberg'), elementType='node', since='2017-01-01T00:00:00Z', to='2017-02-01T00:00:00Z', user='franz-benjamin', out='meta')
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

## Accessing the result of a query

The result of the overpass query is an object containing several functions to easily access the data. All elements returned by the query can be accessed:
```python
busStops.elements()
# [<OSMPythonTools.element.Element object at 0x10963c9b0>, <OSMPythonTools.element.Element object at 0x10963c8d0>, ...
```
Each element is of the type [OSMPythonTools.element.**Element**](element.md), and easy methods to access its properties exist.

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
