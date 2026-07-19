from borb.pdf.document import Document
from borb.pdf.layout_element.annotation.squiggly_annotation import SquigglyAnnotation
from borb.pdf.page import Page
from tests.test_case import TestCase


class TestSquigglyAnnotation(TestCase):

    def test_squiggly_annotation(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        # add SquigglyAnnotation
        SquigglyAnnotation(
            size=(100, 100),
        ).paint(
            available_space=(
                x,
                y,
                w,
                h,
            ),
            page=p,
        )

        TestCase.write(what=d, where_to="test_squiggly_annotation.pdf")
