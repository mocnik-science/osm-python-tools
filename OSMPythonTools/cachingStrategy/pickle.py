import os.path
import pickle
import gzip as libraryGzip

from OSMPythonTools.cachingStrategy.base import CachingStrategyBase

class Pickle(CachingStrategyBase):
    def __init__(self, cacheFile='cache', gzip=True):
        self._cacheFile = cacheFile + '.pickle' + ('.gzip' if gzip else '')
        self._open = libraryGzip.open if gzip else open
        self.close()

    def get(self, key):
        if self._cache is None:
            self.open()
        return self._cache[key] if key in self._cache else None

    def set(self, key, value):
        if self._cache is None:
            self.open()
        with self._open(self._cacheFile, 'wb') as file:
            pickle.dump((key, value), file)
        self._cache[key] = value

    def open(self):
        if os.path.exists(self._cacheFile):
            with self._open(self._cacheFile, 'rb') as file:
                self._cache = {}
                try:
                    while True:
                        k, v = pickle.load(file)
                        self._cache[k] = v
                except EOFError:
                    pass
        else:
            self._cache = {}

    def close(self):
        self._cache = None
