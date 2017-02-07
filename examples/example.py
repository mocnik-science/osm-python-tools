#!/usr/bin/env python3

print('=' * 6, 'Example 1', '=' * 6)

from OSMPythonTools.api import Api

api = Api()
way = api.query('way/5887599')
print('building:        %s' % way.tag('building'))
print('historic         %s' % way.tag('historic'))
print('architect:       %s' % way.tag('architect'))
print('website:         %s' % way.tag('website'))

print('=' * 6, 'Example 2', '=' * 6)

from OSMPythonTools.overpass import Overpass

overpass = Overpass()
result = overpass.query('way["name"="Stephansdom"]; out body;')
stephansdom = result.elements()[0]
print('name:en:         %s' % stephansdom.tag('name:en'))
print('address:         %s %s, %s %s' % (stephansdom.tag('addr:street'), stephansdom.tag('addr:housenumber'), stephansdom.tag('addr:postcode'), stephansdom.tag('addr:city')))
print('building:        %s' %  stephansdom.tag('building'))
print('denomination:    %s' % stephansdom.tag('denomination'))

print('=' * 6, 'Example 3', '=' * 6)

from OSMPythonTools.nominatim import Nominatim
nominatim = Nominatim()
areaId = nominatim.query('Vienna').areaId()

from OSMPythonTools.overpass import overpassQueryBuilder
query = overpassQueryBuilder(area=areaId, elementType='node', selector='"natural"="tree"', out='count')
result = overpass.query(query)
print('number of trees (now):  %s' % result.countElements())
result = overpass.query(query, date='2013-01-01T00:00:00Z', timeout=60)
print('number of trees (2013): %s' % result.countElements())

print('=' * 6, 'Example 4', '=' * 6)

from collections import OrderedDict
from OSMPythonTools.data import Data, dictRangeYears, ALL

dimensions = OrderedDict([
    ('year', dictRangeYears(2013, 2017.5, 1)),
    ('city', OrderedDict({
        'berlin': 'Berlin, Germany',
        'paris': 'Paris, France',
        'vienna': 'Vienna, Austria',
    })),
])

def fetch(year, city):
    areaId = nominatim.query(city).areaId()
    query = overpassQueryBuilder(area=areaId, elementType='node', selector='"natural"="tree"', out='count')
    return overpass.query(query, date=year, timeout=60).countElements()

data = Data(fetch, dimensions)

print(data.select(city=ALL).getCSV())
data.plot(city=ALL, filename='example4.png')
