from borb.pdf import SmartArt
from borb.pdf.document import Document
from borb.pdf.page import Page
from borb.pdf.page_layout.page_layout import PageLayout
from borb.pdf.page_layout.single_column_layout import SingleColumnLayout
from tests.test_case import TestCase


class TestVerticalBulletListFontSize(TestCase):

    def test_vertical_bullets_list_font_size_small(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        l: PageLayout = SingleColumnLayout(p)
        l.append_layout_element(
            SmartArt.vertical_bullet_list(
                level_1_items=["Cherries", "Papaya", "Avocado"],
                level_2_items=[
                    ["Vitamin C", "Potassium"],
                    ["Vitamin C", "Vitamin A"],
                    ["Potassium", "Healthy Fats", "Fiber"],
                ],
                level_1_font_size=8,
                level_2_font_size=6,
            )
        )

        TestCase.write(
            what=d, where_to="test_vertical_bullets_list_font_size_small.pdf"
        )

    def test_vertical_bullets_list_font_size_regular(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        l: PageLayout = SingleColumnLayout(p)
        l.append_layout_element(
            SmartArt.vertical_bullet_list(
                level_1_items=["Cherries", "Papaya", "Avocado"],
                level_2_items=[
                    ["Vitamin C", "Potassium"],
                    ["Vitamin C", "Vitamin A"],
                    ["Potassium", "Healthy Fats", "Fiber"],
                ],
                level_1_font_size=12,
                level_2_font_size=10,
            )
        )

        TestCase.write(
            what=d, where_to="test_vertical_bullets_list_font_size_regular.pdf"
        )

    def test_vertical_bullets_list_font_size_large(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        l: PageLayout = SingleColumnLayout(p)
        l.append_layout_element(
            SmartArt.vertical_bullet_list(
                level_1_items=["Cherries", "Papaya", "Avocado"],
                level_2_items=[
                    ["Vitamin C", "Potassium"],
                    ["Vitamin C", "Vitamin A"],
                    ["Potassium", "Healthy Fats", "Fiber"],
                ],
                level_1_font_size=16,
                level_2_font_size=14,
            )
        )

        TestCase.write(
            what=d, where_to="test_vertical_bullets_list_font_size_large.pdf"
        )
