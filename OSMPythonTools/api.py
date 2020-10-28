from bs4 import BeautifulSoup

from OSMPythonTools.element import Element
from OSMPythonTools.internal.cacheObject import CacheObject
from OSMPythonTools.internal.singletonApi import SingletonApi

class Api(CacheObject):
    def __init__(self, endpoint='http://www.openstreetmap.org/api/0.6/', **kwargs):
        super().__init__('api', endpoint, jsonResult=False, **kwargs)
    
    def _queryString(self, query, params={}):
        return (query, query, params)
    
    def _queryRequest(self, endpoint, queryString, params={}):
        return endpoint + queryString
    
    def _rawToResult(self, data, queryString, params, shallow=False):
        return ApiResult(data, queryString, params, shallow=shallow)

class ApiResult(Element):
    def __init__(self, xml, queryString, params, shallow=False):
        self._isValid = (xml != {} and xml is not None)
        self._xml = xml
        self._soup = None
        soupElement = None
        if self._isValid:
            self._soup = BeautifulSoup(xml, 'xml')
            if len(self._soup.find_all('node')) > 0:
                soupElement = self._soup.node
            if len(self._soup.find_all('way')) > 0:
                soupElement = self._soup.way
            if len(self._soup.find_all('relation')) > 0:
                soupElement = self._soup.relation
        super().__init__(soup=soupElement, shallow=shallow)
        self._queryString = queryString
        self._params = params
    
    def _unshallow(self):
        api = SingletonApi()
        x = api.query(self.type() + '/' + str(self.id()))
        self.__init__(x._xml, x._queryString, x._params)
    
    def isValid(self):
        return self._isValid
    
    def toXML(self):
        return self._xml
    
    def queryString(self):
        return self._queryString
    
    def __get(self, prop):
        return self._soup.attrs[prop] if self._isValid and prop in self._soup.attrs else None
    
    ### general information
    def version(self):
        return self.__get('version')
    def generator(self):
        return self.__get('generator')
    def copyright(self):
        return self.__get('copyright')
    def attribution(self):
        return self.__get('attribution')
    def license(self):
        return self.__get('license')
