[back to readme](../../../)

# Nominatim

## Geocoding

OSM data contains numerous place names. Nominatim is a geocoder which is able to identify geometries in OSM data corresponding to a given string. If you are, for example, interested in the German town Heidelberg, you can query:
```python
from OSMPythonTools.nominatim import Nominatim
nominatim = Nominatim()
heidelberg = nominatim.query('Heidelberg')
```
As can be checked by the (full) place name, the place has been identified correctly:
```python
heidelberg.displayName()
# Heidelberg, Baden-Württemberg, Deutschland
```
The result of this query is an object, which contains a number of methods to access the data. Most important, the area id can be accessed:
```python
heidelberg.areaId()
# 3600285864
```
This raw data provided by Nominatim potentially contains more than one geometry. The function `areaId` only returns the area id of the first geometry. The (complete) raw data of the answer by Nominatim can be accessed:
```python
heidelberg.toJSON()
# [{'place_id': '580259', 'licence': 'Data © OpenStreetMap ...
```

If you want to know the geometry as [well-known text](https://en.wikipedia.org/wiki/Well-known_text), you have to provide an corresponding parameter for the request, because this will inform the Nominatim webservie to provide the geometry in the result:
```python
heidelberg = nominatim.query('Heidelberg', wkt=True)
heidelberg.wkt()
# 'POINT(8.694724 49.4093582)'
```
Additional parameters can be sent with the query request by providing a `params` dictionary to `nominatim.query`.

## Reverse geocoding

Nominatim also offers reverse geocoding capabilities, that is, it can for given coordinates determine the corresponding place name.  Reverse geocoding works very similiar to the geocoding process described above, but the coordinates need to be provided instead of the place name:
```python
from OSMPythonTools.nominatim import Nominatim
nominatim = Nominatim()
heidelberg = nominatim.query(49.4093582, 8.694724, reverse=True, zoom=10)
```
The fact that the entity is the result of a reverse geocoding process can be checked as follows:
```python
heidelberg.isReverse()
# True
```
Besides the usual attributes, the result of a geocoding process also provides the address information in a more structured way by the method `address`:
```python
heidelberg.address()
# {'city': 'Heidelberg', 'state': 'Baden-Württemberg', 'country': 'Deutschland', 'country_code': 'de'}
heidelberg.displayName()
# Heidelberg, Baden-Württemberg, Deutschland
heidelberg.areaId()
# 3600285864
heidelberg.toJSON()
# [{'place_id': 235110274, 'licence': 'Data © OpenStreetMap ...
```
Note that we have provided a ‘zoom’ level, which determines at which scale we want to know the place name. By default, Nominatim assumes a zoom level of 18, which corresponds to the building level, thus allowing to encode the address:
```python
buildingInHeidelberg = nominatim.query(49.4093582, 8.694724, reverse=True)
buildingInHeidelberg.address()
# {'house_number': '8', 'road': 'Hauptstraße', 'suburb': 'Altstadt', 'city_district': 'Altstadt', 'city': 'Heidelberg', 'state': 'Baden-Württemberg', 'postcode': '69117', 'country': 'Deutschland', 'country_code': 'de'}
buildingInHeidelberg.displayName()
# 8, Hauptstraße, Altstadt, Heidelberg, Baden-Württemberg, 69117, Deutschland
```
A zoom value of 3 corresponds to the country level:
```python
countryContainingHeidelberg = nominatim.query(49.4093582, 8.694724, reverse=True, zoom=3)
countryContainingHeidelberg.displayName()
# Deutschland
```
Further information on the zoom levels can be found in the [Nominatim documentation](https://nominatim.org/release-docs/develop/api/Reverse/).

Again and as before, the well-known text representation of the geometry can be accessed:
```python
heidelberg = nominatim.query(49.4093582, 8.694724, reverse=True, zoom=10, wkt=True)
# POLYGON((8.5731788 49.4236,8.5732444 49.4232662,8.5735169 49.4217463, ...
```

## Parameters

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
