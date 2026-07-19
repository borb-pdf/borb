from borb.pdf.color.x11_color import X11Color
from borb.pdf.document import Document
from borb.pdf.layout_element.annotation.rubber_stamp_annotation import (
    RubberStampAnnotation,
)
from borb.pdf.page import Page
from tests.test_case import TestCase


class TestRubberStampAnnotationBackground(TestCase):

    def test_rubber_stamp_annotation_background(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        RubberStampAnnotation(
            background_color=X11Color.YELLOW_MUNSELL,
            size=(100, 100),
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        TestCase.write(what=d, where_to="test_rubber_stamp_annotation_background.pdf")
