from flask import Flask, Response, render_template, g
import argparse
import mapsource
import pkg_resources
from kml import *


app = Flask(__name__)


def kml_response(kml_map):
    """
    Args:
        kml_map (KMLMap): KMLMap object

    Returns:
        Response: a Flask Response with proper MIME-type.

    """
    return Response(kml_map.get_kml(), mimetype=kml_map.MIME_TYPE)


@app.route('/')
def main():
    # TODO overview of maps
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


def run_app():
    argp = argparse.ArgumentParser("KML Overlay generator. ")
    argp.add_argument("-m", "--mapsource", required=False,
                      default=pkg_resources.resource_filename(__name__, "mapsources"),
                      help="path to the directory containing the mapsource files.")
    args = argp.parse_args()

    app.config.from_object('default_settings')
    app.config['url_formatter'] = URLFormatter(app.config["SERVER_NAME"],
                                               app.config["PREFERRED_URL_SCHEME"])
    app.config['mapsources'] = mapsource.load_maps(args.mapsource)
    app.run()

if __name__ == '__main__':
    run_app()

