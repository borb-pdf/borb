from borb.pdf.document import Document
from borb.pdf.layout_element.image.image import Image
from borb.pdf.page import Page
from tests.test_case import TestCase


class TestImage(TestCase):

    def test_image_001(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        Image(
            bytes_path_pil_image_or_url="https://images.unsplash.com/photo-1717942110740-80424da8eccc",
            size=(100, 100),
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        TestCase.write(what=d, where_to="test_image_001.pdf")

    def test_image_002(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        Image(
            bytes_path_pil_image_or_url="https://images.unsplash.com/photo-1778596301893-f919b121dd43",
            size=(100, 100),
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        TestCase.write(what=d, where_to="test_image_002.pdf")
