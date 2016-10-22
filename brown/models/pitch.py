import re

from brown.models.accidental import Accidental

class InvalidPitchDescriptionError(Exception):
    """An exception raised when an invalid pitch specifier is used."""
    pass


class Pitch:
    """A pitch with a letter, octave, and accidental"""

    _pitch_regex = re.compile("^([a-g])([snf])?('*|,*)$")
    natural_pitch_classes = {
        'c': 0,
        'd': 2,
        'e': 4,
        'f': 5,
        'g': 7,
        'a': 9,
        'b': 11
    }
    _diatonic_degrees_from_c = {
        'c': 1,
        'd': 2,
        'e': 3,
        'f': 4,
        'g': 5,
        'a': 6,
        'b': 7
    }
    _middle_c_octave = 4
    _midi_middle_c = 60


    def __init__(self, pitch):
        """
        Args:
            pitch (str): A pitch representation of a string
                in lilypond notation

        Notes:
            Valid pitch accidentals suffixes are `s` for sharp, `f` for flat,
            and `n` for explicit natural.

            Octaves are denoted by suffixes of commas or apostrophes,
            where none is C below middle-C, and each comma / apostrophe
            indicates an octave down or up, respectively.

            TODO: Support other input methods, as in mothballed version
            TODO: Explain better, needs examples - most users will not be
                  familiar with lilypond pitch notation
        """
        self._letter = None
        self._accidental = None
        self._octave = None      # These three are initialized by the pitch setter
        self.pitch = pitch

    ######## PUBLIC PROPERTIES ########

    @property
    def pitch(self):
        """str: A string representation of the pitch.

        See __init__() documentation for a complete description.
        """
        return self._pitch

    @pitch.setter
    def pitch(self, value):
        match = Pitch._pitch_regex.match(value)
        if match is None:
            raise InvalidPitchDescriptionError
        letter = match.group(1)
        accidental = match.group(2)
        ticks = match.group(3)
        self._letter = letter
        self._accidental = Accidental(accidental)
        if not ticks:
            self._octave = 3
        else:
            self._octave = 3 + (len(ticks) * (-1 if ticks[0] == ',' else 1))
        self._pitch = value

    @property
    def letter(self):
        """str: The a-g letter name of the pitch

        This property is read-only. To modify, set the `pitch` property.
        TODO: maybe implement setters
        """
        return self._letter

    @property
    def accidental(self):
        """str or None: A character representing the accidental.

        Supported values:
        * 'f': flat
        * 'n': natural (explicit)
        * 's': sharp
        * None: no accidental

        This property is read-only. To modify, set the `pitch` property.
        TODO: maybe implement setters
        """
        return self._accidental

    @property
    def octave(self):
        """int: The octave number for the pitch in scientific notation.

        `octave == 4` corresponds to middle-C.
        Descending pitches correspond to lower octave numbers.

        This property is read-only. To modify, set the `pitch` property.
        TODO: maybe implement setters
        """
        return self._octave

    @property
    def pitch_class(self):
        """int: The 0-11 pitch class of this pitch."""
        natural = Pitch.natural_pitch_classes[self.letter]
        if self.accidental.value is not None:
            return natural + self.accidental.value
        return natural

    @property
    def midi_number(self):
        """int: The midi pitch number, where A440 == 69 and middle C == 60"""
        return (Pitch._midi_middle_c +                           # Start point
                ((self.octave - Pitch._middle_c_octave) * 12) +  # 8ve offset
                self.pitch_class)                                # pitch offset

    @property
    def diatonic_degree_from_c(self):
        """int: The diatonic degree of the pitch as if it were in C.

            'c': 1,
            'd': 2,
            'e': 3,
            'f': 4,
            'g': 5,
            'a': 6,
            'b': 7
        """
        return Pitch._diatonic_degrees_from_c[self.letter]
