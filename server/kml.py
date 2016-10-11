from pykml.factory import KML_ElementMaker as KML
from geometry import *
from lxml import etree
import itertools

# TODO Documentation!
# TODO Unittesting


class KMLBuilder:
    MIME_TYPE = "application/vnd.google-earth.kml+xml"
    TILES_PER_ROW_PER_REGION = 2

    def get_map_url(self, map, z, x, y):
        return self.url_formatter("/maps/{}/{}/{}/{}.kml".format(map.id, z, x, y))

    def add_elem(self, kml_elem):
        self.kml_doc.append(kml_elem)

    def add_elems(self, kml_elems):
        for kml_elem in kml_elems:
            self.add_elem(kml_elem)

    @staticmethod
    def make_lat_lon_box(geo_bb):
        """Create the north/south/east/west tags
        for a LatLonBox or LatLonAltBox Bounding Box"""
        return (
            KML.north(geo_bb.max.lat),
            KML.south(geo_bb.min.lat),
            KML.east(geo_bb.max.lon),
            KML.west(geo_bb.min.lon)
        )

    def make_level_of_detail(self, min_lod_pixels=128, max_lod_pixels=-1):
        """Create the KML LevelOfDetail (LOD) Tag"""
        # TODO: min_lod_pixels should be dependent on tiles per row
        return KML.Lod(
            KML.minLodPixels(min_lod_pixels),
            KML.maxLodPixels(max_lod_pixels))

    def make_region(self, tile_coords):
        """Create the KML Region tag with the appropriate
        geographic coordinates"""
        p1 = tile_coords.to_geographic()
        p2 = TileCoordinate(tile_coords.zoom, tile_coords.x + self.TILES_PER_ROW_PER_REGION,
                            tile_coords.y + self.TILES_PER_ROW_PER_REGION)
        bbox = GeographicBB(p1.lon, p2.lat, p2.long, p1.lat)
        return KML.Region(
            self.make_level_of_detail(),
            KML.LatLonAltBox(
                *self.make_lat_lon_box(bbox)
            )
        )

    @staticmethod
    def zoom_in(tile_coords):
        return TileCoordinate(zoom=tile_coords.zoom + 1,
                              x=tile_coords.x * 2,
                              y=tile_coords.y * 2)

    @staticmethod
    def tileiter(tile_coords, ncol, step=1):
        for x, y in itertools.product(range(tile_coords.x, tile_coords.x + ncol, step),
                                      range(tile_coords.y, tile_coords.y + ncol, step)):
            yield TileCoordinate(zoom=tile_coords.zoom,
                                 x=x, y=y)

    def make_network_link(self, tile_coords):
        return KML.NetworkLink(
            KML.name("NL_{}_{}_{}".format(tile_coords.zoom, tile_coords.x, tile_coords.y)),
            self.make_region(tile_coords),
            KML.Link(
                KML.href(self.get_map_url(self.mapsource, tile_coords.zoom, tile_coords.x, tile_coords.y)),
                KML.viewRefreshMode("onRegion")
            )
        )

    def make_ground_overlay(self, tile_coords):
        z = tile_coords.zoom
        x = tile_coords.x
        y = tile_coords.y
        return KML.GroundOverlay(
            KML.name("GO_{}_{}_{}".format(z, x, y)),
            KML.drawOrder(z),
            KML.Icon(
                KML.href(self.mapsource.get_tile_url(z, x, y))
            ),
            KML.LatLonBox(
                *self.make_lat_lon_box(tile_coords.geographic_bounds())
            ),
        )

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

    def __init__(self, mapsource, url_formatter):
        super().__init__(url_formatter)
        self.mapsource = mapsource

        z = mapsource.min_zoom
        n_tiles = 2 ** z
        base_coord = TileCoordinate(z, 0, 0)

        self.add_elem(KML.name("{} root".format(mapsource.name)))

        for current_tile in self.tileiter(self.zoom_in(base_coord), ncol=n_tiles, step=self.TILES_PER_ROW_PER_REGION):
            self.add_elem(self.make_network_link(current_tile))
        for current_tile in self.tileiter(base_coord, ncol=n_tiles):
            self.add_elem(self.make_ground_overlay(current_tile))


class KMLRegion(KMLBuilder):
    """Create a KML that displays the actual tiles
    as GroundOverlay and contains NetworkLinks
    to the next LevelOfDetail"""

    def make_child_links(self):
        nls = []
        if self.tile_coords.zoom < self.mapsource.max_zoom:
            for nl_coords in self.tileiter(self.zoom_in(self.tile_coords), 2 * self.TILES_PER_ROW_PER_REGION,
                                           step=self.TILES_PER_ROW_PER_REGION):
                nls.append(self.make_network_link(nl_coords))
        return nls

    def __init__(self, mapsource, z, x, y, url_formatter):
        super().__init__(url_formatter)
        self.tile_coords = TileCoordinate(z, x, y)
        self.mapsource = mapsource

        self.add_elem(KML.name("DOC_{}_{}_{}".format(z, x, y)))
        self.add_elems(self.make_child_links())
        for overlay_tile in self.tileiter(self.tile_coords):
            self.add_elem(self.make_ground_overlay(overlay_tile))
