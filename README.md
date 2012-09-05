# lcov to cobertura XML converter [![Build Status](https://secure.travis-ci.org/eriwen/lcov-to-cobertura-xml.png)](http://travis-ci.org/eriwen/lcov-to-cobertura-xml)

This project does as the name implies: it coverts code coverage report 
files in [lcov](http://ltp.sourceforge.net/coverage/lcov.php) format to
[Cobertura](http://cobertura.sourceforge.net/)'s XML report format so that
CI servers like [Jenkins](http://jenkins-ci.org) can aggregate results and 
determine build stability etc.

## Quick command-line usage

[Grab it raw]() and run it with python:
```bash
python lcov_cobertura.py lcov-file.dat
```

 - `-b/--base-dir` - (Optional) Directory where source files are located. Defaults to the current directory
 - `-e/--excludes` - (Optional) Comma-separated list of regexes of packages to exclude
 - `-o/--output` - (Optional) Path to store cobertura xml file. _Defaults to ./coverage.xml_

```bash
python lcov-to-cobertura-xml.py lcov-file.dat --base-dir src/dir -excludes test.lib -output output/cobertura.xml
```

## Usage as a Python module

You can install lcov_cobertura with [easy_install](http://peak.telecommunity.com/DevCenter/EasyInstall):
```bash
sudo easy_install lcov_cobertura
```

Then just use it in your terminal:
```bash
python -m lcov_cobertura lcov-file.dat
```

OR anywhere in your python:
```python
from lcov_cobertura import LcovCobertura

LCOV_INPUT = 'SF:foo/file.ext\nDA:1,1\nDA:2,0\nend_of_record\n'
converter = LcovCobertura(LCOV_INPUT)
cobertura_xml = converter.convert()
print cobertura_xml
```

## License

This project is provided under the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0).