from flask import Flask, Response, render_template, g
import argparse
import mapsource
import pkg_resources
from kml import KMLMaster, KMLRegion

# default_settings = {
#     "SERVER_NAME":  "localhost:5000",
#     "DEBUG": True
# }

app = Flask(__name__)


def abs_url(rel_url):
    """Create n absolute url with respect to SERVER_NAME"""
    rel_url = rel_url.lstrip("/")
    return "{}://{}/{}".format(app.config["PREFERRED_URL_SCHEME"],
                               app.config["SERVER_NAME"], rel_url)


@app.route('/')
def main():
    return render_template("index.html")


@app.route("/kml-master.kml")
def kml_master():
    kml_doc = KMLMaster(app.config["mapsources"].values(), url_formatter=abs_url)
    return Response(kml_doc.get_kml(), mimetype=kml_doc.MIME_TYPE)


@app.route("/maps/<map_source>/<int:z>/<int:x>/<int:y>.kml")
def kml_region(map_source, z, x, y):
    map = app.config["mapsources"][map_source]
    kml_doc = KMLRegion(map, z, x, y, url_formatter=abs_url)
    return Response(kml_doc.get_kml(), mimetype=kml_doc.MIME_TYPE)

def run_app():
    argp = argparse.ArgumentParser("KML Overlay generator. ")
    argp.add_argument("-m", "--mapsource", required=False,
                      default=pkg_resources.resource_filename(__name__, "mapsources"),
                      help="path to the directory containing the mapsource files.")
    args = argp.parse_args()

    app.config.from_object('default_settings')
    app.config['mapsources'] = mapsource.load_maps(args.mapsource)
    app.run()

if __name__ == '__main__':
    run_app()