# lcov to cobertura XML converter

This project does as the name implies: it coverts code coverage report 
files in [lcov](http://ltp.sourceforge.net/coverage/lcov.php) format to
[Cobertura](http://cobertura.sourceforge.net/)'s XML report format so that
CI servers like [Jenkins](http://jenkins-ci.org) can aggregate results and 
determine build stability etc.

## Usage

    python lcov-to-cobertura-xml.py lcov-file.dat

 - `-b/--base-dir` - (Optional) Directory where source files are located. Defaults to the current directory
 - `-e/--excludes` - (Optional) Comma-separated list of regexes of packages to exclude
 - `-o/--output` - (Optional) Path to store cobertura xml file. Defaults to ./coverage.xml

## Caveats
This was originally intended to convert [JsTestDriver](http://code.google.com/p/js-test-driver/) coverage results, so it
may not work properly with all LCOV constructs. If you have any problems or
suggestions, feel free to 
[file an issue](https://github.com/eriwen/lcov-to-cobertura-xml/issues) 
and it'll be addressed

## License

This project is provided under the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0).