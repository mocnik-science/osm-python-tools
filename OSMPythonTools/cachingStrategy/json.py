import os.path
import ujson

from OSMPythonTools.cachingStrategy.strategy import CachingStrategy

class CachingStrategyJSON(CachingStrategy):
    _instance = None

    def __init__(self, cacheDir='cache'):
        raise RuntimeError('Call instance() instead')

    @classmethod
    def instance(cls, cacheDir='cache'):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
        else:
            cls._instance.close()
        cls._instance._cacheDir = cacheDir
        return cls._instance

    def _filename(self, key):
        return os.path.join(self._cacheDir, key)

    def get(self, key):
        filename = self._filename(key)
        data = None
        if not os.path.exists(self._cacheDir):
            os.makedirs(self._cacheDir)
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                data = ujson.load(file)
        return data

    def set(self, key, data):
        with open(self._filename(key), 'w') as file:
            ujson.dump(data, file)
