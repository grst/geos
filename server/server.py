from flask import Flask, Response
import argparse
import os
import mapsource
from pykml.factory import KML_ElementMaker as KML
from lxml import etree

app = Flask(__name__)
SERVER_HOST = "127.0.0.1:5000"


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route("/kml-master.kml")
def kml_master():
    maps = mapsource.load_maps('/home/sturm/repos/other/geoverlay/server/mapsources')
    map = maps['osm.xml']
    kml_doc = KML.kml(
        KML.NetworkLink(
            KML.name(map.name),
            KML.Link(
                KML.href("http://{}/maps/{}/15/0/0".format(SERVER_HOST, map.id))
            )
        )
    )
    return Response(etree.tostring(kml_doc, pretty_print=True), mimetype="application/vnd.google-earth.kml+xml")


@app.route("/maps/<mapsource>/<int:z>/<int:x>/<int:y>")
def kml_region(mapsource, z, x, y):
    pass


if __name__ == '__main__':
    # argp = argparse.ArgumentParser("KML Overlay generator. ")
    # argp.add_argument("-m", "--mapsource", required=False,
    #                   default="{}/mapsources".format(os.path.realpath(__file__)),
    #                   help="path to the directory containing the mapsource files.")
    #
    # args = argp.parse_args()

    app.run()
