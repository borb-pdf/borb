from borb.pdf import SmartArt
from borb.pdf.document import Document
from borb.pdf.page import Page
from borb.pdf.page_layout.page_layout import PageLayout
from borb.pdf.page_layout.single_column_layout import SingleColumnLayout
from tests.test_case import TestCase


class TestVerticalEquation(TestCase):

    def test_vertical_equation_3_items(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        l: PageLayout = SingleColumnLayout(p)
        l.append_layout_element(
            SmartArt.vertical_equation(
                level_1_items=[
                    "Vitamin C",
                    "Potassium",
                    "Vitamin A",
                ],
            )
        )

        TestCase.write(what=d, where_to="test_vertical_equation_3_items.pdf")

    def test_vertical_equation_4_items(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        l: PageLayout = SingleColumnLayout(p)
        l.append_layout_element(
            SmartArt.vertical_equation(
                level_1_items=[
                    "Vitamin C",
                    "Potassium",
                    "Vitamin A",
                    "Healthy Fats",
                ],
            )
        )

        TestCase.write(what=d, where_to="test_vertical_equation_4_items.pdf")
