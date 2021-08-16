from OSMPythonTools.cachingStrategy import JSON

class CachingStrategy():
    __strategy = JSON()
    @classmethod
    def use(cls, strategy, **kwargs):
        cls.__strategy.close()
        cls.__strategy = strategy(**kwargs)
        return cls.__strategy
    @classmethod
    def get(cls, key):
        return cls.__strategy.get(key)
    @classmethod
    def set(cls, key, value):
        cls.__strategy.set(key, value)
