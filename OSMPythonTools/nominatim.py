import urllib.parse

from OSMPythonTools.internal.cacheObject import CacheObject

class Nominatim(CacheObject):
    def __init__(self, endpoint='https://nominatim.openstreetmap.org/search', **kwargs):
        super().__init__('nominatim', endpoint, **kwargs)
    
    def _queryString(self, query):
        return (query, query)
    
    def _queryRequest(self, endpoint, queryString):
        return endpoint + '?format=json&q=' + urllib.parse.quote_plus(queryString, safe='')
    
    def _jsonToResult(self, data, queryString):
        return NominatimResult(data, queryString)

class NominatimResult:
    def __init__(self, json, queryString):
        self._json = json
        self._queryString = queryString
    
    def toJSON(self):
        return self._json
    
    def getQueryString(self):
        return self._queryString
    
    def getAreaId(self):
        for d in self._json:
            if 'osm_type' in d and d['osm_type'] == 'relation' and 'osm_id' in d:
                return 3600000000 + int(d['osm_id'])
        return None
