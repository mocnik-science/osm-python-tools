import urllib.parse

from OSMPythonTools.internal.cacheObject import CacheObject

class Nominatim(CacheObject):
    def __init__(self, endpoint='https://nominatim.openstreetmap.org/', **kwargs):
        super().__init__('nominatim', endpoint, **kwargs)
    
    def _queryString(self, *args, wkt=False, reverse=False, zoom=None, **kwargs):
        if reverse:
            query='reverse'
            [lat, lon] = args
            params = kwargs['params'] if 'params' in kwargs else {}
            params['lat'] = lat
            params['lon'] = lon
            if zoom is not None:
                params['zoom'] = zoom
            if wkt:
                params['polygon_text'] = '1'
        else:
            query='search'
            [q] = args
            params = kwargs['params'] if 'params' in kwargs else {}
            params['q'] = q
            if wkt:
                params['polygon_text'] = '1'
        return (query, query, params)
    
    def _queryRequest(self, endpoint, queryString, params={}):
        if not params:
            params = {}
        params['format'] = 'json'
        return endpoint + queryString + '?' + urllib.parse.urlencode(params)
    
    def _rawToResult(self, data, queryString, params, shallow=False):
        return NominatimResult(data, queryString, params)

class NominatimResult:
    def __init__(self, json, queryString, params):
        self._json = [json] if queryString == 'reverse' else json
        self._queryString = queryString
        self._params = params
    
    def toJSON(self):
        return self._json
    
    def queryString(self):
        return [self._params['lat'], self._params['lon']] if self.isReverse() else self._params['q']
    
    def isReverse(self):
        return self._queryString == 'reverse'

    def displayName(self):
        for d in self._json:
            if 'display_name' in d:
                return d['display_name']
        return None
    
    def address(self):
        for d in self._json:
            if 'address' in d:
                return d['address']
        return None

    def areaId(self):
        for d in self._json:
            if 'osm_type' in d and 'osm_id' in d:
                id_as_int = int(d['osm_id'])
                if d['osm_type'] == 'relation':
                    return 3600000000 + id_as_int
                elif d['osm_type'] == 'way':
                    return 2400000000 + id_as_int
        return None

    def wkt(self):
        for d in self._json:
            if 'geotext' in d:
                return d['geotext']
        return None
