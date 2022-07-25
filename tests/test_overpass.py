import random

from OSMPythonTools.nominatim import Nominatim
from OSMPythonTools.overpass import Overpass, overpassQueryBuilder

def assertForQueryResult(minElements=100, overpassKwargs={}, **kwargs):
  overpass = Overpass()
  y = overpass.query(overpassQueryBuilder(**kwargs), **overpassKwargs)
  assert y.isValid()
  assert len(y.elements()) > minElements
  assert len(y.elements()) == y.countElements()
  assert len(y.nodes()) >= 0
  assert len(y.nodes()) == y.countNodes()
  assert len(y.ways()) >= 0
  assert len(y.ways()) == y.countWays()
  assert len(y.relations()) >= 0
  assert len(y.relations()) == y.countRelations()
  assert len(y.areas()) >= 0
  assert len(y.areas()) == y.countAreas()
  assert y.countNodes() + y.countWays() + y.countRelations() + y.countAreas() == y.countElements()
  assert y.toJSON()
  assert y.version() > 0
  assert y.generator()
  assert y.timestamp_osm_base()
  assert y.copyright()
  return y

def test_queryAreaID():
  nominatim = Nominatim()
  x = nominatim.query('Enschede')
  assertForQueryResult(area=x, elementType='node', selector='"highway"="bus_stop"', out='body')

def test_queryAreaIDWithCondition():
  nominatim = Nominatim()
  x = nominatim.query('Enschede')
  assertForQueryResult(area=x, elementType='node', selector='"highway"="bus_stop"', conditions='count_tags() > 1', out='body')

def test_queryAreaIDWithCondition2():
  nominatim = Nominatim()
  x = nominatim.query('Enschede')
  assertForQueryResult(area=x, elementType='node', selector='"highway"="bus_stop"', conditions=['count_tags() > 2', 'count_tags() > 1'], out='body')

def test_queryAreaIDTimeout():
  nominatim = Nominatim()
  x = nominatim.query('Enschede')
  assertForQueryResult(area=x, elementType='node', selector='"highway"="bus_stop"', out='body', overpassKwargs={'timeout': 25})

def test_queryAreaIDTimeout():
  nominatim = Nominatim()
  x = nominatim.query('Enschede')
  assertForQueryResult(area=x, elementType='node', selector='"highway"="bus_stop"', out='body', overpassKwargs={'date': '2017-01-01T00:00:00Z'})

def test_queryBbox():
  nominatim = Nominatim()
  x = nominatim.query('Enschede')
  assertForQueryResult(bbox=[52.1, 6.7, 52.3, 6.9], elementType='node', selector='"highway"="bus_stop"', out='body')

def test_queryAreaIDGeometry():
  nominatim = Nominatim()
  x = nominatim.query('Enschede')
  y = assertForQueryResult(area=x, elementType='node', selector='"highway"="bus_stop"', includeGeometry=True)
  assert abs(y.nodes()[0].lat() - 52.2) < .5
  assert abs(y.nodes()[0].lon() - 6.8) < .5

def test_queryAreaIDCenter():
  nominatim = Nominatim()
  x = nominatim.query('Zandvoort')
  y = assertForQueryResult(area=x, elementType='way', selector='"highway"', includeCenter=True)
  assert abs(y.ways()[0].centerLat() - 52.4) < .5
  assert abs(y.ways()[0].centerLon() - 4.6) < .5

def test_queryAreaIDOut():
  nominatim = Nominatim()
  x = nominatim.query('Zandvoort')
  y = assertForQueryResult(area=x, elementType='way', selector='"highway"', out=['center', 'body'])
  assert abs(y.ways()[0].centerLat() - 52.4) < .5
  assert abs(y.ways()[0].centerLon() - 4.6) < .5

def test_queryBboxGeometry():
  nominatim = Nominatim()
  x = nominatim.query('Enschede')
  y = assertForQueryResult(bbox=[52.1, 6.7, 52.3, 6.9], elementType='node', selector='"highway"="bus_stop"', out='body')
  assert abs(y.nodes()[0].lat() - 52.2) < .5
  assert abs(y.nodes()[0].lon() - 6.8) < .5

def test_queryAreaIDSelector():
  nominatim = Nominatim()
  x = nominatim.query('Dublin')
  assertForQueryResult(minElements=5, area=x, elementType=['node', 'way'], selector=['"name"~"Tesco"', 'opening_hours'])

def test_queryAreaIDFormatArea():
  q = overpassQueryBuilder(area=2771744961, elementType='node')
  assert q == overpassQueryBuilder(area='way/371744961', elementType='node')
  assert q == overpassQueryBuilder(area='way 371744961', elementType='node')
  assert q == overpassQueryBuilder(area='w371744961', elementType='node')

def test_queryAreaIDFormatRelation():
  q = overpassQueryBuilder(area=3600415473, elementType='node')
  assert q == overpassQueryBuilder(area='relation/415473', elementType='node')
  assert q == overpassQueryBuilder(area='relation 415473', elementType='node')
  assert q == overpassQueryBuilder(area='r415473', elementType='node')

def test_differentAreaFormats():
  nominatim = Nominatim()
  overpass = Overpass()
  x = nominatim.query('Enschede')
  rs = []
  rs.append(overpass.query(overpassQueryBuilder(area=x, elementType='node', selector='"highway"="bus_stop"', out='body')))
  rs.append(overpass.query(overpassQueryBuilder(area=x.areaId(), elementType='node', selector='"highway"="bus_stop"', out='body')))
  rs.append(overpass.query(overpassQueryBuilder(area=x.typeId(), elementType='node', selector='"highway"="bus_stop"', out='body')))
  for r in rs:
    assert rs[0].countElements() == r.countElements()

def test_queryWaiting():
  nominatim = Nominatim()
  areaId = nominatim.query('Vienna, Austria').areaId()
  overpass = Overpass()
  n = 2 # If n get too large, we might experience a _504 Gateway Timeout_ error
  assert len([overpass.query(overpassQueryBuilder(area=areaId, elementType='node', selector='"natural"="' + ''.join(random.choice('abcdefghijklmopqrstuvwxyz') for _ in range(10)) + '"', out='count'), timeout=600) for _ in range(n)]) == n
