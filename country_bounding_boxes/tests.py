from unittest import TestCase

from country_bounding_boxes import (
    get_countries_containing_point,
    get_country_by_iso_code
)


class TestCountries(TestCase):

    def test_codes(self):
        self.assertEqual(get_country_by_iso_code('AF').name,
                         'Afghanistan')
        self.assertEqual(get_country_by_iso_code('AFG').name,
                         'Afghanistan')

    def test_codes_2(self):
        self.assertEqual(get_country_by_iso_code('ZW').name,
                         'Zimbabwe')
        self.assertEqual(get_country_by_iso_code('ZWE').name,
                         'Zimbabwe')

    def test_codes_case(self):
        self.assertEqual(get_country_by_iso_code('it').name,
                         'Italy')
        self.assertEqual(get_country_by_iso_code('iTa').name,
                         'Italy')

    def test_codes_case_2(self):
        self.assertEqual(get_country_by_iso_code('Tm').name,
                         'Turkmenistan')
        self.assertEqual(get_country_by_iso_code('Tkm').name,
                         'Turkmenistan')

    def test_codes_missing(self):
        self.assertEqual(get_country_by_iso_code('ZZ'),
                         None)
        self.assertEqual(get_country_by_iso_code('LFQ'),
                         None)

    def test_codes_wrong_type(self):
        self.assertEqual(get_country_by_iso_code(None),
                         None)
        self.assertEqual(get_country_by_iso_code(1.2),
                         None)

    def test_point(self):
        cs = get_countries_containing_point(lon=27.5125,
                                            lat=-21.173611)
        cs = [c.name for c in cs]
        self.assertEqual(cs, ['Botswana', 'Zimbabwe'])

    def test_point_2(self):
        cs = get_countries_containing_point(lon=5.983333,
                                            lat=50.883333)
        cs = [c.name for c in cs]
        self.assertEqual(cs, ['Belgium', 'France', 'Netherlands', 'Russia'])

    def test_point_3(self):
        cs = get_countries_containing_point(lon=-171.714086,
                                            lat=-75.185789)
        cs = [c.name for c in cs]
        self.assertEqual(cs, ['Antarctica'])

    def test_point_4(self):
        cs = get_countries_containing_point(lon=-79.888252,
                                            lat=32.819747)
        cs = [c.name for c in cs]
        self.assertEqual(cs, ['United States'])
