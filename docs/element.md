[back to readme](../../../)

# Element

Several services, amongst them the [OSMPythonTools.**api**](api.md) and [OSMPythonTools.**overpass**](overpass.md) return OSM objects, which are represented by an instance of the class `Element`, which provides functions to access its properties.

## Accessing general properties

Consider the following example of a query to the OSM Api:
```python
from OSMPythonTools.api import Api
api = Api()
busStop = api.query('node/42467507')
```
The result, that is, `busStop`, is an element, whose properties can easily be access as follows:
```python
busStop.id()
# 42467507
busStop.type()
# 'node'
busStop.lat()
# 40.7014417
busStop.lon()
# -73.9430797
```

## Accessing tags

The tags can be accessed as a python dictionary:
```python
busStop.tags()
# {'asset_ref': '2030', 'highway': 'bus_stop', 'location': 'Broadway / Thornton Street', 'name': 'Broadway / Thornton Street', 'route_ref': 'B46;B46-LTD'}
```
The value of a single tag can be accessed like follows:
```python
busStop.tag('highway')
# 'bus_stop'
```

## Accessing nodes and members

Ways incorporate nodes, and relations other elements, called members. Nodes of a way can easily be accessed:
```python
way = api.query('way/108402486')
way.nodes()
# [<OSMPythonTools.api.ApiResult object at 0x104c06940>, <OSMPythonTools.api.ApiResult object at 0x104c2d8d0>, ...
way.nodes()[0].id()
# 1243967857
```
The members of a relation can also easily be accessed:
```python
relation = api.query('relation/1539714')
relation.members()
# [<OSMPythonTools.api.ApiResult object at 0x104c20240>, <OSMPythonTools.api.ApiResult object at 0x104c2db38>, ...
relation.members()[0].id()
# 108402486
```

It should be noted that the nodes and members accessed this way are shallow by default.  That is, the objects representing these elements (nodes and members) have only preloaded the type and the ID of the element.  If more properties of the elements are accessed, the corresponding data is automatically downloaded and cached.  Accordingly, the command
```python
way.nodes()[0].id()
```
does not download the data for the nodes but rather just outputs the ID.  If the latitude of the first node shall be accessed, this can be done as follows:
```python
way.nodes()[0].lat()
```
As the data is downloaded only when needed and as the elements (in this case the nodes) are shallow by default, the data is only downloaded for the first node.  In rare cases, the data should be downloaded for elements.  In this case, the parameter `shallow=False` needs to be added:
```python
way.nodes(shallow=False)
```
Members of a relation are shallow by default as well, and the same parameter `shallow=False` can be used.

## Accessing the geometry

In order to receive geometry information, the argument `includeGeometry=True` needs to be provided to the `overpassQueryBuilder` in order to let him generate a query that downloads the geometry data.  As an example, one can query for all waterbodies in Vienna:
```python
from OSMPythonTools.nominatim import Nominatim
from OSMPythonTools.overpass import overpassQueryBuilder, Overpass

vienna = Nominatim().query('Vienna, Austria')
query = overpassQueryBuilder(area=vienna.areaId(), elementType=['way', 'relation'], selector='"natural"="water"', includeGeometry=True)
result = Overpass().query(query)
```
The geometry of the downloaded elements can be obtained in the [GeoJSON](https://en.wikipedia.org/wiki/GeoJSON) format:
```python
result.elements()[0].geometry()
# {"coordinates": [[[16.498671, 48.27628], [16.4991, 48.276345], ... ]], "type": "Polygon"}
```
Some relations contain invalid geometries.  If this is the case, an exception is returned.

## Accessing the history and data about the creation

If explicitly queried, the resulting elements contain information about the history.  As an example, one can query for the changes made by the user `franz-benjamin` in `Heidelberg` in March 2017:
```python
from OSMPythonTools.nominatim import Nominatim
from OSMPythonTools.overpass import overpassQueryBuilder, Overpass

heidelberg = Nominatim().query('Heidelberg, Germany')
query = overpassQueryBuilder(area=heidelberg.areaId(), elementType='node', since='2017-01-01T00:00:00Z', to='2017-02-01T00:00:00Z', user='franz-benjamin', out='meta')
changedNodes = Overpass().query(query)
```

It is important to use `out='meta'` because this will fetch the meta data about the history and the creation of the corresponding elements:
```python
changedNodes.elements()[0].version()
# 8
changedNodes.elements()[0].changeset()
# 44871772
changedNodes.elements()[0].user()
# 'franz-benjamin'
changedNodes.elements()[0].userid()
# 4913117
changedNodes.elements()[0].timestamp()
'2017-01-03T13:47:23Z'
```
