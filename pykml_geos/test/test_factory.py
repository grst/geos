import unittest
from os import path
from lxml import etree
from pykml.parser import Schema
from pykml.factory import KML_ElementMaker as KML
from pykml.factory import ATOM_ElementMaker as ATOM
from pykml.factory import GX_ElementMaker as GX

class KmlFactoryTestCase(unittest.TestCase):
    
    def test_get_factory_object_name(self):
        "Tests obtaining a factory object"
        from pykml.factory import get_factory_object_name
        
        self.assertEqual(
            get_factory_object_name('http://www.opengis.net/kml/2.2'),
            'KML'
        )
        self.assertEqual(
            get_factory_object_name('http://www.w3.org/2005/Atom'),
            'ATOM'
        )
        self.assertEqual(get_factory_object_name(None), 'KML')
    
    def test_trivial_kml_document(self):
        """Tests the creation of a trivial OGC KML document."""
        doc = KML.kml()
        schema = Schema("ogckml22.xsd")
        self.assertTrue(schema.validate(doc))
        self.assertEquals(
            etree.tostring(doc),
            '<kml xmlns:gx="http://www.google.com/kml/ext/2.2" '
                 'xmlns:atom="http://www.w3.org/2005/Atom" '
                 'xmlns="http://www.opengis.net/kml/2.2"/>'
        )
    
    def test_basic_kml_document_2(self):
        """Tests the creation of a basic OGC KML document."""
        doc = KML.kml(
            KML.Document(
                KML.name("KmlFile"),
                KML.Placemark(
                    KML.name("Untitled Placemark"),
                    KML.Point(
                        KML.coordinates("-95.265,38.959,0")
                    )
                )
            )
        )
        self.assertTrue(Schema("kml22gx.xsd").validate(doc))
        self.assertEquals(
            etree.tostring(doc),
            '<kml xmlns:gx="http://www.google.com/kml/ext/2.2" '
                 'xmlns:atom="http://www.w3.org/2005/Atom" '
                 'xmlns="http://www.opengis.net/kml/2.2">'
              '<Document>'
                '<name>KmlFile</name>'
                '<Placemark>'
                  '<name>Untitled Placemark</name>'
                  '<Point>'
                    '<coordinates>-95.265,38.959,0</coordinates>'
                  '</Point>'
                '</Placemark>'
              '</Document>'
            '</kml>'
        )
    
    def test_basic_kml_document(self):
        """Tests the creation of a basic KML with Google Extensions ."""
        doc = KML.kml(
            GX.Tour(
                GX.Playlist(
                    GX.SoundCue(
                        KML.href("http://dev.keyhole.com/codesite/cntowerfacts.mp3")
                    ),
                    GX.Wait(
                        GX.duration(10)
                    ),
                    GX.FlyTo(
                        GX.duration(5),
                        GX.flyToMode("bounce"),
                        KML.LookAt(
                            KML.longitude(-79.387),
                            KML.latitude(43.643),
                            KML.altitude(0),
                            KML.heading(-172.3),
                            KML.tilt(10),
                            KML.range(1200),
                            KML.altitudeMode("relativeToGround"),
                        )
                    )
                )
            )
        )
        self.assertTrue(Schema("kml22gx.xsd").validate(doc))
        self.assertEquals(
            etree.tostring(doc),
            '<kml xmlns:gx="http://www.google.com/kml/ext/2.2" '
                 'xmlns:atom="http://www.w3.org/2005/Atom" '
                 'xmlns="http://www.opengis.net/kml/2.2">'
              '<gx:Tour>'
                '<gx:Playlist>'
                  '<gx:SoundCue>'
                    '<href>http://dev.keyhole.com/codesite/cntowerfacts.mp3</href>'
                  '</gx:SoundCue>'
                  '<gx:Wait>'
                    '<gx:duration>10</gx:duration>'
                  '</gx:Wait>'
                  '<gx:FlyTo>'
                    '<gx:duration>5</gx:duration>'
                    '<gx:flyToMode>bounce</gx:flyToMode>'
                    '<LookAt>'
                      '<longitude>-79.387</longitude>'
                      '<latitude>43.643</latitude>'
                      '<altitude>0</altitude>'
                      '<heading>-172.3</heading>'
                      '<tilt>10</tilt>'
                      '<range>1200</range>'
                      '<altitudeMode>relativeToGround</altitudeMode>'
                    '</LookAt>'
                  '</gx:FlyTo>'
                '</gx:Playlist>'
              '</gx:Tour>'
            '</kml>'
        )
    
    def test_kml_document_with_atom_element(self):
        """Tests the creation of a KML document with an ATOM element."""
        doc = KML.kml(
            KML.Document(
                ATOM.author(
                    ATOM.name("J. K. Rowling")
                ),
                ATOM.link(href="http://www.harrypotter.com"),
                KML.Placemark(
                    KML.name("Hogwarts"),
                    KML.Point(
                        KML.coordinates("1,1")
                    )
                )
            )
        )
        self.assertTrue(Schema("kml22gx.xsd").validate(doc))
        self.assertEquals(
            etree.tostring(doc),
            '<kml xmlns:gx="http://www.google.com/kml/ext/2.2" '
                 'xmlns:atom="http://www.w3.org/2005/Atom" '
                 'xmlns="http://www.opengis.net/kml/2.2">'
              '<Document>'
                '<atom:author>'
                  '<atom:name>J. K. Rowling</atom:name>'
                '</atom:author>'
                '<atom:link href="http://www.harrypotter.com"/>'
                '<Placemark>'
                  '<name>Hogwarts</name>'
                  '<Point>'
                    '<coordinates>1,1</coordinates>'
                  '</Point>'
                '</Placemark>'
              '</Document>'
            '</kml>'
        )

    def test_kml_document_with_cdata_description(self):
        """Tests the creation of a KML document with a CDATA element."""
        from pykml.factory import KML_ElementMaker as KML
        from lxml import etree
        
        doc = KML.description(
                '<h1>CDATA Tags are useful!</h1>'
            )
        self.assertEquals(
            etree.tostring(doc),
              '<description '
                    'xmlns:gx="http://www.google.com/kml/ext/2.2" '
                    'xmlns:atom="http://www.w3.org/2005/Atom" '
                    'xmlns="http://www.opengis.net/kml/2.2">'
                  '&lt;h1&gt;CDATA Tags are useful!&lt;/h1&gt;'
              '</description>'
        )
    
    def test_kml_document_with_cdata_description_2(self):
        """Tests the creation of a KML document with a CDATA element."""
        
        from pykml.factory import KML_ElementMaker as KML
        from pykml.factory import ATOM_ElementMaker as ATOM
        from pykml.factory import GX_ElementMaker as GX
        from lxml import etree
        doc = KML.kml(
          KML.Document(
            KML.Placemark(
              KML.name("CDATA example"),
              KML.description(
                  '<h1>CDATA Tags are useful!</h1>'
                  '<p><font color="red">Text is <i>more readable</i> and '
                  '<b>easier to write</b> when you can avoid using entity '
                  'references.</font></p>'
              ),
              KML.Point(
                KML.coordinates("102.595626,14.996729"),
              ),
            ),
          ),
        )
        self.assertEquals(
            etree.tostring(doc),
            '<kml xmlns:gx="http://www.google.com/kml/ext/2.2" '
                 'xmlns:atom="http://www.w3.org/2005/Atom" '
                 'xmlns="http://www.opengis.net/kml/2.2">'
              '<Document>'
                '<Placemark>'
                  '<name>CDATA example</name>'
                  '<description>'
                    '&lt;h1&gt;CDATA Tags are useful!&lt;/h1&gt;'
                    '&lt;p&gt;&lt;font color="red"&gt;Text is &lt;i&gt;more readable&lt;/i&gt; and '
                    '&lt;b&gt;easier to write&lt;/b&gt; when you can avoid using entity '
                    'references.&lt;/font&gt;&lt;/p&gt;'
                  '</description>'
                  '<Point>'
                    '<coordinates>102.595626,14.996729</coordinates>'
                  '</Point>'
                '</Placemark>'
              '</Document>'
            '</kml>'
        )


