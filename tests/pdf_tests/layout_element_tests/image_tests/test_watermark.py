import pathlib
import unittest

from borb.pdf import SingleColumnLayout, PageLayout, Paragraph, Lipsum, LayoutElement, Image, X11Color, Color, RGBColor
from borb.pdf.document import Document
from borb.pdf.layout_element.image.watermark import Watermark
from borb.pdf.page import Page
from borb.pdf.visitor.pdf import PDF


class TestWatermark(unittest.TestCase):


    def test_watermark(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        l: PageLayout = SingleColumnLayout(p)
        for _ in range(0, 5):
           l.append_layout_element(Paragraph(Lipsum.generate_lorem_ipsum(512),
                                             text_alignment=LayoutElement.TextAlignment.JUSTIFIED))

        l.append_layout_element(Watermark(text='CONFIDENTIAL',
                                          font_size=40,
                                          font_color=X11Color.DARK_RED))

        PDF.write(what=d, where_to="assets/test_watermark.pdf")
