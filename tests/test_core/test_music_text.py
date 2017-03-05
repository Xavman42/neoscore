import os
import unittest

from mock_graphic_object import MockGraphicObject

from brown.config import config
from brown.core import brown
from brown.core.music_char import MusicChar
from brown.core.music_font import MusicFont
from brown.core.music_text import MusicText
from brown.core.staff import Staff
from brown.utils.units import Mm


class TestMusicText(unittest.TestCase):

    def setUp(self):
        brown.setup()
        font_file_path = os.path.join(
            config.RESOURCES_DIR, 'fonts', 'Bravura.otf')
        metadata_file_path = os.path.join(
            config.RESOURCES_DIR, 'fonts', 'bravura_metadata.json')
        self.font_id = brown.register_music_font(
            font_file_path, metadata_file_path)
        self.staff = Staff((Mm(0), Mm(0)), Mm(100),
                           frame=None, staff_unit=Mm(1))
        self.font = MusicFont('Bravura', self.staff.unit)

    def test_init(self):
        mock_parent = MockGraphicObject((10, 11), parent=self.staff)
        test_object = MusicText((5, 6),
                                      'accidentalFlat',
                                mock_parent,
                                self.font)
        assert(test_object.x == 5)
        assert(test_object.y == 6)
        assert(test_object.text == '\ue260')
        assert(test_object.font == self.font)
        assert(test_object.parent == mock_parent)

    def test_init_with_one_tuple(self):
        test_object = MusicText((5, 6),
                                ('brace', 1),
                                self.staff)
        assert(test_object.text == '\uF400')

    def test_init_with_one_music_char(self):
        test_object = MusicText((5, 6),
                                MusicChar(self.staff.music_font, 'brace', 1),
                                self.staff)
        assert(test_object.text == '\uF400')

    def test_init_with_multiple_chars_in_list(self):
        test_object = MusicText((5, 6),
                                ['accidentalFlat', ('brace', 1)],
                                self.staff)
        assert(test_object.text == '\ue260\uF400')