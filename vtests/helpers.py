import os
import pathlib
import sys
import tempfile

from neoscore.core import neoscore

output_dir = pathlib.Path(__file__).parent / "output"


def render_vtest(name: str):
    if not output_dir.exists():
        os.mkdir(output_dir)
    if "--image" in sys.argv:
        if "--tmp" in sys.argv:
            image_path = pathlib.Path(tempfile.NamedTemporaryFile(suffix=".png").name)
        else:
            image_path = output_dir / f"{name}_image.png"
        neoscore.render_image(
            neoscore.document.pages[0].document_space_bounding_rect, image_path
        )

    elif "--pdf" in sys.argv:
        # PDF export is currently broken
        if "--tmp" in sys.argv:
            pdf_path = pathlib.Path(tempfile.NamedTemporaryFile(suffix=".pdf").name)
        else:
            pdf_path = output_dir / f"{name}_pdf.pdf"
        neoscore.render_pdf(pdf_path)
    else:
        neoscore.show()
