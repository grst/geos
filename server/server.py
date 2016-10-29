#!/usr/bin/env python3

from flask import Flask, Response, render_template
import argparse
import mapsource
import pkg_resources
from kml import *

# todo pip
# todo fix maps

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


def run_app(default_host="127.0.0.1", default_port=5000):
    argp = argparse.ArgumentParser("GEOS. The Google Earth Overlay Server. ")
    argp.add_argument("-m", "--mapsource", required=False,
                      default=pkg_resources.resource_filename(__name__, "mapsources"),
                      help="path to the directory containing the mapsource files.")
    argp.add_argument("-H", "--host", required=False,
                      help="Hostname of the Flask app [default {}]".format(default_host),
                      default=default_host)
    argp.add_argument("-P", "--port", required=False,
                      help="Port for the Flask app [default {}]".format(default_port),
                      default=default_port)

    # Two options useful for debugging purposes, but
    # a bit dangerous so not exposed in the help message.
    argp.add_argument("-d", "--debug", required=False,
                      action="store_true", dest="debug", help=argparse.SUPPRESS)
    argp.add_argument("-p", "--profile", required=False,
                      action="store_true", dest="profile", help=argparse.SUPPRESS)

    args = argp.parse_args()

    # If the user selects the profiling option, then we need
    # to do a little extra setup
    if args.profile:
        from werkzeug.contrib.profiler import ProfilerMiddleware

        app.config['PROFILE'] = True
        app.wsgi_app = ProfilerMiddleware(app.wsgi_app,
                                          restrictions=[30])
        args.debug = True

    app.config.from_object('default_settings')
    app.config['url_formatter'] = URLFormatter(app.config["SERVER_NAME"],
                                               app.config["PREFERRED_URL_SCHEME"])
    app.config['mapsources'] = mapsource.load_maps(args.mapsource)

    app.run(
        debug=args.debug,
        host=args.host,
        port=int(args.port)
    )


if __name__ == '__main__':
    run_app()
