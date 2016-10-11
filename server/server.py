from flask import Flask, Response, render_template
import argparse
import os
import mapsource
from kml import KMLMaster, KMLRegion

app = Flask(__name__)


@app.route('/')
def main():
    return render_template("index.html")


@app.route("/kml-master.kml")
def kml_master():
    maps = mapsource.load_maps('/home/sturm/repos/other/geoverlay/server/mapsources')
    map = maps['osm.xml']
    kml_doc = KMLMaster([map])
    return Response(kml_doc.get_kml(), mimetype=kml_doc.MIME_TYPE)


@app.route("/maps/<map_source>/<int:z>/<int:x>/<int:y>.kml")
def kml_region(map_source, z, x, y):
    maps = mapsource.load_maps('/home/sturm/repos/other/geoverlay/server/mapsources')
    map = maps[map_source]
    kml_doc = KMLRegion(map, z, x, y)

    return Response(kml_doc.get_kml(), mimetype=kml_doc.MIME_TYPE)


if __name__ == '__main__':
    # argp = argparse.ArgumentParser("KML Overlay generator. ")
    # argp.add_argument("-m", "--mapsource", required=False,
    #                   default="{}/mapsources".format(os.path.realpath(__file__)),
    #                   help="path to the directory containing the mapsource files.")
    #
    # args = argp.parse_args()

    app.run()
