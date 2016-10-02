from lxml import etree
from pykml.factory import KML_ElementMaker as KML


def make_kml_master(map_sources):
    pass


class OverlayCreator(object):
    def __init__(self, map_source):
        self.map_source = map_source