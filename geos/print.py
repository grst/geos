"""
Module for printing maps / exporting them as pdf
"""

# TODO documentation
# TODO add scales bar

from geos.geometry import *
import urllib.request
from urllib.error import URLError
from PIL import Image
from geos import app
from tempfile import NamedTemporaryFile

TILE_SIZE = 256  # px
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, ' \
             'like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0'

# set default user agent
opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', USER_AGENT)]
urllib.request.install_opener(opener)


class MapPrintError(Exception):
    pass


def dpi_to_dpmm(dpi):
    return dpi / 25.4


def print_map(map_source, x, y, zoom=14, width=297, height=210, dpi=300, format="pdf"):
    """

    Args:
        map_source (MapSource):
        lon: center longitude
        lat: center latitude
        zoom: tile zoom level
        width: page width in mm
        height: page height in mm
        dpi: resolution
        format: output format

    Returns:
        pdf file

    """
    bbox = get_print_bbox(x, y, zoom, width, height, dpi)
    tiles = get_tiles(map_source, bbox)
    img = stitch_map(tiles, width, height, bbox, dpi)
    outfile = NamedTemporaryFile(delete=False)
    img.save(outfile, format, quality=100)
    outfile.close()
    return outfile.name


def get_print_bbox(x, y, zoom, width, height, dpi):
    """
    Calculate the tile bounding box based on position, map size and resolution.

    Args:
        lon:
        lat:
        zoom:
        width:
        height:
        dpi:

    Returns:
        GridBB:

    >>> str(get_print_bbox(4164462.1505763642, 985738.7965919945, 14, 297, 150, 120))
    """
    tiles_h = width * dpi_to_dpmm(dpi) / TILE_SIZE
    tiles_v = height * dpi_to_dpmm(dpi) / TILE_SIZE
    mercator_coords = MercatorCoordinate(x, y)
    tile_coords = mercator_coords.to_tile(zoom)
    tile_bb = GridBB(zoom,
                     min_x=tile_coords.x - math.ceil(tiles_h/2),
                     max_x=tile_coords.x + math.ceil(tiles_h/2),
                     min_y=tile_coords.y - math.ceil(tiles_v/2),
                     max_y=tile_coords.y + math.ceil(tiles_v/2))
    return tile_bb


def get_tiles(map_source, bbox):
    """
    Download tiles.

    Args:
        map_source (MapSource):
        bbox:

    Returns:
        tile store directory.

    """
    # todo make parallel
    tiles = {}
    try:
        for x, y in bboxiter(bbox):
            tile_url = map_source.get_tile_url(bbox.zoom, x, y)
            tiles[(x, y)], _ = urllib.request.urlretrieve(tile_url)
            app.logger.info("Downloaded tile x={}, y={}, z={}".format(x, y, bbox.zoom))
    except URLError as e:
        raise MapPrintError("Error downloading tile x={}, y={}, z={} for map {}: {}".format(
            x, y, bbox.zoom, map_source.id, e.reason))

    return tiles


def stitch_map(tiles, width, height, bbox, dpi):
    """
    Merge tiles together into one image.

    Args:
        tiles:
        width:
        height:
        dpi:

    Returns:
        PIL.Image:

    """
    size = (int(width * dpi_to_dpmm(dpi)), int(height * dpi_to_dpmm(dpi)))
    img = Image.new("RGB", size)
    for (x, y), tile_path in tiles.items():
        tile = Image.open(tile_path)
        img.paste(tile, ((x - bbox.min.x) * TILE_SIZE, (y - bbox.min.y) * TILE_SIZE))
    return img



