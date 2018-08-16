import datetime as dt
import sys
import time
import urllib.parse
import urllib.request

from OSMPythonTools.element import Element
from OSMPythonTools.internal.cacheObject import CacheObject

def _raiseException(prefix, msg):
    sys.tracebacklimit = None
    raise(Exception('[OSMPythonTools.' + prefix + '] ' + msg))

def overpassQueryBuilder(area=None, bbox=None, elementType=None, selector=[], since=None, to=None, userid=None, user=None, out='body'):
    if not elementType:
        _raiseException('overpassQueryBuilder', 'Please provide an elementType')
    if not area and not bbox:
        _raiseException('overpassQueryBuilder', 'Please provide an area or a bounding box')
    if area and bbox:
        _raiseException('overpassQueryBuilder', 'Please do not provide an area and a bounding box')
    if userid and user:
        _raiseException('overpassQueryBuilder', 'Please do only provide one of the following: user id and username')
    if not isinstance(elementType, list):
        elementType = [elementType]
    if not isinstance(selector, list):
        selector = [selector]
    if userid and not isinstance(userid, list):
        userid = [userid]
    if user and not isinstance(user, list):
        user = [user]
    dateRestriction = '(changed:"' + since + '"' + (',"' + to + '"' if to else '') + ')' if since else ''
    userRestriction = '(uid:' + ','.join(map(str, userid)) + ')' if userid else ''
    userRestriction2 = '(user:' + ','.join(map(lambda u: '"' + u + '"', user)) + ')' if user else ''
    searchArea = '(' + 'area.searchArea' + ')' if area else ''
    searchBbox = '(' + ','.join(map(str, bbox)) + ')' if bbox else ''
    query = ('area(' + str(area) + ')->.searchArea;(') if area else '('
    for e in elementType:
        query += e + ''.join(map(lambda x: '[' + x + ']', selector)) + dateRestriction + userRestriction + userRestriction2 + searchArea + searchBbox + ';'
    query += '); out ' + out + ';'
    return query

class Overpass(CacheObject):
    def __init__(self, endpoint='http://overpass-api.de/api/', **kwargs):
        super().__init__('overpass', endpoint, **kwargs)
    
    def queryString(self, *args, **kwargs):
        return self._queryString(*args, **kwargs)
    
    def _queryString(self, query, timeout=25, date=None, out='json', settings={}, params={}):
        settingsNotInHash = {
            'timeout': timeout,
        }
        if date:
            settings['date'] = '"' + date + '"'
        settings['out'] = out
        hashString = ''.join(['[' + k + ':' + str(v) + ']' for (k, v) in sorted(settings.items())]) + ';' + query
        queryString = ''.join(['[' + k + ':' + str(v) + ']' for (k, v) in sorted(settingsNotInHash.items())]) + hashString
        return (queryString, hashString, params)
    
    def _queryRequest(self, endpoint, queryString, params={}):
        return urllib.request.Request(endpoint + 'interpreter', urllib.parse.urlencode({'data': queryString}).encode('utf-8'))
    
    def _rawToResult(self, data, queryString):
        return OverpassResult(data, queryString)
    
    def _isValid(self, result):
        return result.isValid()
    
    def _waitForReady(self):
        try:
            haveWaited = False
            while True:
                response = urllib.request.urlopen(urllib.request.Request(self._endpoint + 'status', headers= {'User-Agent': self._userAgent()}))
                encoding = response.info().get_content_charset('utf-8')
                statusString = response.read().decode(encoding).split('\n')
                if statusString[2] == 'Rate limit: 0':
                    return True
                if statusString[3].endswith('slots available now.'):
                    if haveWaited:
                        print('[' + self._prefix + '] start processing')
                    return True
                waitTo = dt.datetime.strptime(statusString[3].split(' ')[3], '%Y-%m-%dT%H:%M:%SZ,')
                currentTime = dt.datetime.strptime(statusString[1].split(' ')[2], '%Y-%m-%dT%H:%M:%SZ')
                sec = min((waitTo - currentTime).total_seconds(), 10.)
                if sec > 0:
                    print('[' + self._prefix + '] waiting for ' + str(sec) + (' more' if haveWaited else '') + ' seconds')
                    time.sleep(sec)
                    haveWaited = True
        except:
            raise(Exception('[' + self._prefix + '] could not fetch or interpret status of the endpoint'))

class OverpassResult:
    def __init__(self, json, queryString):
        self._json = json
        self._elements = list(map(lambda e: Element(json=e), self.__get('elements')))
        self._queryString = queryString
    
    def isValid(self):
        remark = self.remark()
        return remark.find('error') < 0 if remark else True
    
    def toJSON(self):
        return self._json
    
    def queryString(self):
        return self._queryString
    
    def __get(self, prop):
        return self._json[prop] if prop in self._json else None
    def __get2(self, prop1, prop2):
        value1 = self.__get(prop1)
        return value1[prop2] if value1 and prop2 in value1 else None
    
    ### general information
    def version(self):
        return self.__get('version')
    def generator(self):
        return self.__get('generator')
    def timestamp_osm_base(self):
        return self.__get2('osm3s', 'timestamp_osm_base')
    def timestamp_area_base(self):
        return self.__get2('osm3s', 'timestamp_area_base')
    def copyright(self):
        return self.__get2('osm3s', 'copyright')
    def remark(self):
        return self.__get('remark')
    
    ### elements
    def elements(self):
        es = self.__get('elements')
        if len(es) == 1 and 'type' in es[0] and es[0]['type'] == 'count':
            return None
        else:
            return self._elements
    def __elementsOfType(self, elementType):
        elements = self.elements()
        return list(filter(lambda element: element.type() == elementType, elements)) if elements else None
    def nodes(self):
        return self.__elementsOfType('node')
    def ways(self):
        return self.__elementsOfType('way')
    def relations(self):
        return self.__elementsOfType('relation')
    def areas(self):
        return self.__elementsOfType('area')
    
    ### counting elements
    def __count(self, key, elements):
        es = self.__get('elements')
        if len(es) != 1 or 'type' not in es[0] or es[0]['type'] != 'count' or 'tags' not in es[0] or key not in es[0]['tags']:
            return len(elements) if elements is not None else None
        else:
            return int(es[0]['tags'][key])
    def countElements(self):
        return self.__count('total', self.elements())
    def countNodes(self):
        return self.__count('nodes', self.nodes())
    def countWays(self):
        return self.__count('ways', self.ways())
    def countRelations(self):
        return self.__count('relations', self.relations())
    def countAreas(self):
        return self.__count('areas', self.areas())
