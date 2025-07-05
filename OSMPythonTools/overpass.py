from OSMPythonTools.nominatim import NominatimResults, NominatimResult
import datetime as dt
import dateutil.parser
import time
import urllib.parse
import urllib.request

import OSMPythonTools
from OSMPythonTools.element import Element
from OSMPythonTools.internal.cacheObject import CacheObject
from OSMPythonTools.internal.response import Response

def overpassQueryBuilder(area=None, bbox=None, polygon=None, elementType=None, selector=[], conditions=[], since=None, to=None, userid=None, user=None, includeGeometry=False, includeCenter=False, out='body'):
    if not elementType:
        OSMPythonTools._raiseException('overpassQueryBuilder', 'Please provide an elementType')
    if not area and not bbox and not polygon:
        OSMPythonTools._raiseException('overpassQueryBuilder', 'Please provide an area, a bounding box, or a polygon')
    if area and bbox:
        OSMPythonTools._raiseException('overpassQueryBuilder', 'Please do not provide an area and a bounding box')
    if area and polygon:
        OSMPythonTools._raiseException('overpassQueryBuilder', 'Please do not provide an area and a polygon')
    if bbox and polygon:
        OSMPythonTools._raiseException('overpassQueryBuilder', 'Please do not provide a bounding box and a polygon')
    if userid and user:
        OSMPythonTools._raiseException('overpassQueryBuilder', 'Please do only provide one of the following: user ID and username')
    if isinstance(area, str) or isinstance(area, Element) or isinstance(area, NominatimResults) or isinstance(area, NominatimResult):
        area = Element.fromId(area)
        areaId = area.areaId()
    elif isinstance(area, int):
        areaId = area
    else:
        areaId = None
    if not isinstance(elementType, list):
        elementType = [elementType]
    if not isinstance(selector, list):
        selector = [selector]
    if not isinstance(conditions, list):
        conditions = [conditions]
    if userid and not isinstance(userid, list):
        userid = [userid]
    if user and not isinstance(user, list):
        user = [user]
    dateRestriction = '(changed:"' + since + '"' + (',"' + to + '"' if to else '') + ')' if since else ''
    userRestriction = '(uid:' + ','.join(map(str, userid)) + ')' if userid else ''
    userRestriction2 = '(user:' + ','.join(map(lambda u: '"' + u + '"', user)) + ')' if user else ''
    searchArea = '(' + 'area.searchArea' + ')' if areaId else ''
    searchBbox = '(' + ','.join(map(str, bbox)) + ')' if bbox else ''
    searchPolygon = '(poly:"' + ' '.join([f'{lat} {lon}' for [lat, lon] in polygon]) + '")' if polygon else ''
    conditions = '(if: ' + ' && '.join(map(str, conditions)) + ')' if conditions else ''
    query = ('area(' + str(areaId) + ')->.searchArea;(') if areaId else '('
    for e in elementType:
        query += e + ''.join(map(lambda x: '[' + x + ']', selector)) + conditions + dateRestriction + userRestriction + userRestriction2 + searchArea + searchBbox + searchPolygon + ';'
    if isinstance(out, str):
        out = [out]
    if includeCenter:
        out.insert(0, 'center')
    out = '; '.join(map(lambda o: 'out ' + o, out))
    query += '); ' + out + (' geom' if includeGeometry and 'geom' not in [o.strip() for o in out.split()] else '') + ';'
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

    def _rawToResult(self, data, queryString, params, kwargs, cacheMetadata=None, shallow=False):
        return OverpassResult(data, queryString, params, cacheMetadata=cacheMetadata)

    def _isValid(self, result):
        return result.isValid()

    def _waitForReady(self):
        try:
            state = {
                'haveWaited': False,
            }
            while True:
                # get the status string
                response = urllib.request.urlopen(urllib.request.Request(self._endpoint + 'status', headers= {'User-Agent': self._userAgent()}))
                encoding = response.info().get_content_charset('utf-8')
                statusString = response.read().decode(encoding).split('\n')
                # initialize the waiting time detection
                state['waitTo'] = None
                state['currentTime'] = None
                def wait(state):
                    if state['waitTo'] is not None and state['currentTime'] is not None:
                        sec = min((state['waitTo'] - state['currentTime']).total_seconds(), 10.)
                        if sec > 0:
                            OSMPythonTools.logger.info('[' + self._prefix + '] waiting for ' + str(sec) + (' more' if state['haveWaited'] else '') + ' seconds')
                            time.sleep(sec)
                            state['haveWaited'] = True
                        return True
                    return False
                # iterate through the lines of the status string
                for line in statusString:
                    if line == 'Rate limit: 0':
                        return True
                    if line.endswith('slots available now.'):
                        if state['haveWaited']:
                            OSMPythonTools.logger.info('[' + self._prefix + '] start processing')
                        return True
                    if line.startswith('Current time:'):
                        state['currentTime'] = dt.datetime.strptime(line.split(' ')[-1], '%Y-%m-%dT%H:%M:%SZ')
                        if wait(state):
                            break
                    if line.startswith('Slot available after:'):
                        state['waitTo'] = dt.datetime.strptime(line.split(': ')[-1].split(',')[0], '%Y-%m-%dT%H:%M:%SZ')
                        if wait(state):
                            break
        except:
            raise(Exception('[' + self._prefix + '] could not fetch or interpret status of the endpoint'))

class OverpassResult(Response):
    def __init__(self, json, queryString, params, cacheMetadata=None):
        self._json = json
        self._elements = list(map(lambda e: Element(json=e), self.__get('elements')))
        self._queryString = queryString
        super().__init__(cacheMetadata)

    def isValid(self):
        remark = self.remark()
        if remark and remark.find('timed out'):
            OSMPythonTools.logger.exception('Exception: [overpass] ' + remark)
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
        return dateutil.parser.isoparse(self.__get2('osm3s', 'timestamp_osm_base'))
    def timestamp_area_base(self):
        return dateutil.parser.isoparse(self.__get2('osm3s', 'timestamp_area_base'))
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
