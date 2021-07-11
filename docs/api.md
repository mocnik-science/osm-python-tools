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
