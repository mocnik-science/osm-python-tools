from setuptools import setup

name = 'OSMPythonTools'
version = '0.2.6'
url = 'https://github.com/mocnik-science/osm-python-tools'

with open('./OSMPythonTools/__info__.py', 'w') as f:
    f.write('__name__ = \'%s\'\n' % name)
    f.write('__version__ = \'%s\'\n' % version)
    f.write('__url__ = \'%s\'\n' % url)

setup(
    name = name,
    packages = ['OSMPythonTools', 'OSMPythonTools.internal'],
    install_requires = [
        'beautifulsoup4',
        'geojson',
        'lxml',
        'matplotlib',
        'numpy',
        'pandas',
        'ujson',
        'xarray',
    ],
    version = version,
    author = 'Franz-Benjamin Mocnik',
    author_email = 'mail@mocnik-science.net',
    description = 'A library to access OpenStreetMap related services',
    license = 'GPL-3',
    url = url,
    download_url = '',
    keywords = ['OpenStreetMap', 'OSM', 'service', 'overpass', 'nominatim'],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
    ],
)
