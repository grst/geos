# Google Earth Overlay Server (GEOS)
This is a python-based server for creating Google Earth overlays 
of tiled maps. 

## Installation
`pip install geos`

## Usage
`geos [-h] [-m MAPSOURCE] [-H HOST] [-P PORT]`

To try out *GEOS*, simply open a terminal, type `geos` and hit enter! A webserver will start. Open your browser and navigate to the URL. A simple web page will open where you can download a KML Document containing all maps. Per default, it only contains the [OSM Mapnik](https://wiki.openstreetmap.org/wiki/Mapnik) map. 

In Google Earth, the KML file will appear in the 'places' pane. Activate the checkbox
of the map you want to display there: 

![](doc/ge-places.png)

Once the checkbox is activated, the mapoverlay should load.
Note, that some maps do not provide tiles below a certain zoom level.
In that case you have to zoom in for the tiles to load. 

## More maps! 
*GEOS* uses XML [Mapsource](http://mobac.sourceforge.net/wiki/index.php/Custom_XML_Map_Sources#Simple_custom_map_sources
) files, to tell the server where it can find the tiles. I started a collection of such mapsources in a [dedicated Github repository](https://github.com/grst/mapsources). 

You can specify a directory containing xml mapsources using the `-m` command line parameter. *GEOS* will load all maps from that directory and put them into the kml file. 

So, to start off, you can do the following: 
```
git clone git@github.com:grst/mapsources.git
geos -m mapsources
```

Of course, you can create your own maps, too! If you do so, it would be cool if you shared them, e.g. by creating a pull request to the [mapsources repo](https://github.com/grst/mapsources). 

## Creating Mapsources
http://mobac.sourceforge.net/wiki/index.php/Custom_XML_Map_Sources#Simple_custom_map_sources

## Contributing
