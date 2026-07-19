from borb.pdf import SmartArt, X11Color
from borb.pdf.document import Document
from borb.pdf.page import Page
from borb.pdf.page_layout.page_layout import PageLayout
from borb.pdf.page_layout.single_column_layout import SingleColumnLayout
from tests.test_case import TestCase


class TestHorizontalBulletListColor(TestCase):

    def test_horizontal_bullets_list_color_red(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        l: PageLayout = SingleColumnLayout(p)
        l.append_layout_element(
            SmartArt.horizontal_bullet_list(
                level_1_items=["Cherries", "Papaya", "Avocado"],
                level_2_items=[
                    ["Vitamin C", "Potassium"],
                    ["Vitamin C", "Vitamin A"],
                    ["Potassium", "Healthy Fats", "Fiber"],
                ],
                level_1_font_color=X11Color.BLACK,
                level_2_font_color=X11Color.DARK_GRAY,
                background_color=X11Color.RED,
            )
        )

        TestCase.write(what=d, where_to="test_horizontal_bullets_list_color_red.pdf")

    def test_horizontal_bullets_list_color_orange(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        l: PageLayout = SingleColumnLayout(p)
        l.append_layout_element(
            SmartArt.horizontal_bullet_list(
                level_1_items=["Cherries", "Papaya", "Avocado"],
                level_2_items=[
                    ["Vitamin C", "Potassium"],
                    ["Vitamin C", "Vitamin A"],
                    ["Potassium", "Healthy Fats", "Fiber"],
                ],
                level_1_font_color=X11Color.BLACK,
                level_2_font_color=X11Color.DARK_GRAY,
                background_color=X11Color.ORANGE,
            )
        )

        TestCase.write(what=d, where_to="test_horizontal_bullets_list_color_orange.pdf")

    def test_horizontal_bullets_list_color_yellow(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        l: PageLayout = SingleColumnLayout(p)
        l.append_layout_element(
            SmartArt.horizontal_bullet_list(
                level_1_items=["Cherries", "Papaya", "Avocado"],
                level_2_items=[
                    ["Vitamin C", "Potassium"],
                    ["Vitamin C", "Vitamin A"],
                    ["Potassium", "Healthy Fats", "Fiber"],
                ],
                level_1_font_color=X11Color.BLACK,
                level_2_font_color=X11Color.DARK_GRAY,
                background_color=X11Color.YELLOW_MUNSELL,
            )
        )

        TestCase.write(what=d, where_to="test_horizontal_bullets_list_color_yellow.pdf")

    def test_horizontal_bullets_list_color_green(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        l: PageLayout = SingleColumnLayout(p)
        l.append_layout_element(
            SmartArt.horizontal_bullet_list(
                level_1_items=["Cherries", "Papaya", "Avocado"],
                level_2_items=[
                    ["Vitamin C", "Potassium"],
                    ["Vitamin C", "Vitamin A"],
                    ["Potassium", "Healthy Fats", "Fiber"],
                ],
                level_1_font_color=X11Color.BLACK,
                level_2_font_color=X11Color.DARK_GRAY,
                background_color=X11Color.GREEN_YELLOW,
            )
        )

        TestCase.write(what=d, where_to="test_horizontal_bullets_list_color_green.pdf")

    def test_horizontal_bullets_list_color_blue(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        l: PageLayout = SingleColumnLayout(p)
        l.append_layout_element(
            SmartArt.horizontal_bullet_list(
                level_1_items=["Cherries", "Papaya", "Avocado"],
                level_2_items=[
                    ["Vitamin C", "Potassium"],
                    ["Vitamin C", "Vitamin A"],
                    ["Potassium", "Healthy Fats", "Fiber"],
                ],
                level_1_font_color=X11Color.WHITE,
                level_2_font_color=X11Color.WHITE,
                background_color=X11Color.BLUE,
            )
        )

        TestCase.write(what=d, where_to="test_horizontal_bullets_list_color_blue.pdf")

    def test_horizontal_bullets_list_color_indigo(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        l: PageLayout = SingleColumnLayout(p)
        l.append_layout_element(
            SmartArt.horizontal_bullet_list(
                level_1_items=["Cherries", "Papaya", "Avocado"],
                level_2_items=[
                    ["Vitamin C", "Potassium"],
                    ["Vitamin C", "Vitamin A"],
                    ["Potassium", "Healthy Fats", "Fiber"],
                ],
                level_1_font_color=X11Color.WHITE,
                level_2_font_color=X11Color.WHITE,
                background_color=X11Color.INDIGO,
            )
        )

        TestCase.write(what=d, where_to="test_horizontal_bullets_list_color_indigo.pdf")

    def test_horizontal_bullets_list_color_violet(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        l: PageLayout = SingleColumnLayout(p)
        l.append_layout_element(
            SmartArt.horizontal_bullet_list(
                level_1_items=["Cherries", "Papaya", "Avocado"],
                level_2_items=[
                    ["Vitamin C", "Potassium"],
                    ["Vitamin C", "Vitamin A"],
                    ["Potassium", "Healthy Fats", "Fiber"],
                ],
                level_1_font_color=X11Color.WHITE,
                level_2_font_color=X11Color.WHITE,
                background_color=X11Color.VIOLET,
            )
        )

        TestCase.write(what=d, where_to="test_horizontal_bullets_list_color_violet.pdf")
