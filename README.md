# OSMPythonTools

The python package `OSMPythonTools` provides easy access to [OpenStreetMap (OSM)](http://www.openstreetmap.org) related services, amongst them an [Overpass endpoint](http://wiki.openstreetmap.org/wiki/Overpass_API) and [Nominatim](http://nominatim.openstreetmap.org).

## Examples

TODO

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

## Author

This application is written and maintained by Franz-Benjamin Mocnik, <mail@mocnik-science.net>.

(c) by Franz-Benjamin Mocnik, 2017.

The code is licensed under the [GPL-3](https://github.com/mocnik-science/osm-python-tools/blob/master/LICENSE.md).
