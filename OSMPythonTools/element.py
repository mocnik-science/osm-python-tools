import sys

class SingletonApi():
    __instance = None
    def __init__(self, *args, **kwargs):
        from OSMPythonTools.api import Api
        if not SingletonApi.__instance:
            SingletonApi.__instance = Api(*args, **kwargs)
    def __getattr__(self, name):
        return getattr(self.__instance, name)

class Element:
    def __init__(self, json=None, soup=None):
        self._json = json
        self._soup = soup

    def __getElement(self, prop):
        if self._json is not None:
            return self._json[prop] if prop in self._json else None
        return self._soup[prop] if self._isValid and prop in self._soup.attrs else None

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
    
    ### nodes
    def __nodes(self):
        return self.__getElement('nodes') if self._json is not None else self._soup.find_all('nd')
    def nodes(self):
        nodes = self.__nodes()
        if nodes is None or len(nodes) == 0:
            return []
        api = SingletonApi()
        return list(map(lambda n: api.query('node/' + str(n if self._json is not None else n['ref'])), nodes))
    def countNodes(self):
        nodes = self.__nodes()
        return len(nodes) if nodes is not None else None
    
    ### members
    def __members(self):
        return self.__getElement('members') if self._json is not None else self._soup.find_all('member')
    def members(self):
        members = self.__members()
        if members is None or len(members) == 0:
            return []
        api = SingletonApi()
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
