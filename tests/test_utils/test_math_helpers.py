from brown.utils.units import Unit
from brown.utils.point import Point
from brown.utils.math_helpers import linear_interp, clamp_value


def test_linear_interp():
    assert(linear_interp((0, 0), (1, 1), 2) == 2)
    assert(linear_interp((1, 1), (0, 0), -1) == -1)
    assert(linear_interp((0, 0), (2, 1), 3) == 1.5)


def test_linear_interp_with_points():
    assert(linear_interp(Point(0, 0), Point(1, 1), 2) == 2)


def test_linear_interp_with_units_preserves_units():
    assert(linear_interp(
        (Unit(0), Unit(0)),
        (Unit(2), Unit(1)),
        Unit(3)
        ) == Unit(1.5))


def test_clamp_value():
    assert(clamp_value(-50, 3, 5) == 3)
    assert(clamp_value(3, 3, 5) == 3)
    assert(clamp_value(4, 3, 5) == 4)
    assert(clamp_value(5, 3, 5) == 5)
    assert(clamp_value(50, 3, 5) == 5)