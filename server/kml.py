from pykml.factory import KML_ElementMaker as KML
from geometry import *
from lxml import etree


class KMLBuilder:
    MIME_TYPE = "application/vnd.google-earth.kml+xml"

    def get_map_url(self, map, z, x, y):
        return self.url_formatter("/maps/{}/{}/{}/{}.kml".format(map.id, z, x, y))

    def add_elem(self, kml_elem):
        self.kml_doc.append(kml_elem)

    def add_elems(self, kml_elems):
        for kml_elem in kml_elems:
            self.add_elem(kml_elem)

    def __init__(self, url_formatter=lambda x: x):
        """

        Args:
            url_formatter: Callback function for creating an absolute
             URL from a relative paths
        """
        self.url_formatter = url_formatter
        self.kml_doc = KML.Document()
        self.kml_root = KML.kml(self.kml_doc)

    def get_kml(self):
        return etree.tostring(self.kml_root, pretty_print=True, xml_declaration=True)


class KMLMaster(KMLBuilder):
    """Create a KML Master document that
    contains NetworkLinks to all Maps
    in the mapsource directory"""

    def __init__(self, mapsources, url_formatter):
        super().__init__(url_formatter)
        for map_s in mapsources:
            self.add_elem(
                KML.NetworkLink(
                    KML.name(map_s.name),
                    KML.Link(
                        KML.href(self.get_map_url(map_s, 0, 0, 0)),
                        KML.viewRefreshMode("onRegion")
                    )
                )
            )


class KMLMapRoot(KMLBuilder):
    """Create root Document for an
    individual Map. Can be used as standalone KML
    to display that map only"""


class KMLRegion(KMLBuilder):
    """Create a KML that displays the actual tiles
    as GroundOverlay and contains NetworkLinks
    to the next LevelOfDetail"""

    QUADS = ['ne', 'se', 'sw', 'nw']

    def make_lat_lon_box(self):
        """Create the north/south/east/west tags
        for a LatLonBox or LatLonAltBox Bounding Box"""
        geo_bb = self.tile_coords.geographic_bounds()
        return (
            KML.north(geo_bb.max.lat),
            KML.south(geo_bb.min.lat),
            KML.east(geo_bb.max.lon),
            KML.west(geo_bb.min.lon)
        )

    @staticmethod
    def make_level_of_detail(min_lod_pixels=128, max_lod_pixels=-1):
        """Create the KML LevelOfDetail (LOD) Tag"""
        return KML.Lod(
            KML.minLodPixels(min_lod_pixels),
            KML.maxLodPixels(max_lod_pixels)
        )

    def make_region(self):
        """Create the KML Region tag with the appropriate
        geographic coordinates"""
        return KML.Region(
            self.make_level_of_detail(),
            KML.LatLonAltBox(
                *self.make_lat_lon_box()
            )
        )

    def get_quad_coords(self, quad):
        """Calculate the TileCoordinates
        for the next level of Detail.

        Args:
            quad: direction, either ne, nw, sw, se

        Returns:
            TileCoordinates
        """
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

    def make_network_link(self, tile_coords):
        return KML.NetworkLink(
            KML.name("NL_{}_{}_{}".format(tile_coords.zoom, tile_coords.x, tile_coords.y)),
            self.make_region(),
            KML.Link(
                KML.href(self.get_map_url(self.mapsource, tile_coords.zoom, tile_coords.x, tile_coords.y)),
                KML.viewRefreshMode("onRegion")
            )
        )

    def make_child_links(self):
        nls = []
        if self.tile_coords.zoom < self.mapsource.max_zoom:
            for quad in self.QUADS:
                quad_coords = self.get_quad_coords(quad)
                nls.append(self.make_network_link(quad_coords))
        return nls

    def make_ground_overlay(self):
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
                *self.make_lat_lon_box()
            ),
        )

    def __init__(self, mapsource, z, x, y, url_formatter):
        super().__init__(url_formatter)
        self.tile_coords = TileCoordinate(z, x, y)
        self.mapsource = mapsource

        self.add_elem(KML.name("DOC_{}_{}_{}".format(z, x, y)))
        self.add_elems(self.make_child_links())
        self.add_elem(self.make_ground_overlay())


