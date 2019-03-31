FROM continuumio/miniconda3
RUN pip install geos Pillow
EXPOSE 5000
