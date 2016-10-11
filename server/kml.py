from pykml.factory import KML_ElementMaker as KML
from geometry import *
from lxml import etree

SERVER_HOST = "127.0.0.1:5000"


def get_map_url(map, z, x, y):
    return "http://{}/maps/{}/{}/{}/{}.kml".format(SERVER_HOST, map.id, z, x, y)


class KMLBuilder:
    MIME_TYPE = "application/vnd.google-earth.kml+xml"

    def __init__(self):
        self.kml_doc = KML.kml()

    def get_kml(self):
        return etree.tostring(self.kml_doc, pretty_print=True, xml_declaration=True)


class KMLMaster(KMLBuilder):
    def __init__(self, mapsources):
        kml_elements = []
        for map_s in mapsources:
            kml_elements.append(
                KML.NetworkLink(
                    KML.name(map_s.name),
                    KML.Link(
                        KML.href(get_map_url(map_s, 0, 0, 0)),
                        KML.viewRefreshMode("onRegion")
                    )
                )
            )
        self.kml_doc = KML.kml(*kml_elements)


class KMLRegion(KMLBuilder):
    QUADS =  ['ne', 'se', 'sw', 'nw']

    def lat_lon_box(self, geo_bb):
        return (
            KML.north(geo_bb.max.lat),
            KML.south(geo_bb.min.lat),
            KML.east(geo_bb.max.lon),
            KML.west(geo_bb.min.lon)
        )

    def lod(self, min_lod_pixels=128, max_lod_pixels=-1):
        return KML.Lod(
            KML.minLodPixels(min_lod_pixels),
            KML.maxLodPixels(max_lod_pixels)
        )

    def kml_region(self):
        return KML.Region(
            self.lod(),
            KML.LatLonAltBox(
                *self.lat_lon_box(self.tile_coords.geographic_bounds())
            )
        )

    def get_quad_coords(self, quad):
        assert quad in self.QUADS

        z = self.tile_coords.zoom + 1
        x = self.tile_coords.x * 2
        y = self.tile_coords.y * 2
        if quad == "nw":
            pass
        elif quad == "ne":
            x += 1
        elif quad == "se":
            x += 1
            y += 1
        elif quad == "sw":
            y += 1

        return TileCoordinate(z, x, y)

    def network_link(self, tile_coords):
        return KML.NetworkLink(
            KML.name("NL_{}_{}_{}".format(tile_coords.zoom, tile_coords.x, tile_coords.y)),
            self.kml_region(),
            KML.Link(
                KML.href(get_map_url(self.mapsource, tile_coords.zoom, tile_coords.x, tile_coords.y)),
                KML.viewRefreshMode("onRegion")
            )
        )

    def make_child_links(self):
        nls = []
        for quad in  self.QUADS:
            quad_coords = self.get_quad_coords(quad)
            nls.append(self.network_link(quad_coords))
        return nls

    def ground_overlay(self):
        z = self.tile_coords.zoom
        x = self.tile_coords.x
        y = self.tile_coords.y
        return KML.GroundOverlay(
            KML.name("GO_{}_{}_{}".format(z, x, y)),
            KML.drawOrder(self.tile_coords.zoom),
            KML.Icon(
                KML.href(self.mapsource.get_tile_url(z, x, y))
            ),
            KML.LatLonBox(
                *self.lat_lon_box(self.tile_coords.geographic_bounds())
            ),
        )

    def __init__(self, mapsource, z, x, y):
        self.tile_coords = TileCoordinate(z, x, y)
        self.mapsource = mapsource
        bbox = self.tile_coords.geographic_bounds()

        kml_elems = []
        kml_elems.append(KML.name("doc_{}_{}_{}".format(z, x, y)))
        kml_elems.extend(self.make_child_links())
        kml_elems.append(self.ground_overlay())

        self.kml_doc = KML.kml(
            KML.Document(
                *kml_elems
            )
        )
