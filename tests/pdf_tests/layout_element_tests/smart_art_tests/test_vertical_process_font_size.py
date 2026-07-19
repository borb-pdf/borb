from borb.pdf import SmartArt, PageSize
from borb.pdf.document import Document
from borb.pdf.page import Page
from borb.pdf.page_layout.page_layout import PageLayout
from borb.pdf.page_layout.single_column_layout import SingleColumnLayout
from tests.test_case import TestCase


class TestVerticalProcessFontSize(TestCase):

    def test_vertical_process_font_size_small(self):
        d: Document = Document()

        p: Page = Page(
            width_in_points=PageSize.A4_LANDSCAPE[0],
            height_in_points=PageSize.A4_LANDSCAPE[1],
        )
        d.append_page(p)

        l: PageLayout = SingleColumnLayout(p)
        l.append_layout_element(
            SmartArt.vertical_process(
                level_1_items=[
                    "Vitamin C",
                    "Potassium",
                    "Vitamin A",
                    "Healthy Fats",
                ],
                level_1_font_size=10,
            )
        )

        TestCase.write(what=d, where_to="test_vertical_process_font_size_small.pdf")

    def test_vertical_process_font_size_regular(self):
        d: Document = Document()

        p: Page = Page(
            width_in_points=PageSize.A4_LANDSCAPE[0],
            height_in_points=PageSize.A4_LANDSCAPE[1],
        )
        d.append_page(p)

        l: PageLayout = SingleColumnLayout(p)
        l.append_layout_element(
            SmartArt.vertical_process(
                level_1_items=[
                    "Vitamin C",
                    "Potassium",
                    "Vitamin A",
                    "Healthy Fats",
                ],
                level_1_font_size=12,
            )
        )

        TestCase.write(what=d, where_to="test_vertical_process_font_size_regular.pdf")

    def test_vertical_process_font_size_large(self):
        d: Document = Document()

        p: Page = Page(
            width_in_points=PageSize.A4_LANDSCAPE[0],
            height_in_points=PageSize.A4_LANDSCAPE[1],
        )
        d.append_page(p)

        l: PageLayout = SingleColumnLayout(p)
        l.append_layout_element(
            SmartArt.vertical_process(
                level_1_items=[
                    "Vitamin C",
                    "Potassium",
                    "Vitamin A",
                    "Healthy Fats",
                ],
                level_1_font_size=16,
            )
        )

        TestCase.write(what=d, where_to="test_vertical_process_font_size_large.pdf")
