import unittest

from brown.core import brown
from brown.core.fill_pattern import FillPattern
from brown.interface.brush_interface import BrushInterface
from brown.interface.font_interface import FontInterface
from brown.interface.text_interface import TextInterface
from brown.utils.color import Color


class TestTextInterface(unittest.TestCase):

    def setUp(self):
        brown.setup()
        self.brush = BrushInterface(Color('#000000'), FillPattern.SOLID_COLOR)

    def test_init(self):
        test_font = FontInterface('Bravura', 12, 1, False)
        test_object = TextInterface((5, 6), 'testing', test_font, self.brush)
        assert(test_object.text == 'testing')
        assert(test_object._qt_object.text() == test_object.text)
        assert(test_object.font == test_font)
        assert(test_object._qt_object.font() == test_object.font._qt_object)

    def test_text_setter_changes_qt_object(self):
        test_font = FontInterface('Bravura', 12, 1, False)
        test_object = TextInterface((5, 6), 'testing', test_font, self.brush)
        test_object.text = 'new value'
        assert(test_object.text == 'new value')
        assert(test_object._qt_object.text() == 'new value')

    def test_font_setter_changes_qt_object(self):
        test_font = FontInterface('Bravura', 12, 1, False)
        test_object = TextInterface((5, 6), 'testing', test_font, self.brush)
        new_test_font = FontInterface('Bravura', 16, 1, False)
        test_object.font = new_test_font
        assert(test_object.font == new_test_font)
        assert(test_object._qt_object.font() == new_test_font._qt_object)
