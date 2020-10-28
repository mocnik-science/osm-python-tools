from OSMPythonTools.nominatim import Nominatim

def test_place():
  nominatim = Nominatim()
  x = nominatim.query('Heidelberg')
  assert x.isReverse() == False
  assert x.displayName().startswith('Heidelberg')
  assert x.areaId() == 3600285864
  assert len(x.toJSON()) > 0
  assert x.toJSON()

def test_placeWkt():
  nominatim = Nominatim()
  x = nominatim.query('Heidelberg', wkt=True)
  assert x.isReverse() == False
  assert x.displayName().startswith('Heidelberg')
  assert x.areaId() == 3600285864
  assert len(x.toJSON()) > 0
  assert len(x.wkt()) > 0
  assert x.toJSON()

def test_coordinates():
  nominatim = Nominatim()
  x = nominatim.query(49.4093582, 8.694724, reverse=True, zoom=10)
  assert x.isReverse() == True
  assert x.displayName() == 'Heidelberg, Baden-Württemberg, Deutschland'
  print(x.toJSON())
  assert x.areaId() == 3600285864
  assert x.address() == {
    'city': 'Heidelberg',
    'state': 'Baden-Württemberg',
    'country': 'Deutschland',
    'country_code': 'de',
  }
  assert len(x.toJSON()) > 0
  assert x.toJSON()

def test_coordinatesCountry():
  nominatim = Nominatim()
  x = nominatim.query(49.4093582, 8.694724, reverse=True, zoom=3)
  assert x.isReverse() == True
  assert x.displayName().startswith('Deutschland')
  assert x.areaId() == 3600051477
  assert x.address() == {
    'country': 'Deutschland',
    'country_code': 'de',
  }
  assert len(x.toJSON()) > 0
  assert x.toJSON()

def test_coordinatesWkt():
  nominatim = Nominatim()
  x = nominatim.query(49.4093582, 8.694724, reverse=True, zoom=10, wkt=True)
  assert x.isReverse() == True
  assert x.displayName() == 'Heidelberg, Baden-Württemberg, Deutschland'
  print(x.toJSON())
  assert x.areaId() == 3600285864
  assert x.address() == {
    'city': 'Heidelberg',
    'country': 'Deutschland',
    'country_code': 'de',
    'state': 'Baden-Württemberg',
  }
  assert len(x.toJSON()) > 0
  assert len(x.wkt()) > 0
  assert x.toJSON()

def test_coordinatesCountryWkt():
  nominatim = Nominatim()
  x = nominatim.query(49.4093582, 8.694724, reverse=True, zoom=3, wkt=True)
  assert x.isReverse() == True
  assert x.displayName().startswith('Deutschland')
  assert x.areaId() == 3600051477
  assert x.address() == {
    'country': 'Deutschland',
    'country_code': 'de',
  }
  assert len(x.toJSON()) > 0
  assert len(x.wkt()) > 0
  assert x.toJSON()
