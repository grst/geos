from flask import Flask, Response
import argparse
import os
import mapsource
from pykml.factory import KML_ElementMaker as KML
from lxml import etree
from geometry import *

app = Flask(__name__)
SERVER_HOST = "127.0.0.1:5000"
KML_LOD = KML.Lod(
    KML.minLodPixels(128),
    KML.maxLodPixels(-1)
)


@app.route('/')
def hello_world():
    return 'Hello World!'


def get_map_url(map, z, x, y):
    return "http://{}/maps/{}/{}/{}/{}.kml".format(SERVER_HOST, map.id, z, x, y)


@app.route("/kml-master.kml")
def kml_master():
    maps = mapsource.load_maps('/home/sturm/repos/other/geoverlay/server/mapsources')
    map = maps['osm.xml']
    kml_doc = KML.kml(
        KML.NetworkLink(
            KML.name(map.name),
            KML.Link(
                KML.href(get_map_url(map, 0, 0, 0)),
                KML.viewRefreshMode("onRegion")
            )
        )
    )
    return Response(etree.tostring(kml_doc, pretty_print=True), mimetype="application/vnd.google-earth.kml+xml")


def lat_lon_box(geo_bb):
    return (
        KML.north(geo_bb.max.lat),
        KML.south(geo_bb.min.lat),
        KML.east(geo_bb.max.lon),
        KML.west(geo_bb.min.lon)
    )


def network_link(map, tile_coords, quad):
    assert quad in ['ne', 'se', 'sw', 'nw']
    # geo_center = geo_bb.center()
    # # GeographicBB(min_lon, min_lat, max_lon, max_lat)
    # if quad == "nw":
    #     geo_bb_new = GeographicBB(geo_bb.min.lon, geo_bb.min.lat,
    #                               geo_center.lon, geo_center.lat)
    # elif quad == "ne":
    #     geo_bb_new = GeographicBB(geo_center.lon, geo_bb.min.lat,
    #                               geo_bb.max.lon, geo_center.lat)
    # elif quad == "sw":
    #     geo_bb_new = GeographicBB(geo_bb.min.lon, geo_center.lat,
    #                               geo_bb.max.lat, geo_center.lon)
    # elif quad == "se":
    #     geo_bb_new = GeographicBB(geo_center.lon, geo_center.lat,
    #                               geo_bb.max.lon, geo_bb.max.lat)

    z = tile_coords.zoom + 1
    x = tile_coords.x
    y = tile_coords.y
    if quad == "nw":
        pass
    elif quad == "ne":
        x += 1
    elif quad == "se":
        x += 1
        y += 1
    elif quad == "sw":
        y += 1

    new_tile_coords = TileCoordinate(z, x, y)

    nl = KML.NetworkLink(
        KML.name("{}_{}_{}_{}".format(quad, z, x, y)),
        KML.Region(
            KML_LOD,
            *lat_lon_box(new_tile_coords.geographic_bounds())
        ),
        KML.Link(
            KML.href(get_map_url(map, z, x, y)),
            KML.viewRefreshMode("onRegion")
        )
    )
    return nl


@app.route("/maps/<map_source>/<int:z>/<int:x>/<int:y>.kml")
def kml_region(map_source, z, x, y):
    maps = mapsource.load_maps('/home/sturm/repos/other/geoverlay/server/mapsources')
    tile_coords = TileCoordinate(z, x, y)
    bbox = tile_coords.geographic_bounds()
    map = maps['osm.xml']
    kml_doc = KML.kml(
        KML.Document(
            KML.name("doc_{}_{}_{}".format(z, x, y)),
            KML.Region(
                KML_LOD,
                KML.LatLonAltBox(
                    *lat_lon_box(bbox)
                )
            ),
            network_link(map, tile_coords, "ne"),
            network_link(map, tile_coords, "se"),
            network_link(map, tile_coords, "sw"),
            network_link(map, tile_coords, "nw"),
            KML.GroundOverlay(
                KML.name("ge_{}_{}_{}".format(z, x, y)),
                KML.drawOrder(z),
                KML.Icon(
                    KML.href(map.get_tile_url(z, x, y))
                ),
                KML.LatLonBox(
                    *lat_lon_box(bbox)
                ),
            )
        )
    )
    # if z > 3:
    #     # temporary recursion limit.
    #     kml_doc = KML.Document()
    return Response(etree.tostring(kml_doc, pretty_print=True), mimetype="application/vnd.google-earth.kml+xml")


if __name__ == '__main__':
    # argp = argparse.ArgumentParser("KML Overlay generator. ")
    # argp.add_argument("-m", "--mapsource", required=False,
    #                   default="{}/mapsources".format(os.path.realpath(__file__)),
    #                   help="path to the directory containing the mapsource files.")
    #
    # args = argp.parse_args()

    app.run()
