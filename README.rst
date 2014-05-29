Contains the bounding boxes and miscallaneous additional information for
countries extracted from

http://www.naturalearthdata.com/

Note that many countries have a number of "subunits": geographically
disjoint components like Alaska in the USA, administratively distinct
regions such as the countries of Great Britain, or overseas islands for
many European nations. As a result this module returns *iterators* over
sets of Country objects for each country code, rather than single Country
objects.

Previous versions of this library returned an (often large) singular
bounding box for each country code; in many cases these spanned much of the
globe and were therefore geographically less useful.


Installation
============

::

    $ pip install country-bounding-boxes

Usage
=====

::

    >>> from country_bounding_boxes import (
          country_subunits_containing_point,
          country_subunits_by_iso_code
        )

Get a country by its 2- or 3-letter ISO code::

    >>> [c.name for c in country_subunits_by_iso_code('ZW')]
    ['Zimbabwe']

    >>> [c.name for c in country_subunits_by_iso_code('ZWE')]
    ['Zimbabwe']

    >>> [c.name for c in country_subunits_by_iso_code('TM')]
    ['Turkmenistan']

    >>> [c.name for c in country_subunits_by_iso_code('GB')]
    ['Wales', 'England', 'N. Ireland', 'Scotland']

Inspect bounding box as (lon1, lat1, lon2, lat2) tuples::

    >>> [c.bbox for c in country_subunits_by_iso_code('TM')]
    [(52.5024597512, 35.2706639674, 66.5461503437, 42.7515510117)]

    >>> [c.bbox for c in country_subunits_by_iso_code('GB')]
    [(-5.2623046875, 51.3904296875, -2.6623046875, 53.4192871094),
     (-5.65625, 50.0213867188, 1.74658203125, 55.8079589844),
     (-8.14482421875, 54.0512695312, -5.47041015625, 55.241796875),
     (-7.54296875, 54.689453125, -0.774267578125, 60.8318847656)]

Get a set of countries by their intersection with a point::

    >>> [c.name for c in
         country_subunits_containing_point(lon=-79.888252,
                                           lat=32.819747)]
    ['U.S.A.']

    >>> [c.name for c in
         country_subunits_containing_point(lon=5.983333,
                                           lat=50.883333)]
    ['Germany', 'France', 'Netherlands']

Development
===========

If you want to do development on the library, follow these steps:

* Create a virtualenv
* bin/pip install -r requirements/tests.txt
* bin/nosetests -s country_bounding_boxes
