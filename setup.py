from distutils.core import setup
setup(
  name = 'OSMPythonTools',
  packages = ['OSMPythonTools', 'OSMPythonTools.internal'],
  install_requires = [
    'beautifulsoup4',
    'datetime',
    'lxml',
    'matplotlib',
    'numpy',
    'pandas',
    'ujson',
    'xarray',
  ],
  version = '0.1.1',
  author = 'Franz-Benjamin Mocnik',
  author_email = 'mail@mocnik-science.net',
  description = 'A library to access OpenStreetMap related services',
  license = 'GPL-3',
  url = 'https://github.com/mocnik-science/osm-python-tools',
  download_url = '',
  keywords = ['OpenStreetMap', 'OSM', 'service', 'overpass', 'nominatim'],
  classifiers = [
    'Development Status :: 4 - Beta',
    'Programming Language :: Python :: 3',
  ],
)
