import os.path
import pickle
import gzip as libraryGzip

from OSMPythonTools.cachingStrategy.strategy import CachingStrategy

class CachingStrategyPickle(CachingStrategy):
    _instance = None

    def __init__(self, cacheDir='cache'):
        raise RuntimeError('Call instance() instead')

    @classmethod
    def instance(cls, cacheFile='cache', gzip=True):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
        cls._instance.close()
        cls._instance._cacheFileRaw = cacheFile
        cls._instance.useGzip(gzip)
        return cls._instance

    def useGzip(self, gzip=True):
        if self._cache is not None:
            self._instance.close()
        self._instance._cacheFile = self._cacheFileRaw + '.pickle' + ('.gzip' if gzip else '')
        self._instance._open = libraryGzip.open if gzip else open
        return self

    def get(self, key):
        if self._cache is None:
            self.open()
        return self._cache[key] if key in self._cache else None

    def set(self, key, data):
        if self._cache is None:
            self.open()
        with self._open(self._cacheFile, 'wb') as file:
            pickle.dump((key, data), file)
        self._cache[key] = data

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
