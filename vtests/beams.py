from typing import NamedTuple, Optional

from helpers import render_vtest

from neoscore.common import *
from neoscore.core.directions import VerticalDirection
from neoscore.western.duration import DurationDef
from neoscore.western.pitch import PitchDef

neoscore.setup()


class TestChord(NamedTuple):
    pitches: Optional[list[PitchDef]]
    duration: DurationDef
    stem_direction: Optional[VerticalDirection] = None
    beam_break_depth: Optional[int] = None
    beam_hook_dir: Optional[HorizontalDirection] = None


staff_y = ZERO


def create_example(
    chords: list[TestChord], direction: Optional[VerticalDirection] = None
):
    global staff_y
    staff = Staff((ZERO, staff_y), None, Mm(150))
    staff_y = staff.y
    clef = Clef(ZERO, staff, "treble")
    unit = staff.unit
    group = []
    spacing = unit(6)
    for i, c in enumerate(chords):
        group.append(
            Chordrest(
                unit(7) + (spacing * i),
                staff,
                c.pitches,
                c.duration,
                c.stem_direction,
                c.beam_break_depth,
                c.beam_hook_dir,
            )
        )
    bg = BeamGroup(group, direction)
    staff_y += Mm(24)


# Flat beams

create_example(
    [
        TestChord(["f'"], (1, 8)),
        TestChord(["f'"], (1, 8)),
    ]
)

create_example(
    [
        TestChord(["f'"], (1, 8)),
        TestChord(["f'"], (1, 8)),
        TestChord(["f'"], (1, 16)),
        TestChord(["f'"], (1, 16)),
        TestChord(["f'"], (1, 32)),
        TestChord(["f'"], (1, 32)),
    ]
)

create_example(
    [
        TestChord(["f''"], (3, 16)),
        TestChord(["f''"], (1, 16)),
    ]
)


create_example(
    [
        TestChord(["f'"], (1, 32)),
        TestChord(["f'"], (1, 32), beam_break_depth=1),
        TestChord(["f'"], (1, 32)),
        TestChord(["f'"], (1, 32)),
    ]
)

# Hook direction overrides

create_example(
    [
        TestChord(["f'"], (1, 8)),
        TestChord(["f'"], (1, 16)),
        TestChord(["f'"], (1, 8)),
    ]
)

create_example(
    [
        TestChord(["f'"], (1, 8)),
        TestChord(["f'"], (1, 16), beam_hook_dir=HorizontalDirection.RIGHT),
        TestChord(["f'"], (1, 8)),
    ]
)

# Beam direction override

create_example(
    [
        TestChord(["a'"], (1, 8)),
        TestChord(["a'"], (1, 16)),
        TestChord(["a'"], (1, 8)),
    ],
    VerticalDirection.DOWN,
)


# Angled beams

create_example(
    [
        TestChord(["f'"], (1, 32)),
        TestChord(["f'"], (1, 32), beam_break_depth=1),
        TestChord(["f'"], (1, 32)),
        TestChord(["g''"], (1, 32)),
        TestChord(["c#'"], (3, 16)),
        TestChord(["d'"], (1, 16)),
    ]
)

create_example(
    [
        TestChord(["bb''", "e''"], (1, 32)),
        TestChord(["f'"], (1, 32), beam_break_depth=2),
        TestChord(["f'"], (1, 32)),
        TestChord(["g''"], (1, 32)),
        TestChord(["c#'"], (3, 16)),
        TestChord(["e''"], (1, 32)),
        TestChord(["eb''"], (1, 32)),
        TestChord(["d''"], (1, 8)),
    ]
)

render_vtest("beams")
