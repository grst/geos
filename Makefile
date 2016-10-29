install:
	python setup.py sdist
	pip uninstall -y geos
	pip install dist/geos-0.1.0.tar.gz

