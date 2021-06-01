## Installation

### Using Python
_GEOS_ is python3 only. If you don't have python, I recommend downloading
[Anaconda Python](https://www.continuum.io/downloads).

Usually, it's easiest to install _GEOS_ through `pip`:

```sh
pip install geos
```

Alternatively, you can install _GEOS_ from the github sources:
```sh
git clone https://github.com/grst/geos.git
cd geos
pip install -e geos
```

To try out _GEOS_, simply open a terminal, type `geos` and hit enter! A web server will start.

### Using Docker-compose

If you prefer, you can install Docker compose and avoid additional instalation steps.

1. Create a `docker-compose.yml` file using the following template :
   ```docker-compose
   version: '3.7'
   services:
     geos:
       build: https://github.com/grst/geos.git
       container_name: geos
       ports:
	 - '<host_port>:5000'
       volumes:
	 - <host_mapsources_directory>:/mapsources
       command: geos --host 0.0.0.0 --display-host <host_address> --mapsource /mapsources
   ```

   You will have to substitute the following variables with values that are relevant to your host machine :

   - `<host_port>` : Port used for accessing _GEOS_ on the host machine <br/>
     For example, `5000`
   - `<host_mapsources_directory>` : Path to the `mapsources` directory on the host machine <br/>
     For example `./mapsources` <br/>
     Don't worry if you don't have any mapsources yet.
   - `<host_address>` : adress of the host machine <br/>
     For example, `192.168.0.1`, `localhost`, or `geos.example.com` <br/>
     On Linux systems, the host machine's IP address can be found by running `ip route get 1| sed 's/.* src \([0-9.]*\) .*/\1/;q'`.

2. Start _GEOS_ by issuing
   ```sh
   docker-compose up -d
   ```
   This command will take care of building the _GEOS_ image if it does not exist locally.

3. Open _GEOS_ in a browser at `http://<host_address>:<host_port>`.

4. You can stop _GEOS_ by issuing
   ```sh
   docker-compose down
   ```

## Usage
```
usage: geos [-h] [-m MAPSOURCE] [-H HOST] [-P PORT]
            [--display-host DISPLAY_HOST] [--display-port DISPLAY_PORT]
            [--display-scheme DISPLAY_SCHEME]

optional arguments:
  -h, --help            show this help message and exit
  -m MAPSOURCE, --mapsource MAPSOURCE
                        path to the directory containing the mapsource files.
                        [default: integrated mapsources]
  -H HOST, --host HOST  Hostname of the Flask app [default localhost]
  -P PORT, --port PORT  Port for the Flask app [default 5000]
  --display-host DISPLAY_HOST
                        Hostname used for self-referencing links [defaults to
                        Flask hostname]
  --display-port DISPLAY_PORT
                        Port used for self-referencing links [defaults to
                        Flask port]
  --display-scheme DISPLAY_SCHEME
                        URI-scheme used for self-referencing links [default
                        http]
```

Note, that by default, the webserver is only reachable locally. You can adjust this using the `-host` parameter. If you use _GEOS_ with a public url, e.g. `http://geos.example.com`, you can adjust the public hostname, port and scheme using the `--display-*` arguments. 

Open your browser and navigate to the URL. A web page will displaying a map and a menu bar.
You can use the menu bar to choose between maps. Per default, it only contains the
[OSM Mapnik](https://wiki.openstreetmap.org/wiki/Mapnik).
From the menu bar, you can also choose tools to measure, draw and print maps.

![geos-web](_static/geos_web.png)

### Open in Google Earth
Choose *"Open in Google Earth (KML)"* from the menu bar to download a KML file which you can open in Google Earth.
The KML file will appear in the 'places' pane. Activate the checkbox
of the map you want to display there:

![](_static/ge-places.png)

Once the checkbox is activated, the mapoverlay should load.
Note, that some maps do not provide tiles below a certain zoom level.
In that case you have to zoom in for the tiles to load.

## More maps!
_GEOS_ uses XML [Mapsource](http://mobac.sourceforge.net/wiki/index.php/Custom_XML_Map_Sources#Simple_custom_map_sources)
files, to tell the server where it can find the tiles. I started a collection of such mapsources in a
[dedicated Github repository](https://github.com/grst/mapsources).

You can specify a directory containing xml mapsources using the `-m` command line parameter.
_GEOS_ will load all maps from that directory and put them into the kml file.

So, to start off, you can do the following:
```
git clone git@github.com:grst/mapsources.git
geos -m mapsources
```

Of course, you can create your own maps, too! If you do so, it would be cool if you shared them,
 e.g. by creating a pull request to the [mapsources repo](https://github.com/grst/mapsources).

## Creating Mapsources
Essentially, the mapsources for _GEOS_ are based on the [MOBAC Mapsource XML Format](http://mobac.sourceforge.net/wiki/index.php/Custom_XML_Map_Sources#Simple_custom_map_sources).

A minimal Mapsource file for _GEOS_ looks like this:
```xml
<customMapSource>
    <name>Example Map</name>  <!-- Name of the map as displayed in Google Earth -->
    <minZoom>5</minZoom>      <!-- minimal zoom level supported by the web map -->
    <maxZoom>15</maxZoom>     <!-- maximal zoom level supported by the web map -->
    <!-- url: tells _GEOS_ where to find the tiles. Tile URLs contain three
    Parameters: zoom, x and y -->
    <url>http://example.com/map?zoom={$z}&amp;x={$x}&amp;y={$y}</url>
</customMapSource>
```

Additonally, _GEOS_ currently supports the following optional parameters:
```xml
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

### Multi Layer Mapsources
_GEOS_ supports Mapsources which consist of multiple layers. Such a file looks as follows:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<customMultiLayerMapSource>
   <name>Custom OSM Mapnik with Hills (Ger)</name>
   <layers>
      <customMapSource>
         <name>Custom OSM Mapnik</name>
         <minZoom>0</minZoom>
         <maxZoom>18</maxZoom>
         <url>http://tile.openstreetmap.org/{$z}/{$x}/{$y}.png</url>
      </customMapSource>
      <customMapSource>
         <name>cycling trails</name>
         <minZoom>0</minZoom>
         <maxZoom>18</maxZoom>
         <url>https://tile.waymarkedtrails.org/cycling/{$z}/{$x}/{$y}.png</url>
       </customMapSource>
   </layers>
</customMultiLayerMapSource>
```
