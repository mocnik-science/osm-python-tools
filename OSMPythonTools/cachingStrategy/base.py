class CachingStrategyBase:
    def __init__(self):
        pass

    def get(self, key):
        raise(NotImplementedError('Subclass should implement get'))

    def set(self, key, data):
        raise(NotImplementedError('Subclass should implement set'))

    def close(self):
        pass
