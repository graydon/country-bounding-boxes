#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shapefile
import urllib2
import os.path
from zipfile import ZipFile

fn = 'ne_50m_admin_0_map_subunits.zip'
sh_fn = fn.replace(".zip", ".shp")

# Yes, this URL is as weird as it looks. They put the protocol and
# hostname in there twice. Maybe it's a bug and they're going to
# fix it someday; for the time being it's required to fetch.


url = ('http://www.naturalearthdata.com/' +
       'http//www.naturalearthdata.com/download/50m/cultural/' + fn)


def download_shapefile():
    f = urllib2.urlopen(url)
    data = f.read()
    with open(fn, "wb") as out:
        out.write(data)


def extract_shapefile():
    with ZipFile(fn) as z:
        z.extractall()


def fmt(x):
    if isinstance(x, str):
        return '"' + x.decode("latin-1").encode("utf8").strip() + '"'
    else:
        return repr(x)


def emit_country(bbox, fields, rec):
    box = str.format("({}, {}, {}, {})", *bbox)
    fs = ','.join([str.format('\n        {}={}', k, fmt(v))
                   for (k, v) in zip(fields, rec)])
    print('    Country(')
    print('        bbox=' + box + ',' + fs + '),')


def extract_data():
    sf = shapefile.Reader(sh_fn)
    fields = [f[0] for f in sf.fields if isinstance(f, list)]

    print("#!/usr/bin/env python")
    print("# -*- coding: utf-8 -*-")
    print("#")
    print("# extracted from " + url)
    print("# under public domain terms")
    print("")
    print("from collections import namedtuple")
    print("")
    print("Country = namedtuple('Country', [")
    print("    'bbox'," +
          ','.join([str.format("\n    '{}'", f) for f in fields]) + "])")

    shapes = sf.shapes()
    records = sf.records()

    assert len(shapes) == len(records)

    print("countries = [")
    for i in range(0, len(records)):
        rec = records[i]

        if "Kingdom of the Netherlands" in rec:

            # The NaturalEarth data is incorrect in the bounding box for
            # the Netherlands; it includes the extent of the Caribbean
            # Netherlands by accident. Correct that here.
            bbox = [3.133, 50.750, 7.217, 53.683]
            emit_country(bbox, fields, rec)

        elif abs(shapes[i].bbox[0] - shapes[i].bbox[2]) > 340:

            # This is a bbox that's more than 340 degrees long. It's very
            # likely a misinterpretation of facts: namely a much smaller
            # logical region that happens to have points on both sides of
            # the 180th meridian, the international date line.
            #
            # We treat this specially by splitting the shape in two, one
            # piece holding all the points in [-180.0, 0), and one piece
            # holding all the points in [0, 180.0]. We then emit two
            # country-subunits.
            #
            # There does not appear to be a better "standard" way to fix
            # this.  If we do not make this adjustment, we wind up emitting
            # a box that wraps all the way around the world, because the
            # "minimum" lon was -180 and the "maximum" lon was 180 in the
            # point-set.

            pts = shapes[i].points
            lo_pts = [p for p in pts if p[0] < 0]
            hi_pts = [p for p in pts if p[0] >= 0]
            lo_box = [
                min([p[0] for p in lo_pts]), min([p[1] for p in lo_pts]),
                max([p[0] for p in lo_pts]), max([p[1] for p in lo_pts])
            ]

            hi_box = [
                min([p[0] for p in hi_pts]), min([p[1] for p in hi_pts]),
                max([p[0] for p in hi_pts]), max([p[1] for p in hi_pts])
            ]

            print('    # Splitting antimeridian-spanning bbox')
            print(str.format('    # [{}, {}, {}, {}]', *shapes[i].bbox))
            print('    # into')
            print(str.format('    # [{}, {}, {}, {}]', *lo_box))
            print(str.format('    # [{}, {}, {}, {}]', *hi_box))

            emit_country(lo_box, fields, rec)
            emit_country(hi_box, fields, rec)

        else:
            emit_country(shapes[i].bbox, fields, rec)

    print(']')

if __name__ == "__main__":
    if not os.path.exists(fn):
        download_shapefile()
    if not os.path.exists(sh_fn):
        extract_shapefile()
    extract_data()
