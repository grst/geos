FROM continuumio/miniconda3
COPY . .
RUN python setup.py install 
RUN cd /opt/conda/lib/python*/site-packages && ln -s geos-*/geos geos
