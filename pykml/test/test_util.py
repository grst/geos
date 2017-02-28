import unittest
from os import path
from pykml.parser import Schema
from pykml.parser import parse

class KmlUtilTestCase(unittest.TestCase):
    
    def test_count_elements(self):
        """Tests the counting of elements in a KML document."""
        from pykml.util import count_elements
        
        test_datafile = path.join(
            path.dirname(__file__),
            'testfiles',
            'google_kml_developers_guide/complete_tour_example.kml'
        )
        with open(test_datafile) as f:
            doc = parse(f, schema=Schema('kml22gx.xsd'))
        summary = count_elements(doc)
        
        self.assertTrue(summary.has_key('http://www.opengis.net/kml/2.2'))
        self.assertEqual(4,
            summary['http://www.opengis.net/kml/2.2']['Placemark']
        )
        self.assertTrue(summary.has_key('http://www.google.com/kml/ext/2.2'))
        self.assertEqual(5,
            summary['http://www.google.com/kml/ext/2.2']['FlyTo']
        )
        self.assertEqual(2,
            summary['http://www.google.com/kml/ext/2.2']['Wait']
        )
