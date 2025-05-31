import unittest

from borb.pdf.document import Document
from borb.pdf.font.font import Font
from borb.pdf.font.simple_font.standard_14_fonts import Standard14Fonts
from borb.pdf.layout_element.text.chunk import Chunk
from borb.pdf.page import Page
from borb.pdf.visitor.pdf import PDF


class TestSymbol(unittest.TestCase):

    def test_symbol(self):

        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # font
        font: Font = Standard14Fonts.get("Symbol")

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        Chunk("Σ", font=font).paint(available_space=(x, y, w, h), page=p)

        PDF.write(what=d, where_to="assets/test_symbol.pdf")
