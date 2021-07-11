import copy
import geojson
import re

import OSMPythonTools
from OSMPythonTools.internal.singletonApi import SingletonApi
from OSMPythonTools.internal.elementShallow import ElementShallow

def _extendAndRaiseException(e, msg):
    msgComplete = str(e) + msg
    OSMPythonTools.logger.exception(msgComplete)
    raise(Exception(msgComplete))

class Element(ElementShallow):
    def __init__(self, json=None, soup=None, shallow=False):
        self._json = json
        self._soup = soup
        self._shallow = shallow
    
    @staticmethod
    def fromId(idToParse):
        if isinstance(idToParse, Element):
            return idToParse
        if isinstance(idToParse, ElementShallow):
            idToParse = idToParse.typeId()
        if idToParse is None:
            Element._raiseException(None, 'Could not parse element. Please make sure that your node, way, or relation ID is formatted properly: \'node/***\', \'node ***\', \'n***\', \'way/***\', \'way ***\', \'w***\', or \'relation/***\', \'relation ***\', or \'r***\'')
        idToParse = idToParse.strip().lower()
        type = None
        if idToParse[0].lower() == 'n':
            type = 'node'
        elif idToParse[0].lower() == 'w':
            type = 'way'
        elif idToParse[0].lower() == 'r':
            type = 'relation'
        else:
            Element._raiseException(None, 'Could not parse element type. Please make sure that your node, way, or relation ID is formatted properly: \'node/***\', \'node ***\', \'n***\', \'way/***\', \'way ***\', \'w***\', or \'relation/***\', \'relation ***\', or \'r***\'')
        idToParse = re.sub('[^0-9]', '', idToParse)
        if len(idToParse) > 0:
            id = int(idToParse)
        else:
            Element._raiseException(None, 'Could not parse element ID. Please make sure that your node, way, or relation ID is formatted properly: \'node/***\', \'node ***\', \'n***\', \'way/***\', \'way ***\', \'w***\', or \'relation/***\', \'relation ***\', or \'r***\'')
        return Element(json={'type': type, 'id': id}, shallow=True)

    def _raiseException(self, msg):
        OSMPythonTools._raiseException('Element', msg)

    def __getElement(self, prop):
        if self._shallow and prop not in ['type', 'id']:
            self._unshallow()
            self._shallow = False
        if self._json is not None:
            return self._json[prop] if prop in self._json else None
        return self._soup[prop] if self._isValid and prop in self._soup.attrs else None

    def _unshallow(self):
        raise(NotImplementedError('Subclass should implement _unshallow'))

    ### properties
    def type(self):
        if self._json is not None:
            return self.__getElement('type')
        return self._soup.name if self._isValid else None
    def id(self):
        return int(self.__getElement('id'))
    def visible(self):
        return self.__getElement('visible')
    def version(self):
        return self.__getElement('version')
    def changeset(self):
        return self.__getElement('changeset')
    def timestamp(self):
        return self.__getElement('timestamp')
    def user(self):
        return self.__getElement('user')
    def uid(self):
        return self.__getElement('uid')
    def userid(self):
        return self.__getElement('uid')
    def lat(self):
        return float(self.__getElement('lat')) if self.__getElement('lat') else None
    def lon(self):
        return float(self.__getElement('lon')) if self.__getElement('lon') else None
    def geometry(self):
        return self.geometry()
    def centerLat(self):
        return float(self.__getElement('center')['lat']) if self.__getElement('center') else None
    def centerLon(self):
        return float(self.__getElement('center')['lon']) if self.__getElement('center') else None

    ### nodes
    def __nodes(self):
        return self.__getElement('nodes') if self._json is not None else self._soup.find_all('nd')
    def nodes(self, shallow=True):
        nodes = self.__nodes()
        if nodes is None or len(nodes) == 0:
            return []
        api = SingletonApi()
        if shallow:
            return list(map(lambda n: api.query('node/' + str(n if self._json is not None else n['ref']), shallow='''
<?xml version="1.0" encoding="UTF-8"?>
<osm>
    <node id="''' + str(n if self._json is not None else n['ref']) + '''"/>
</osm>
            '''), nodes))
        else:
            return list(map(lambda n: api.query('node/' + str(n if self._json is not None else n['ref'])), nodes))
    def countNodes(self):
        nodes = self.__nodes()
        return len(nodes) if nodes is not None else None
    
    ### members
    def __members(self):
        return self.__getElement('members') if self._json is not None else self._soup.find_all('member')
    def members(self, shallow=True):
        members = self.__members()
        if members is None or len(members) == 0:
            return []
        api = SingletonApi()
        if shallow:
            return list(map(lambda m: api.query(m['type'] + '/' + str(m['ref']), shallow='''
<?xml version="1.0" encoding="UTF-8"?>
<osm>
    <''' + m['type'] + ''' id="''' + str(m['ref']) + '''"/>
</osm>
            '''), members))
        else:
            return list(map(lambda m: api.query(m['type'] + '/' + str(m['ref'])), members))
    def countMembers(self):
        members = self.__members()
        return len(members) if members is not None else None
    
    ### tags
    def tags(self):
        if self._json is not None:
            return self.__getElement('tags')
        return dict(map(lambda t: (t['k'], t['v']), self._soup.find_all('tag') if self._isValid else []))
    def tag(self, key):
        tags = self.tags()
        return tags[key] if key in tags else None

    ### geometry
    def geometry(self):
        try:
            if self.type() == 'node':
                if not self.lon() or not self.lat():
                    self._raiseException('Cannot build geometry: geometry information not included.')
                return geojson.Point((self.lon(), self.lat()))
            elif self.type() == 'way':
                if not self.__getElement('geometry'):
                    self._raiseException('Cannot build geometry: geometry information not included.')
                cs = self.__geometry_csToList(self.__getElement('geometry'))
                if self.__geometry_equal(cs[0], cs[-1]):
                    return geojson.Polygon([cs])
                else:
                    return geojson.LineString(cs)
            elif self.type() == 'relation':
                members = copy.deepcopy(self.__members())
                membersOuter = self.__geometry_extract(members, 'outer')
                if len(membersOuter) == 0:
                    self._raiseException('Cannot build geometry: no outer rings found.')
                membersInner = self.__geometry_extract(members, 'inner')
                ringsOuter = self.__geometry_buildRings(membersOuter)
                ringsInner = self.__geometry_buildRings(membersInner)
                ringsOuter = self.__geometry_orientRings(ringsOuter, positive=True)
                ringsInner = self.__geometry_orientRings(ringsInner, positive=False)
                polygons = self.__geometry_buildPolygons(ringsOuter, ringsInner)
                if len(polygons) > 1:
                    return geojson.MultiPolygon(polygons)
                else:
                    return geojson.Polygon(polygons[0])
            else:
                self._raiseException('Cannot build geometry: type of element unknown.')
        except Exception as e:
            _extendAndRaiseException(e, ' ({}/{})'.format(self.type(), self.id()))
    def __geometry_equal(self, x, y):
        return x[0] == y[0] and x[1] == y[1]
    def __geometry_pointInsidePolygon(self, p, polygon):
        x = p[0]
        y = p[1]
        inside = False
        n = len(polygon)
        px, py = polygon[0]
        for i in range(n + 1):
            qx, qy = polygon[i % n]
            if y > min(py, qy):
                if y <= max(py, qy):
                    if x <= max(px, qx):
                        if py != qy:
                            xintersect = (y - py) * (qx - px) / (qy - py) + px
                        if px == qx or x <= xintersect:
                            inside = not inside
            px, py = qx, qy
        return inside
    def __geometry_polygonPositiveOriented(self, polygon):
        signedArea = 0
        n = len(polygon)
        px, py = polygon[0]
        for i in range(n + 1):
            qx, qy = polygon[i % n]
            signedArea += px * qy - qx * py
        signedArea = signedArea / 2
        return signedArea > 0
    def __geometry_orientRings(self, rings, positive=True):
        return [list(reversed(r)) if positive ^ self.__geometry_polygonPositiveOriented(r) else r for r in rings]
    def __geometry_csToList(self, cs):
        return [(c['lon'], c['lat']) for c in cs]
    def __geometry_extract(self, members, role):
        extracted = []
        for m in members:
            if m['role'] == role:
                if 'geometry' in m:
                    extracted.append(self.__geometry_csToList(m['geometry']))
                else:
                    self._raiseException('Cannot build geometry: relation in relation not supported.')
        return extracted
    def __geometry_buildRings(self, members):
        rings = []
        r = []
        while len(members) > 0:
            if not r:
                r.extend(members.pop())
            if len(r) > 3 and self.__geometry_equal(r[0], r[-1]):
                rings.append(r)
                r = []
            else:
                found = False
                for i, m in enumerate(members):
                    if self.__geometry_equal(r[-1], m[0]):
                        found = True
                    elif self.__geometry_equal(r[-1], m[-1]):
                        found = True
                        m.reverse()
                    if found:
                        r.extend(m[1:])
                        del members[i]
                        break
                if not found:
                    self._raiseException('Cannot build geometry: cannot close ring.')
        if len(r) > 3 and self.__geometry_equal(r[0], r[-1]):
            rings.append(r)
        elif r:
            self._raiseException('Cannot build geometry: cannot close ring.')
        return rings
    def __geometry_buildPolygons(self, ringsOuter, ringsInner):
        polygons = []
        for r in ringsOuter:
            polygon = [r]
            ringsInnerTodo = []
            for r2 in ringsInner:
                isInside = False
                for p in r2:
                    if self.__geometry_pointInsidePolygon(p, r):
                        polygon.append(r2)
                        isInside = True
                        break
                if not isInside:
                    ringsInnerTodo.append(r2)
            ringsInner = ringsInnerTodo
            polygons.append(polygon)
        if len(ringsInner) > 0:
            self._raiseException('Cannot build geometry: cannot find outer ring for inner ring.')
        return polygons
