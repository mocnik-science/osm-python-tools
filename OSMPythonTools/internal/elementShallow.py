from OSMPythonTools.internal.response import Response

class ElementShallow(Response):
    def __init__(self, cacheMetadata):
        super().__init__(cacheMetadata)
    def type(self):
        return None
    def id(self):
        return None
    def typeId(self):
        return self.type() + '/' + str(self.id()) if self.type() != None and self.id() != None else None
    def typeIdShort(self):
        return self.type()[0] + str(self.id()) if self.type() != None and self.id() != None else None
    def areaId(self):
        return self._areaId(self.type(), self.id())
    def _areaId(self, type, id):
        if type == 'way':
            return id + 2400000000
        elif type == 'relation':
            return id + 3600000000
        else:
            return None
