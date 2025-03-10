# 0.1.13 (2023-02-13)
- Fix `breakable_length` on all built-in spanners. Users with custom spanners should see [the updated documentation](https://neoscore.org/api/neoscore.core.spanner.html) on proper superclass declaration order.
- Make `PaintedObject.parent` no longer a kwarg providing a default `= None`. This aligns the class with how we do this everywhere else. This is technically a breaking change, but it's largely an internal class so we don't expect any users will be affected.

# 0.1.12 (2023-01-29)
- Add support for 8va treble clefs ('treble_8va') and bridge clefs ('bridge'). Bridge clef acts like percussion clefs - it uses the center staff position as middle C regardless of staff line count.
- Add support for image transparency with new `opacity` field. The field is accessible through the `Image` constructor and a new `opacity` property.
- Add built-in tremolo support with new `Tremolo` class (by @craigvear)
- Replace `Chordrest.notehead_column_width` with more general `Chordrest.notehead_column_bounding_rect`. This new method corrects some bugs with the implementation of the old method.

# 0.1.11 (2023-01-05)

- Fix bug where viewport scales were set and got incorrectly (#89)
- Fix viewport scaling support in Python < 3.8
- Slightly improve initial scene render performance by not clearing the scene before rendering.
- Support optimizing refresh functions when the scene doesn't change in every frame. This is done with a new class `neoscore.RefreshFuncResut`, which provided refresh functions can return. The class has a field, `scene_render_needed: bool = True` which tells neoscore whether it needs to clear and re-render the scene after the refresh function returns. This can be set to `False` in situations where the scene did not change in the frame, a significant optimization in complex scenes. It should be noted though that in complex scenes this could result in a noticeable frame rate drop when the scene _does_ change. The `input_scene_interaction` example has been updated to demonstrate this capability.
- Fix bounding rects on qt paths not starting at local origin, causing clipping errors on many objects, especially text objects.

# 0.1.10 (2022-12-20)

- Dataclass tweaks to support Python 3.11 breaking changes.

# 0.1.9 (2022-12-15)

- Create a dedicated `Tie` class for ties. Both it and `Slur` now inherit from a shared `AbstractSlur` class which provides common drawing functionality. `Tie` is a nice convenience class in that it is automatically kept horizontal; in the future it may also be shaped slightly differently than a slur. (by @craigvear)
- Add a new method `PositionedObject.distance_to` which provides a convenient way to find the Euclidean distance to another object.
- Add document-space positions to mouse events

# 0.1.8 (2022-12-02)

- Add a new `Tuplet` class for simple notation of tuplets. (by @craigvear)
- Add a new method `Spanner.point_along_spanner` for easily finding points along the spanner's line.
- Switch to using the [pre-commit](https://pre-commit.com/) framework for our precommit hooks, improving stability and cross-platform dev environment support. See the updated [`CONTRIBUTING.md`](/CONTRIBUTING.md) file for new pre-commit setup instructions. You can easily migrate by first installing new dependencies with `poetry install` then setting up the new pre-commit hook with `pre-commit install -f`.
- Fix a bug where `PedalLine` without half-lift positions errored. (by @craigvear)

# 0.1.7 (2022-10-03) - BREAKING CHANGE

This release includes substantial breaking changes. See [the announcement post](https://github.com/DigiScore/neoscore/discussions/73) for more information.

- Fix [clipping of thick pens](https://github.com/DigiScore/neoscore/issues/14) thanks to help from @Xavman42.
- Add a new field `transform_origin` to all graphical objects and corresponding interface classes, with help from @Xavman42. This new field sets the origin point (relative to the object's `pos`) for rotation and scaling.
- Explicit z-index support has been removed. Stacking order is now strictly set by the order of the document tree's depth-first traversal.
- The interface and Qt layer now reflects the document parent-child tree outside of flowable contexts. Interface classes now have a `parent` field. Outside flowables, interfaces are now given positions relative to their parent, another interface set with the parent object's position and transform properties. Inside flowables, interfaces are given no parent and they still receive global document-based positions. See `PositionedObject.render_complete()` and `PositionedObject.interface_for_children` for more.
- Rotation and scaling transforms are now inherited by children outside flowable contexts.
- Paths now support scaling

# 0.1.6 (2022-07-27)
- Fix bug affecting path resolution in image export on Windows with Python 3.7

# 0.1.5 (2022-07-27)
- Fix bug breaking support on Python 3.7

# 0.1.4 (2022-07-17)
- Fix bug where chordrest flags were not properly reset when rebuilding chords after mutations
- Added built-in support for mouse event handlers with `neoscore.set_mouse_event_handler`.
- Added built-in support for keyboard event handlers with `neoscore.set_key_event_handler`.

# 0.1.3 (2022-07-07)
- Reduce minimum Python version to 3.7
- Fix bug where arrowkeys still scrolled the viewport with `neoscore.show(auto_viewport_interaction_enabled=False)`


# 0.1.2 (2022-07-02)
- Support disabling automatic viewport interaction with `neoscore.show(auto_viewport_interaction_enabled=False)`. This disables scroll-zooming, drag-moving, and the appearance of window scrollbars.
- Support setting the preview window size with new `neoscore.show()` options `min_window_size` and `max_window_size`.
- Support launching the preview window in fullscreen mode with `neoscore.show(fullscreen=True)`.
- Support programmatically controlling the viewport's center position, scale (zoom), and rotation with `neoscore.set_viewport_center_pos()`, `neoscore.set_viewport_scale()`, and `neoscore.set_viewport_rotation()`. Corresponding getters are also provided.

# 0.1.1 (2022-05-20)

- [Fixed PDF export on Windows](https://github.com/DigiScore/neoscore/issues/37)
- Updated `neoscore.render_image()` to block by default. Set the new kwarg `wait=False` to finalize export asynchronously.
- Fixed bug where image and PDF export exceptions could be ignored. Exceptions in image export threads now propagate on join via the new `PropagatingThread` class.

# 0.1.0 (2020-05-15)

Initial release! ❤️❤️❤️
