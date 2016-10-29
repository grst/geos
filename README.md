# Google Earth Overlay Server (GEOS)
This is a python based server for creating Google Earth overlays 
of tiled maps. 

## Installation
`pip install geos`

## Usage
```
geos -m path/to/mapsources
```
Will start a webserver. Open your browser and navigate to the URL. A simple web page
will open where you can download a KML Document containing links to all maps
in the mapsource directory. 

In Google earth, the KML file will appear in the 'places' pane. Activate the checkbox
of the map you want to display there: 

![](doc/ge-places.png)

## Creating Mapsources
http://mobac.sourceforge.net/wiki/index.php/Custom_XML_Map_Sources#Simple_custom_map_sources

## Contributing
