import os
import sys
sys.path.insert(0, os.path.abspath('..'))

from unittest import TestCase
from mapsource import MapSource


class TestMapSource(TestCase):
  def test_from_xml(self):
    ms = MapSource.from_xml("../../mapsources/outdooractive.xml")
    self.assertEquals(ms.name, "Outdooractive")
    self.assertEquals(ms.min_zoom, 5)
    self.assertEquals(ms.max_zoom, 16)
    self.assertEquals(ms.tile_url, "http://s2.outdooractive.com/portal/map/{$z}/{$x}/{$y}.png")
