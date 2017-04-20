#!/usr/bin/env python3

from geos import app
import geos.mapsource
from geos.geos_web_tools import GeosWebUrlFormatter

app.config.from_object('geos.default_settings')

HOST = "geos-web.appspot.com"
PORT = 80

app.config['url_formatter'] = GeosWebUrlFormatter(HOST, PORT, 'https')
app.config['mapsources'] = geos.mapsource.load_maps('mapsources')
app.config['mapsources_powerup'] = geos.mapsource.load_maps('mapsources_powerup')
app.secret_key = 'no_critical_data_used'
