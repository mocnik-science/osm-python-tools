[back to readme](../../)

# Version History

Observe that some of the following versions include breaking changes:

## Version v0.3.3

* [feature] access to history
* [feature] caching strategies introduced
* [feature] caching strategy `CachingStrategyPickle`
* [improvement] dependencies for testing are now only installed on request
* [improvement; breaking change] timestamps are now returned as objects
* [bug] metadata did not work for Api queries
* [minor bug] version was not returned as an integer
* [minor bug] the method to access the Api version was overwritten by the method to access the element version
