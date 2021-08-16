import os.path
import ujson

from OSMPythonTools.cachingStrategy.base import CachingStrategyBase

class JSON(CachingStrategyBase):
    def __init__(self, cacheDir='cache'):
        self._cacheDir = cacheDir

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

    def set(self, key, value):
        with open(self._filename(key), 'w') as file:
            ujson.dump(value, file)
