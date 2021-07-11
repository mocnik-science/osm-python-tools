import setuptools

pkgName='OSMPythonTools'
pkgVersion='0.3.1'
pkgUrl='https://github.com/mocnik-science/osm-python-tools'

with open('./OSMPythonTools/__info__.py', 'w') as f:
    f.write('pkgName = \'%s\'\n' % pkgName)
    f.write('pkgVersion = \'%s\'\n' % pkgVersion)
    f.write('pkgUrl = \'%s\'\n' % pkgUrl)

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
        'pytest',
        'pytest-sugar',
        'ujson',
        'xarray',
    ],
    version=pkgVersion,
    author='Franz-Benjamin Mocnik',
    author_email='mail@mocnik-science.net',
    description='A library to access OpenStreetMap related services',
    license='GPL-3',
    url=pkgUrl,
    download_url='',
    keywords=['OpenStreetMap', 'OSM', 'service', 'overpass', 'nominatim'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
    ],
)
