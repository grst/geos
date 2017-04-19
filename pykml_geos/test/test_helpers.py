import unittest
from pykml.factory import KML_ElementMaker as K
from pykml.factory import ATOM_ElementMaker as ATOM
from pykml.factory import GX_ElementMaker as GX
from pykml.parser import Schema
from pykml.parser import fromstring

class KmlHelpersTestCase(unittest.TestCase):
    
    def test_separate_namespace(self):
        """Tests the function that separates namespaces from qualified names"""
        from pykml.helpers import separate_namespace
        
        namespace, element_name = separate_namespace('{garden}eggplant')
        self.assertEqual(namespace, 'garden')
        self.assertEqual(element_name, 'eggplant')
        
        namespace, element_name = separate_namespace('eggplant')
        self.assertEqual(namespace, None)
        self.assertEqual(element_name, 'eggplant')
    
    def test_set_max_decimal_places(self):
        """Tests setting the number of decimal places in a document"""
        
        from pykml.helpers import set_max_decimal_places
        
        test_kml = (
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<kml xmlns="http://www.opengis.net/kml/2.2" '
                 'xmlns:gx="http://www.google.com/kml/ext/2.2" '
                 'xmlns:kml="http://www.opengis.net/kml/2.2" '
                 'xmlns:atom="http://www.w3.org/2005/Atom">'
                '<Document>'
                    '<Placemark>'
                        '<name>Spearhead</name>'
                        '<LookAt>'
                            '<longitude>-105.6381333137406</longitude>'
                            '<latitude>40.25542364754504</latitude>'
                            '<altitude>0.123456789</altitude>'
                            '<heading>-75.2679217880259</heading>'
                            '<tilt>23.33768008163944</tilt>'
                            '<range>234.1234567890</range>'
                            '<altitudeMode>relativeToGround</altitudeMode>'
                        '</LookAt>'
                        '<Point>'
                            '<altitudeMode>absolute</altitudeMode>'
                            '<coordinates>-105.6381333137406,40.25542364754504,3826.1234567890</coordinates>'
                        '</Point>'
                    '</Placemark>'
                    '<Placemark>'
                        '<name>North Ridge</name>'
                        '<LineString>'
                            '<tessellate>1</tessellate>'
                            '<coordinates>'
                                '-105.6400899274733,40.25778038346723,0 -105.6397083557171,40.25680995109639,0 -105.6389193178716,40.25606911151127,0 -105.6385344464865,40.25559941617504,0 '
                            '</coordinates>'
                        '</LineString>'
                    '</Placemark>'
                    '<Placemark>'
                        '<name>Black Lake</name>'
                        '<Polygon>'
                            '<tessellate>1</tessellate>'
                            '<outerBoundaryIs>'
                                '<LinearRing>'
                                    '<coordinates>'
                                        '-105.6411566922825,40.26642751482452,0 -105.6424707115566,40.26600581412304,0 -105.6428010853679,40.26549238687588,0 -105.6423465680717,40.26464873270425,0 -105.6414735029203,40.2645201246226,0 -105.6404885591011,40.2647647504581,0 -105.6402035173736,40.26539046743765,0 -105.6405618656529,40.26617884849238,0 -105.6411566922825,40.26642751482452,0 '
                                    '</coordinates>'
                                '</LinearRing>'
                            '</outerBoundaryIs>'
                        '</Polygon>'
                    '</Placemark>'
                '</Document>'
            '</kml>'
        )
        doc = fromstring(test_kml, schema=Schema("ogckml22.xsd"))
        set_max_decimal_places(
            doc, 
            max_decimals={
                'longitude': 6,
                'latitude': 5,
                'altitude': 2,
                'heading': 1,
                'tilt': 0,
                #'range': 0,  # range values will not be changed
            }
        )
        
        longitude_list = doc.findall(".//{http://www.opengis.net/kml/2.2}longitude")
        self.assertAlmostEquals(longitude_list[0], -105.638133)
        
        latitude_list = doc.findall(".//{http://www.opengis.net/kml/2.2}latitude")
        self.assertAlmostEquals(latitude_list[0], 40.25542)
        
        altitude_list = doc.findall(".//{http://www.opengis.net/kml/2.2}altitude")
        self.assertAlmostEquals(altitude_list[0], 0.12)
        
        heading_list = doc.findall(".//{http://www.opengis.net/kml/2.2}heading")
        self.assertAlmostEquals(heading_list[0], -75.3)
        
        tilt_list = doc.findall(".//{http://www.opengis.net/kml/2.2}tilt")
        self.assertAlmostEquals(tilt_list[0], 23.0)
        
        # Note that the range value was not changed
        range_list = doc.findall(".//{http://www.opengis.net/kml/2.2}range")
        self.assertAlmostEquals(range_list[0], 234.1234567890)
        
        coords_list = doc.findall(".//{http://www.opengis.net/kml/2.2}coordinates")
        self.assertEquals(
            coords_list[0],
            "-105.638133,40.25542,3826.12"
        )
        self.assertEquals(
            coords_list[1], 
            '-105.64009,40.25778,0.0 '
            '-105.639708,40.25681,0.0 '
            '-105.638919,40.25607,0.0 '
            '-105.638534,40.2556,0.0'
        )
        #import ipdb; ipdb.set_trace()
        self.assertEquals(
            coords_list[2], 
            '-105.641157,40.26643,0.0 '
            '-105.642471,40.26601,0.0 '
            '-105.642801,40.26549,0.0 '
            '-105.642347,40.26465,0.0 '
            '-105.641474,40.26452,0.0 '
            '-105.640489,40.26476,0.0 '
            '-105.640204,40.26539,0.0 '
            '-105.640562,40.26618,0.0 '
            '-105.641157,40.26643,0.0'
        )


    def test_set_max_decimal_places_track(self):
        """Tests setting the number of decimal places for track data"""
        
        from pykml.helpers import set_max_decimal_places
        
        test_kml = (
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<kml xmlns="http://www.opengis.net/kml/2.2" '
                 'xmlns:gx="http://www.google.com/kml/ext/2.2">'
            '<Folder>'
              '<Placemark>'
                '<gx:Track>'
                  '<when>2010-05-28T02:02:09Z</when>'
                  '<when>2010-05-28T02:02:35Z</when>'
                  '<when>2010-05-28T02:02:44Z</when>'
                  '<gx:coord>-122.111111 37.111111 151.333333</gx:coord>'
                  '<gx:coord>-122.222222 37.222222 152.222222</gx:coord>'
                  '<gx:coord>-122.333333 37.333333 153.333333</gx:coord>'
                '</gx:Track>'
              '</Placemark>'
            '</Folder>'
            '</kml>'
        )
        doc = fromstring(test_kml, schema=Schema("kml22gx.xsd"))
        set_max_decimal_places(
            doc, 
            max_decimals={
                'longitude': 3,
                'latitude': 2,
                'altitude': 1,
            }
        )
        
        coords_list = doc.findall(".//{http://www.google.com/kml/ext/2.2}coord")
        #import ipdb; ipdb.set_trace()
        self.assertEquals(
            coords_list[0], 
            '-122.111 37.11 151.3'
        )