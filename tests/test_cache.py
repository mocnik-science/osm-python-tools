import pytest

from OSMPythonTools.api import Api
from OSMPythonTools.cachingStrategy import CachingStrategyJSON, CachingStrategyPickle

@pytest.mark.parametrize(('cachingStrategy'), [CachingStrategyJSON.instance(), CachingStrategyPickle.instance(), CachingStrategyPickle.instance(gzip=False)])
def test_cache(cachingStrategy):
  api = Api(cachingStrategy=cachingStrategy)
  x = api.query('node/42467507')
  y = api.query('node/42467507')
  cachingStrategy.close()
  api = Api(cachingStrategy=cachingStrategy)
  z = api.query('node/42467507')
  for a in [x, y, z]:
    assert a.version() >= 5
    assert float(a.cacheVersion()) >= 1
  assert x.cacheTimestamp() == y.cacheTimestamp()
  assert x.cacheTimestamp() == z.cacheTimestamp()
