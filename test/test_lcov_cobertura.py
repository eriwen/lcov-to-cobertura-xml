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
            'SF:foo/file.ext\nDA:1,1\nDA:2,0\nBRDA:1,1,1,1\nBRDA:1,1,2,0\nend_of_record\n')
        result = converter.parse()
        self.assertTrue('packages' in result)
        self.assertTrue('foo' in result['packages'])
        self.assertEqual(result['packages']['foo']['branches-covered'], 1)
        self.assertEqual(result['packages']['foo']['branches-total'], 2)
        self.assertEqual(result['packages']['foo']['branch-rate'], '0.5')
        self.assertEqual(result['packages']['foo']['line-rate'], '0.5')
        self.assertEqual(result['packages']['foo']['lines-covered'], 1)
        self.assertEqual(result['packages']['foo']['lines-total'], 2)
        self.assertEqual(result['packages']['foo']['classes']['foo/file.ext']['branches-covered'], 1)
        self.assertEqual(result['packages']['foo']['classes']['foo/file.ext']['branches-total'], 2)
        self.assertEqual(result['packages']['foo']['classes']['foo/file.ext']['methods'], {})

    def test_parse_with_functions(self):
        converter = LcovCobertura(
            'TN:\nSF:foo/file.ext\nDA:1,1\nDA:2,0\nFN:1,(anonymous_1)\nFN:2,namedFn\nFNDA:1,(anonymous_1)\nend_of_record\n')
        result = converter.parse()
        self.assertEqual(result['packages']['foo']['line-rate'], '0.5')
        self.assertEqual(result['packages']['foo']['lines-covered'], 1)
        self.assertEqual(result['packages']['foo']['lines-total'], 2)
        self.assertEqual(result['packages']['foo']['classes']['foo/file.ext']['methods']['(anonymous_1)'], '1')
        self.assertEqual(result['packages']['foo']['classes']['foo/file.ext']['methods']['namedFn'], '0')

    def test_exclude_package_from_parser(self):
        converter = LcovCobertura(
            'SF:foo/file.ext\nDA:1,1\nDA:2,0\nend_of_record\nSF:bar/file.ext\nDA:1,1\nDA:2,1\nend_of_record\n',
            '.',
            'foo')
        result = converter.parse()
        self.assertTrue('foo' not in result['packages'])
        self.assertTrue('bar' in result['packages'])
        # Verify that excluded package did not skew line coverage totals
        self.assertEqual(result['packages']['bar']['line-rate'], '1.0')

    def test_generate_cobertura_xml(self):
        converter = LcovCobertura(
            'TN:\nSF:foo/file.ext\nDA:1,1\nDA:2,0\nBRDA:1,1,1,1\nBRDA:1,1,2,0\nFN:1,(anonymous_1)\nFN:2,namedFn\nFNDA:1,(anonymous_1)\nend_of_record\n')
        parsed_lcov = {'packages': {
            'foo': {'branches-covered': 1, 'line-rate': '0.5', 'branch-rate': '0.5',
                    'lines-covered': 1, 'branches-total': 2, 'lines-total': 2,
                    'classes': {
                    'Bar': {'branches-covered': 1, 'lines-covered': 1,
                            'branches-total': 2,
                            'methods': {
                                '(anonymous_1)': '1',
                                'namedFn': '0'
                            },
                            'lines': {
                                1: {'hits': '1', 'branches-covered': 1,
                                    'branches-total': 2, 'branch': 'true'},
                                2: {'hits': '0', 'branches-covered': 0,
                                    'branches-total': 0, 'branch': 'false'}
                            },
                            'lines-total': 2, 'name': 'file.ext'}},
                    }},
                       'summary': {'branches-covered': 1, 'branches-total': 2,
                                   'lines-covered': 1, 'lines-total': 2},
                       'timestamp': '1346815648000'}
        xml = converter.generate_cobertura_xml(parsed_lcov)
        self.assertEqual(xml, '<?xml version="1.0" ?>\n<!DOCTYPE coverage\n  SYSTEM \'http://cobertura.sourceforge.net/xml/coverage-03.dtd\'>\n<coverage branch-rate="0.5" branches-covered="1" branches-valid="2" complexity="0" line-rate="0.5" lines-valid="2" timestamp="1346815648000" version="1.9">\n\t<sources>\n\t\t<source>\n\t\t\t.\n\t\t</source>\n\t</sources>\n\t<packages>\n\t\t<package branch-rate="0.5" line-rate="0.5" name="foo">\n\t\t\t<classes>\n\t\t\t\t<class branch-rate="0.5" complexity="0" filename="Bar" line-rate="0.5" name="file.ext">\n\t\t\t\t\t<methods>\n\t\t\t\t\t\t<method hits="0" name="namedFn" signature=""/>\n\t\t\t\t\t\t<method hits="1" name="(anonymous_1)" signature=""/>\n\t\t\t\t\t</methods>\n\t\t\t\t\t<lines>\n\t\t\t\t\t\t<line branch="true" condition-coverage="50% (1/2)" hits="1" number="1"/>\n\t\t\t\t\t\t<line branch="false" hits="0" number="2"/>\n\t\t\t\t\t</lines>\n\t\t\t\t</class>\n\t\t\t</classes>\n\t\t</package>\n\t</packages>\n</coverage>\n')

if __name__ == '__main__':
    unittest.main()
