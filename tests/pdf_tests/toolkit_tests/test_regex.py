import random
import unittest

from borb.pdf import (
    Document,
    Page,
    SingleColumnLayout,
    Paragraph,
    Lipsum,
    PageLayout,
    PDF,
    Source,
    Pipeline,
    SquareAnnotation,
    X11Color,
)
from borb.pdf.toolkit.sink.regex import Regex


class TestRegex(unittest.TestCase):

    def test_regex(self):

        # step 1: build PDF
        d: Document = Document()

        # add Page
        p: Page = Page()
        d.append_page(p)

        # add SingleColumnLayout
        l: PageLayout = SingleColumnLayout(p)

        # add Paragraph(s)
        random.seed(0)
        for _ in range(0, 5):
            l.append_layout_element(
                Paragraph(
                    Lipsum.generate_lorem_ipsum(512),
                    font_size=12,
                )
            )

        # store
        PDF.write(what=d, where_to="assets/test_regex.pdf")

        # step 2: read PDF
        d: Document = PDF.read("assets/test_regex.pdf")

        # step 3: process
        rectangles = Pipeline(
            [
                Source(),
                Regex(pattern="[qQ]uam"),
            ]
        ).process(d)

        # assert
        assert len(rectangles) == 1

        # step 4: mark
        for i, m in enumerate(rectangles[0]):
            for x, y, w, h in m.rectangles:
                SquareAnnotation(stroke_color=X11Color.RED, size=(w, h)).paint(
                    available_space=(x, y, w, h), page=d.get_page(0)
                )

        # store
        PDF.write(what=d, where_to="assets/test_regex_marked.pdf")
