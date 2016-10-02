import xml.etree.ElementTree
from glob import glob
from os.path import basename


def load_maps(dir):
    maps = {}
    for xml_file in glob(dir + "/*.xml"):
        map = MapSource.from_xml(xml_file)
        maps[map.id] = map
    return maps


class MapSourceException(Exception):
    pass


class MapSource(object):
    """
    object storing all information on how to access the tiles
    of a certain map
    """

    def __init__(self, id, name, tile_url, min_zoom=1, max_zoom=17):
        """

        Args:
            id: unique identifier (e.g. filename)
            name: display name
            tile_url: url of the format "http://mymap.xyz/tiles/{$z}/{$x}/{$y}"
             where z is zoom level, and x and y the tile coordinates respectively.
            min_zoom: minimal allowed zoom level of the map
            max_zoom: maximal allowed zoom level of the map

        >>> ms = MapSource.from_xml("../mapsources/outdooractive.xml")
        >>> ms.name
        'Outdooractive'
        >>> ms.min_zoom
        5
        >>> ms.max_zoom
        16
        >>> ms.tile_url
        'http://s2.outdooractive.com/portal/map/{$z}/{$x}/{$y}.png'
        """
        self.id = id
        self.name = name
        self.tile_url = tile_url
        self.min_zoom = min_zoom
        self.max_zoom = max_zoom

    def get_tile_url(self, zoom, x, y):
        """
        Fill the placeholders of the tile url with zoom, x and y.

        >>> ms = MapSource.from_xml("../mapsources/outdooractive.xml")
        >>> ms.get_tile_url(42, 43, 44)
        'http://s2.outdooractive.com/portal/map/42/43/44.png'
        """
        return self.tile_url.format(**{"$z": zoom, "$x": x, "$y": y})

    @staticmethod
    def from_xml(xml_path):
        """
        Create a MapSource object from a MOBAC
        mapsource xml.

        Args:
            xml_path: path to the MOBAC mapsource xml file.

        Returns:
            MapSource object.

        Raises:
            MapSourceException: when the xml file could not be parsed properly.

        """
        xmldoc = xml.etree.ElementTree.parse(xml_path).getroot()
        attrs = {}
        for elem in xmldoc.getchildren():
            attrs[elem.tag] = elem.text

        try:
            return MapSource(basename(xml_path), attrs['name'], attrs['url'],
                             int(attrs['minZoom']), int(attrs['maxZoom']))
        except KeyError:
            raise MapSourceException("Mapsource XML does not contain all required attributes. ")
        except ValueError:
            raise MapSourceException("minZoom/maxZoom must be an integer. ")

    def __str__(self):
        return "<MapSource: {} ({}), url:{}, min_zoom:{}, max_zoom:{}>".format(
            self.id, self.name, self.tile_url, self.min_zoom, self.max_zoom)


