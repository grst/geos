#!/usr/bin/env python3

from geos import app
import geos.mapsource
from geos.kml import URLFormatter

HOST = "geos-web.appspot.com"
PORT = 80

app.config['url_formatter'] = URLFormatter(HOST, PORT, 'https')
app.config['mapsources'] = geos.mapsource.load_maps('mapsources')
