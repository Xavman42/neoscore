from brown.core import brown
from brown.config import config
from brown.core.path import Path
from brown.primitives.staff import Staff
from brown.models.pitch import Pitch
from brown.primitives.staff_object import StaffObject
from brown.utils import units



class LedgerLine(StaffObject):

    def __init__(self, staff, position_x, staff_position, length=None):
        """
        Args:
            staff (Staff): The parent staff
            position_x (float): Position in pixels of the left edge of the line
            staff_position (int): The staff position of the ledger line
            length (float): Length in pixels of the ledger line
        """
        super(LedgerLine, self).__init__(staff, position_x)
        self._staff_position = staff_position
        # HACK --- length should be handled more elegantly later
        self._length = length if length else 1.75 * self.staff.staff_unit
        y_pos = self.staff._staff_pos_to_rel_pixels(self.staff_position)
        self._grob = Path.straight_line(
            self.staff.x + self.position_x,
            self.staff.y + y_pos,
            self.length,
            0,
        )

    ######## PUBLIC PROPERTIES ########

    @property
    def staff_position(self):
        """int: The centered staff position of the ledger line"""
        return self._staff_position

    @property
    def length(self):
        """int: The length in staff units of the ledger line"""
        return self._length

    ######## PUBLIC METHODS ########

    def render(self):
        self.grob.render()