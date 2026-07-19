import random

from borb.pdf import (
    Document,
    Page,
    SingleColumnLayout,
    Paragraph,
    Lipsum,
    PageLayout,
    TableOfContents,
    Heading,
)
from tests.test_case import TestCase


class TestTableOfContents(TestCase):

    def test_table_of_contents_001(self):
        d: Document = Document()
        # d.append_page(TableOfContents())

        p: Page = Page()
        d.append_page(p)

        l: PageLayout = SingleColumnLayout(p)

        l.append_layout_element(Heading("Heading 0"))
        l.append_layout_element(Heading("Heading 1", outline_level=1))
        l.append_layout_element(Heading("Heading 2"))
        l.append_layout_element(Heading("Heading 3", outline_level=1))

        TestCase.write(what=d, where_to="test_table_of_contents_001.pdf")

    def test_table_of_contents_002(self):
        d: Document = Document()
        d.append_page(TableOfContents())

        p: Page = Page()
        d.append_page(p)

        l: PageLayout = SingleColumnLayout(p)

        random.seed(0)
        for i in range(0, 5):
            l.append_layout_element(Heading(f"Heading {i+1}"))

            for j in range(0, 3):
                l.append_layout_element(
                    Heading(f"Subheading {i+1}.{j+1}", outline_level=1)
                )
                for _ in range(0, 3):
                    l.append_layout_element(
                        Paragraph(Lipsum.generate_lorem_ipsum(300), font_size=12)
                    )

        TestCase.write(what=d, where_to="test_table_of_contents_002.pdf")
