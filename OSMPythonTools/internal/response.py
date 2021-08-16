class Response:
    def __init__(self, cacheMetadata):
        self._cacheMetadata = cacheMetadata
    def __get(self, prop):
        return self._cacheMetadata[prop] if self._cacheMetadata and prop in self._cacheMetadata else None
    def cacheTimestamp(self):
        return self.__get('timestamp')
    def cacheVersion(self):
        return self.__get('version')
