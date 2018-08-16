from bs4 import BeautifulSoup

from OSMPythonTools.element import Element
from OSMPythonTools.internal.cacheObject import CacheObject

def _raiseException(prefix, msg):
    sys.tracebacklimit = None
    raise(Exception('[OSMPythonTools.' + prefix + '] ' + msg))

class Api(CacheObject):
    def __init__(self, endpoint='http://www.openstreetmap.org/api/0.6/', **kwargs):
        super().__init__('api', endpoint, jsonResult=False, **kwargs)
    
    def _queryString(self, query, params={}):
        return (query, query, params)
    
    def _queryRequest(self, endpoint, queryString, params={}):
        return endpoint + queryString
    
    def _rawToResult(self, data, queryString):
        return ApiResult(data, queryString)

class ApiResult(Element):
    def __init__(self, xml, queryString):
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
        super().__init__(soup=soupElement)
        self._queryString = queryString
    
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
