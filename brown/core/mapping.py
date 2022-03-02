from __future__ import annotations

from typing import Any, Iterator, Optional, Protocol, Type, Union

from brown.core.page import Page
from brown.utils.point import ORIGIN, Point
from brown.utils.units import ZERO, Unit


class Positioned(Protocol):
    @property
    def pos(self) -> Point:
        ...

    @property
    def parent(self) -> Positioned:
        ...


def ancestors(obj: Positioned) -> Iterator[Positioned]:
    """All ancestors of this object.

    Follows the chain of parents up to the document root.

    The order begins with `self.parent` and traverses upward in the document tree.
    """
    ancestor = obj.parent
    while True:
        yield (ancestor)
        if type(ancestor).__name__ == "Document":
            break
        ancestor = ancestor.parent


def map_between(src: Positioned, dst: Positioned) -> Point:
    """Find a Positioned object's logical position relative to another

    This calculates the position in *logical* space, which differs
    from canvas space in that it doesn't account for repositioning of
    objects inside `Flowable` containers. For example, this function
    will return the same relative position for two objects in a
    `Flowable` container whether or not they are separated by a line
    break.

    Args:
        src: The object to map from
        dst: The object to map to
    """
    # Handle easy cases
    if src == dst:
        return ORIGIN
    if src.parent == dst.parent:
        return dst.pos - src.pos
    if dst.parent == src:
        return dst.pos
    if src.parent == dst:
        return -src.pos
    # Start by collecting all ancestor using IDs because they're hashable
    src_ancestor_ids = set(id(grob) for grob in ancestors(src))
    relative_dst_pos = dst.pos
    for dst_ancestor in ancestors(dst):
        # TODO MEDIUM find a better way to do these is-root-node checks
        if type(dst_ancestor).__name__ != "Document":
            relative_dst_pos += dst_ancestor.pos
        if id(dst_ancestor) in src_ancestor_ids:
            # Now find relative_src_pos and return relative_dst_pos - relative_src_pos
            relative_src_pos = src.pos
            for src_ancestor in ancestors(src):
                if type(src_ancestor).__name__ != "Document":
                    relative_src_pos += src_ancestor.pos
                if src_ancestor == dst_ancestor:
                    return relative_dst_pos - relative_src_pos
            # Since we've already determined there is a common
            # ancestor, this should never happen
            assert False, "Unreachable"
    raise ValueError(f"{src} and {dst} have no common ancestor")


def map_between_x(src: Positioned, dst: Positioned) -> Unit:
    # TODO once main function is shown to work, copy here and edit as needed
    return map_between(src, dst).x


def descendant_pos(descendant: Positioned, ancestor: Positioned) -> Point:
    """Find the position of a descendant relative to one of its ancestors.

    Raises:
        ValueError: If `ancestor` is not an ancestor of `descendant`
    """
    pos = descendant.pos
    for parent in ancestors(descendant):
        if parent == ancestor:
            return pos
        pos += parent.pos
    raise ValueError(f"{ancestor} is not an ancestor of {descendant}")


def descendant_pos_x(descendant: Positioned, ancestor: Positioned) -> Unit:
    """Find the x position of a descendant relative to one of its ancestors.

    This is a specialized version of `descendant_pos` provided for optimization.

    Raises:
        ValueError: If `ancestor` is not an ancestor of `descendant`
    """
    pos_x = descendant.pos.x
    for parent in ancestors(descendant):
        if parent == ancestor:
            return pos_x
        pos_x += parent.pos.x
    raise ValueError(f"{ancestor} is not an ancestor of {descendant}")


# this doesn't really belong here...


def first_ancestor_of_exact_class(
    positioned: Positioned, type_: Union[str, Type]
) -> Optional[Any]:
    """Get a `Positioned` object's nearest ancestor with a class.

    If none can be found, returns `None`.

    Args:
        graphic_object_class (type or str): The type to search for.
            This should be a subclass of GraphicObject.
            A str of a class name may also be used.

    Returns: GraphicObject or None
    """
    if isinstance(type_, str):
        return next(
            (item for item in ancestors(positioned) if type(item).__name__ == type_),
            None,
        )
    return next(
        (item for item in ancestors(positioned) if type(item) == type_),
        None,
    )