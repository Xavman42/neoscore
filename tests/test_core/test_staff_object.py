import unittest

from brown.core import brown
from brown.core.flowable import Flowable
from brown.core.paper import Paper
from brown.core.staff import Staff
from brown.utils.point import Point
from brown.utils.units import Mm

from tests.mocks.mock_staff_object import MockStaffObject


class TestStaffObject(unittest.TestCase):

    def setUp(self):
        brown.setup(
            Paper(*[Mm(val) for val in [210, 297, 20, 20, 20, 20, 10]]))
        self.flowable = Flowable((Mm(0), Mm(0)), Mm(10000), Mm(30), Mm(5))
        self.staff = Staff((Mm(0), Mm(0)), Mm(5000), self.flowable)

    def test_find_staff_with_direct_parent(self):
        child_object = MockStaffObject((Mm(0), Mm(0)), self.staff)
        assert(child_object.staff == self.staff)

    def test_find_staff_with_ancestor(self):
        parent_object = MockStaffObject((Mm(0), Mm(0)), self.staff)
        child_object = MockStaffObject((Mm(10), Mm(1)), parent_object)
        assert(child_object.staff == self.staff)

    @unittest.skip
    def test_find_staff_with_no_staff_raises_error(self):
        # TODO: Implement this test once this functionality is locked down
        pass

    def test_pos_in_staff(self):
        test_object = MockStaffObject((Mm(5000), Mm(0)), self.staff)
        assert(test_object.pos_in_staff == test_object.pos)

    def test_pos_in_staff_with_indirect_ancestor_staff(self):
        parent_object = MockStaffObject((Mm(1), Mm(2)), self.staff)
        test_object = MockStaffObject((Mm(10), Mm(1)), parent_object)
        pos_in_staff = test_object.pos_in_staff.to_unit(Mm)
        self.assertAlmostEqual(pos_in_staff.x.value, 11)
        self.assertAlmostEqual(pos_in_staff.y.value, 3)
