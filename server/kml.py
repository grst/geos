from pykml.factory import KML_ElementMaker as KML
from geometry import *
from lxml import etree
import itertools

# TODO Documentation!
# TODO Unittesting
# TODO something with the regions is wrong (loads way too much)
"""
it would proabably be more pythonic if
I removed all map specific functions from
KML Builder and turned them into module
level functions
"""

LOG_R = -1
assert LOG_R in range(-1, 3)  # log ratio for tiles/network links


def kml_lat_lon_box(geo_bb):
    """Create the north/south/east/west tags
    for a LatLonBox or LatLonAltBox Bounding Box"""
    return (
        KML.north(geo_bb.max.lat),
        KML.south(geo_bb.min.lat),
        KML.east(geo_bb.max.lon),
        KML.west(geo_bb.min.lon)
    )


def kml_lod(self, min_lod_pixels=128, max_lod_pixels=-1):
    """Create the KML LevelOfDetail (LOD) Tag"""
    # TODO: min_lod_pixels should be dependent on tiles per row
    return KML.Lod(
        KML.minLodPixels(min_lod_pixels),
        KML.maxLodPixels(max_lod_pixels))

def kml_region(region_coords):
    """Create the KML Region tag with the appropriate
    geographic coordinates"""
    p1 = region_coords.to_geographic()
    p2 = TileCoordinate(region_coords.zoom, region_coords.x + self.TILES_PER_ROW_PER_REGION,
                        region_coords.y + self.TILES_PER_ROW_PER_REGION).to_geographic()
    bbox =
    return KML.Region(
        self.make_level_of_detail(),
        KML.LatLonAltBox(
            *self.make_lat_lon_box(bbox)
        )
    )

    def make_network_link(self, tile_coords, visible=True):
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



class KMLMap:
    MIME_TYPE = "application/vnd.google-earth.kml+xml"

    def __init__(self, url_formatter=lambda x: x):
        """

        Args:
            url_formatter: Callback function for creating an absolute
             URL from a relative paths
        """
        self.url_formatter = url_formatter
        self.kml_doc = KML.Document()
        self.kml_root = KML.kml(self.kml_doc)

    def get_map_url(self, map, z=None, x=None, y=None):
        if z is None:
            # request root document
            return self.url_formatter("/maps/{}.kml".format(map.id))
        else:
            return self.url_formatter("/maps/{}/{}/{}/{}.kml".format(map.id, z, x, y))

    def add_elem(self, kml_elem):
        """Add an element to the KMLDocument"""
        self.kml_doc.append(kml_elem)

    def add_elems(self, kml_elems):
        """
        Add elements from an iterator.

        Args:
            kml_elems: any iterator containing KML elements.
                Can also be a KMLMap instance
        """
        for kml_elem in kml_elems:
            self.add_elem(kml_elem)

    def get_kml(self):
        """Return the KML Document as formatted kml/xml"""
        return etree.tostring(self.kml_root, pretty_print=True, xml_declaration=True)

    def __iter__(self):
        yield from self.kml_doc



class KMLMaster(KMLMap):
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
                        KML.href(self.get_map_url(map_s)),
                        KML.viewRefreshMode("onRegion")
                    ),
                    KML.visibility(0)
                )
            )


class KMLMapRoot(KMLMap):
    """Create root Document for an
    individual Map. Can be used as standalone KML
    to display that map only"""

    def __init__(self, mapsource, url_formatter):
        super().__init__(url_formatter)
        self.mapsource = mapsource

        z = mapsource.min_zoom
        n_tiles = 2 ** z
        r = 2 ** self.LOG_R
        n_regions = min(n_tiles, n_tiles/r)
        self.add_elem(KML.name("{} root".format(mapsource.name)))
        for x, y in griditer(0, 0, n_regions):
            self.add_elems(KMLRegion(z, x, y))


class KMLRegion(KMLMap):
    """Create a KML that displays the actual tiles
    as GroundOverlay and contains NetworkLinks
    to the next LevelOfDetail.

    A region contains a certain number of GroundOverlays and
    a certain number of NetworkLinks for a given zoom level.
    A Region is identified by it's tile in the top left corner
    and a zoom level.

    """

    def add_ground_overlay(self, tile_coord):
        pass

    def add_network_link(self):
        pass

    def __init__(self, mapsource, z, x, y, url_formatter, log_r=LOG_R):
        super().__init__(url_formatter)
        self.tile_coords = TileCoordinate(z, x, y)
        self.mapsource = mapsource

        rc = RegionCoordinate(z, x, y, log_r)

        self.add_elem(KML.name("DOC_{}_{}_{}".format(z, x, y)))

        for tc in rc.get_tiles():
            self.add_ground_overlay(tc)
        for rc_child in rc.zoom_in():
            self.add_network_link(rc_child)

