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


  # print(data)



# def test_node():
#   api = Api()
#   x = api.query('node/42467507')
#   assert x.isValid()
#   assert x.id() == 42467507
#   assert x.type() == 'node'
#   assert len(x.tags()) > 0
#   assert 'highway' in x.tags()
#   assert x.tag('highway') is not None
#   assert x.tag('abcde') is None
#   assert abs(x.lat() - 40.7014417) < .00001
#   assert abs(x.lon() - (-73.9430797)) < .00001
#   assert int(x.version()) > 0

# def test_way():
#   api = Api()
#   x = api.query('way/108402486')
#   assert x.isValid()
#   assert x.id() == 108402486
#   assert x.type() == 'way'
#   assert len(x.nodes()) > 0
#   assert 1243967857 in [n.id() for n in x.nodes()]
#   assert abs(x.nodes()[0].lat() - 40.866) < .01
#   assert abs(x.nodes()[0].lon() - (-73.795)) < .01
#   assert abs(x.nodes(shallow=False)[1].lat() - 40.866) < .01
#   assert abs(x.nodes(shallow=False)[1].lon() - (-73.795)) < .01
#   assert int(x.version()) > 0

# def test_relation():
#   api = Api()
#   x = api.query('relation/1539714')
#   assert x.isValid()
#   assert x.id() == 1539714
#   assert x.type() == 'relation'
#   assert len(x.members()) > 0
#   assert 108402486 in [n.id() for n in x.members()]
#   assert abs(x.members()[0].nodes()[0].lat() - 40.866) < .01
#   assert abs(x.members()[0].nodes()[0].lon() - (-73.795)) < .01
#   assert abs(x.members(shallow=False)[1].nodes()[0].lat() - 40.866) < .01
#   assert abs(x.members(shallow=False)[1].nodes()[0].lon() - (-73.795)) < .01
#   assert int(x.version()) > 0
