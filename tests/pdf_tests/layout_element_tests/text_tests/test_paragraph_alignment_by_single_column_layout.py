from borb.pdf import (
    Document,
    Page,
    SingleColumnLayout,
    PageLayout,
    Paragraph,
    LayoutElement,
    X11Color,
)
from tests.test_case import TestCase


class TestParagraphAlignmentBySingleColumnLayout(TestCase):

    def test_paragraph_vertical_alignment_middle(self):
        # Create an empty Document
        d: Document = Document()

        # Create an empty Page
        p: Page = Page()
        d.append_page(p)

        # Create a PageLayout
        l: PageLayout = SingleColumnLayout(p)

        # Add a Paragraph
        for _ in range(0, 3):
            l.append_layout_element(
                Paragraph(
                    "Lorem Ipsum Dolor Sit Amet",
                    background_color=X11Color.YELLOW_MUNSELL,
                    vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
                )
            )

        # Write the PDF
        TestCase.write(what=d, where_to="test_paragraph_vertical_alignment_middle.pdf")

    def test_paragraph_horizontal_alignment_middle(self):
        # Create an empty Document
        d: Document = Document()

        # Create an empty Page
        p: Page = Page()
        d.append_page(p)

        # Create a PageLayout
        l: PageLayout = SingleColumnLayout(p)

        # Add a Paragraph
        for _ in range(0, 3):
            l.append_layout_element(
                Paragraph(
                    "Lorem Ipsum Dolor Sit Amet",
                    background_color=X11Color.YELLOW_MUNSELL,
                    horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
                )
            )

        # Write the PDF
        TestCase.write(
            what=d, where_to="test_paragraph_horizontal_alignment_middle.pdf"
        )
