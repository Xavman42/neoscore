from PyQt5 import QtWidgets, QtCore

from brown.utils.units import GraphicUnit
from brown.interface.qt_ext.q_clipping_path import QClippingPath


class QEnhancedTextItem(QtWidgets.QGraphicsSimpleTextItem):

    """A text item giving explicit control over positioning and scale.

    This is a modified QGraphicsSimpleTextItem which acts mostly like
    its superclass, with the following extensions:

    * It can be given a rendering offset which forces a painting offset
      indicated by a point vector.
    * It can be given a scaling factor which triggers a hard scale on
      top of its font size. Scaling is performed relative to the origin.
    * It can be clipped to render any horizontal slice of its image.
    """

    def __init__(self,
                 *args,
                 origin_offset=None,
                 scale_factor=1,
                 clip_start_x=None,
                 clip_width=None,
                 **kwargs):
        """
        Args:
            origin_offset(QPointF): The offset of the glyph's origin from (0, 0)
            scale_factor(float): A hard scaling factor.
            clip_start_x (Unit or None): The local starting position for the
                clipping region. Use `None` to render from the start.
            clip_width (Unit or None): The width of the clipping region.
                Use `None` to render to the end

        All other args are passed directly to QGraphicsSimpleTextItem
        """
        self.origin_offset = origin_offset
        self.scale_factor = scale_factor
        self.clip_start_x = clip_start_x
        self.clip_width = clip_width
        super().__init__(*args, **kwargs)

    def boundingRect(self):
        rect = super().boundingRect()
        rect.translate(self.origin_offset * -1)
        scaled_rect = QtCore.QRectF(rect.x() * self.scale_factor,
                                    rect.y() * self.scale_factor,
                                    rect.width() * self.scale_factor,
                                    rect.height() * self.scale_factor)
        return scaled_rect

    def paint(self, painter, option, widget):
        # For some reason, this seems to need to be scaled *before*
        # translating, while the boundingRect needs to be translated
        # before scaling...
        painter.scale(self.scale_factor, self.scale_factor)
        if self.clip_start_x is not None:
            clip_offset = QtCore.QPointF(
                -1 * float(GraphicUnit(self.clip_start_x)), 0)
        else:
            clip_offset = QtCore.QPointF(0, 0)
        painter.translate((self.origin_offset * -1) + clip_offset)

        clip_area = QClippingPath.create_clipping_area(
            # Get clip area in logical (not scaled or offset) space
            super().boundingRect(),
            (self.clip_start_x / self.scale_factor
             if self.clip_start_x is not None else None),
            (self.clip_width / self.scale_factor
             if self.clip_width is not None else None),
            self.pen().width())
        painter.setClipRect(clip_area)

        super().paint(painter, option, widget)
