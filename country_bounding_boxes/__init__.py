#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import iso3166
import json
from country_bounding_boxes.generated import countries


# The naturalearth dataset we're using contains "subunits" of a variety of
# forms; Some are "full sized" countries, some are historically or
# politically significant divisions within the country (eg. Scotland and
# Wales in the UK), some are physically disjoint components of countries
# (eg. Alaska) and some are islands, dependencies, overseas departments,
# or similar special cases. As a result, we return a _set_ of countries
# for each iso code.
_iso_2_cache = {}
_iso_3_cache = {}


# The legitimate ISO 3166 alpha2 and alpha3 names, which appear in a variety
# of contexts in the naturalearth dataset depending on the subunit being
# described.
_iso_2_names = set()
_iso_3_names = set()


def _is_iso_3_name(n):
    if len(_iso_3_names) == 0:
        for c in iso3166.countries:
            _iso_3_names.add(c.alpha3)
    return n in _iso_3_names


def _is_iso_2_name(n):
    if len(_iso_2_names) == 0:
        for c in iso3166.countries:
            _iso_2_names.add(c.alpha2)
    return n in _iso_2_names


# Depending on the type of the (sub)unit, the ISO alpha3 name this
# "country" is connected to might be denoted in a variety of fields. Search
# them all in a hopefully-useful order of precedence and take the first
# that looks legit.
def _best_guess_iso_3(c):
    for n in [c.iso_a3, c.adm0_a3, c.adm0_a3_is,
              c.adm0_a3_us, c.gu_a3, c.su_a3, c.sov_a3]:
        if n != "-99" and _is_iso_3_name(n):
            return n
    return None


# ISO alpha3 names are much more prevalent in the NE dataset; look up the
# corresponding alpha2 name from iso3166 and cross-check against any alpha2
# name we have in the NE record.
def _best_guess_iso_2(c):
    iso3 = _best_guess_iso_3(c)
    if iso3 is None:
        return None
    isoc = iso3166.countries.get(iso3)
    if isoc is None:
        return None
    iso2 = isoc.alpha2
    if c.iso_a2 != "-99" and _is_iso_2_name(c.iso_a2):
        assert c.iso_a2 == iso2
    return iso2


def _ensure_caches_populated():
    global _iso_2_cache
    global _iso_3_cache
    if not _iso_2_cache:
        for c in countries:
            iso2 = _best_guess_iso_2(c)
            iso3 = _best_guess_iso_3(c)
            if iso2 not in _iso_2_cache:
                _iso_2_cache[iso2] = set()
            if iso3 not in _iso_3_cache:
                _iso_3_cache[iso3] = set()
            _iso_2_cache[iso2].add(c)
            _iso_3_cache[iso3].add(c)


def country_subunits_containing_point(lon, lat):
    """
    Iterate over the country subunits that contain the provided point.
    Each subunit will have a .bbox field indicating its (lon1, lat1, lon2,
    lat2) bounding box.

    """
    res = []
    for c in countries:
        (lon1, lat1, lon2, lat2) = c.bbox

        # To handle international date line spanning
        # bboxes -- namely Fiji -- we treat any country that's
        #
        # Fiji spans the international date line
        # (-180.0, -21.705859375, 180.0, -12.476953125),
        #
        # England does not
        # (-5.65625, 50.0213867188, 1.74658203125, 55.8079589844),
        #
        # This poses a bit of difficulty, because they both appear
        # "numerically" the same way, as a bounding box going from low
        # longitude to high longitude. The problem is that passing the
        # international date line means you should interpret the box
        # as running from high to low

        if lon1 <= lon and lon <= lon2 and \
           lat1 <= lat and lat <= lat2:
            res.append(c)
    return iter(res)


def country_subunits_by_iso_code(code):
    """
    Iterate over all country subunits, some of which are full countries and
    some of which are smaller components thereof; all have a .bbox field
    indicating their (lon1, lat1, lon2, lat2) bounding box.
    """
    if not isinstance(code, str):
        return iter([])
    _ensure_caches_populated()
    code = code.upper()
    if len(code) == 2 and code in _iso_2_cache:
            return iter(_iso_2_cache[code])
    elif len(code) == 3 and code in _iso_3_cache:
            return iter(_iso_3_cache[code])
    return iter([])


def all_country_subunits():
    """
    Iterate over all country subunits, some of which are full countries and
    some of which are smaller components thereof; all have a .bbox field
    indicating their (lon1, lat1, lon2, lat2) bounding box.
    """
    return iter(countries)


def all_country_subunits_grouped_by_iso_3_code():
    """
    Iterate over pairs of strings and sets of country subunits, where the
    string is an ISO 3166 alpha3 country code and the subunits all have a
    .bbox field indicating their (lon1, lat1, lon2, lat2) bounding box.
    """
    _ensure_caches_populated()
    return _iso_3_cache.items()


def show_all_bounding_boxes():
    """
    Diagnostic routine to emit all bounding boxes as GeoJSON.
    """
    fs = []

    for c in all_country_subunits():
        (lon1, lat1, lon2, lat2) = c.bbox
        fs.append(dict(type="Feature",
                       properties=[],
                       geometry=dict(type="Polygon",
                                     coordinates=[[
                                         [lon1, lat1],
                                         [lon1, lat2],
                                         [lon2, lat2],
                                         [lon2, lat1],
                                         [lon1, lat1]
                                     ]])))

    fc = dict(type="FeatureCollection",
              features=fs)

    print json.dumps(fc, indent=True)
