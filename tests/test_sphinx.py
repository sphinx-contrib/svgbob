import os
import shutil
import tempfile
import textwrap
import unittest

import sphinx.cmd.build
import sphinx.cmd.quickstart



class TestSphinx(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.docs_folder = tempfile.mkdtemp()
        sphinx.cmd.quickstart.generate({
            "path": cls.docs_folder,
            "sep": False,
            "project": "testdoc",
            "author": "Martin Larralde",
            "version": "0.1.0",
            "release": "0.1.0",
            "language": "en",
            "dot": "_",
            "suffix": ".rst",
            "master": "index",
            "makefile": True,
            "batchfile": True,
            "extensions": ["sphinxcontrib.svgbob"],
        }, silent=True)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.docs_folder)

    def build(self, builder="html"):
        retcode = sphinx.cmd.build.main([
            "-q",
            "-b",
            builder,
            self.docs_folder,
            os.path.join(self.docs_folder, "_build"),
        ])
        self.assertEqual(retcode, 0)

    def test_svgbob_directive(self):
        with open(os.path.join(self.docs_folder, "index.rst"), "w") as f:
            f.write(textwrap.dedent(r"""
            .. svgbob::

                /---------\
                |  Hello  |
                \---------/
            """))

        self.build()
        self.build(builder="man")
