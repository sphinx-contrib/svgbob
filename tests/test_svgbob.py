import unittest
from xml.etree import ElementTree as etree

from sphinxcontrib.svgbob._svgbob import to_svg

class TestSvgbob(unittest.TestCase):

    def test_to_svg(self):
        text = r"""
            /-------\
            | Hello |
            \-------/
        """
        svg = to_svg(text)
        print(svg)
