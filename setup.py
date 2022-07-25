import setuptools

pkgName='OSMPythonTools'
pkgVersion='0.3.5'
pkgUrl='https://github.com/mocnik-science/osm-python-tools'

with open('./OSMPythonTools/__info__.py', 'w') as f:
    f.write('pkgName = \'%s\'\n' % pkgName)
    f.write('pkgVersion = \'%s\'\n' % pkgVersion)
    f.write('pkgUrl = \'%s\'\n' % pkgUrl)

# see setup.cfg for metadata
setuptools.setup(
    name=pkgName,
    packages=setuptools.find_packages(),
    install_requires=[
        'beautifulsoup4',
        'geojson',
        'lxml',
        'matplotlib',
        'numpy',
        'pandas',
        'ujson',
        'xarray',
    ],
    extras_require={
        'test': [
            'pytest',
            'pytest-sugar',
            'pytest-cov',
        ],
    },
    version=pkgVersion,
    author='Franz-Benjamin Mocnik',
    author_email='mail@mocnik-science.net',
    license='GPL-3',
    url=pkgUrl,
    download_url='',
    keywords=['OpenStreetMap', 'OSM', 'service', 'overpass', 'nominatim'],
)
