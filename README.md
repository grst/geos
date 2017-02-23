# Google Earth Overlay Server (GEOS)
This is a python-based server for creating Google Earth overlays 
of tiled maps. 

## Installation

### Requirements
GEOS is python3 only!

### Install GEOS through `pip`:
`pip3 install geos`

## Usage
```
usage: geos [-h] [-m MAPSOURCE] [-H HOST] [-P PORT]

optional arguments:
  -h, --help            show this help message and exit
  -m MAPSOURCE, --mapsource MAPSOURCE
                        path to the directory containing the mapsource files.
                        [default: integrated mapsources]
  -H HOST, --host HOST  Hostname of the Flask app [default localhost]
  -P PORT, --port PORT  Port for the Flask app [default 5000]

```

To try out *GEOS*, simply open a terminal, type `geos` and hit enter! A web server will start. 
Note, that by default, the webserver is only reachable locally. You can adjust this using the `-H` prameter.

Open your browser and navigate to the URL. A simple web page will open where you can download a KML Document containing all maps.
Per default, it only contains the [OSM Mapnik](https://wiki.openstreetmap.org/wiki/Mapnik) map.

In Google Earth, the KML file will appear in the 'places' pane. Activate the checkbox
of the map you want to display there: 

![](doc/ge-places.png)

Once the checkbox is activated, the mapoverlay should load.
Note, that some maps do not provide tiles below a certain zoom level.
In that case you have to zoom in for the tiles to load. 

## More maps! 
*GEOS* uses XML [Mapsource](http://mobac.sourceforge.net/wiki/index.php/Custom_XML_Map_Sources#Simple_custom_map_sources)
files, to tell the server where it can find the tiles. I started a collection of such mapsources in a
[dedicated Github repository](https://github.com/grst/mapsources).

You can specify a directory containing xml mapsources using the `-m` command line parameter.
*GEOS* will load all maps from that directory and put them into the kml file.

So, to start off, you can do the following: 
```
git clone git@github.com:grst/mapsources.git
geos -m mapsources
```

Of course, you can create your own maps, too! If you do so, it would be cool if you shared them,
 e.g. by creating a pull request to the [mapsources repo](https://github.com/grst/mapsources).

## Creating Mapsources
Essentially, the mapsources for *GEOS* are based on the [MOBAC Mapsource XML Format](http://mobac.sourceforge.net/wiki/index.php/Custom_XML_Map_Sources#Simple_custom_map_sources). 

A minimal Mapsource file for *GEOS* looks like this: 
```
<customMapSource>
    <name>Example Map</name>  <!-- Name of the map as displayed in Google Earth -->
    <minZoom>5</minZoom>      <!-- minimal zoom level supported by the web map -->
    <maxZoom>15</maxZoom>     <!-- maximal zoom level supported by the web map -->
    <!-- url: tells GEOS where to find the tiles. Tile URLs contain three 
    Parameters: zoom, x and y -->
    <url>http://example.com/map?zoom={$z}&amp;x={$x}&amp;y={$y}</url>
</customMapSource>
```

Additonally, *GEOS* currently supports the following optional parameters: 
```
    <id>example_id</id>                    <!-- unique map identifier. If not specified,
                                                the filename will be used as id -->
    <folder>europe/switzerland</folder>    <!-- use this tag to organize your maps in Folders 
                                                which will show up in Google Earth. If not specified,
                                                GEOS will try to obtain the folder from the directory 
                                                tree, in which the mapsources are saved in. --> 
    <region>                               <!-- Set map boundaries. No tiles will load outside -->
        <north>54.5</north>                <!-- Use geographic coordinates here.  --> 
        <south>40</south>
        <east>15</east>
        <west>5</west>
   </region>
```

## Aspirations
Can GEOS become a unified interface for converting, displaying and using web maps?
Like a web-based version of the seemingly old-fashioned [MOBAC](http://mobac.sourceforge.net)?

Imagine you can draw and measure on a map like in [Swisstopo](https://map.geo.admin.ch), download paper maps
as simple as with [nkart.no](http://www.nkart.no/) and create an offline map for your GPS device just as
with [MOBAC](http://mobac.sourceforge.net) for any map out there simply in your web browser.

## Contributing
If that sounds as awesome to you as it does to me, feel free to fork and create
pull requests or simply drop me a message.

## Alternatives
If you want to setup `geos` on a server, you might as well consider [MapProxy](https://mapproxy.org), which is much more professional but a bit more challenging to configure.
