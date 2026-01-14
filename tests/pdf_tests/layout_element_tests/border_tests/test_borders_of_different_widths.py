import unittest

from borb.pdf import Button, Paragraph, X11Color
from borb.pdf.document import Document
from borb.pdf.page import Page
from borb.pdf.visitor.pdf import PDF


class TestBordersOfDifferentWidths(unittest.TestCase):

    def test_borders_of_different_widths_no_background(self):

        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        Paragraph(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
            border_color=X11Color.YELLOW_MUNSELL,
            border_width_top=1,
            border_width_right=2,
            border_width_bottom=3,
            border_width_left=4,
            padding_top=5,
            padding_right=5,
            padding_bottom=5,
            padding_left=5,
        ).paint(available_space=(x, y, w, h), page=p)

        PDF.write(
            what=d, where_to="assets/test_borders_of_different_widths_no_background.pdf"
        )

    def test_borders_of_different_widths_with_background(self):

        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        Paragraph(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
            font_color=X11Color.WHITE,
            background_color=X11Color.PRUSSIAN_BLUE,
            border_color=X11Color.YELLOW_MUNSELL,
            border_width_top=1,
            border_width_right=2,
            border_width_bottom=3,
            border_width_left=4,
            padding_top=5,
            padding_right=5,
            padding_bottom=5,
            padding_left=5,
        ).paint(available_space=(x, y, w, h), page=p)

        PDF.write(
            what=d,
            where_to="assets/test_borders_of_different_widths_with_background.pdf",
        )
