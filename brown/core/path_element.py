from brown.core.invisible_object import InvisibleObject
from brown.core.path_element_type import PathElementType


class PathElement(InvisibleObject):
    """A point with a parent to be use in Path objects.

    Although this is a GraphicObject, typically in practice they will be
    invisible.
    """
    def __init__(self, pos, element_type, path, parent=None):
        """
        Args:
            pos (Point): The position of the element relative to its parent
            element_type (PathElementType or int): The type of the element
            path (Path): The path this element belongs in
            parent (GraphicObject): The parent object. If None, the parent
                will be the path.
        """
        super().__init__(pos, parent=parent)
        self.parent_path = path
        self.element_type = element_type

    ######## PUBLIC PROPERTIES ########

    @property
    def element_type(self):
        """PathElementType: Enumeration for the type of element.

        This value is read-only.
        """
        return self._element_type
        return self._path_element_interface.element_type

    @element_type.setter
    def element_type(self, value):
        self._element_type = PathElementType(value)

    ######## PRIVATE METHODS ########

    @staticmethod
    def _assert_soft_equal(first, second):
        """An internal soft equality assertion for testing.

        Tells whether the following properties are equal with another object:

            * Type
            * pos
            * parent
            * parent_path
            * element_type

        WARNING: This is for testing purposes only.

        Returns: Bool

        Raises: AssertionError
        """
        assert(type(first) == type(second) == PathElement)
        assert(first.pos == second.pos)
        assert(first.parent == second.parent)
        assert(first.parent_path == second.parent_path)
        assert(first.element_type == second.element_type)
