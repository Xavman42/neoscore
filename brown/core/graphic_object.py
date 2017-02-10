from abc import ABC

from brown.utils.units import Unit
from brown.utils.point import Point


class GraphicObject(ABC):
    """An abstract graphic object.

    All classes in `core` which have the ability to be displayed
    should be subclasses of this.

    A single GraphicObject can have multiple graphical representations,
    calculated at render-time. If the object's ancestor is a FlowableFrame,
    it will be rendered as a flowable object, capable of being wrapped around
    lines.
    """
    def __init__(self, pos, breakable_width=None,
                 pen=None, brush=None, parent=None):
        """
        Args:
            pos (Point[Unit] or tuple): The position of the object
                relative to its parent
            breakable_width (Unit): The width of the object which can be
                subject to breaking across line breaks when in a FlowableFrame.
                If the object is not inside a FlowableFrame, this has no effect
            pen (Pen): The pen to draw outlines with.
            brush (Brush): The brush to draw outlines with.
            parent (GraphicObject): The parent object or None
        """
        self.pos = pos
        self._breakable_width = (breakable_width if breakable_width
                                 else Unit(0))
        self.pen = pen
        self.brush = brush
        self._children = set()
        self.parent = parent
        self._interfaces = set()

    ######## PUBLIC PROPERTIES ########

    @property
    def interfaces(self):
        """set{GraphicObjectInterface}: The interfaces for this object

        Interface objects are created upon calling `GraphicObject.render()`

        Typically each GraphicObject will have one interface for each
        flowable line it appears in. Objects which fit completely
        in one visual line will typically have exactly one interface.

        If this is an empty set, the object has not been rendered yet
        with the `render()` method.
        """
        return self._interfaces

    @property
    def pos(self):
        """Point: The position of the object relative to its parent."""
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = Point(value)

    @property
    def x(self):
        """Unit: The x position of the object relative to its parent."""
        return self.pos.x

    @x.setter
    def x(self, value):
        self.pos.x = value

    @property
    def y(self):
        """Unit: The x position of the object relative to its parent."""
        return self.pos.y

    @y.setter
    def y(self, value):
        self.pos.y = value

    @property
    def breakable_width(self):
        """Unit: The breakable_width of the object.

        This is used to determine how and where rendering cuts should be made.
        """
        return self._breakable_width

    @property
    def pen(self):
        """Pen: The pen to draw outlines with"""
        return self._pen

    @pen.setter
    def pen(self, value):
        self._pen = value

    @property
    def brush(self):
        """Brush: The brush to draw outlines with"""
        return self._brush

    @brush.setter
    def brush(self, value):
        self._brush = value

    @property
    def parent(self):
        """GraphicObject: The parent object"""
        return self._parent

    @parent.setter
    def parent(self, value):
        if hasattr(self, '_parent') and self._parent is not None:
            self._parent._unregister_child(self)
        self._parent = value
        if self._parent is not None:
            self._parent._register_child(self)

    @property
    def children(self):
        """set{GraphicObject}: All objects who have self as their parent."""
        return self._children

    @children.setter
    def children(self, value):
        self._children = value

    @property
    def frame(self):
        """FlowableFrame or None: The frame this object belongs in.

        This property is read-only
        """
        try:
            ancestor = self.parent
            while type(ancestor).__name__ != 'FlowableFrame':
                ancestor = ancestor.parent
            return ancestor
        except AttributeError:
            return None

    @property
    def is_in_flowable(self):
        """bool: Whether or not this object is in a FlowableFrame"""
        return (self.frame is not None)

    @property
    def document_pos(self):
        """Point: The position of the object in document space."""
        if self.is_in_flowable:
            return self.frame._map_to_doc(self.pos)
        else:
            raise NotImplementedError  # TODO

    ######## CLASS METHODS ########

    @classmethod
    def map_from_origin(cls, item):
        """Find an object's position relative to the document origin.

        Return: Point

        TODO: This doesn't actually work for objects *not* in a Flowable
              (such as a flowable itself). The FlowableFrame._map_to_doc
              method compensates for page offsets in the document space,
              while this does not!

              The logic around the difference between logical document
              space and real, visual document space (including page
              margins) clearly needs to be worked out further!
        """
        if not isinstance(item, GraphicObject):
            raise TypeError(
                'Cannot map {} from origin'.format(type(item).__name__))
        pos = Point(Unit(0), Unit(0))
        current = item
        while current is not None:
            pos += current.pos
            current = current.parent
            if type(current).__name__ == 'FlowableFrame':
                # If it turns out we are inside a flowable frame,
                # just short circuit and ask it where we are
                return current._map_to_doc(pos)
        return pos

    @classmethod
    def map_between_items(cls, source, destination):
        """Find a GraphicObject's position relative to another GraphicObject

        Args:
            source (GraphicObject): The object to map from
            destination (GraphicObject): The object to map to

        Returns: Point
        """
        # inefficient for now - find position relative to doc root of both
        # and find delta between the two.
        return (cls.map_from_origin(destination) -
                cls.map_from_origin(source))

    ######## PUBLIC METHODS ########

    def render(self):
        """Render the object to the scene.

        Returns: None
        """
        if self.is_in_flowable:
            self._render_flowable()
        else:
            self._render_complete(self.pos)

    ######## PRIVATE METHODS ########

    def _register_child(self, child):
        """Add an object to `self.children`.

        Args:
            child (GraphicObject): The object to add

        Returns: None
        """
        self.children.add(child)

    def _unregister_child(self, child):
        """Remove an object from `self.children`.

        Args:
            child (GraphicObject): The object to remove

        Returns: None
        """
        self.children.remove(child)

    def _render_flowable(self):
        """Render the object to the scene, dispatching partial rendering calls
        when needed if an object flows across a break in the frame.

        Returns: None
        """
        # TODO: Clean up!
        remaining_x = self.breakable_width
        remaining_x += self.frame._dist_to_line_end(self.x)
        if remaining_x < 0:
            self._render_complete(GraphicObject.map_from_origin(self))
            return

        # Calculate position within flowable
        # (HACK while map_between_items with source=FlowableFrame is broken)
        pos_in_flowable = Point(Unit(0), Unit(0))
        current = self
        while type(current).__name__ != 'FlowableFrame':
            pos_in_flowable += current.pos
            current = current.parent

        # Render before break
        first_line_i = self.frame._last_break_index_at(pos_in_flowable.x)
        current_line = self.frame.layout_controllers[first_line_i]
        render_start_pos = GraphicObject.map_from_origin(self)
        first_line_length = self.frame._dist_to_line_end(pos_in_flowable.x) * -1
        render_end_pos = (render_start_pos + Point(first_line_length, 0))
        self._render_before_break(Unit(0), render_start_pos, render_end_pos)

        # Iterate through remaining breakable_width
        for current_line_i in range(first_line_i + 1,
                                    len(self.frame.layout_controllers)):
            current_line = self.frame.layout_controllers[current_line_i]
            if remaining_x > current_line.length:
                # Render spanning continuation
                render_start_pos = self.frame._map_to_doc(
                    Point(current_line.x, pos_in_flowable.y))
                render_end_pos = render_start_pos + Point(current_line.length, 0)
                self._render_spanning_continuation(
                    self.breakable_width - remaining_x,
                    render_start_pos,
                    render_end_pos)
                remaining_x -= current_line.length
            else:
                break

        # Render end
        render_start_pos = self.frame._map_to_doc(
            Point(current_line.x, pos_in_flowable.y))
        render_end_pos = render_start_pos + Point(remaining_x, 0)
        self._render_after_break(self.breakable_width - remaining_x,
                                 render_start_pos,
                                 render_end_pos)

    def _render_complete(self, pos):
        """Render the entire object.

        For use in flowable containers when rendering a FlowableObject
        which happens to completely fit within a span of the FlowableFrame.
        This function should render the entire object at `self.pos`

        This method should create a GraphicInterface and store it in
        `self.interfaces`.

        Args:
            pos (Point): The rendering position in document space for drawing.

        Returns: None

        Note: All GraphicObject subclasses should implement this
              for correct rendering.
        """
        raise NotImplementedError

    def _render_before_break(self, local_start_x, start, stop):
        """Render the beginning of the object up to a stopping point.

        For use in flowable containers when rendering an object that
        crosses a line or page break. This function should render the
        beginning portion of the object up to the break.

        This method should create a GraphicInterface and store it in
        `self.interfaces`.

        Args:
            local_start_x (Unit): The local starting position of this
                drawing segment.
            start (Point): The starting point in document space for drawing.
            stop (Point): The stopping point in document space for drawing.

        Returns: None

        Note: Any GraphicObject subclasses whose breakable_width can
              be nonzero must implement this method.
        """
        raise NotImplementedError

    def _render_after_break(self, local_start_x, start, stop):
        """Render the continuation of an object after a break.

        For use in flowable containers when rendering an object that
        crosses a line or page break. This function should render the
        ending portion of an object after a break.

        This method should create a GraphicInterface and store it in
        `self.interfaces`.

        Args:
            local_start_x (Unit): The local starting position of this
                drawing segment.
            start (Point): The starting point in document space for drawing.
            stop (Point): The stopping point in document space for drawing.

        Returns: None

        Note: Any GraphicObject subclasses whose breakable_width can
              be nonzero must implement this method.
        """
        raise NotImplementedError

    def _render_spanning_continuation(self, local_start_x, start, stop):
        """
        Render the continuation of an object after a break and before another.

        For use in flowable containers when rendering an object that crosses
        two breaks. This function should render the portion of the object
        surrounded by breaks on either side.

        This method should create a GraphicInterface and store it in
        `self.interfaces`.

        Args:
            local_start_x (Unit): The local starting position of this
                drawing segment.
            start (Point): The starting point in document space for drawing.
            stop (Point): The stopping point in document space for drawing.

        Returns: None

        Note: Any GraphicObject subclasses whose breakable_width can
              be nonzero must implement this method.
        """
        raise NotImplementedError
