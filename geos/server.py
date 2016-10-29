from flask import Response, render_template
from geos.kml import *
from geos import app

# todo pip
# todo fix maps


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
    return render_template("index.html")


@app.route("/kml-master.kml")
def kml_master():
    kml_doc = KMLMaster(app.config["url_formatter"], app.config["mapsources"].values())
    return kml_response(kml_doc)


@app.route("/maps/<map_source>.kml")
def kml_map_root(map_source):
    map = app.config["mapsources"][map_source]
    kml_doc = KMLMapRoot(app.config["url_formatter"], map, app.config["LOG_TILES_PER_ROW"])
    return kml_response(kml_doc)


@app.route("/maps/<map_source>/<int:z>/<int:x>/<int:y>.kml")
def kml_region(map_source, z, x, y):
    map = app.config["mapsources"][map_source]
    kml_doc = KMLRegion(app.config["url_formatter"], map, app.config["LOG_TILES_PER_ROW"],
                        z, x, y)
    return kml_response(kml_doc)
