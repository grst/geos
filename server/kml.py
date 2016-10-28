from pykml.factory import KML_ElementMaker as KML
from geometry import *
from lxml import etree

# TODO Documentation! Make clear that we distinguish between regionGrid and TileGrid
# TODO Knuth: "Code should read as if it was a piece of literature"
# TODO Unittesting
# TODO maxzoom

"""
it would proabably be more pythonic if
I removed all map specific functions from
KML Builder and turned them into module
level functions
"""

LOG_R = 0  # TODO, newly defined as log_2 GroundOverlays per row per Region (makes more sense)
MAX_LOD_PIXELS = -1
MIN_LOD_PIXELS = 128 * (2 ** LOG_R)


def kml_element_name(grid_coords, elem_id="KML"):
    return "_".join(str(x) for x in [elem_id, grid_coords.zoom, grid_coords.x, grid_coords.y])


def kml_lat_lon_box(geo_bb):
    """
    Create the north/south/east/west tags
    for a LatLonBox or LatLonAltBox Bounding Box

    Args:
        geo_bb: GeographicBB
    """
    return (
        KML.north(geo_bb.max.lat),
        KML.south(geo_bb.min.lat),
        KML.east(geo_bb.max.lon),
        KML.west(geo_bb.min.lon)
    )


def kml_lod(min_lod_pixels=MIN_LOD_PIXELS, max_lod_pixels=MAX_LOD_PIXELS):
    """Create the KML LevelOfDetail (LOD) Tag"""
    # TODO: min_lod_pixels should be dependent on tiles per row
    return KML.Lod(
        KML.minLodPixels(min_lod_pixels),
        KML.maxLodPixels(max_lod_pixels))


def kml_region(region_coords):
    """Create the KML Region tag with the appropriate
    geographic coordinates"""
    bbox = region_coords.geographic_bounds()
    return KML.Region(
        kml_lod(),
        KML.LatLonAltBox(
            *kml_lat_lon_box(bbox)
        )
    )


def kml_network_link(href, name=None, region_coords=None, visible=True):
    """
    Create the KML NetworkLink Tag for a
    certain Region in the RegionGrid.

    Args:
        region_coords: RegionCoordinate
        href: the href attribute of the NetworkLink
        visible: If true the network link will appear as 'visible'
            (i.e. checked) in Google Earth.

    Returns:
        KMLElement

    """
    nl = KML.NetworkLink()
    if name is None and region_coords is not None:
        name = kml_element_name(region_coords, "NL")
    if name is not None:
        nl.append(KML.name(name))
    if region_coords is not None:
        nl.append(kml_region(region_coords))
    if not visible:
        nl.append(KML.visibility(0))

    nl.append(KML.Link(
        KML.href(href), KML.viewRefreshMode("onRegion")))

    return nl


def kml_ground_overlay(tile_coords, tile_url):
    """
    Create a KML GroundOverlay for a certain
    TileCoordinate.

    Args:
        tile_coords: TileCoordinate
        tile_url: web-url to the actual tile image.

    Returns:
        KMLElement

    """
    return KML.GroundOverlay(
        KML.name(kml_element_name(tile_coords, "GO")),
        KML.drawOrder(tile_coords.zoom),
        KML.Icon(
            KML.href(tile_url)
        ),
        KML.LatLonBox(
            *kml_lat_lon_box(tile_coords.geographic_bounds())
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

    def get_map_url(self, map, grid_coords=None):
        if grid_coords is None:
            # request root document
            return self.url_formatter("/maps/{}.kml".format(map.id))
        else:
            return self.url_formatter(
                "/maps/{}/{}/{}/{}.kml".format(map.id, grid_coords.zoom,
                                               grid_coords.x, grid_coords.y))

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
        yield from self.kml_doc.iterchildren()


class KMLMaster(KMLMap):
    """Create a KML Master document that
    contains NetworkLinks to all Maps
    in the mapsource directory"""

    def __init__(self, mapsources, url_formatter):
        super().__init__(url_formatter)
        for map_s in mapsources:
            self.add_elem(
                kml_network_link(self.get_map_url(map_s), name=map_s.name, visible=False)
            )


class KMLMapRoot(KMLMap):
    """Create root Document for an
    individual Map. Can be used as standalone KML
    to display that map only"""

    def __init__(self, mapsource, url_formatter, log_r=LOG_R):
        super().__init__(url_formatter)
        self.mapsource = mapsource

        self.log_r = log_r
        z = max(mapsource.min_zoom, log_r)  # on zoom level 0, one cannot have more than one tile per region.
        n_tiles = 2 ** z
        r = 2 ** self.log_r
        n_regions = n_tiles//r
        assert n_tiles % r == 0
        self.add_elem(KML.name("{} root".format(mapsource.name)))
        for x, y in griditer(0, 0, n_regions):
            self.add_elems(KMLRegion(self.mapsource, z, x, y, self.url_formatter, self.log_r))


class KMLRegion(KMLMap):
    """Create a KML that displays the actual tiles
    as GroundOverlay and contains NetworkLinks
    to the next LevelOfDetail.

    A region contains a certain number of GroundOverlays and
    a certain number of NetworkLinks for a given zoom level.
    A Region is identified by it's tile in the top left corner
    and a zoom level.

    """

    def add_ground_overlay(self, tile_coords):
        tile_url = self.mapsource.get_tile_url(tile_coords.zoom, tile_coords.x, tile_coords.y)
        self.add_elem(kml_ground_overlay(tile_coords, tile_url))

    def add_network_link(self, region_coords):
        href = self.get_map_url(self.mapsource, region_coords)
        self.add_elem(kml_network_link(href, region_coords=region_coords))

    def __init__(self, mapsource, z, x, y, url_formatter, log_r=LOG_R):
        super().__init__(url_formatter)
        self.mapsource = mapsource

        rc = RegionCoordinate(z, x, y, log_r)

        self.add_elem(KML.name(kml_element_name(rc, "DOC")))

        for tc in rc.get_tiles():
            self.add_ground_overlay(tc)
        for rc_child in rc.zoom_in():
            self.add_network_link(rc_child)