class GeneratePythonScriptTestCase(unittest.TestCase):
    
    def test_write_python_script_for_kml_document(self):
        """Tests the creation of a trivial OGC KML document."""
        from pykml.factory import write_python_script_for_kml_document
        
        doc = KML.kml(
            KML.Document(
                ATOM.author(
                    ATOM.name("J. K. Rowling")
                ),
                ATOM.link(href="http://www.harrypotter.com"),
                KML.Placemark(
                    KML.name("Hogwarts"),
                    KML.Point(
                        KML.coordinates("1,1")
                    )
                )
            )
        )
        script = write_python_script_for_kml_document(doc)
        self.assertEquals(
            script,
            'from lxml import etree\n'
            'from pykml.factory import KML_ElementMaker as KML\n'
            'from pykml.factory import ATOM_ElementMaker as ATOM\n'
            'from pykml.factory import GX_ElementMaker as GX\n'
            '\n'
            'doc = KML.kml(\n'
            '  KML.Document(\n'
            '    ATOM.author(\n'
            '      ATOM.name(\'J. K. Rowling\'),\n'
            '    ),\n'
            '    ATOM.link(  href="http://www.harrypotter.com",\n'
            '),\n'
            '    KML.Placemark(\n'
            '      KML.name(\'Hogwarts\'),\n'
            '      KML.Point(\n'
            '        KML.coordinates(\'1,1\'),\n'
            '      ),\n'
            '    ),\n'
            '  ),\n'
            ')\n'
            'print etree.tostring(etree.ElementTree(doc),pretty_print=True)\n'
        )

    def test_write_python_script_for_kml_document_with_cdata(self):
        """Tests the creation of an OGC KML document with a cdata tag"""
        import os
        import tempfile
        from pykml.parser import parse
        from pykml.factory import write_python_script_for_kml_document
        
        test_datafile = path.join(
            path.dirname(__file__),
            'testfiles',
            'google_kml_tutorial/using_the_cdata_element.kml'
        )
        file = 'test/testfiles/'
        schema = Schema('kml22gx.xsd')
        with open(test_datafile) as f:
            doc = parse(f, schema=schema)
        script = write_python_script_for_kml_document(doc)
        self.assertEquals(
            script,
            'from lxml import etree\n'
            'from pykml.factory import KML_ElementMaker as KML\n'
            'from pykml.factory import ATOM_ElementMaker as ATOM\n'
            'from pykml.factory import GX_ElementMaker as GX\n'
            '\n'
            'doc = KML.kml(\n'
            '  KML.Document(\n'
            '    KML.Placemark(\n'
            '      KML.name(\'CDATA example\'),\n'
            '      KML.description(\n'
            '          \'<h1>CDATA Tags are useful!</h1>\'\n'
            '          \'<p><font color="red">Text is <i>more readable</i> and \'\n'
            '          \'<b>easier to write</b> when you can avoid using entity \'\n'
            '          \'references.</font></p>\'\n'
            '      ),\n'
            '      KML.Point(\n'
            '        KML.coordinates(\'102.595626,14.996729\'),\n'
            '      ),\n'
            '    ),\n'
            '  ),\n'
            ')\n'
            'print etree.tostring(etree.ElementTree(doc),pretty_print=True)\n'
        )
        # create a temporary python file
        handle, tfile = tempfile.mkstemp(suffix='.py')
        #print tfile
        with open(tfile, 'w') as f:
            f.write(script)
        
        # execute the temporary python file to create a KML file
        import subprocess
        current_env = os.environ.copy()
        current_env["PYTHONPATH"] = os.path.abspath(os.path.join(os.getcwd(),'..'))
        handle, temp_kml_file = tempfile.mkstemp(suffix='.kml')
        #print temp_kml_file
        with open(temp_kml_file, 'w') as f:
            exit_code = subprocess.call(
                    ["python",tfile],
                    stdout=f,
                    env=current_env
            )
        self.assertEqual(exit_code, 0)
        
        # parse and validate the KML generated by the temporary script
        doc2 = parse(temp_kml_file, schema=schema)
        # test that the root element is as expected
        self.assertEqual(doc2.docinfo.root_name, 'kml')
    
    def test_write_python_script_for_kml_document_with_namespaces(self):
        """Tests the creation of an OGC KML document with several namespaces"""
        import os
        import tempfile
        from pykml.parser import parse
        from pykml.factory import write_python_script_for_kml_document
        
        test_datafile = path.join(
            path.dirname(__file__),
            'testfiles',
            'google_kml_developers_guide/complete_tour_example.kml'
        )
        schema = Schema('kml22gx.xsd')
        with open(test_datafile) as f:
            doc = parse(f, schema=schema)
        script = write_python_script_for_kml_document(doc)
        
        # create a temporary python file
        handle, tfile = tempfile.mkstemp(suffix='.py')
        #print tfile
        with open(tfile, 'w') as f:
            f.write(script)
        
        # execute the temporary python file to create a KML file
        import subprocess
        current_env = os.environ.copy()
        current_env["PYTHONPATH"] = os.path.abspath(os.path.join(os.getcwd(),'..'))
        handle, temp_kml_file = tempfile.mkstemp(suffix='.kml')
        #print temp_kml_file
        with open(temp_kml_file, 'w') as f:
            exit_code = subprocess.call(["python",tfile], stdout=f, env=current_env)
        self.assertEqual(exit_code, 0)
        
        # parse and validate the KML generated by the temporary script
        doc2 = parse(temp_kml_file, schema=schema)
        # test that the root element is as expected
        self.assertEqual(doc2.docinfo.root_name, 'kml')

    def test_write_python_script_for_kml_document_with_comments(self):
        """Tests the creation of an OGC KML document with several comments"""
        import os
        import tempfile
        from pykml.parser import parse
        from pykml.factory import write_python_script_for_kml_document
        
        test_datafile = path.join(
            path.dirname(__file__),
            'testfiles',
            'simple_file_with_comments.kml'
        )
        schema = Schema('kml22gx.xsd')
        with open(test_datafile) as f:
            doc = parse(f, schema=schema)
        script = write_python_script_for_kml_document(doc)
        
        # create a temporary python file
        handle, tfile = tempfile.mkstemp(suffix='.py')
        #print tfile  # Useful for debugging
        with open(tfile, 'w') as f:
            f.write(script)
        
        # execute the temporary python file to create a KML file
        import subprocess
        current_env = os.environ.copy()
        current_env["PYTHONPATH"] = os.path.abspath(os.path.join(os.getcwd(),'..'))
        handle, temp_kml_file = tempfile.mkstemp(suffix='.kml')
        #print temp_kml_file  # Useful for debugging
        with open(temp_kml_file, 'w') as f:
            exit_code = subprocess.call(["python",tfile], stdout=f, env=current_env)
        self.assertEqual(exit_code, 0)
        
        # parse and validate the KML generated by the temporary script
        doc2 = parse(temp_kml_file, schema=schema)
        # test that the root element is as expected
        self.assertEqual(doc2.docinfo.root_name, 'kml')
        
        self.assertEqual(etree.tostring(doc), etree.tostring(doc2))
        
        #import ipdb; ipdb.set_trace()
        pass

if __name__ == '__main__':
    unittest.main()