import unittest
from os import path
import urllib2
from StringIO import StringIO
from lxml import etree
from pykml.parser import Schema
from pykml.parser import fromstring
from pykml.parser import parse


class ValidatorTestCase(unittest.TestCase):
    
    def test_initialize_schema(self):
        """Tests the creation Schema instance"""
        schema = Schema("ogckml22.xsd")
        self.assertTrue(isinstance(schema.schema, etree.XMLSchema))


class ParseKmlOgcTestCase(unittest.TestCase):
    "A collection of tests related to parsing KML OGC documents"
    
    def test_fromstring_kml_document(self):
        "Tests the parsing of an valid KML string"
        test_kml = '<kml xmlns="http://www.opengis.net/kml/2.2"/>'
        tree = fromstring(test_kml, schema=Schema("ogckml22.xsd"))
        self.assertEquals(etree.tostring(tree), test_kml)
        tree = fromstring(test_kml)
        self.assertEquals(etree.tostring(tree), test_kml)
    
    def test_fromstring_invalid_kml_document(self):
        "Tests the parsing of an invalid KML string"
        test_kml = '<bad_element />'
        try:
            tree = fromstring(test_kml, schema=Schema("ogckml22.xsd"))
            self.assertTrue(False)
        except etree.XMLSyntaxError:
            self.assertTrue(True)
        except:
            self.assertTrue(False)
    
    def test_parse_kml_document(self):
        "Tests the parsing of an valid KML file object"
        test_kml = '<kml xmlns="http://www.opengis.net/kml/2.2"/>'
        fileobject = StringIO(test_kml)
        schema = Schema("ogckml22.xsd")
        tree = parse(fileobject, schema=schema)
        self.assertEquals(etree.tostring(tree), test_kml)
        tree = parse(fileobject, schema=schema)
        self.assertEquals(etree.tostring(tree), test_kml)
    
    def test_parse_invalid_kml_document(self):
        "Tests the parsing of an invalid KML document"
        fileobject = StringIO('<bad_element />')
        try:
            tree = parse(fileobject, schema=Schema("ogckml22.xsd"))
            self.assertTrue(False)
        except etree.XMLSyntaxError:
            self.assertTrue(True)
        except:
            self.assertTrue(False)
    
    def test_parse_kml_url(self):
        "Tests the parsing of a KML URL"
        url = 'http://code.google.com/apis/kml/documentation/KML_Samples.kml'
        #url = 'http://kml-samples.googlecode.com/svn/trunk/kml/Document/doc-with-id.kml'
        #url = 'http://code.google.com/apis/kml/documentation/kmlfiles/altitudemode_reference.kml'
        #url = 'http://code.google.com/apis/kml/documentation/kmlfiles/animatedupdate_example.kml'
        fileobject = urllib2.urlopen(url)
        tree = parse(fileobject, schema=Schema("ogckml22.xsd"))
        self.assertEquals(
            etree.tostring(tree)[:78],
            '<kml xmlns="http://www.opengis.net/kml/2.2">'
              '<Document>'
                '<name>KML Samples</name>'
        )
    
    def test_parse_invalid_ogc_kml_document(self):
        """Tests the parsing of an invalid KML document.  Note that this KML
        document uses elements that are not in the OGC KML spec.
        """
        url = 'http://code.google.com/apis/kml/documentation/kmlfiles/altitudemode_reference.kml'
        fileobject = urllib2.urlopen(url)
        try:
            tree = parse(fileobject, schema=Schema("ogckml22.xsd"))
            self.assertTrue(False)
        except etree.XMLSyntaxError:
            self.assertTrue(True)
        except:
            self.assertTrue(False)

class ParseKmlGxTestCase(unittest.TestCase):
    "A collection of tests related to parsing KML Google Extension documents"
    
    def test_parse_kml_url(self):
        "Tests the parsing of a KML URL"
        url = 'http://code.google.com/apis/kml/documentation/kmlfiles/altitudemode_reference.kml'
        fileobject = urllib2.urlopen(url)
        tree = parse(fileobject, schema=Schema('kml22gx.xsd'))
        self.assertEquals(
            etree.tostring(tree)[:185],
            '<kml xmlns="http://www.opengis.net/kml/2.2" '
                 'xmlns:gx="http://www.google.com/kml/ext/2.2">'
                '<!-- required when using gx-prefixed elements -->'
                '<Placemark>'
                  '<name>gx:altitudeMode Example</name>'
        )
    
    def test_parse_kml_file(self):
        "Tests the parsing of a local KML file, with validation"
        test_datafile = path.join(
            path.dirname(__file__),
            'testfiles',
            'google_kml_developers_guide/complete_tour_example.kml'
        )
        # parse with validation
        with open(test_datafile) as f:
            doc = parse(f, schema=Schema('kml22gx.xsd'))
        # parse without validation
        with open(test_datafile) as f:
            doc = parse(f)
        self.assertTrue(True)
    
    def test_parse_kml_file_with_cdata(self):
        "Tests the parsing of a local KML file, with a CDATA description string"
        test_datafile = path.join(
            path.dirname(__file__),
            'testfiles',
            'google_kml_tutorial/using_the_cdata_element.kml'
        )
        # parse with validation
        with open(test_datafile) as f:
            doc = parse(f, schema=Schema('kml22gx.xsd'))
        self.assertEquals(
            etree.tostring(doc),
            '<kml xmlns="http://www.opengis.net/kml/2.2">'
              '<Document>'
                '<Placemark>'
                  '<name>CDATA example</name>'
                  '<description>'
                    '<![CDATA[\n'
                    '          <h1>CDATA Tags are useful!</h1>\n'
                    '          <p><font color="red">Text is <i>more readable</i> and \n'
                    '          <b>easier to write</b> when you can avoid using entity \n'
                    '          references.</font></p>\n'
                    '        ]]>'
                  '</description>'
                '<Point>'
                  '<coordinates>102.595626,14.996729</coordinates>'
                '</Point>'
              '</Placemark>'
            '</Document>'
          '</kml>'
        )
    
    def test_parse_kml_url_2(self):
        "Tests the parsing of a KML URL"
        url = 'http://code.google.com/apis/kml/documentation/kmlfiles/animatedupdate_example.kml'
        fileobject = urllib2.urlopen(url)
        tree = parse(fileobject, schema=Schema('kml22gx.xsd'))
        self.assertEquals(
            etree.tostring(tree)[:137],
            '<kml xmlns="http://www.opengis.net/kml/2.2" '
                 'xmlns:gx="http://www.google.com/kml/ext/2.2">'
                '<Document>'
                  '<name>gx:AnimatedUpdate example</name>'
        )

if __name__ == '__main__':
    unittest.main()