from OSMPythonTools.nominatim import Nominatim
from OSMPythonTools.overpass import Overpass, overpassQueryBuilder
from OSMPythonTools.data import Data, dictRangeYears, ALL

from collections import OrderedDict

def test_data():
  dimensions = OrderedDict([
    ('year', dictRangeYears(2015, 2016.5, 1)),
    ('city', OrderedDict({
      # 'manhattan': 'Manhattan, New York',
      # 'vienna': 'Vienna, Austria',
      'enschede': 'Enschede, Netherlands',
      'vienna': 'Vienna, Austria',
    })),
    ('typeOfShop', OrderedDict({
      'supermarket': 'supermarket',
      'coffee': 'coffee',
    })),
  ])

  nominatim = Nominatim()
  overpass = Overpass()

  def fetch(year, city, typeOfShop):
      areaId = nominatim.query(city).areaId()
      query = overpassQueryBuilder(area=areaId, elementType='way', selector='"shop"="' + typeOfShop + '"', out='count')
      x = overpass.query(query, date=year, timeout=30).countElements()
      assert x >= 0
      return x

  data = Data(fetch, dimensions)
