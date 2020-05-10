from OSMPythonTools.nominatim import Nominatim

def test_place():
  nominatim = Nominatim()
  x = nominatim.query('Heidelberg')
  assert x.areaId() == 3600285864
  assert len(x.toJSON()) > 0

def test_placeWkt():
  nominatim = Nominatim()
  x = nominatim.query('Heidelberg', wkt=True)
  assert x.areaId() == 3600285864
  assert len(x.toJSON()) > 0
  assert len(x.wkt()) > 0
  assert x.toJSON()
