KEY = 'powerup42'
from flask import session
from geos.kml import URLFormatter
from geos import app


def enable_powerup():
    session["powerup"] = True


def has_powerup():
    return 'powerup' in session


def get_mapsources():
    if has_powerup():
        return app.config["mapsources_powerup"]
    else:
        return app.config["mapsources"]


class GeosWebUrlFormatter(URLFormatter):
    def __init__(self, host, port, url_scheme="http"):
        self.host = host
        self.port = port
        self.url_scheme = url_scheme

    def get_key(self):
        return '{}/'.format(KEY) if has_powerup() else ''

    def get_abs_url(self, rel_url):
        """
        Create an absolute url from a relative one.

        >>> url_formatter = URLFormatter("example.com", 80)
        >>> url_formatter.get_abs_url("kml_master.kml")
        'http://example.com:80/kml_master.kml'
        """
        rel_url = rel_url.lstrip("/")
        return "{}://{}:{}/{}{}".format(self.url_scheme, self.host, self.port, self.get_key(), rel_url)

    def get_map_root_url(self, mapsource):
        return self.get_abs_url("/maps/{}.kml".format(mapsource.id))

    def get_map_url(self, mapsource, grid_coords):
        """ Get URL to a map region. """
        return self.get_abs_url(
                "/maps/{}/{}/{}/{}.kml".format(mapsource.id, grid_coords.zoom,
                                               grid_coords.x, grid_coords.y))