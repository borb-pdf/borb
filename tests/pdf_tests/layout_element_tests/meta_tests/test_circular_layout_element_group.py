import random

from borb.pdf import Document, Page, LayoutElement, Lipsum, Paragraph, X11Color
from borb.pdf.layout_element.meta.circular_layout_element_group import (
    CircularLayoutElementGroup,
)
from tests.test_case import TestCase


class TestCircularLayoutElementGroup(TestCase):

    def test_circular_layout_element_group(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        random.seed(0)
        CircularLayoutElementGroup(
            layout_elements=[
                Paragraph(
                    Lipsum.generate_lorem_ipsum(64),
                    font_size=8,
                    background_color=X11Color.YELLOW_MUNSELL,
                    text_alignment=LayoutElement.TextAlignment.JUSTIFIED,
                )
                for _ in range(0, 6)
            ],
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        TestCase.write(what=d, where_to="test_circular_layout_element_group.pdf")
