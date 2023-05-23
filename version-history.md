[back to readme](../../)

# Version History

Please note that versions may include breaking changes.

## Version v0.4.0

* [improvement; breaking change] make data module's dependencies optional, to reduce the number of required packages

## Version v0.3.5

* [improvement] missing geometric information is downloaded when needed
* [bug] package metadata has been updated to match the standard
* [bug] `Api` test did not run not successfully
* [bug] adaption to newer versions of the `Overpass` server
* [improvement] test for the waiting strategy related to the `Overpass` server introduced

## Version v0.3.4

* [bug] areaId was only computed for the first element of a `NominatimResult`, but not for the first element for which it does not vanish

## Version v0.3.3

* [feature] access to history
* [feature] caching strategies introduced
* [feature] caching strategy `CachingStrategyPickle`
* [improvement] dependencies for testing are now only installed on request
* [improvement; breaking change] timestamps are now returned as objects
* [bug] metadata did not work for Api queries
* [minor bug] version was not returned as an integer
* [minor bug] the method to access the `Api` version was overwritten by the method to access the element version

Breaking changes:

* The constructors of the classes `Api`, `Nominatim`, and `Overpass` do not accept the paramter `cacheDir` any longer.  Instead, the parameter needs to be provided to the method `CachingStrategy.use`.
