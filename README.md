# OSMPythonTools

The python package `OSMPythonTools` provides easy access to [OpenStreetMap (OSM)](http://www.openstreetmap.org) related services, among them an [Overpass endpoint](https://wiki.openstreetmap.org/wiki/Overpass_API), [Nominatim](http://nominatim.openstreetmap.org), and the [OSM API](https://wiki.openstreetmap.org/wiki/API).

## Installation

To install `OSMPythonTools`, you will need `python3` and `pip` ([How to install pip](https://pip.pypa.io/en/stable/installing/)). Then execute:
```bash
pip install OSMPythonTools
```
On some operating systems, `pip` for `python3` is named `pip3`:
```bash
pip3 install OSMPythonTools
```

## Example 1

*Which object does the way with the ID `5887599` represent?*

We can use the OSM API to answer this question:
```python
from OSMPythonTools.api import Api
api = Api()
way = api.query('way/5887599')
```
The resulting object contains information about the way, which can easily be accessed:
```python
way.tag('building')
# 'castle'
way.tag('architect')
# 'Johann Lucas von Hildebrandt'
way.tag('website')
# 'http://www.belvedere.at'
```

## Example 2

*What is the English name of the church called ‘Stephansdom’, what address does it have, and which of which denomination is the church?*

We use the Overpass API to query the corresponding data:
```python
from OSMPythonTools.overpass import Overpass
overpass = Overpass()
result = overpass.query('way["name"="Stephansdom"]; out body;')
```
This time, the result is a number of objects, which can be accessed by `result.elements()`. We just pick the first one: 
```python
stephansdom = result.elements()[0]
```
Information about the church can now easily be accessed:
```python
stephansdom.tag('name:en')
# "Saint Stephen's Cathedral"
'%s %s, %s %s' % (stephansdom.tag('addr:street'), stephansdom.tag('addr:housenumber'), stephansdom.tag('addr:postcode'), stephansdom.tag('addr:city'))
# 'Stephansplatz 3, 1010 Wien'
stephansdom.tag('building')
# 'cathedral'
stephansdom.tag('denomination')
# 'catholic'
```

## Example 3

*How many trees are in the OSM data of Vienna? And how many trees have there been in 2013?*

This time, we have to first resolve the name ‘Vienna’ to an area ID:
```python
from OSMPythonTools.nominatim import Nominatim
nominatim = Nominatim()
areaId = nominatim.query('Vienna, Austria').areaId()
```
This area ID can now be used to build the corresponding query:
```python
from OSMPythonTools.overpass import overpassQueryBuilder, Overpass
overpass = Overpass()
query = overpassQueryBuilder(area=areaId, elementType='node', selector='"natural"="tree"', out='count')
result = overpass.query(query)
result.countElements()
# 137830
```
There are 134520 trees in the current OSM data of Vienna. How many have there been in 2013?
```python
result = overpass.query(query, date='2013-01-01T00:00:00Z', timeout=60)
result.countElements()
# 127689
```

## Example 4

*Where are waterbodies located in Vienna?*

Again, we have to resolve the name ‘Vienna’ before running the query:
```python
from OSMPythonTools.nominatim import Nominatim
nominatim = Nominatim()
areaId = nominatim.query('Vienna, Austria').areaId()
```
The query can be built like in the examples before.  This time, however, the argument `includeGeometry=True` is provided to the `overpassQueryBuilder` in order to let him generate a query that downloads the geometry data.
```python
from OSMPythonTools.overpass import overpassQueryBuilder, Overpass
overpass = Overpass()
query = overpassQueryBuilder(area=areaId, elementType=['way', 'relation'], selector='"natural"="water"', includeGeometry=True)
result = overpass.query(query)
```
Next, we can exemplarily choose one random waterbody (the first one of the download ones) and compute its geometry like follows:
```python
firstElement = result.elements()[0]
firstElement.geometry()
# {"coordinates": [[[16.498671, 48.27628], [16.4991, 48.276345], ... ]], "type": "Polygon"}
```
Observe that the resulting geometry is provided in the [GeoJSON](https://en.wikipedia.org/wiki/GeoJSON) format.

## Example 5

*How did the number of trees in Berlin, Paris, and Vienna change over time?*

Before we can answer the question, we have to import some modules:
```python
from collections import OrderedDict
from OSMPythonTools.data import Data, dictRangeYears, ALL
from OSMPythonTools.overpass import overpassQueryBuilder, Overpass
```
The question has two ‘dimensions’: the dimension of time, and the dimension of different cities:
```python
dimensions = OrderedDict([
    ('year', dictRangeYears(2013, 2017.5, 1)),
    ('city', OrderedDict({
        'berlin': 'Berlin, Germany',
        'paris': 'Paris, France',
        'vienna': 'Vienna, Austria',
    })),
])
```
We have to define how we fetch the data. We again use Nominatim and the Overpass API to query the data (it can take some time to perform this query the first time!):
```python
overpass = Overpass()
def fetch(year, city):
    areaId = nominatim.query(city).areaId()
    query = overpassQueryBuilder(area=areaId, elementType='node', selector='"natural"="tree"', out='count')
    return overpass.query(query, date=year, timeout=60).countElements()
data = Data(fetch, dimensions)
```
We can now easily generate a plot from the result:
```python
data.plot(city=ALL, filename='example4.png')
```

![data.plot(city=ALL, filename='example4.png')](https://github.com/mocnik-science/osm-python-tools/blob/master/examples/example4.png)

Alternatively, we can generate a table from the result
```python
data.select(city=ALL).getCSV()
# year,berlin,paris,vienna
# 2013.0,10180,1936,127689
# 2014.0,17971,26905,128905
# 2015.0,28277,90599,130278
# 2016.0,86769,103172,132293
# 2017.0,108432,103246,134616
```

More examples can be found inside the documentation of the modules.

## Usage

The following modules are available (please click on their names to access further documentation):

* [OSMPythonTools.**Api**](docs/api.md) - Access to the official OSM API
* [OSMPythonTools.**Data**](docs/data.md) - Collecting, mining, and drawing data from OSM; to be used in combination with the other modules
* [OSMPythonTools.**Element**](docs/element.md) - Elements are returned by other services, like the OSM API or the Overpass API
* [OSMPythonTools.**Nominatim**](docs/nominatim.md) - Access to Nominatim, a reverse geocoder
* [OSMPythonTools.**Overpass**](docs/overpass.md) - Access to the Overpass API

Please refer to the [general remarks](docs/general-remarks.md) page if you have further questions related to `OSMPythonTools` in general or functionality that the several modules have in common.

**Observe the [breaking changes as included in the version history](version-history.md).**

## Logging

This library is a little bit more verbose than other Python libraries. The good reason behind is that the OpenStreetMap, the Nominatim, and the Overpass servers experience a heavy load already and their resources should be used carefully. In order to make you, the user of this library, aware of when `OSMPythonTools` accesses these servers, corresponding information is logged by default. In case you want to suppress these messages, you have to insert the following lines *after* the import of `OSMPythonTools`:
```python
import logging
logging.getLogger('OSMPythonTools').setLevel(logging.ERROR)
```
Please note that suppressing the messages means that you have to ensure on your own that you do not overuse the provided services and that you stick to their fair policy guidelines.

## Tests

You can test the package by installing the corresponding dependencies
```bash
pip install OSMPythonTools [test]
# or: pip3 install OSMPythonTools [test]
```
and then running
```bash
pytest --verbose
```
Please note that the tests might run very long (several minutes) because the overpass server will most likely defer the downloads.

## Author

This application is written and maintained by Franz-Benjamin Mocnik, <mail@mocnik-science.net>.

(c) by Franz-Benjamin Mocnik, 2017-2022.

The code is licensed under the [GPL-3](https://github.com/mocnik-science/osm-python-tools/blob/master/LICENSE).
