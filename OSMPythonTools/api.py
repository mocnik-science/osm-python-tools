from bs4 import BeautifulSoup

from OSMPythonTools.element import Element
from OSMPythonTools.internal.cacheObject import CacheObject
from OSMPythonTools.internal.singletonApi import SingletonApi

class Api(CacheObject):
    def __init__(self, endpoint='http://www.openstreetmap.org/api/0.6/', **kwargs):
        super().__init__('api', endpoint, jsonResult=False, **kwargs)
    
    def _queryString(self, query, params={}, history=False):
        query = query + ('/history' if history else '')
        return (query, query, params)
    
    def _queryRequest(self, endpoint, queryString, params={}):
        return endpoint + queryString
    
    def _rawToResult(self, data, queryString, params, kwargs, cacheMetadata=None, shallow=False):
        return ApiResult(data, queryString, params, cacheMetadata=cacheMetadata, shallow=shallow, history=kwargs['history'] if 'history' in kwargs else False)

class ApiResult(Element):
    def __init__(self, xml, queryString, params, cacheMetadata=None, shallow=False, history=False):
        self._isValid = (xml != {} and xml is not None)
        self._xml = xml
        self._soup2 = None
        soup = None
        soupHistory = None
        if self._isValid:
            self._soup2 = BeautifulSoup(xml, 'xml').find('osm')
            soupHistory = self._soup2.find_all(['node', 'way', 'relation'])
            if len(soupHistory) > 0:
                soup = soupHistory[-1]
        super().__init__(cacheMetadata, soup=soup, soupHistory=soupHistory if history else None, shallow=shallow)
        self._queryString = queryString
        self._params = params
    
    def _unshallow(self):
        api = SingletonApi()
        x = api.query(self.type() + '/' + str(self.id()) + ('/full' if self.type() != 'node' else ''))
        self.__init__(x._xml, x._queryString, x._params)
    
    def isValid(self):
        return self._isValid
    
    def toXML(self):
        return self._xml
    
    def queryString(self):
        return self._queryString
    
    def __get(self, prop):
        return self._soup2.attrs[prop] if self._isValid and prop in self._soup2.attrs else None
    
    ### general information
    def apiVersion(self):
        return self.__get('version')
    def generator(self):
        return self.__get('generator')
    def copyright(self):
        return self.__get('copyright')
    def attribution(self):
        return self.__get('attribution')
    def license(self):
        return self.__get('license')
