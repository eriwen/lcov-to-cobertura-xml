export PYTHONPATH := $(realpath lcov_cobertura):$(PYTHONPATH)
PYTHON=python3
SRCDIR=lcov_cobertura

.PHONY: doc release pypi clean test

release: clean doc $(SRCDIR)/*.py test/*.py
	rm -f dist/*
	$(PYTHON) setup.py sdist bdist_wininst

pypi: doc
	$(PYTHON) setup.py sdist upload
	$(PYTHON) setup.py bdist_wininst upload

doc:
	cd docs; $(MAKE) html

test:
	cd test; $(PYTHON) test_lcov_cobertura.py

clean:
	cd docs; $(MAKE) clean
	rm -rf dist build
	rm -f $(SRCDIR)/*.pyc test/*.pyc setup.pyc MANIFEST
