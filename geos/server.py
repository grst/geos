from flask import Response, render_template, send_file
from geos.kml import *
from geos.print import print_map
from geos import app


def kml_response(kml_map):
    """
    Args:
        kml_map (KMLMap): KMLMap object

    Returns:
        Response: a Flask Response with proper MIME-type.

    """
    return Response(kml_map.get_kml(), mimetype=kml_map.MIME_TYPE)


@app.route('/')
def index():
    tile_urls = {
        map_source.id : map_source.tile_url.replace("$", "") for id, map_source in app.config["mapsources"].items()
    }
    return render_template("index.html", tile_urls=tile_urls)


@app.route("/mapsources.json")
def map_sources():
    pass


@app.route('/ol')
def openlayers():
    return render_template("openlayers.html")


@app.route('/print/<map_source>/<x>/<y>/map.pdf')
def map_to_pdf(map_source, x, y):
    """

    Args:
        map_source:
        lon: mercator (EPSG:4326) x
        lat: mercator (EPSG:4326) y

    Returns:

    """
    map_source = app.config["mapsources"][map_source]
    pdf_file = print_map(map_source, float(x), float(y), format='pdf')
    return send_file(pdf_file,
                     attachment_filename="map.pdf",
                     as_attachment=True)


@app.route("/kml-master.kml")
def kml_master():
    """KML master document for loading all maps in Google Earth"""
    kml_doc = KMLMaster(app.config["url_formatter"], app.config["mapsources"].values())
    return kml_response(kml_doc)


@app.route("/maps/<map_source>.kml")
def kml_map_root(map_source):
    """KML for a given map"""
    map = app.config["mapsources"][map_source]
    kml_doc = KMLMapRoot(app.config["url_formatter"], map, app.config["LOG_TILES_PER_ROW"])
    return kml_response(kml_doc)


@app.route("/maps/<map_source>/<int:z>/<int:x>/<int:y>.kml")
def kml_region(map_source, z, x, y):
    """KML region fetched by a Google Earth network link. """
    map = app.config["mapsources"][map_source]
    kml_doc = KMLRegion(app.config["url_formatter"], map, app.config["LOG_TILES_PER_ROW"],
                        z, x, y)
    return kml_response(kml_doc)
