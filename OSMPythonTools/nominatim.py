import urllib.parse

from OSMPythonTools.internal.cacheObject import CacheObject
from OSMPythonTools.internal.elementShallow import ElementShallow
from OSMPythonTools.element import Element

class Nominatim(CacheObject):
    def __init__(self, endpoint='https://nominatim.openstreetmap.org/', **kwargs):
        super().__init__('nominatim', endpoint, **kwargs)

    def _queryString(self, *args, wkt=False, reverse=False, lookup=False, zoom=None, **kwargs):
        if reverse:
            query = 'reverse'
            [lat, lon] = args
            params = kwargs['params'] if 'params' in kwargs else {}
            params['lat'] = lat
            params['lon'] = lon
            if zoom is not None:
                params['zoom'] = zoom
            if wkt:
                params['polygon_text'] = '1'
        elif lookup:
            query = 'lookup'
            params = kwargs['params'] if 'params' in kwargs else {}
            params['osm_ids'] = ','.join(map(lambda a: Element.fromId(a).typeIdShort().upper(), args))
            if wkt:
                params['polygon_text'] = '1'
        else:
            query = 'search'
            [q] = args
            params = kwargs['params'] if 'params' in kwargs else {}
            params['q'] = q
            if wkt:
                params['polygon_text'] = '1'
        return (query, query, params)

    def _queryRequest(self, endpoint, queryString, params=None):
        if not params:
            params = {}
        params['format'] = 'json'
        return endpoint + queryString + '?' + urllib.parse.urlencode(params)

    def _rawToResult(self, data, queryString, params, kwargs, cacheMetadata=None, shallow=False):
        return NominatimResult(data, queryString, params, cacheMetadata=cacheMetadata) if queryString == 'reverse' else NominatimResults(data, queryString, params, cacheMetadata=cacheMetadata)

class NominatimResults(ElementShallow):
    def __init__(self, json, queryString, params, cacheMetadata=None):
        self._json = json
        self._queryString = queryString
        self._params = params
        super().__init__(cacheMetadata)

    def toJSON(self):
        return self._json

    def __iter__(self):
        return (NominatimResult(json, self._queryString, self._params, self._cacheMetadata) for json in self._json)

    def firstResult(self):
        return next(iter(self), None)

    def queryString(self):
        return [self._params['lat'], self._params['lon']] if self.isReverse() else self._params['q']

    def isReverse(self):
        return self._queryString == 'reverse'

    def displayName(self):
      return next((s.displayName() for s in self if s.displayName()), None)

    def address(self):
      return next((s.address() for s in self if s.address()), None)

    def id(self):
        return next((s.id() for s in self if s.id()), None)

    def type(self):
        return next((s.type() for s in self if s.type()), None)

    def wkt(self):
        return next((s.wkt() for s in self if s.wkt()), None)

    def areaId(self):
        return next((s.areaId() for s in self if s.areaId()), None)

class NominatimResult(NominatimResults):
  def __init__(self, json, queryString, params, cacheMetadata=None):
      super().__init__(json, queryString, params, cacheMetadata)

  def isReverse(self):
      return self._queryString == 'reverse'

  def displayName(self):
      return self._json['display_name'] if 'display_name' in self._json else None

  def address(self):
      return self._json['address'] if 'address' in self._json else None

  def id(self):
      return self._json['osm_id'] if 'osm_type' in self._json and 'osm_id' in self._json else None

  def type(self):
      return self._json['osm_type'] if 'osm_type' in self._json and 'osm_id' in self._json else None

  def wkt(self):
      return self._json['geotext'] if 'geotext' in self._json else None

  def areaId(self):
      return self._areaId(self._json['osm_type'], self._json['osm_id']) if 'osm_type' in self._json and 'osm_id' in self._json else None
