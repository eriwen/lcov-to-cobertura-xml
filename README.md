# lcov to cobertura XML converter [![Build Status](https://secure.travis-ci.org/eriwen/lcov-to-cobertura-xml.png?branch=master)](http://travis-ci.org/eriwen/lcov-to-cobertura-xml)

This project does as the name implies: it coverts code coverage report
files in [lcov](http://ltp.sourceforge.net/coverage/lcov.php) format to
[Cobertura](http://cobertura.sourceforge.net/)'s XML report format so that
CI servers like [Jenkins](http://jenkins-ci.org) can aggregate results and
determine build stability etc.

Coverage metrics supported:

 - Package/folder overall line and branch coverage
 - Class/file overall line and branch coverage
 - Functions hit
 - Line and Branch hits

## Quick command-line usage

[Grab it raw](https://raw.github.com/eriwen/lcov-to-cobertura-xml/master/lcov_cobertura/lcov_cobertura.py) and run it with python:
```bash
python lcov_cobertura.py lcov-file.dat
```

 - `-b/--base-dir` - (Optional) Directory where source files are located. Defaults to the current directory
 - `-e/--excludes` - (Optional) Comma-separated list of regexes of packages to exclude
 - `-o/--output` - (Optional) Path to store cobertura xml file. _Defaults to ./coverage.xml_

```bash
python lcov_cobertura.py lcov-file.dat --base-dir src/dir --excludes test.lib --output build/coverage.xml
```

## Usage as a Python module

You can install lcov_cobertura with [pip](http://pypi.python.org/pypi/pip):
```bash
pip install lcov_cobertura
```

Then just use it anywhere in your python:
```python
from lcov_cobertura import LcovCobertura

LCOV_INPUT = 'SF:foo/file.ext\nDA:1,1\nDA:2,0\nend_of_record\n'
converter = LcovCobertura(LCOV_INPUT)
cobertura_xml = converter.convert()
print cobertura_xml
```

## Environment Support

Python 2.6+ is supported (including Python 3). You can also use the *experimental* Jython 2.5 friendly 
version in the [jython branch](https://github.com/eriwen/lcov-to-cobertura-xml/tree/jython).

## Contributions
This project is made possible due to the efforts of these fine people:

 - [Eric Wendelin](http://eriwen.com)
 - [Björge Dijkstra](https://github.com/bjd)
 - [Jon Schewe](http://mtu.net/~jpschewe)

## License
This project is provided under the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0).

I provide this software free of charge. If you find it helpful, please endorse me for Python on coderwall: [![endorse](http://api.coderwall.com/eriwen/endorsecount.png)](http://coderwall.com/eriwen)
