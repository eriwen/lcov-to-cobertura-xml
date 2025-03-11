#!/usr/bin/env python

# Copyright 2011-2012 Eric Wendelin
#
# This is free software, licensed under the Apache License, Version 2.0,
# available in the accompanying LICENSE.txt file.

import unittest
from xmldiff import main as xmldiff

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
            'TN:\nSF:foo/file.ext\nDA:1,1\nDA:2,0\nFN:1,(anonymous_1)\nFN:1,2,(anonymous_2)\nFN:2,namedFn\nFNDA:1,(anonymous_1)\nend_of_record\n')
        result = converter.parse()
        self.assertEqual(result['packages']['foo']['line-rate'], '0.5')
        self.assertEqual(result['packages']['foo']['lines-covered'], 1)
        self.assertEqual(result['packages']['foo']['lines-total'], 2)
        self.assertEqual(result['packages']['foo']['classes']['foo/file.ext']['methods']['(anonymous_1)'], ['1', '1'])
        self.assertEqual(result['packages']['foo']['classes']['foo/file.ext']['methods']['(anonymous_2)'], ['1', '0'])
        self.assertEqual(result['packages']['foo']['classes']['foo/file.ext']['methods']['namedFn'], ['2', '0'])

    def test_parse_with_checksum(self):
        converter = LcovCobertura(
            'SF:foo/file.ext\nDA:1,1,dummychecksum\nDA:2,0,dummychecksum\nBRDA:1,1,1,1\nBRDA:1,1,2,0\nend_of_record\n')
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
        TEST_XML = r"""<?xml version="1.0" ?>
<!DOCTYPE coverage
  SYSTEM 'http://cobertura.sourceforge.net/xml/coverage-04.dtd'>
<coverage branch-rate="0.5" branches-covered="1" branches-valid="2" complexity="0" line-rate="0.5" lines-covered="1" lines-valid="2" timestamp="1346815648000" version="2.0.3">
    <sources>
        <source>.</source>
    </sources>
    <packages>
        <package line-rate="0.5" branch-rate="0.5" name="foo" complexity="0">
            <classes>
                <class branch-rate="0.5" complexity="0" filename="Bar" line-rate="0.5" name="file.ext">
                    <methods>
                        <method name="(anonymous_1)" signature="" line-rate="1.0" branch-rate="1.0">
                            <lines>
                                <line hits="1" number="1" branch="false"/>
                            </lines>
                        </method>
                        <method name="namedFn" signature="" line-rate="0.0" branch-rate="0.0">
                            <lines>
                                <line hits="0" number="2" branch="false"/>
                            </lines>
                        </method>
                    </methods>
                    <lines>
                        <line branch="true" hits="1" number="1" condition-coverage="50% (1/2)"/>
                        <line branch="false" hits="0" number="2"/>
                    </lines>
                </class>
            </classes>
        </package>
    </packages>
</coverage>
"""

        parsed_lcov = {'packages': {
            'foo': {'branches-covered': 1, 'line-rate': '0.5', 'branch-rate': '0.5',
                    'lines-covered': 1, 'branches-total': 2, 'lines-total': 2,
                    'classes': {
                    'Bar': {'branches-covered': 1, 'lines-covered': 1,
                            'branches-total': 2,
                            'methods': {
                                '(anonymous_1)': ['1', '1'],
                                'namedFn': ['2', '0']
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
        xml = converter.generate_cobertura_xml(parsed_lcov, indent="    ")
        xml_diff = xmldiff.diff_texts(xml, TEST_XML)
        self.assertEqual(len(xml_diff), 0)

    def test_treat_non_integer_line_execution_count_as_zero(self):
        converter = LcovCobertura(
            'SF:foo/file.ext\nDA:1,=====\nDA:2,2\nBRDA:1,1,1,1\nBRDA:1,1,2,0\nend_of_record\n')
        result = converter.parse()
        self.assertEqual(result['packages']['foo']['lines-covered'], 1)
        self.assertEqual(result['packages']['foo']['lines-total'], 2)

    def test_support_function_names_with_commas(self):
        converter = LcovCobertura(
            'TN:\nSF:foo/file.ext\nDA:1,1\nDA:2,0\nFN:1,2,(anonymous_1<foo, bar>)\nFN:2,namedFn\nFNDA:1,(anonymous_1<foo, bar>)\nend_of_record\n')
        result = converter.parse()
        self.assertEqual(result['packages']['foo']['classes']['foo/file.ext']['methods']['(anonymous_1<foo, bar>)'], ['1', '1'])
        self.assertEqual(result['packages']['foo']['classes']['foo/file.ext']['methods']['namedFn'], ['2', '0'])

    def test_demangle(self):
        converter = LcovCobertura(
            "TN:\nSF:foo/foo.cpp\nFN:3,_ZN3Foo6answerEv\nFNDA:1,_ZN3Foo6answerEv\nFN:8,_ZN3Foo3sqrEi\nFNDA:1,_ZN3Foo3sqrEi\nDA:3,1\nDA:5,1\nDA:8,1\nDA:10,1\nend_of_record",
            demangle=True)
        TEST_TIMESTAMP = 1594850794
        TEST_XML = r"""<?xml version="1.0" ?>
<!DOCTYPE coverage
  SYSTEM 'http://cobertura.sourceforge.net/xml/coverage-04.dtd'>
<coverage branch-rate="0.0" branches-covered="0" branches-valid="0" complexity="0" line-rate="1.0" lines-covered="4" lines-valid="4" timestamp="{}" version="2.0.3">
    <sources>
        <source>.</source>
    </sources>
    <packages>
        <package line-rate="1.0" branch-rate="0.0" name="foo" complexity="0">
            <classes>
                <class branch-rate="0.0" complexity="0" filename="foo/foo.cpp" line-rate="1.0" name="foo.foo.cpp">
                    <methods>
                        <method name="Foo::answer()" signature="" line-rate="1.0" branch-rate="1.0">
                            <lines>
                                <line hits="1" number="3" branch="false"/>
                            </lines>
                        </method>
                        <method name="Foo::sqr(int)" signature="" line-rate="1.0" branch-rate="1.0">
                            <lines>
                                <line hits="1" number="8" branch="false"/>
                            </lines>
                        </method>
                    </methods>
                    <lines>
                        <line branch="false" hits="1" number="3"/>
                        <line branch="false" hits="1" number="5"/>
                        <line branch="false" hits="1" number="8"/>
                        <line branch="false" hits="1" number="10"/>
                    </lines>
                </class>
            </classes>
        </package>
    </packages>
</coverage>
""".format(TEST_TIMESTAMP)
        result = converter.parse(timestamp=TEST_TIMESTAMP)
        xml = converter.generate_cobertura_xml(result, indent="    ")
        xml_diff = xmldiff.diff_texts(xml, TEST_XML)
        self.assertEqual(len(xml_diff), 0)

if __name__ == '__main__':
    unittest.main(verbosity=2)
