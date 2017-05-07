import os

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtPrintSupport import QPrinter

from brown import config
from brown.interface.qt_to_util import rect_to_qt_rect_f
from brown.utils.exceptions import FontRegistrationError


class AppInterface:
    """The primary interface to the application state.

    This holds much of the global state for interacting with the API,
    and must be created (and `create_document()` must be called) before
    working with the API.
    """

    def __init__(self, document):
        """
        Args:
            document (Document):
        """
        self.document = document
        self.app = QtWidgets.QApplication([])
        self.scene = QtWidgets.QGraphicsScene()
        self.registered_music_fonts = {}
        self.view = QtWidgets.QGraphicsView(self.scene)
        self.view.setRenderHint(QtGui.QPainter.Antialiasing)

    ######## PUBLIC METHODS ########

    def show(self):
        """Open a window showing a preview of the document."""
        print('Launching Qt Application instance')
        self.view.show()
        self.app.exit(self.app.exec_())

    def render_pdf(self, pages, path):
        """Render the document to a pdf file.

        Args:
            pages (iter[int]): The page numbers to render
            path (str): An output file path.

        Warning: If the file at `path` already exists, it will be overwritten.
        """
        printer = QPrinter()
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setOutputFileName(os.path.realpath(path))
        printer.setResolution(config.PRINT_DPI)
        printer.setPageLayout(self.document.paper._to_interface())
        painter = QtGui.QPainter()
        painter.begin(printer)
        # Scaling ratio for Qt point 72dpi -> config.PRINT_DPI
        ratio = (config.PRINT_DPI / 72)
        target_rect_unscaled = printer.paperRect(QPrinter.Point)
        target_rect_scaled = QtCore.QRectF(
            target_rect_unscaled.x() * ratio,
            target_rect_unscaled.y() * ratio,
            target_rect_unscaled.width() * ratio,
            target_rect_unscaled.height() * ratio,
        )
        for page_number in pages:
            source_rect = rect_to_qt_rect_f(
                self.document.paper_bounding_rect(page_number))
            self.scene.render(painter, target=target_rect_scaled, source=source_rect)
            printer.newPage()
        painter.end()

    def destroy(self):
        """Destroy the window and all global interface-level data."""
        print('Tearing down Qt Application instance')
        self.app.exit()
        self.app = None
        self.scene = None

    ######## STATIC METHODS ########

    @staticmethod
    def register_font(font_file_path):
        """Register a list of fonts to the graphics engine.

        Args:
            font_file_path (str): A list of paths to font files.
                Paths may be either absolute or relative to the package-level
                `brown` directory. (One folder below the top)

        Returns: None

        Raises: FontRegistrationError: If the font could not be loaded.
            Typically, this is because the given path does not lead to
            a valid font file.
        """
        font_id = QtGui.QFontDatabase.addApplicationFont(font_file_path)
        # Qt returns -1 if something went wrong.
        if font_id == -1:
            raise FontRegistrationError(font_file_path)
