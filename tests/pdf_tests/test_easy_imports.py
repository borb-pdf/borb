import random

from borb.pdf import (
    Document,
    Page,
    SingleColumnLayout,
    Paragraph,
    Lipsum,
    PageLayout,
)
from tests.test_case import TestCase


class TestEasyImports(TestCase):

    def test_easy_imports(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        l: PageLayout = SingleColumnLayout(p)

        random.seed(0)
        l.append_layout_element(
            Paragraph(Lipsum.generate_lorem_ipsum(300), font_size=4)
        )

        TestCase.write(what=d, where_to="test_easy_imports.pdf")
