# Google Earth Overlay Server (GEOS)
This is a python-based server for creating Google Earth overlays 
of tiled maps. 

## Installation
`pip install geos`

## Usage

Simply open a terminal, type `geos` and hit enter! A webserver will start. Open your browser and navigate to the URL.
A simple web page will open where you can download a KML Document containing links to all maps
in the mapsource directory. 

In Google Earth, the KML file will appear in the 'places' pane. Activate the checkbox
of the map you want to display there: 

![](doc/ge-places.png)

Once the checkbox is activated, the mapoverlay should load.
Note, that some maps do not provide tiles below a certain zoom level.
In that case you have to zoom in for the tiles to load. 

## Creating Mapsources
http://mobac.sourceforge.net/wiki/index.php/Custom_XML_Map_Sources#Simple_custom_map_sources

## Contributing
