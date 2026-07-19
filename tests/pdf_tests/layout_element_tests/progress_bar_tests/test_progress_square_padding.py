from borb.pdf.document import Document
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.layout_element.progress_bar.progress_square import ProgressSquare
from borb.pdf.page import Page
from tests.pdf_tests.visual_assert import VisualAssert
from tests.test_case import TestCase


class TestProgressSquare(TestCase):

    def test_progress_square_padding_left(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        ProgressSquare(
            value=33,
            padding_left=100,
            horizontal_alignment=LayoutElement.HorizontalAlignment.LEFT,
            vertical_alignment=LayoutElement.VerticalAlignment.TOP,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        TestCase.write(
            what=d,
            where_to=TestCase.get_assets_dir()
            / "test_progress_square_padding_left.pdf",
        )
        VisualAssert.assert_equals(
            TestCase.get_ground_truth_dir() / "test_progress_square_padding_left.png",
            TestCase.get_assets_dir() / "test_progress_square_padding_left.pdf",
        )

    def test_progress_square_padding_top(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        ProgressSquare(
            value=33,
            padding_top=100,
            horizontal_alignment=LayoutElement.HorizontalAlignment.LEFT,
            vertical_alignment=LayoutElement.VerticalAlignment.TOP,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        TestCase.write(
            what=d,
            where_to=TestCase.get_assets_dir() / "test_progress_square_padding_top.pdf",
        )
        VisualAssert.assert_equals(
            TestCase.get_ground_truth_dir() / "test_progress_square_padding_top.png",
            TestCase.get_assets_dir() / "test_progress_square_padding_top.pdf",
        )

    def test_progress_square_padding_right(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        ProgressSquare(
            value=33,
            padding_right=100,
            horizontal_alignment=LayoutElement.HorizontalAlignment.RIGHT,
            vertical_alignment=LayoutElement.VerticalAlignment.BOTTOM,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        TestCase.write(
            what=d,
            where_to=TestCase.get_assets_dir()
            / "test_progress_square_padding_right.pdf",
        )
        VisualAssert.assert_equals(
            TestCase.get_ground_truth_dir() / "test_progress_square_padding_right.png",
            TestCase.get_assets_dir() / "test_progress_square_padding_right.pdf",
        )

    def test_progress_square_padding_bottom(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        ProgressSquare(
            value=33,
            padding_bottom=100,
            horizontal_alignment=LayoutElement.HorizontalAlignment.RIGHT,
            vertical_alignment=LayoutElement.VerticalAlignment.BOTTOM,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        TestCase.write(
            what=d,
            where_to=TestCase.get_assets_dir()
            / "test_progress_square_padding_bottom.pdf",
        )
        VisualAssert.assert_equals(
            TestCase.get_ground_truth_dir() / "test_progress_square_padding_bottom.png",
            TestCase.get_assets_dir() / "test_progress_square_padding_bottom.pdf",
        )
