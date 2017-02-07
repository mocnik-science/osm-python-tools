# OSMPythonTools

The python package `OSMPythonTools` provides easy access to [OpenStreetMap (OSM)](http://www.openstreetmap.org) related services, amongst them an [Overpass endpoint](http://wiki.openstreetmap.org/wiki/Overpass_API) and [Nominatim](http://nominatim.openstreetmap.org).

## Examples



## Installation

To install `OSMPythonTools`, you will need `python3` and `pip` ([How to install pip](https://pip.pypa.io/en/stable/installing/)). Then execute:
```
pip install OSMPythonTools
```

## Usage

The following modules are available (please click on their names to access further documentation):

* [OSMPythonTools.**Api**](docs/api.md) - Access to the official OSM API
* [OSMPythonTools.**Data**](docs/data.md) - Collecting, mining, and drawing data from OSM; to be used in combination with the other modules
* [OSMPythonTools.**Element**](docs/element.md) - Elements are returned by other services, like the OSM API or the Overpass API
* [OSMPythonTools.**Nominatim**](docs/nominatim.md) - Access to Nominatim, a reverse geocoder
* [OSMPythonTools.**Overpass**](docs/overpass.md) - Access to the Overpass API

## Author

This application is written and maintained by Franz-Benjamin Mocnik, <mail@mocnik-science.net>.

(c) by Franz-Benjamin Mocnik, 2017.

The code is licensed under the [GPL-3](https://github.com/mocnik-science/osm-python-tools/blob/master/LICENSE.md).
