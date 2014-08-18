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
    if not isinstance(code, basestring):
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


# Discrepancies / missing units from the naturalearth data set
def adjust_countries():

    new_subunits = []

    for (i, c) in enumerate(countries):

        # Adjust Madeira bounding box to include to the island of Porto Santo
        # by adding 1 degree to edges.
        if c.gu_a3 == "PMD":
            countries[i] = c._replace(bbox=(-17.3, 32.4, -16.25, 33.15))

        # Add a subunit to Italy for the Pelagie Islands based on Pantelleria
        # (an adjacent island with similar relationship to the Italian
        # mainland). The Pelagie Islands are administered by the province of
        # Agrigento (AG).
        elif c.subunit == "Pantelleria":
            n = c._replace(bbox=(12.315, 35.487, 12.893, 35.885),
                           subunit="Pelagie Islands",
                           name="Pelagie Islands",
                           name_long="Pelagie Islands",
                           brk_name="Pelagie Islands",
                           su_a3="IAG",
                           brk_a3="IAG",
                           abbrev="Pel.",
                           postal="",   # No idea what to put for 'postal'
                           pop_est=6066.0,
                           gdp_md_est=-99.0,
                           lastcensus=2004,
                           name_len=15.0,
                           long_len=15.0,
                           abbrev_len=4.0)
            new_subunits.append(n)

        # Add a subunit for Tuvalu based on Kiribati (the island it used to be
        # part of, as the Ellice Islands).
        elif c.subunit == "Kiribati":
            n = c._replace(bbox=(176.7, -12.7, 180.0, -5.4),
                           sovereignt="Tuvalu",
                           sov_a3="TUV",
                           admin="Tuvalu",
                           adm0_a3="TUV",
                           geounit="Tuvalu",
                           gu_a3="TUV",
                           subunit="Tuvalu",
                           su_a3="TUV",
                           name="Tuvalu",
                           name_long="Tuvalu",
                           brk_a3="TUV",
                           brk_name="Tuvalu",
                           abbrev="Tuvalu",
                           postal="TV",
                           formal_en="Tuvalu",
                           name_sort="Tuvalu",
                           pop_est=10837.0,
                           gdp_md_est=3400.0,
                           lastcensus=2012.0,
                           iso_a2="TV",
                           iso_a3="TUV",
                           iso_n3="789",
                           un_a3="789",
                           wb_a2="TV",
                           wb_a3="TUV",
                           adm0_a3_is="TUV",
                           adm0_a3_us="TUV",
                           name_len=6.0,
                           long_len=6.0,
                           abbrev_len=6.0)
            new_subunits.append(n)

        # Add a subunit for the Archipelago of San Andrés, Providencia and
        # Santa Catalina, based on Colombia. The achipelago has (as far as
        # I can tell) no international status beyond "department of Colombia";
        # no ISO code of its own or anything.
        elif c.subunit == "Colombia":
            n = c._replace(bbox=(-82.39, 11.16, -79.60, 15.33),
                           pop_est=75167,
                           formal_en=("Department of San Andrés"
                                      + " and Providencia"))
            new_subunits.append(n)

        # Add a subunit for Gibraltar, based on the British Virgin Islands
        # (another similarly-populated "overseas territory" of the UK).
        elif c.subunit == "British Virgin Islands":
            n = c._replace(bbox=(-5.368, 36.108618, -5.336, 36.155),
                           pop_est=30001,
                           admin="Gibraltar",
                           adm0_a3="GIB",
                           geounit="Gibraltar",
                           gu_a3="GIB",
                           subunit="Gibraltar",
                           su_a3="GIB",
                           name="Gibraltar",
                           name_long="Gibraltar",
                           brk_a3="GIB",
                           brk_name="Gibraltar",
                           abbrev="Gibraltar",
                           postal="GI",
                           formal_en="Gibraltar",
                           name_sort="Gibraltar",
                           gdp_md_est=45834,
                           iso_a2="GI",
                           iso_a3="GIB",
                           iso_n3="292",
                           un_a3="292",
                           adm0_a3_is="GIB",
                           adm0_a3_us="GIB",
                           continent="Europe",
                           region_un="Europe",
                           subregion="Southern Europe",
                           region_wb="Europe & Central Asia",
                           name_len=9.0,
                           long_len=9.0,
                           abbrev_len=9.0)
            new_subunits.append(n)

    countries.extend(new_subunits)


adjust_countries()
