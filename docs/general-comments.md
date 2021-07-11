[back to readme](../../../)

# General comments

Here, we make some general remarks that are of more generic character. They do not refer to a single module but rather to the entire library.

## Common paramters for all modules

All modules that allow fetching data, such as [Api](api.md), [Nominatim](nominatim.md), and [Overpass](overpass.md), share some common parameters to adjust the way the data is fetched and cached.

### Endpoint

In order to adjust the endpoint being used, i.e., the server that requests are directed to, the default URL can be replaced by a user-defined one:
```python
api = API(endpoint='XYZ')
nominatim = Nominatim(endpoint='XYZ')
overpass = Overpass(endpoint='XYZ')
```
Such change of the endpoint makes sense in particular if you have your own server instance of the OSM API, Nominatim, or Overpass. The following URLs are used by default:

| Module | Default URL |
| ------ | ----------- |
| [Api](api.md) | `http://www.openstreetmap.org/api/0.6/` |
| [Nominatim](nominatim.md) | `https://nominatim.openstreetmap.org/` |
| [Overpass](overpass.md) | `http://overpass-api.de/api/` |

Please ensure that you comply with the usage policy of the server you use.

### Waiting time between queries

Complying with the usage policy of a server usually means to not overuse the service offered in order to allow for a fair sharing of the available resources. In case you want or have to reduce the number of requests send out, you can provde a minimum waiting time between to queries. To do so, you can provide the number of seconds to wait, such as:
```python
api = Api(waitBetweenQueries=5) # waits at least 5 seconds between requests
```
Please note that this paramter does not work for the [Overpass](overpass.md) module, because the Overpass server implements a load balancing strategy already. The [Overpass](overpass.md) module therefore receives such information from the Overpass server automatically and acts accordingly.
