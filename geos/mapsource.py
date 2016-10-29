import xml.etree.ElementTree
import itertools
import os
from pprint import pprint
from geos.geometry import GeographicBB
import re

F_SEP = "/"  # folder separator in mapsources (not necessarily == os.sep)


def load_maps(maps_dir):
    maps_dir = os.path.abspath(maps_dir)
    maps = {}
    for root, dirnames, filenames in os.walk(maps_dir):
        for filename in filenames:
            if filename.endswith(".xml"):
                xml_file = os.path.join(root, filename)
                map = MapSource.from_xml(xml_file, maps_dir)
                if map.id in maps:
                    raise MapSourceException("duplicate map id: {} in file {}".format(map.id, xml_file))
                else:
                    maps[map.id] = map
    return maps


def walk_mapsources(mapsources, root=""):
    """
    like os.walk, only for the paths saved in the mapsources.
    Args:
        mapsources:

    Yield:
        (root, foldernames, maps)

    >>> mapsources = load_maps("test/mapsources")
    >>> pprint([x for x in walk_mapsources(mapsources.values())])
    [('',
      ['asia', 'europe'],
      [<MapSource: osm1 (root 1), url:http://tile.openstreetmap.org/{$z}/{$x}/{$y}.png, min_zoom:5, max_zoom:18>,
       <MapSource: osm10 (root 2), url:http://tile.openstreetmap.org/{$z}/{$x}/{$y}.png, min_zoom:5, max_zoom:18>]),
     ('/asia',
      [],
      [<MapSource: osm6 (asia), url:http://tile.openstreetmap.org/{$z}/{$x}/{$y}.png, min_zoom:5, max_zoom:18>]),
     ('/europe',
      ['france', 'germany', 'switzerland'],
      [<MapSource: osm4 (eruope 1), url:http://tile.openstreetmap.org/{$z}/{$x}/{$y}.png, min_zoom:1, max_zoom:18>]),
     ('/europe/france',
      [],
      [<MapSource: osm2 (europe/france 1), url:http://tile.openstreetmap.org/{$z}/{$x}/{$y}.png, min_zoom:5, max_zoom:18>,
       <MapSource: osm3 (europe/france 2), url:http://tile.openstreetmap.org/{$z}/{$x}/{$y}.png, min_zoom:1, max_zoom:18>,
       <MapSource: osm5 (europe/france 3), url:http://tile.openstreetmap.org/{$z}/{$x}/{$y}.png, min_zoom:5, max_zoom:18>]),
     ('/europe/germany',
      [],
      [<MapSource: osm7 (europe/germany 1), url:http://tile.openstreetmap.org/{$z}/{$x}/{$y}.png, min_zoom:5, max_zoom:18>,
       <MapSource: osm8 (europe/germany 2), url:http://tile.openstreetmap.org/{$z}/{$x}/{$y}.png, min_zoom:5, max_zoom:18>]),
     ('/europe/switzerland',
      [],
      [<MapSource: osm9 (europe/switzerland), url:http://tile.openstreetmap.org/{$z}/{$x}/{$y}.png, min_zoom:5, max_zoom:18>])]

    """
    def get_first_folder(path):
        """
        Get the first folder in a path
        > get_first_folder("europe/switzerland/bs")
        europe
        """
        path = path[len(root):]
        path = path.lstrip(F_SEP)
        return path.split(F_SEP)[0]

    path_tuples = sorted(((get_first_folder(m.folder), m) for m in mapsources), key=lambda x: x[0])
    groups = {k: [x for x in g] for k, g in itertools.groupby(path_tuples, lambda x: x[0])}
    folders = sorted([x for x in groups.keys() if x != ""])
    mapsources = sorted([t[1] for t in groups.get("", [])], key=lambda x: x.id)
    yield (root, folders, mapsources)
    for fd in folders:
        yield from walk_mapsources([t[1] for t in groups[fd]], F_SEP.join([root, fd]))


class MapSourceException(Exception):
    pass


