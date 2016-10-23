import unittest

from brown.core import brown
from brown.primitives.notehead import Notehead
from brown.primitives.staff import Staff


# WARNING: Keep an eye on this global brown state
#          this pattern very likely will not work
#          for all testing needs
#brown.setup()


class TestNotehead(unittest.TestCase):
    # def setUp(self):
    #     # TODO: Once clefs are implemented, make this this mock
    #     #       has an explicit clef!
    #     mock_staff = Staff(0, 0, 100)

    def test_staff_position_middle_c_treble(self):
        mock_staff = Staff(0, 0, 100)
        brown.setup()
        assert(Notehead(mock_staff, 50, "c'").staff_position == -6)

    def test_staff_position_low_octaves(self):
        mock_staff = Staff(0, 0, 100)
        brown.setup()
        assert(Notehead(mock_staff, 50, "c").staff_position == -13)
        assert(Notehead(mock_staff, 50, "c,").staff_position == -20)
        assert(Notehead(mock_staff, 50, "c,,").staff_position == -27)
        assert(Notehead(mock_staff, 50, "c,,,").staff_position == -34)

    def test_staff_position_high_octaves(self):
        mock_staff = Staff(0, 0, 100)
        brown.setup()
        assert(Notehead(mock_staff, 50, "c'").staff_position == -6)
        assert(Notehead(mock_staff, 50, "c''").staff_position == 1)
        assert(Notehead(mock_staff, 50, "c'''").staff_position == 8)
        assert(Notehead(mock_staff, 50, "c''''").staff_position == 15)
        assert(Notehead(mock_staff, 50, "c'''''").staff_position == 22)

    def test_staff_position_with_accidentals(self):
        mock_staff = Staff(0, 0, 100)
        brown.setup()
        assert(Notehead(mock_staff, 50, "cf'").staff_position == -6)
        assert(Notehead(mock_staff, 50, "cn'").staff_position == -6)
        assert(Notehead(mock_staff, 50, "cs'").staff_position == -6)

    def test_staff_position_with_all_letter_names(self):
        mock_staff = Staff(0, 0, 100)
        brown.setup()
        assert(Notehead(mock_staff, 50, "c'").staff_position == -6)
        assert(Notehead(mock_staff, 50, "d'").staff_position == -5)
        assert(Notehead(mock_staff, 50, "e'").staff_position == -4)
        assert(Notehead(mock_staff, 50, "f'").staff_position == -3)
        assert(Notehead(mock_staff, 50, "g'").staff_position == -2)
        assert(Notehead(mock_staff, 50, "a'").staff_position == -1)
        assert(Notehead(mock_staff, 50, "b'").staff_position == 0)
