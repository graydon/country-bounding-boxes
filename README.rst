Contains the bounding boxes and miscallaneous additional information for countries
extracted from 

http://www.naturalearthdata.com/

Installation
============

::

    $ pip install country-bounding-boxes

Usage
=====

::

    >>> from country_bounding_boxes import (
          get_countries_containing_point,
          get_country_by_iso_code
        )

Get a country by its 2- or 3-letter ISO code::

    >>> get_country_by_iso_code('ZW').name
    "Zimbabwe"
    >>> get_country_by_iso_code('ZWE').name
    "Zimbabwe"
    >>> get_country_by_iso_code('TM').name
    "Turkmenistan"

Inspect bounding box as (lon1, lat1, lon2, lat2) tuples::

    >>> get_country_by_iso_code('TM').bbox
    (52.5024597512, 35.2706639674, 66.5461503437, 42.7515510117)

Get a set of countries by their intersection with a point::

    >>> cs = get_countries_containing_point(lon=-79.888252,
                                            lat=32.819747)
    >>> [c.name for c in cs]
    ['United States']



Development
===========

If you want to do development on the library, follow these steps:

* Create a virtualenv
* bin/pip install -r requirements/tests.txt
* bin/nosetests -s mobile_codes
