from geos import app
import argparse
import geos.mapsource
import pkg_resources
from geos.kml import URLFormatter


def run_app(default_host="127.0.0.1", default_port=5000):
    argp = argparse.ArgumentParser("geos")
    argp.add_argument("-m", "--mapsource", required=False,
                      default=pkg_resources.resource_filename("geos", "mapsources"),
                      help="path to the directory containing the mapsource files. [default: integrated mapsources]")
    argp.add_argument("-H", "--host", required=False,
                      help="Hostname of the Flask app [default {}]".format(default_host),
                      default=default_host)
    argp.add_argument("-P", "--port", required=False,
                      help="Port for the Flask app [default {}]".format(default_port),
                      default=default_port)

    args = argp.parse_args()

    app.config.from_object('geos.default_settings')
    app.config['url_formatter'] = URLFormatter(app.config["SERVER_NAME"],
                                               app.config["PREFERRED_URL_SCHEME"])
    app.config['mapsources'] = geos.mapsource.load_maps(args.mapsource)

    app.run(
        host=args.host,
        port=int(args.port)
    )

if __name__ == "__main__":
    run_app()