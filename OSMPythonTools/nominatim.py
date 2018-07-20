import urllib.parse

from OSMPythonTools.internal.cacheObject import CacheObject

class Nominatim(CacheObject):
    def __init__(self, endpoint='https://nominatim.openstreetmap.org/search', params={}, **kwargs):
        super().__init__('nominatim', endpoint, **kwargs)
        self._params = params
    
    def _queryString(self, query):
        return (query, query)
    
    def _queryRequest(self, endpoint, queryString):
        paramsDict = {'format':'json', 'q':queryString, **self._params}
        queryParams = urllib.parse.urlencode(paramsDict, safe='')
        return "{}?{}".format(endpoint, queryParams)
    
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
