#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from country_bounding_boxes.generated import countries


_iso_2_cache = {}


_iso_3_cache = {}


def get_countries_containing_point(lon, lat):
    res = []
    for c in countries:
        (lon1, lat1, lon2, lat2) = c.bbox
        if lon1 <= lon and lon <= lon2 and \
           lat1 <= lat and lat <= lat2:
            res.append(c)
    return res


def get_country_by_iso_code(code):

    if not isinstance(code, str):
        return None

    # lazily populate cache
    if len(_iso_2_cache) == 0:
        for c in countries:
            _iso_2_cache[c.iso_a2] = c
            _iso_3_cache[c.iso_a3] = c

    code = code.upper()

    if len(code) == 2 and code in _iso_2_cache:
            return _iso_2_cache[code]

    elif len(code) == 3 and code in _iso_3_cache:
            return _iso_3_cache[code]

    return None
