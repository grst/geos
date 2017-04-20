#!/usr/bin/env python3
from main import * 

HOST = 'localhost'
PORT = 8080

app.config['url_formatter'] = GeosWebUrlFormatter(HOST, PORT, 'http')

if __name__ == '__main__':
	app.run(port=PORT, host=HOST)
