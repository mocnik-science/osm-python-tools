class SingletonApi():
    __instance = None
    def __init__(self, *args, **kwargs):
        from OSMPythonTools.api import Api
        if not SingletonApi.__instance:
            SingletonApi.__instance = Api(*args, **kwargs)
    def __getattr__(self, name):
        return getattr(self.__instance, name)
