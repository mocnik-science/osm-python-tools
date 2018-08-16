import urllib.parse

from OSMPythonTools.internal.cacheObject import CacheObject

class Nominatim(CacheObject):
    def __init__(self, endpoint='https://nominatim.openstreetmap.org/search', **kwargs):
        super().__init__('nominatim', endpoint, **kwargs)
    
    def _queryString(self, query, wkt=False, **kwargs):
        params = kwargs['params'] if 'params' in kwargs else {}
        if wkt:
            params['polygon_text'] = '1'
        return (query, query, params)
    
    def _queryRequest(self, endpoint, queryString, params={}):
        if not params:
            params = {}
        params['format'] = 'json'
        params['q'] = queryString
        return endpoint + '?' + urllib.parse.urlencode(params)
    
    def _rawToResult(self, data, queryString):
        return NominatimResult(data, queryString)

class NominatimResult:
    def __init__(self, json, queryString):
        self._json = json
        self._queryString = queryString
    
    def toJSON(self):
        return self._json
    
    def queryString(self):
        return self._queryString
    
    def areaId(self):
        for d in self._json:
            if 'osm_type' in d and d['osm_type'] == 'relation' and 'osm_id' in d:
                return 3600000000 + int(d['osm_id'])
        return None

    def wkt(self):
        for d in self._json:
            if 'geotext' in d:
                return d['geotext']
