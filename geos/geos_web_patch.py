from geos.server import index, kml_master, kml_map_root, kml_region
from geos.geos_web_tools import KEY, enable_powerup
from geos import app


@app.route('/{}'.format(KEY))
def powerup_maps():
    enable_powerup()
    return index()


@app.route("/{}/kml-master.kml".format(KEY))
def pu_kml_master():
    enable_powerup()
    return kml_master()


@app.route("/{}/maps/<map_source>.kml".format(KEY))
def pu_kml_map_root(map_source):
    """KML for a given map"""
    enable_powerup()
    return kml_map_root(map_source)


@app.route("/{}/maps/<map_source>/<int:z>/<int:x>/<int:y>.kml".format(KEY))
def pu_kml_region(map_source, z, x, y):
    enable_powerup()
    return kml_region(map_source, z, x, y)