class MapSource(object):
    """
    object storing all information on how to access the tiles
    of a certain map
    """

    def __init__(self, id, name, tile_url, folder="", bbox=None, min_zoom=1, max_zoom=17):
        """

        Args:
            id (str): unique identifier (e.g. filename)
            name (str): display name
            tile_url (str): url of the format "http://mymap.xyz/tiles/{$z}/{$x}/{$y}"
             where z is zoom level, and x and y the tile coordinates respectively.
            folder (str): folder to organize the map in (e.g. /europe/germany)
            bbox (GeographicBB): bounding box, only load tiles within
            min_zoom (int): minimal allowed zoom level of the map
            max_zoom (int): maximal allowed zoom level of the map

        >>> ms = MapSource.from_xml("mapsources/osm.xml")
        >>> ms.name
        'OSM Mapnik'
        >>> ms.min_zoom
        0
        >>> ms.max_zoom
        18
        >>> ms.tile_url
        'http://tile.openstreetmap.org/{$z}/{$x}/{$y}.png'
        """
        self.id = id
        self.name = name
        self.tile_url = tile_url
        self.folder = folder
        self.bbox = bbox
        self.min_zoom = min_zoom
        self.max_zoom = max_zoom

    def get_tile_url(self, zoom, x, y):
        """
        Fill the placeholders of the tile url with zoom, x and y.

        >>> ms = MapSource.from_xml("mapsources/osm.xml")
        >>> ms.get_tile_url(42, 43, 44)
        'http://tile.openstreetmap.org/42/43/44.png'
        """
        return self.tile_url.format(**{"$z": zoom, "$x": x, "$y": y})

    @staticmethod
    def parse_xml_boundary(xml_region):
        """
        Get the geographic bounds from an XML element

        Args:
            xml_region (Element): The <region> tag as XML Element

        Returns:
            GeographicBB:
        """
        try:
            bounds = {}
            for boundary in xml_region.getchildren():
                bounds[boundary.tag] = float(boundary.text)
            bbox = GeographicBB(min_lon=bounds["west"], max_lon=bounds["east"],
                                min_lat=bounds["south"], max_lat=bounds["north"])
            return bbox
        except (KeyError, ValueError):
            raise MapSourceException("region boundaries are invalid. ")

    @staticmethod
    def from_xml(xml_path, mapsource_prefix=""):
        """
        Create a MapSource object from a MOBAC
        mapsource xml.

        Args:
            xml_path: path to the MOBAC mapsource xml file.
            mapsource_prefix: root path of the mapsource folder.
              Used to determine relative path within the maps
              directory.

        Note:
            The Information is read from the xml
            <id>, <folder>, <name>, <url>, <minZoom>, <maxZoom> tags. If <id> is
            not available it defaults to the xml file basename. If <folder> is not available
            if defaults to the folder of the xml file with the `mapsource_prefix` removed.

        Returns:
            MapSource object.

        Raises:
            MapSourceException: when the xml file could not be parsed properly.

        """
        xmldoc = xml.etree.ElementTree.parse(xml_path).getroot()
        attrs = {}
        for elem in xmldoc.getchildren():
            attrs[elem.tag] = elem

        try:
            # id defaults to filename
            map_id = attrs['id'].text if 'id' in attrs else os.path.splitext(os.path.basename(xml_path))[0]
            # folder defaults to relative path.
            map_folder = attrs['folder'].text if 'folder' in attrs else re.sub("^" + re.escape(mapsource_prefix),
                                                                          "", os.path.dirname(xml_path))
            bbox = MapSource.parse_xml_boundary(attrs["region"]) if "region" in attrs else None
            map_folder = "" if map_folder is None else map_folder

            return MapSource(map_id, attrs['name'].text, attrs['url'].text, map_folder, bbox=bbox,
                             min_zoom=int(attrs['minZoom'].text), max_zoom=int(attrs['maxZoom'].text))
        except KeyError:
            raise MapSourceException("Mapsource XML does not contain all required attributes. ")
        except ValueError:
            raise MapSourceException("minZoom/maxZoom must be an integer. ")

    def __repr__(self):
        return "<MapSource: {} ({}), url:{}, min_zoom:{}, max_zoom:{}>".format(
            self.id, self.name, self.tile_url, self.min_zoom, self.max_zoom)


