#!/usr/bin/env python

# Copyright 2011-2012 Eric Wendelin
#
# This is free software, licensed under the Apache License, Version 2.0,
# available in the accompanying LICENSE.txt file.

import unittest

from lcov_cobertura import LcovCobertura

class Test(unittest.TestCase):
    """Unit tests for lcov_cobertura."""

    def test_parse(self):
        converter = LcovCobertura(
            'SF:foo/file.ext\nDA:1,1\nDA:2,0\nend_of_record\n')
        result = converter.parse()
        self.assertTrue(result.has_key('packages'))
        self.assertTrue(result['packages'].has_key('foo'))
        self.assertEqual(result['packages']['foo']['branches-covered'], 0)
        self.assertEqual(result['packages']['foo']['branches-total'], 0)
        self.assertEqual(result['packages']['foo']['line-rate'], '0.5')
        self.assertEqual(result['packages']['foo']['lines-covered'], 1)
        self.assertEqual(result['packages']['foo']['lines-total'], 2)

    def test_exclude_package_from_parser(self):
        converter = LcovCobertura(
            'SF:foo/file.ext\nDA:1,1\nDA:2,0\nend_of_record\nSF:bar/file.ext\nDA:1,1\nDA:2,1\nend_of_record\n',
            '.',
            'foo')
        result = converter.parse()
        self.assertFalse(result['packages'].has_key('foo'))
        self.assertTrue(result['packages'].has_key('bar'))
        # Verify that excluded package did not skew line coverage totals
        self.assertEqual(result['packages']['bar']['line-rate'], '1.0')

    def test_generate_cobertura_xml(self):
        converter = LcovCobertura(
            'SF:foo/file.ext\nDA:1,1\nDA:2,0\nend_of_record\n')
        parsed_lcov = {'packages': {
            'foo': {'branches-covered': 0, 'line-rate': '0.5',
                    'lines-covered': 1, 'branches-total': 0, 'lines-total': 2,
                    'classes': {
                    'Bar': {'branches-covered': 0, 'lines-covered': 1,
                            'branches-total': 0, 'lines': {
                        1: {'hits': '1', 'branch-conditions-covered': 0,
                            'branch-conditions-total': 0, 'branch': 'false'},
                        2: {'hits': '0', 'branch-conditions-covered': 0,
                            'branch-conditions-total': 0, 'branch': 'false'}},
                            'lines-total': 2, 'name': 'file.ext'}},
                    'branch-rate': '0.0'}},
                       'summary': {'branches-covered': 0, 'branches-total': 0,
                                   'lines-covered': 1, 'lines-total': 2},
                       'timestamp': '1346815648'}
        xml = converter.generate_cobertura_xml(parsed_lcov)
        self.assertEqual(xml,
                         '<?xml version="1.0" ?>\n<!DOCTYPE coverage\n  SYSTEM \'http://cobertura.sourceforge.net/xml/coverage-03.dtd\'>\n<coverage branch-rate="0.0" branches-covered="0" branches-valid="0" complexity="0" line-rate="0.5" lines-valid="2" timestamp="1346815648" version="1.9">\n\t<sources/>\n\t<packages>\n\t\t<package branch-rate="0.0" line-rate="0.5" name="foo">\n\t\t\t<classes>\n\t\t\t\t<class branch-rate="0.0" complexity="0" filename="Bar" line-rate="0.5" name="file.ext">\n\t\t\t\t\t<lines>\n\t\t\t\t\t\t<line branch="false" hits="1" number="1"/>\n\t\t\t\t\t\t<line branch="false" hits="0" number="2"/>\n\t\t\t\t\t</lines>\n\t\t\t\t</class>\n\t\t\t</classes>\n\t\t</package>\n\t</packages>\n</coverage>\n')

if __name__ == '__main__':
    unittest.main()