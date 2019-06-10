FROM continuumio/miniconda3
COPY . .
RUN python setup.py install 
RUN export GEOS_VERSION="$(python setup.py --version)" \
    && ln -s /opt/conda/lib/python3.7/site-packages/geos-"$GEOS_VERSION"-py3.7.egg/geos /opt/conda/lib/python3.7/site-packages/geos
