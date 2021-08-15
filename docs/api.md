[back to readme](../../../)

# API

The [OSM API](http://wiki.openstreetmap.org/wiki/API) provides access to many kind of information in the OSM database. Currently, this module only supports the requests `node`, `way`, and `relation`.

We can access information about a node with the ID `42467507` as follows:
```python
from OSMPythonTools.api import Api
api = Api()
busStop = api.query('node/42467507')
```
The result is an element of the type [OSMPythonTools.element.**Element**](element.md), and easy methods to access its properties exist.

In a similar way, also ways and relations can be accessed:
```python
from OSMPythonTools.api import Api
api = Api()
api.query('way/108402486')
api.query('relation/1539714')
```

## Metadata

When requesting data from the Api, the resulting object even contains some metadata about the request:
```python
from OSMPythonTools.api import Api
api = Api()
busStop = api.query('node/42467507')
busStop.version()
# 0.6
busStop.generator()
# CGImap 0.8.5 (3882970 spike-07.openstreetmap.org)
busStop.copyright()
# OpenStreetMap and contributors
busStop.attribution()
# http://www.openstreetmap.org/copyright
busStop.license()
# http://opendatacommons.org/licenses/odbl/1-0/
```
