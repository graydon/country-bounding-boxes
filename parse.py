#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shapefile
import urllib2
from zipfile import ZipFile

fn = 'ne_50m_admin_0_map_subunits.zip'

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


def extract_data():
    sf = shapefile.Reader(fn.replace(".zip", ".shp"))
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
        box = str.format("({}, {}, {}, {})", *shapes[i].bbox)
        fs = ','.join([str.format('\n        {}={}', k, fmt(v))
                       for (k, v) in zip(fields, rec)])
        print('    Country(')
        print('        bbox=' + box + ',' + fs + '),')
    print(']')

if __name__ == "__main__":
    #download_shapefile()
    #extract_shapefile()
    extract_data()
