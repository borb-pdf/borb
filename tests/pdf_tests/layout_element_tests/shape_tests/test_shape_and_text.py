from borb.pdf import (
    Document,
    Page,
    SingleColumnLayout,
    PageLayout,
    LineArt,
    Paragraph,
    Shape,
    X11Color,
)
from tests.test_case import TestCase


class TestShapeAndText(TestCase):

    def test_shape_and_text(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        layout: PageLayout = SingleColumnLayout(p)

        layout.append_layout_element(LineArt.n_gon(3))
        layout.append_layout_element(Paragraph("Lorem Ipsum"))

        TestCase.write(what=d, where_to="test_shape_and_text.pdf")

    def test_shape_and_shape(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        layout: PageLayout = SingleColumnLayout(p)

        layout.append_layout_element(
            Shape(
                coordinates=[
                    [(0, 0), (50, 50), (0, 100), (0, 0)],
                    [(0, 100), (50, 150), (0, 200), (0, 100)],
                ],
                background_color=None,
                stroke_color=X11Color.BLACK,
            )
        )

        print(p["Contents"]["DecodedBytes"].decode("latin1"))
        TestCase.write(what=d, where_to="test_shape_and_shape.pdf")
