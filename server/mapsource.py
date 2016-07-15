import xml.etree.ElementTree

class MapSourceException(Exception):
    pass

class MapSource(object):
    """
    object storing all information on how to access the tiles
    of a certain map
    """

    def __init__(self, name, tile_url, min_zoom=1, max_zoom=17):
        """

        Args:
            tile_url: url of the format "http://mymap.xyz/tiles/{$z}/{$x}/{$y}"
             where z is zoom level, and x and y the tile coordinates respectively.
            min_zoom: minimal allowed zoom level of the map
            max_zoom: maximal allowed zoom level of the map

        """
        self.name = name
        self.tile_url = tile_url
        self.min_zoom = min_zoom
        self.max_zoom = max_zoom

    def get_tile_url(self, zoom, x, y):
        """Fill the placeholders of the tile url with zoom, x and y"""
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
            return MapSource(attrs['name'], attrs['url'], int(attrs['minZoom']), int(attrs['maxZoom']))
        except KeyError:
            raise MapSourceException("Mapsource XML does not contain all required attributes. ")
        except ValueError:
            raise MapSourceException("minZoom/maxZoom must be an integer. ")

    def __str__(self):
        return "<MapSource: {}, url:{}, min_zoom:{}, max_zoom:{}>".format(
            self.name, self.tile_url, self.min_zoom, self.max_zoom)


