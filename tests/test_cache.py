import pytest

from OSMPythonTools.api import Api
from OSMPythonTools.cachingStrategy import CachingStrategy, JSON, Pickle

@pytest.mark.parametrize(('cachingStrategyF'), [
  lambda: CachingStrategy.use(JSON),
  lambda: CachingStrategy.use(Pickle),
  lambda: CachingStrategy.use(Pickle, gzip=False),
])
def test_cache(cachingStrategyF):
  cachingStrategy = cachingStrategyF()
  api = Api()
  x = api.query('node/42467507')
  y = api.query('node/42467507')
  cachingStrategy.close()
  api = Api()
  z = api.query('node/42467507')
  for a in [x, y, z]:
    assert a.version() >= 5
    assert float(a.cacheVersion()) >= 1
  assert x.cacheTimestamp() == y.cacheTimestamp()
  assert x.cacheTimestamp() == z.cacheTimestamp()
  CachingStrategy.use(JSON)
