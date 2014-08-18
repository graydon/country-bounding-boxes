from unittest import TestCase

from country_bounding_boxes import (
    country_subunits_containing_point as by_point,
    country_subunits_by_iso_code as by_code,
)


def code_to_names(code):
    bc = by_code(code)
    print(repr(bc))
    return sorted([c.name for c in bc])


def point_to_names(lon, lat):
    return sorted([c.name for c in by_point(lon, lat)])


class TestCountries(TestCase):

    def test_codes(self):
        self.assertEqual(code_to_names('AF'), ['Afghanistan'])
        self.assertEqual(code_to_names('AFG'), ['Afghanistan'])

    def test_codes_2(self):
        self.assertEqual(code_to_names('ZW'), ['Zimbabwe'])
        self.assertEqual(code_to_names('ZWE'), ['Zimbabwe'])

    def test_codes_case(self):
        italy = ['Italy', 'Pantelleria', 'Pelagie Islands',
                 'Sardinia', 'Sicily']
        self.assertEqual(code_to_names('it'), italy)
        self.assertEqual(code_to_names('iTa'), italy)

    def test_codes_case_2(self):
        self.assertEqual(code_to_names('Tm'), ['Turkmenistan'])
        self.assertEqual(code_to_names('Tkm'), ['Turkmenistan'])

    def test_codes_missing(self):
        self.assertEqual(code_to_names('ZZ'), [])
        self.assertEqual(code_to_names('LFQ'), [])

    def test_codes_wrong_type(self):
        self.assertEqual(code_to_names(None), [])
        self.assertEqual(code_to_names(1.2), [])

    def test_codes_unicode(self):
        self.assertEqual(code_to_names(u'TM'), ['Turkmenistan'])

    def test_point(self):
        cs = point_to_names(lon=27.5125, lat=-21.173611)
        self.assertEqual(cs, ['Botswana', 'Zimbabwe'])

    def test_point_2(self):
        cs = point_to_names(lon=5.983333, lat=50.883333)
        self.assertEqual(cs, ['France', 'Germany', 'Netherlands'])

    def test_point_3(self):
        cs = point_to_names(lon=-171.714086, lat=-75.185789)
        self.assertEqual(cs, ['Antarctica'])

    def test_point_4(self):
        cs = point_to_names(lon=-79.888252, lat=32.819747)
        self.assertEqual(cs, ['U.S.A.'])
