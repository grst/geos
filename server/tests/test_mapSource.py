import os
import sys
sys.path.insert(0, os.path.abspath('..'))

from unittest import TestCase
from mapsource import MapSource


class TestMapSource(TestCase):
  def test_from_xml(self):
    ms = MapSource.from_xml("../../mapsources/outdooractive.xml")
    self.assertEquals("Outdooractive", ms.name)
    self.assertEquals(5, ms.min_zoom)
    self.assertEquals(16, ms.max_zoom)
    self.assertEquals("http://s2.outdooractive.com/portal/map/{$z}/{$x}/{$y}.png", ms.tile_url)

  def test_format_url(self):
    ms = MapSource.from_xml("../../mapsources/outdooractive.xml")
    self.assertEquals("http://s2.outdooractive.com/portal/map/42/43/44.png", ms.get_tile_url(42, 43, 44), )

