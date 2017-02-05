#!/usr/bin/env python3 -i

from OSMPythonTools.nominatim import Nominatim
from OSMPythonTools.overpass import Overpass, overpassQueryBuilder
from OSMPythonTools.data import Data, dictRangeYears, ALL

from collections import OrderedDict

# dimensions

dimensions = OrderedDict([
  ('year', dictRangeYears(2013, 2017.5, 1)),
  ('town', OrderedDict({
    'heidelberg': 'Heidelberg, Germany',
    'manhattan': 'Manhattan, New York',
    'vienna': 'Vienna, Austria',
  })),
  ('typeOfRoad', OrderedDict({
    'primary': 'primary',
    'secondary': 'secondary',
    'tertiary': 'tertiary',
  })),
])

# data mining

nominatim = Nominatim()
overpass = Overpass()

def fetch(year, town, typeOfRoad):
    areaId = nominatim.query(town).getAreaId()
    query = overpassQueryBuilder(area=areaId, elementType='way', selector='"highway"="' + typeOfRoad + '"', out='count')
    return overpass.query(query, date=year, timeout=60).countElements()

data = Data(fetch, dimensions)

# assess the data

data.plot(town='manhattan', typeOfRoad=ALL, filename='plot-manhattan.png')
data.plot(town=ALL, typeOfRoad='primary', filename='plot-primary.png')
data.plotBar(town='manhattan', year=ALL, filename='plotbar-manhattan.png')
data.plotScatter('vienna', 'manhattan', town=['vienna', 'manhattan'], typeOfRoad='primary', filename='plotscatter-primary.png')
